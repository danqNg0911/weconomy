# Weconomy Chatbot

Ứng dụng chat web về **kinh tế và đầu tư quốc tế**, sử dụng GraphRAG để truy xuất dữ liệu Neo4j/AuraDB và suy luận qua nhiều hop. Giao diện xây trên assistant-ui ChatGPT; FastAPI xử lý guard, LLM, truy vấn đồ thị và lưu hội thoại.

## 1. Cài đặt và chạy

### Provider và model hiện tại

Backend dùng chung một model cho các bước kiểm tra, lập plan và tổng hợp. Chọn model qua `.env`. `LLM_PROVIDER=openai` dùng giao thức tương thích OpenAI, có thể kết nối OpenRouter hoặc 9router.

Code cũng hỗ trợ Cloudflare trực tiếp qua `LLM_PROVIDER=cloudflare` và các biến `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_MODEL`. Chế độ này tự đặt URL `/ai/v1`, model, key và giao thức Chat Completions từ cấu hình Cloudflare, bỏ qua lựa chọn provider tương thích OpenAI cũ. Khởi động lại backend sau khi đổi cấu hình.

### Yêu cầu

- Python 3.11 trở lên.
- Node.js 22 trở lên và npm.
- Neo4j/AuraDB đã có dữ liệu nghiệp vụ với node `Entity`, thuộc tính `name`, `entity_type` và các quan hệ giữa thực thể.
- LLM có API tương thích OpenAI, ví dụ 9router.
- Supabase PostgreSQL để lưu hội thoại; có thể dùng SQLite khi phát triển cục bộ.

Các lệnh PowerShell dưới đây bắt đầu từ **thư mục gốc repository**, nơi chứa `apps/chatbot/`.

### Cài backend

```powershell
if (!(Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\python.exe -m pip install -r apps/chatbot/be/requirements.txt
if (!(Test-Path apps/chatbot/be/.env)) {
    Copy-Item apps/chatbot/be/.env.example apps/chatbot/be/.env
}
```

Điền cấu hình vào [be/.env](be/.env), tham khảo [be/.env.example](be/.env.example):

```env
CHAT_MODE=llm
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openrouter-key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=your-model
OPENAI_API_MODE=chat
LLM_HISTORY_MESSAGES=6
LLM_MAX_OUTPUT_TOKENS=1024

NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j

DATABASE_URL=
CREATE_TABLES=false
```

- `OPENAI_API_MODE=responses` dùng endpoint `/responses`; đặt `chat` nếu provider/model dùng `/chat/completions`.
- `OPENAI_BASE_URL` là URL gốc API, thường kết thúc bằng `/v1`, không bao gồm endpoint phía trên.
- `OPENAI_REASONING_EFFORT`, `OPENAI_REASONING_SUMMARY` là tùy chọn phụ thuộc model; summary chỉ gửi với Responses. `LLM_SYSTEM_PROMPT` cho phép điều chỉnh chỉ dẫn trả lời.
- Backend đọc cấu hình theo thứ tự ưu tiên tăng dần: `.env` tại gốc repository → `apps/chatbot/be/.env` → biến môi trường của tiến trình. Neo4j đã cấu hình ở `.env` gốc thì không cần chép lại. `NEO4J_USER` được hỗ trợ khi không có `NEO4J_USERNAME`.
- Backend không đọc `.env.local` của UI. Khởi động lại backend sau khi đổi cấu hình.

Nếu để trống `DATABASE_URL`, backend tự tạo SQLite ở `apps/chatbot/be/.data/chat.db`. Thư mục này được bỏ qua bởi Git.

**Dùng Supabase:** đặt kết nối PostgreSQL trong backend `.env`:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/postgres?sslmode=require
CREATE_TABLES=false
```

Lấy host/port/user/database từ mục Connect của Supabase, dùng direct connection hoặc session pooler phù hợp kết nối mạng. URL-encode ký tự đặc biệt trong mật khẩu. Backend cũng chấp nhận tiền tố `postgresql://` và `postgres://`. Dữ liệu SQLite cũ không tự chuyển sang PostgreSQL.

Nếu database mới chưa có bảng chat, đặt `CREATE_TABLES=true` trước lần khởi động đầu tiên để SQLAlchemy tạo các bảng từ [be/app/models.py](be/app/models.py). Sau khi tạo xong, đổi lại `CREATE_TABLES=false` và khởi động lại. Cơ chế này chỉ tạo bảng còn thiếu, không thay thế migration cho bảng đã tồn tại.

Backend kết nối trực tiếp database; FE không cần Supabase URL/key để sử dụng luồng hiện tại. Database này chỉ chứa hội thoại, không chứa đồ thị nghiệp vụ. Nếu sử dụng Supabase Data API, cấu hình quyền truy cập/RLS riêng; `CREATE_TABLES` không tự thiết lập các policy đó.

Chạy backend:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir apps/chatbot/be --host 127.0.0.1 --port 8000 --reload
```

- Kiểm tra trạng thái: http://127.0.0.1:8000/health
- Swagger API: http://127.0.0.1:8000/docs

Để thử UI/lưu trữ mà không gọi LLM hoặc Neo4j, đặt `CHAT_MODE=mock`. Chế độ này trả dữ liệu minh họa có nhãn mock và bỏ qua pipeline guard/GraphRAG thực.

### Nguồn evidence trên Hugging Face

AuraDB lưu `claim_ids`/`document_ids` trong sự kiện của cạnh, không chứa toàn bộ đoạn trích và bài báo. Export tương ứng với collection hiện tại nằm trong bucket đã cấu hình ở [HUGGINGFACE.md](../../docs/HUGGINGFACE.md):

```text
hf://buckets/weconomy235/weconomy/exports/v15-manual-global-business-only-20261112
```

Sau khi CLI `hf` đã đăng nhập tài khoản có quyền đọc bucket, tải hai file nguồn và dựng chỉ mục (từ gốc repository):

```powershell
hf buckets cp hf://buckets/weconomy235/weconomy/exports/v15-manual-global-business-only-20261112/claims.jsonl apps/chatbot/be/.data/evidence-source/claims.jsonl
hf buckets cp hf://buckets/weconomy235/weconomy/exports/v15-manual-global-business-only-20261112/articles.jsonl apps/chatbot/be/.data/evidence-source/articles.jsonl
$env:PYTHONPATH="apps/chatbot/be"
.\.venv\Scripts\python.exe -m app.evidence --source apps/chatbot/be/.data/evidence-source
```

Export này có 5.362 claim và 923 bài báo. Mặc định chỉ mục nằm ở `apps/chatbot/be/.data/evidence.sqlite3`, có thể đổi bằng `EVIDENCE_INDEX_PATH`. Đây là cache nguồn riêng, không thay database hội thoại Supabase. Thư mục `.data` được Git-ignore. Không cần gọi Hugging Face cho mỗi tin nhắn.

CLI cũng nhận thư mục chứa `gold/relations.parquet` và `silver/articles.parquet`; trường hợp đó cần cài thêm `pyarrow`. Khi thay collection AuraDB, hãy dựng lại chỉ mục từ đúng export tương ứng. Thiếu nguồn thì trả trạng thái thiếu evidence, không bịa đoạn trích. Snapshot cũ đã lưu evidence rỗng không tự được cập nhật; hỏi câu mới hoặc mở ví dụ AuraDB để kiểm tra dữ liệu mới.

### Cài và chạy frontend

Mở terminal thứ hai từ gốc repository:

```powershell
cd apps/chatbot/ui
npm ci
if (!(Test-Path .env.local)) { Copy-Item .env.example .env.local }
npm run dev
```

[ui/.env.local](ui/.env.local) chỉ cần:

```env
CHAT_BACKEND_URL=http://127.0.0.1:8000
```

Mở http://localhost:3000. Trình duyệt gọi `/api/backend/...`; Next.js chuyển tiếp request và stream sang FastAPI. Không có mã gọi LLM hay truy vấn database trực tiếp trong FE. Đổi `CHAT_BACKEND_URL` thì khởi động lại Next.js.

Chạy frontend bằng bản build, từ `apps/chatbot/ui`:

```powershell
npm run build
npm run start
```

Backend vẫn cần chạy riêng. Cấu hình `CORS_ORIGINS` ở BE được dùng nếu client gọi FastAPI trực tiếp; UI hiện tại sử dụng proxy cùng origin.

## 2. Kiến trúc và cách xây dựng

```mermaid
flowchart LR
    UI[Next.js + assistant-ui] --> Proxy[Next.js API proxy]
    Proxy --> API[FastAPI routes]
    API --> Safety[Quy tắc và LLM kiểm tra an toàn]
    Safety -->|Qua| Domain[LLM: domain JSON]
    Domain -->|Qua| Plan[LLM: plan JSON]
    Plan --> Validate[Kiểm tra plan và chuẩn hóa Anh–Việt]
    Validate --> Graph[Neo4j: liên kết thực thể và BFS multi-hop]
    Graph --> Evidence[Tra claim và bài báo trong SQLite evidence]
    Evidence --> LLM[LLM tổng hợp facts và sources]
    Safety -->|Chặn| Reply[Phản hồi trực tiếp]
    Domain -->|Chặn| Reply
    Graph -->|Không có cạnh phù hợp| Reply
    LLM --> Store[(PostgreSQL / SQLite)]
    Reply --> Store
    Store -->|SSE / lịch sử và graph| UI
```

Frontend giữ bố cục và thành phần assistant-ui đã tùy chỉnh, dùng runtime adapter để gọi FastAPI. Backend dùng Pydantic xác thực dữ liệu, SQLAlchemy quản lý hội thoại, Neo4j Python driver đọc đồ thị và httpx nhận stream LLM. Không thêm framework agent; luồng xử lý được viết trực tiếp để dễ đọc và điều chỉnh.

### Pipeline một câu hỏi

1. Backend lưu câu hỏi và tạo câu trả lời ở trạng thái `pending` trước khi xử lý. Nếu request là gửi lại câu đã hoàn tất, đọc lại kết quả đã lưu thay vì chạy pipeline lần nữa.
2. **Safety guard:** kiểm tra một số cụm yêu cầu nguy hiểm rồi dùng LLM phân loại an toàn theo ngữ cảnh.
3. **Domain guard:** một lần phân loại riêng giới hạn nội dung vào kinh tế và đầu tư quốc tế; xét các câu hỏi gần đây để hiểu câu nối tiếp. Bị một trong hai guard chặn thì lưu phản hồi từ chối, trả graph rỗng và không lập plan, truy vấn Neo4j hay gọi LLM sinh câu trả lời. JSON phân loại không hợp lệ/lỗi provider trở thành lỗi có thể thử lại, không tự cho qua guard.
4. **Lập plan:** LLM trả JSON gồm `entities`, `terms`, `relations` và có thể thêm `entity_variants`. Backend xác thực JSON và truyền tham số cho câu Cypher cố định.
5. **Chuẩn hóa:** chuẩn hóa dấu, chữ hoa/thường và khoảng trắng. Backend áp dụng alias Anh–Việt và biến thể tương đương do planner cung cấp. Ví dụ `Mỹ` ↔ `United States`, `Nhật Bản` ↔ `Japan`. Ưu tiên khớp tên chính xác.
6. **Truy xuất multi-hop:** liên kết tên với node `Entity`, rồi duyệt breadth-first từ nhiều seed. Frontier của hop tiếp theo chỉ lấy từ láng giềng thực tế của hop trước. Ưu tiên loại quan hệ trong plan, bỏ chu trình và giới hạn lượng dữ liệu. Có thể duyệt hai chiều để tìm liên hệ, nhưng kết quả vẫn giữ đúng chiều `source → target`, thời điểm và trạng thái khẳng định/kiểm duyệt của cạnh.
7. **Evidence và tổng hợp:** backend nối `claim_id` của từng cạnh với trích đoạn và bài báo qua chỉ mục SQLite. Snapshot lưu evidence của các cạnh truy xuất được. Model nhận node, cạnh, đường đi và tối đa 8 trích đoạn, mỗi đoạn giới hạn 500 ký tự. Khi không có cạnh phù hợp, backend trả thông báo thiếu dữ liệu.
8. **Lưu và hiển thị:** lưu câu trả lời cùng graph, plan, biến thể chuẩn hóa, truy vấn/tham số và đường đi. FE nhận stream rồi hiển thị graph tương ứng.

Luồng đầy đủ gọi model tối đa bốn lần theo thứ tự kiểm tra an toàn, kiểm tra phạm vi, lập plan và tổng hợp.

Giới hạn có thể chỉnh trong backend `.env`:

| Biến                       | Mặc định | Ý nghĩa                            |
| -------------------------- | -------- | ---------------------------------- |
| `GRAPH_MAX_HOPS`           | `3`      | Số hop tối đa, cho phép 1–4        |
| `GRAPH_MAX_SEEDS`          | `4`      | Số thực thể bắt đầu tối đa         |
| `GRAPH_NEIGHBORS_PER_NODE` | `8`      | Số láng giềng lấy cho mỗi node     |
| `GRAPH_MAX_NODES`          | `60`     | Số node tối đa trong graph kết quả |
| `GRAPH_MAX_EDGES`          | `100`    | Số cạnh tối đa trong graph kết quả |
| `LLM_MAX_OUTPUT_TOKENS`    | `1024`   | Giới hạn đầu ra mỗi lần gọi model |
| `LLM_HISTORY_MESSAGES`    | `6`      | Số message tối đa gửi khi tổng hợp |

Guard nhận tối đa 3 câu hỏi gần nhất, mỗi câu 1.500 ký tự. Planner nhận tối đa 6 tin nhắn hợp lệ, mỗi tin 2.000 ký tự. Khi tổng hợp, câu hỏi mới nhất được giữ nguyên và các tin nhắn cũ giới hạn 2.000 ký tự.

Transaction truy xuất có timeout 20 giây; mỗi lần phân loại/lập plan có timeout 40 giây; toàn bộ stream xử lý có giới hạn 240 giây. Khi đạt giới hạn node/cạnh/láng giềng, metadata có `truncated=true`. Kết quả là tập con phục vụ câu hỏi, không phải phép tìm kiếm toàn bộ đồ thị hay thống kê đầy đủ.

### Lưu trữ và giao tiếp FE–BE

- `threads`: thông tin hội thoại, tiêu đề, trạng thái archive và thời gian cập nhật.
- `messages`: nội dung, vai trò, trạng thái và `details` dạng JSONB trên PostgreSQL hoặc JSON trên SQLite.
- `messages.details.graph`: `nodes`, `edges`, `evidence`. Evidence gồm đoạn trích, URL, claim ID và cạnh liên quan; lưu cùng snapshot của câu trả lời.
- `messages.details.metadata`: plan, `normalization`, `queries` (Cypher và tham số), `paths`, `seed_ids`, số hop, giới hạn truy xuất và model; phản hồi bị chặn có `blocked_by=safety|domain`.

Graph được lưu **riêng cho từng câu trả lời**. Hỏi câu mới không ghi đè graph cũ; xóa thread mới xóa các message và snapshot liên quan. Neo4j vẫn là nguồn dữ liệu nghiệp vụ, không sao chép toàn bộ đồ thị vào database hội thoại.

Xem cấu trúc payload tại [ui/docs/query-graph.example.json](ui/docs/query-graph.example.json). File này chỉ dùng làm tài liệu, không nạp vào UI thực tế. FE kiểm tra node/cạnh hợp lệ và bỏ qua đường dẫn evidence không an toàn.

Stream dùng SSE với các event `start`, `token`, `details`, `done`, `error`. Chỉ phát `done` sau khi lưu câu trả lời hoàn tất. Dừng, mất kết nối hoặc lỗi sẽ lưu phần nội dung đã có với trạng thái `failed` để thử lại. Pending do tiến trình bị tắt có thể thử lại sau năm phút.

Mỗi thread chỉ cho một câu trả lời đang xử lý; request đồng thời trả HTTP 409. Cùng ID/nội dung sẽ phát lại kết quả hoàn tất hoặc thử lại câu thất bại, tránh nhân đôi câu hỏi. Các thread khác nhau có thể chạy độc lập.

### Các module chính

| Đường dẫn                                               | Vai trò                                                      |
| ------------------------------------------------------- | ------------------------------------------------------------ |
| `be/app/main.py`                                        | Tạo app, middleware, lifecycle database và đăng ký router    |
| `be/app/routes.py`                                      | API với hai tag `threads`, `message`, điều phối stream       |
| `be/app/guards.py`                                      | Hai lớp guard và xác thực JSON từ LLM                        |
| `be/app/graph_rag.py`                                   | Lập plan, liên kết seed, truy xuất multi-hop và dựng context |
| `be/app/evidence.py`                                    | Dựng chỉ mục claim/bài báo và nối trích đoạn với cạnh |
| `be/app/query_normalization.py`                         | Chuẩn hóa và alias Anh–Việt                                  |
| `be/app/llm.py`                                         | Gọi API LLM tương thích Chat Completions/Responses           |
| `be/app/store.py`, `models.py`, `schemas.py`            | Lưu trữ, mô hình database và schema API                      |
| `be/app/config.py`                                      | Đọc và kiểm tra cấu hình backend                             |
| `be/app/graph_example.py`                               | Query AuraDB mẫu, độc lập với pipeline trả lời               |
| `ui/app/assistant.tsx`                                  | Bố cục chat và chọn graph đang hiển thị                      |
| `ui/hooks/use-backend-runtime.ts`                       | Adapter assistant-ui, lịch sử và nhận stream                 |
| `ui/app/api/backend/[...path]/route.ts`                 | Proxy HTTP/stream sang FastAPI                               |
| `ui/components/thread.aui.tsx`                          | Tin nhắn, composer và link xem graph từng câu trả lời        |
| `ui/components/graph-panel.tsx`, `graph-canvas.tsx`     | Panel graph, evidence và tương tác viewport                  |
| `ui/components/resizable-detail-panel.tsx`              | Kéo thay đổi kích thước panel                                |
| `ui/components/settings-menu.tsx`, `theme-provider.tsx` | Chọn theme và lưu tùy chọn cục bộ                            |

## 3. Chức năng hiện tại

### Chat và giao diện

- Giao diện chat chính phong cách ChatGPT, sidebar Weconomy và danh sách thread; tạo mới, đổi tên, archive, xóa hội thoại. Tiêu đề ban đầu được backend rút gọn từ câu hỏi đầu tiên.
- Chat dạng văn bản, stream câu trả lời, hiển thị Markdown, sao chép/xuất Markdown, dừng và thử lại câu trả lời bị gián đoạn. Lịch sử được tải lại từ backend.
- Menu Setting gọn với theme sáng/tối/theo hệ thống, lưu trên trình duyệt.
- Panel đồ thị thu hẹp vùng chat trên desktop, có thể kéo thanh chia để đổi kích thước; bàn phím hỗ trợ mũi tên, Home/End và nhấp đúp để đặt lại. Trên mobile, panel phủ vùng chat.
- Zoom bằng cuộn chuột/nút, kéo viewport, kéo node và đặt lại góc nhìn. Renderer dùng Neo4j NVL Canvas, nạp phía client; nhận snapshot từ backend, không kết nối AuraDB trực tiếp từ trình duyệt.
- Link **Xem đồ thị đã truy vấn** dưới câu trả lời có graph mở lại snapshot của câu đó. Toggle trên cùng chuyển về graph của message mới nhất; những lần bấm tiếp theo đóng/mở panel bình thường.
- Evidence nằm cạnh hoặc dưới đồ thị tùy chiều rộng panel. Chọn một node để xem trích dẫn gắn trực tiếp hoặc thuộc các cạnh kề. Chọn một cạnh để xem riêng trích dẫn của cạnh đó. Chọn trích dẫn để làm nổi bật phần đồ thị tương ứng. Mỗi thẻ giữ link bài báo gốc.

### Thử graph AuraDB

Nút **Thử graph AuraDB** gọi API mẫu để lấy tối đa sáu đường đi 1–2 hop quanh `TDK Ventures`. Đây là query cố định, chỉ đọc, dùng kiểm tra giao diện; không thay thế pipeline GraphRAG theo câu hỏi. **Đóng ví dụ** quay lại graph của câu trả lời đang xem.

### API hiện có

| Method | Đường dẫn FastAPI                 | Chức năng                               |
| ------ | --------------------------------- | --------------------------------------- |
| GET    | `/health`                         | Trạng thái và chế độ chat               |
| POST   | `/api/threads`                    | Tạo thread                              |
| GET    | `/api/threads?limit=100&offset=0` | Danh sách thread, gồm cả archive        |
| GET    | `/api/threads/{id}`               | Thông tin thread                        |
| PATCH  | `/api/threads/{id}`               | Đổi tiêu đề hoặc trạng thái archive     |
| DELETE | `/api/threads/{id}`               | Xóa thread cùng message                 |
| POST   | `/api/threads/{id}/title`         | Tạo tiêu đề ban đầu từ nội dung câu hỏi |
| GET    | `/api/threads/{id}/messages`      | Lịch sử, trạng thái và graph snapshot   |
| POST   | `/api/threads/{id}/messages`      | Gửi câu hỏi, nhận SSE                   |
| POST   | `/api/graph/example`              | Graph AuraDB mẫu                        |

Body gửi message: `{"id":"client-message-id","content":"Câu hỏi","parent_id":null}`. Ở lượt tiếp theo, `parent_id` là ID câu trả lời assistant đã lưu trước đó. Trong FE, các đường dẫn `/api/...` của FastAPI được truy cập thông qua `/api/backend/...`.

### Giới hạn hiện tại

Chưa có đăng nhập và phân quyền theo chủ hội thoại; hệ thống hiện phục vụ phát triển cục bộ/một người dùng. Chưa hỗ trợ upload, chỉnh sửa tin nhắn, phân nhánh hoặc sinh lại câu trả lời đã hoàn tất. Chưa có vector search, sửa lỗi chính tả tổng quát hoặc công cụ web. Chuẩn hóa Anh–Việt dựa trên từ điển nhỏ, không bảo đảm nhận diện mọi cách dịch. Guard và planner vẫn có thể phân loại nhầm hoặc trả JSON sai. Truy xuất có giới hạn nên không bảo đảm tìm đủ mọi đường đi hay thống kê toàn bộ dữ liệu. Hướng dẫn tổng hợp giới hạn nguồn dữ kiện nhưng không bảo đảm model luôn tuân thủ; chất lượng cần đánh giá theo từng model, cả câu Việt/Anh và câu cần nhiều hop.

## 4. Kiểm tra khi phát triển

Backend, từ gốc repository; cài pytest nếu môi trường chưa có:

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest apps/chatbot/be/tests -q
```

Test tự động dùng SQLite tạm và các mô phỏng provider/graph, không ghi dữ liệu vào Supabase/AuraDB và không gọi LLM trả phí. Bao phủ lưu lịch sử, replay/retry, CRUD/archive, stream/lỗi provider, guard chặn sớm, chuẩn hóa Anh–Việt, duyệt multi-hop và giới hạn graph.

Frontend, từ `apps/chatbot/ui`:

```powershell
npx tsc --noEmit
npm run build
```

Không chạy lại lệnh ghi đè preset assistant-ui nếu chưa xem xét các tùy chỉnh chat/graph hiện có.
