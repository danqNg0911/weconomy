from contextlib import contextmanager
from datetime import timedelta
from uuid import UUID, uuid4, uuid5

from fastapi import HTTPException
from sqlalchemy import create_engine, delete, event, select, update
from sqlalchemy.orm import sessionmaker

from .config import ROOT, Settings
from .models import Base, Message, Thread, now
from .schemas import MessageCreate, MessageOut, ThreadOut


def message_id(thread_id: UUID, client_id: str):
    try:
        return UUID(client_id)
    except ValueError:
        return uuid5(thread_id, client_id)


class Store:
    def __init__(self, settings: Settings):
        url = settings.database_url
        if not url:
            (ROOT / ".data").mkdir(exist_ok=True)
            url = f"sqlite:///{(ROOT / '.data/chat.db').as_posix()}"
        if url.startswith(("postgres://", "postgresql://")):
            url = "postgresql+psycopg://" + url.split("://", 1)[1]
        self.sqlite = url.startswith("sqlite")
        self.engine = create_engine(
            url,
            pool_pre_ping=True,
            **(
                {"connect_args": {"check_same_thread": False, "timeout": 15}}
                if self.sqlite
                else {"connect_args": {"prepare_threshold": None}}
            ),
        )
        if self.sqlite:

            @event.listens_for(self.engine, "connect")
            def foreign_keys(connection, _):
                connection.execute("PRAGMA foreign_keys=ON")

        self.sessions = sessionmaker(self.engine, expire_on_commit=False)
        if self.sqlite or settings.create_tables:
            Base.metadata.create_all(self.engine)

    @contextmanager
    def transaction(self):
        with self.sessions.begin() as db:
            # Serialize writers on SQLite; PostgreSQL uses the thread row lock.
            if self.sqlite:
                db.connection().exec_driver_sql("BEGIN IMMEDIATE")
            yield db

    def thread(self, db, thread_id, lock=False):
        stmt = select(Thread).where(Thread.id == thread_id)
        item = db.scalar(stmt.with_for_update() if lock else stmt)
        if item is None:
            raise HTTPException(404, "Thread not found")
        return item

    def create_thread(self, payload):
        with self.transaction() as db:
            identifier = payload.id or uuid4()
            item = db.get(Thread, identifier)
            if item is None:
                item = Thread(id=identifier, title=payload.title)
                db.add(item)
                db.flush()
            return ThreadOut.model_validate(item)

    def list_threads(self, limit, offset):
        with self.sessions() as db:
            return [
                ThreadOut.model_validate(t)
                for t in db.scalars(
                    select(Thread).order_by(Thread.updated_at.desc(), Thread.id).limit(limit).offset(offset)
                )
            ]

    def get_thread(self, identifier):
        with self.sessions() as db:
            return ThreadOut.model_validate(self.thread(db, identifier))

    def patch_thread(self, identifier, payload):
        with self.transaction() as db:
            item = self.thread(db, identifier, lock=True)
            if payload.archived is not None:
                self.check_idle(db, identifier)
                item.archived = payload.archived
            if payload.title is not None:
                item.title = payload.title
            item.updated_at = now()
            db.flush()
            return ThreadOut.model_validate(item)

    def generate_title(self, identifier, content):
        with self.transaction() as db:
            item = self.thread(db, identifier, lock=True)
            if item.title == "New chat":
                item.title = " ".join(content.split())[:80] or "New chat"
                item.updated_at = now()
            db.flush()
            return ThreadOut.model_validate(item)

    def check_idle(self, db, identifier):
        # Interrupted workers cannot leave a thread permanently blocked.
        db.execute(
            update(Message)
            .where(
                Message.thread_id == identifier,
                Message.status == "pending",
                Message.created_at < now() - timedelta(minutes=5),
            )
            .values(status="failed")
        )
        if db.scalar(
            select(Message.id)
            .where(
                Message.thread_id == identifier,
                Message.status == "pending",
            )
            .limit(1)
        ):
            raise HTTPException(409, "This thread already has a response in progress")

    def delete_thread(self, identifier):
        with self.transaction() as db:
            self.thread(db, identifier, lock=True)
            self.check_idle(db, identifier)
            db.execute(delete(Thread).where(Thread.id == identifier))

    def messages(self, identifier):
        with self.sessions() as db:
            self.thread(db, identifier)
            return [
                MessageOut.model_validate(m)
                for m in db.scalars(
                    select(Message)
                    .where(Message.thread_id == identifier)
                    .order_by(Message.created_at, Message.id)
                )
            ]

    def prepare(self, identifier: UUID, payload: MessageCreate):
        with self.transaction() as db:
            thread = self.thread(db, identifier, lock=True)
            if thread.archived:
                raise HTTPException(409, "Unarchive the thread before sending a message")
            self.check_idle(db, identifier)
            uid = message_id(identifier, payload.id)
            aid = uuid5(uid, "assistant")
            user = db.get(Message, uid)
            answer = db.get(Message, aid)
            if user:
                if user.thread_id != identifier or user.role != "user" or user.content != payload.content:
                    raise HTTPException(409, "Message ID already used for different content")
                if answer and answer.status == "completed":
                    return MessageOut.model_validate(answer), True
                latest_user = db.scalar(
                    select(Message.id)
                    .where(
                        Message.thread_id == identifier,
                        Message.role == "user",
                    )
                    .order_by(Message.created_at.desc(), Message.id.desc())
                    .limit(1)
                )
                if latest_user != uid:
                    raise HTTPException(409, "Only the latest failed message can be retried")
            else:
                latest = db.scalar(
                    select(Message)
                    .where(Message.thread_id == identifier)
                    .order_by(Message.created_at.desc(), Message.id.desc())
                    .limit(1)
                )
                parent = message_id(identifier, payload.parent_id) if payload.parent_id else None
                if (latest.id if latest else None) != parent:
                    raise HTTPException(409, "History changed; reload the thread before sending")
                user = Message(id=uid, thread_id=identifier, role="user", content=payload.content)
                db.add(user)
                db.flush()
            if answer is None:
                answer = Message(id=aid, thread_id=identifier, role="assistant")
                db.add(answer)
            answer.content, answer.status, answer.details = "", "pending", {}
            thread.updated_at = now()
            if thread.title == "New chat":
                thread.title = " ".join(payload.content.split())[:80]
            db.flush()
            return MessageOut.model_validate(answer), False

    def finish(self, identifier, content, details, status):
        with self.transaction() as db:
            message = db.get(Message, identifier)
            if message is None or message.status != "pending":
                return
            message.content, message.details, message.status = content, details, status
            self.thread(db, message.thread_id).updated_at = now()
