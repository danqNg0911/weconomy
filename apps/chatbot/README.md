# Weconomy Chatbot

Ứng dụng chat web về **kinh tế và đầu tư quốc tế**, sử dụng GraphRAG để truy xuất dữ liệu Neo4j/AuraDB và suy luận qua nhiều hop. Giao diện xây trên assistant-ui ChatGPT; FastAPI xử lý guard, LLM, truy vấn đồ thị và lưu hội thoại.

## 1. Cài đặt và chạy

### Provider và model hiện tại

Backend dùng một model chung cho domain guard, lập plan và tổng hợp; chọn qua `.env`, không có model dự phòng tự động. `LLM_PROVIDER=openai` nghĩa là giao thức tương thích OpenAI, có thể dùng OpenRouter hoặc 9router; không bắt buộc gọi dịch vụ OpenAI.

Tại thời điểm cập nhật tài liệu, `.env` cục bộ đang chọn `nvidia/nemotron-3-ultra-550b-a55b:free`, giao thức `chat`, domain guard 32 token và tổng hợp 1024 token. Đây là cấu hình thử nghiệm, không phải xác nhận đáp ứng yêu cầu model ≤9 tỷ tham số. Khi chốt model cho đề tài, cần kiểm tra số tham số riêng. README không chứa API key; cấu hình thực tế luôn lấy từ `.env` và biến môi trường.

Để dùng Liquid qua OpenRouter, cấu hình `OPENAI_MODEL=liquid/lfm-3-1.7b:free`, `OPENAI_BASE_URL=https://openrouter.ai/api/v1` và key OpenRouter. Thử nghiệm trước đó cho thấy endpoint Liquid bắt buộc reasoning: ngân sách mặc định dễ hết token ngay ở guard; tăng token vẫn chưa giải quyết được lỗi chọn ý định đồng đầu tư. Model này chưa được xác nhận chạy ổn với pipeline hiện tại.

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
LLM_GUARD_MAX_TOKENS=64
LLM_PLAN_MAX_TOKENS=512
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

### Dùng graph public với Neo4j local

Repo có graph projection đã lược toàn văn và evidence text tại
[`public-data/v15-global-business-only-20261112`](../../public-data/v15-global-business-only-20261112/README.md).
Từ gốc repo, cấu hình `NEO4J_PASSWORD` trong `.env` (file này không commit), khởi động Neo4j local và nhập graph:

```powershell
docker compose up -d neo4j
$env:NEO4J_URI = 'bolt://localhost:7687'
$env:NEO4J_USERNAME = 'neo4j'
$env:NEO4J_DATABASE = 'neo4j'
uv run --no-sync weconomy import-neo4j public-data/v15-global-business-only-20261112
```

### Evidence source riêng cho chatbot

Graph public không có câu evidence. Để chatbot trả evidence quote, tiếp tục tải `claims.jsonl` và `articles.jsonl`
từ bucket riêng bên dưới; người dùng cần được cấp quyền đọc bucket. Sau khi dựng index, điền cùng cấu hình Neo4j
local vào backend `.env` và cấu hình API key/model của riêng mình.

Neo4j lưu `claim_ids`/`document_ids` trong sự kiện của cạnh, không chứa toàn bộ đoạn trích và bài báo. Export tương ứng với collection hiện tại nằm trong bucket đã cấu hình ở [HUGGINGFACE.md](../../docs/HUGGINGFACE.md):

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
    API --> Safety[Safety rules]
    Safety -->|Qua| Domain[LLM: domain JSON]
    Domain -->|Qua| Plan[LLM: plan JSON]
    Plan --> Validate[Kiểm tra plan và chuẩn hóa Anh–Việt]
    Validate --> Graph[Neo4j: liên kết thực thể và BFS multi-hop]
    Graph --> Select[Chọn cạnh và đường đi theo intent]
    Select --> Evidence[Tra claim và bài báo trong SQLite evidence]
    Evidence --> LLM[LLM tổng hợp facts và sources]
    Safety -->|Chặn| Reply[Phản hồi trực tiếp]
    Domain -->|Chặn| Reply
    Validate -->|Cần làm rõ| Reply
    Graph -->|Tên mơ hồ hoặc chưa xác định| Reply
    Select -->|Không có cạnh phù hợp| Reply
    LLM --> Store[(PostgreSQL / SQLite)]
    Reply --> Store
    Store -->|SSE / lịch sử và graph| UI
```

Frontend giữ bố cục và thành phần assistant-ui đã tùy chỉnh, dùng runtime adapter để gọi FastAPI. Backend dùng Pydantic xác thực dữ liệu, SQLAlchemy quản lý hội thoại, Neo4j Python driver đọc đồ thị và httpx nhận stream LLM. Không thêm framework agent; luồng xử lý được viết trực tiếp để dễ đọc và điều chỉnh.

### Pipeline một câu hỏi

1. Backend lưu câu hỏi và tạo câu trả lời ở trạng thái `pending` trước khi xử lý. Nếu request là gửi lại câu đã hoàn tất, đọc lại kết quả đã lưu thay vì chạy pipeline lần nữa.
2. **Safety guard:** quy tắc chặn các cụm yêu cầu nguy hiểm rõ ràng, không gọi LLM. Đây là bộ lọc cơ bản, không bảo đảm nhận diện mọi cách diễn đạt nguy hiểm.
3. **Domain guard:** một lần phân loại riêng giới hạn nội dung vào kinh tế và đầu tư quốc tế; xét các câu hỏi gần đây để hiểu câu nối tiếp. Bị một trong hai guard chặn thì lưu phản hồi từ chối, trả graph rỗng và không lập plan, truy vấn Neo4j hay gọi LLM sinh câu trả lời. JSON phân loại không hợp lệ/lỗi provider trở thành lỗi có thể thử lại, không tự cho qua guard.
4. **Lập plan:** LLM trả JSON gồm `entities`, `terms`, `relations`, `intent`, `max_hops`, khoảng ngày và câu hỏi làm rõ. Pydantic kiểm tra schema, loại quan hệ và giới hạn; LLM không sinh Cypher để thực thi. Ý định gồm tìm nhà đầu tư, danh mục đầu tư, đồng đầu tư, đường nối và quan hệ tổng quát. Câu mơ hồ như “quỹ đầu tư Google” được hỏi lại, không ép vào mẫu từ khóa.
5. **Chuẩn hóa:** bỏ dấu, chuẩn hóa chữ hoa/thường và khoảng trắng; mở rộng tên quốc gia/tổ chức qua từ điển Anh–Việt trong backend, gộp thực thể trùng. Không dùng biến thể tên thương hiệu do model tự đoán. Ví dụ `Mỹ` ↔ `United States`, `Nhật Bản` ↔ `Japan`. Cypher bỏ dấu bằng hàm gốc, không cần APOC. Ưu tiên khớp chính xác; alias quốc gia/tổ chức chỉ khớp toàn bộ tên. Nếu nhiều thực thể cùng điểm khớp tốt nhất hoặc thiếu tên trong truy vấn liên hệ, hỏi làm rõ thay vì suy luận trên seed sai.
6. **Truy xuất multi-hop:** liên kết tên với node `Entity`, rồi duyệt breadth-first từ nhiều seed. Frontier của hop tiếp theo chỉ lấy từ láng giềng thực tế của hop trước. Ưu tiên loại quan hệ trong plan, bỏ chu trình và giới hạn lượng dữ liệu. Có thể duyệt hai chiều để tìm liên hệ, nhưng kết quả vẫn giữ đúng chiều `source → target`, thời điểm và trạng thái khẳng định/kiểm duyệt của cạnh.
7. **Chọn dữ kiện và tổng hợp:** backend giữ đúng chiều đầu tư, lấy giao danh mục cho đồng đầu tư hoặc đường nối ngắn nhất trong tập đã truy xuất; lọc sự kiện theo ngày nếu có. Graph trả lời mặc định tối đa 16 cạnh. Nối claim với bài báo qua chỉ mục evidence cục bộ. LLM chỉ nhận facts, đường đi và tối đa 8 trích đoạn, mỗi đoạn 500 ký tự; không phải toàn bộ graph thô. Liên hệ gián tiếp không chứng minh đầu tư trực tiếp hoặc nhân quả. Không có cạnh phù hợp thì trả thiếu dữ liệu ngay, không gọi tổng hợp.
8. **Lưu và hiển thị:** lưu câu trả lời cùng graph, plan, biến thể chuẩn hóa, truy vấn/tham số và đường đi. FE nhận stream rồi hiển thị graph tương ứng.

Đây là workflow cố định, không phải agent tự gọi công cụ: tối đa **3 lần gọi cùng model đang cấu hình** (domain → plan → tổng hợp). Giới hạn output mặc định trong code là 64/512/1024 token; `.env` có thể ghi đè, như domain guard hiện đặt 32. Safety chặn thì không gọi model; domain chặn thì một lần; cần làm rõ hoặc không có dữ liệu thì dừng sau plan, không gọi tổng hợp. Lỗi JSON/provider làm request thất bại, không tự vượt guard hoặc gọi model khác. Các câu Cypher cố định và truyền tham số; backend thực hiện duyệt và kiểm tra kết quả.

**Phần đã có và phần mới đề xuất:** code hiện vẫn dùng một lần gọi planner để lấy cả ý định, tên thực thể, quan hệ và điều kiện. Phương án tách thành phân loại domain + ý định, rồi trích xuất thực thể riêng mới là đề xuất, chưa triển khai. Không có vòng lặp agent tự sửa plan hay tự thử lại với model khác.

| Ý định (`intent`) | Backend chọn dữ kiện |
| --- | --- |
| `investors` | Cạnh `INVESTED_IN` đi vào một thực thể đã khớp |
| `investments` | Cạnh `INVESTED_IN` đi ra từ một thực thể đã khớp |
| `common_investments` | Giao danh mục của các seed, đường `A → C ← B`, cần ít nhất 2 hop |
| `connection` | Đường nối ngắn nhất giữa các seed trong tập đã truy xuất, giữ chiều cạnh gốc |
| `neighborhood` | Các cạnh kề trực tiếp seed trong tập đã truy xuất |
| `ambiguous` | Hỏi làm rõ, chưa truy xuất đồ thị |

Giới hạn có thể chỉnh trong backend `.env`:

| Biến                       | Mặc định | Ý nghĩa                            |
| -------------------------- | -------- | ---------------------------------- |
| `GRAPH_MAX_HOPS`           | `3`      | Số hop tối đa, cho phép 1–4        |
| `GRAPH_MAX_SEEDS`          | `4`      | Số thực thể bắt đầu tối đa         |
| `GRAPH_NEIGHBORS_PER_NODE` | `8`      | Số láng giềng lấy cho mỗi node     |
| `GRAPH_MAX_NODES`          | `60`     | Số node tối đa trong graph kết quả |
| `GRAPH_MAX_EDGES`          | `100`    | Số cạnh tối đa trong graph kết quả |
| `GRAPH_ANSWER_MAX_EDGES`   | `16`     | Số cạnh sau khi chọn dữ kiện trả lời |
| `LLM_GUARD_MAX_TOKENS`     | `64`     | Output domain guard; cấu hình hợp lệ 32–256 |
| `LLM_PLAN_MAX_TOKENS`      | `512`    | Output plan; cấu hình hợp lệ 128–2048 |
| `LLM_MAX_OUTPUT_TOKENS`    | `1024`   | Output tổng hợp; cấu hình hợp lệ 128–4096 |
| `LLM_HISTORY_MESSAGES`    | `6`      | Số message tối đa gửi khi tổng hợp |

Domain guard nhận tối đa 3 câu hỏi người dùng gần nhất (mỗi câu 1.500 ký tự); planner nhận tối đa 6 message hợp lệ (mỗi message 2.000 ký tự). Khi tổng hợp, message cũ giới hạn 2.000 ký tự; câu hỏi mới nhất được giữ nguyên. Ngân sách output bao gồm reasoning nếu provider tính reasoning trong completion, nên số token dành cho văn bản/JSON có thể ít hơn giới hạn này. Bản thử tăng guard/plan lên 2048/4096 chỉ dùng script chẩn đoán; các giá trị đó vượt giới hạn Settings hiện tại, không thể chép nguyên vào `.env`.

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
| `be/app/graph_selection.py`                             | Chọn cạnh đúng hướng, đồng đầu tư và đường nối có giới hạn |
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
- Evidence mở dạng drawer đè bên phải graph, không làm mờ, không chia lại layout; phần graph còn thấy vẫn tương tác được. Drawer chỉ đóng bằng toggle/nút đóng của nó, không đóng khi chạm bên ngoài hoặc nhấn Escape. Nội dung lấy từ claim/bài báo thật, không tự tạo trích dẫn khi thiếu nguồn.

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
