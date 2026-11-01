# Weconomy — News Knowledge Graph

Pipeline mã nguồn mở, chạy local cho mạng tập đoàn, cá nhân và quỹ đầu tư từ văn bản Việt/Anh.
Mục tiêu nghiệm thu là **2.000 thực thể / 5.000 sự kiện quan hệ / 10 loại quan hệ / precision ≥90%**.
Các mục tiêu này **chưa đạt**. Xem số đo và bằng chứng ở `reports/SPRINT1.md`.
Kết quả pilot ngày 31/10 sau sửa review, kiểm Docker và nhập Neo4j thật ở `reports/FINAL_2026-10-31.md`.
Các đợt mở rộng sau pilot ghi số đo trong `data/runs/<id>/manifest.json`; dùng manifest của corpus
đã gom để xem số liệu mới nhất. Theo yêu cầu hiện tại, chưa làm báo cáo nộp.
`initial.md` là đề bài gốc, được giữ nguyên.

**Người mới bắt đầu:** đọc [trạng thái hiện tại, giới hạn và những việc chưa làm](docs/STATUS.md).
Mục lục tài liệu nằm ở [docs/README.md](docs/README.md).

**Chia sẻ corpus trong nhóm:** đã có CLI `hf-push` / `hf-pull` cho Hugging Face Dataset Hub private,
checksum và phiên bản commit. Xem [hướng dẫn Hugging Face](docs/HUGGINGFACE.md).
Hiện mới kiểm thử local/Hub giả lập; chưa upload corpus thật lên tài khoản nhóm.

## Thu thập thân bài và chạy NER/quan hệ (cập nhật 31/10)

Nhánh `duy` có lệnh chạy RSS → tải HTML gốc → kiểm định thân bài → NER/RE → Parquet:

```powershell
cd D:\Project\weconomy
# Cài extras/model như hướng dẫn NER bên dưới nếu máy mới chưa có.
uv run --no-sync weconomy collect --source vnexpress --source tuoitre --source techcrunch --limit 3 --ner models
$run = (Get-ChildItem data/runs -Directory | Where-Object {
    $runManifestPath = Join-Path $_.FullName 'manifest.json'
    (Test-Path $runManifestPath) -and ((Get-Content $runManifestPath -Raw | ConvertFrom-Json).status -eq 'completed')
} | Sort-Object Name | Select-Object -Last 1).FullName
uv run --no-sync weconomy validate $run
uv run --no-sync weconomy export $run --table articles --output "$run/articles.jsonl"
uv run --no-sync weconomy export $run --table entities --output "$run/entities.jsonl"
uv run --no-sync weconomy export $run --table relations --output "$run/relations.jsonl"
```

`--limit` là số URL bài thử mỗi nguồn, không hứa đủ từng ấy bài hợp lệ. Mỗi bài lưu bytes gốc
ở `bronze/html/<document_id>.html` và bronze Parquet, gồm checksum/source/URL/headers/căn cứ truy cập.
`discovery.json` giữ URL và metadata RSS; **RSS summary không được dùng thay thân bài**.
Article JSONL chứa văn bản đầy đủ đã lấy cùng trạng thái và chỉ số kiểm tra. Entity/relation JSONL
là đầu ra ứng viên; relation giữ câu evidence và offset, không tự nhận đã đạt precision mục tiêu.

Nguồn có adapter DOM riêng. Loại sidebar, related, quảng cáo, comment, caption, bảng và nội dung ẩn;
so Trafilatura với các đoạn thân bài sạch. Nếu Trafilatura bỏ đoạn thì phục hồi từ DOM thân bài,
giữ tiêu đề mục và đoạn cuối. Chỉ `body_checked` mới được chạy NLP mặc định.

RSS dùng kinh doanh của VnExpress và ưu tiên startup/venture của TechCrunch, có XML/entries khi kiểm tra
local ngày 31/10. Feed `doanh-nghiep.rss` đã được thử nhưng không giữ trong config vì trả nhiều hồ sơ
sản phẩm từ năm 2021. XML hợp lệ không chứng minh đây là feed tin đúng chủ đề hoặc còn cập nhật.
`body_checked` nghĩa là đã lấy đủ phần thân bài **đang có trong HTML được trả về**, không chứng nhận
nội dung nằm ở trang tiếp theo/JavaScript/paywall mà server không gửi. `partial`, `restricted`, `unknown`
được giữ riêng, không tạo thực thể/cạnh. Kết quả run có bài bị cách ly/lỗi trả exit code 1 để kiểm tra.

Chạy lại parser hoặc đổi NER trên cùng dữ liệu **không cần tải báo lần nữa**:

```powershell
uv run --no-sync weconomy run --from-run $run --ner models
```

Kết quả tạo run mới, giữ nguyên ngày thu thập và checksum HTML của dữ liệu cũ. Các run/schema 1.0
vẫn đọc được; bản mới 1.1 thêm kiểm định thân bài. Xem `docs/FULLTEXT.md`.

## Chạy ngay trên Windows (PowerShell)

```powershell
cd D:\Project\weconomy
uv sync --locked --extra dev
uv run weconomy run --manifest samples/excerpts/manifest.json --allow-excerpts
$run = (Get-ChildItem data/runs -Directory | Where-Object {
    $runManifestPath = Join-Path $_.FullName 'manifest.json'
    (Test-Path $runManifestPath) -and ((Get-Content $runManifestPath -Raw | ConvertFrom-Json).status -eq 'completed')
} | Sort-Object Name | Select-Object -Last 1).FullName
uv run weconomy validate $run
uv run weconomy analytics $run --output reports/my-analytics.json
uv run pytest -q
uv run ruff check .
```

Mỗi lệnh `run` tạo thư mục mới, không ghi đè lần chạy cũ. Các đầu ra JSON được chỉ định qua
`--output` cũng từ chối ghi đè. Nếu có lỗi bài, CLI trả mã thoát 1 và ghi lỗi vào manifest;
đọc `counts` và `errors` trước khi dùng kết quả. Không suy ra thành công từ việc có thư mục.
Không có yêu cầu API trả phí. Lần cài đầu cần Internet; chạy mẫu sau đó không cần mạng.

## Nội dung thực sự được triển khai

- RSS/Atom bằng feedparser; nhập URL/JSONL khám phá từ Katana tùy chọn.
- Registry adapter theo host, ngôn ngữ, RSS, giấy phép, căn cứ truy cập và nhịp yêu cầu.
- Cổng truy cập dùng chung: HTTPS, allowlist, kiểm tra IP công khai, robots, giới hạn dung lượng,
  timeout, kiểm tra lại mỗi redirect; dừng khi gặp 403/429. Không vượt paywall.
- Trafilatura → chuẩn hóa Unicode NFC và khoảng trắng → chia câu có offset → định tuyến Việt/Anh.
- `run` mặc định: từ điển thực thể có kiểm soát, **không phải open-world NER**. `collect` mặc định dùng models.
  Chế độ `models`: spaCy cho Anh, underthesea cho Việt; lỗi thiếu model được báo rõ.
- Entity resolution bằng alias rõ ràng + loại thực thể. RapidFuzz chỉ gợi ý, không tự gộp gần giống.
- 11 loại quan hệ có ràng buộc kiểu và mẫu trực tiếp Việt/Anh; gồm `AGREED_TO_ACQUIRE` tách khỏi
  thương vụ đã hoàn tất. Không sinh cạnh chỉ vì cùng câu.
  Tránh phủ định, điều kiện, lời đồn, trích dẫn; chưa xử lý coreference/quan hệ ngầm.
- Bronze/silver/gold Parquet có schema cố định kể cả khi rỗng; provenance, evidence, checksum,
  manifest và cấu hình mỗi lần chạy. Graph chứa **machine candidates**, chưa được người duyệt.
- Dedup URL, văn bản chính xác/gần giống; event dedup bảo thủ trong từng tài liệu.
- CLI nhãn câu đầy đủ; P/R/F1 cho NER exact-span và relation exact-triple, Wilson interval.
- Neo4j import có constraint, tham số hóa, một transaction dữ liệu và MERGE idempotent, không xóa.
- NetworkX: thành phần liên thông, shortest paths trên LCC, clustering, centrality, PageRank,
  communities và small-world sigma có điều kiện. GDS để giai đoạn 2, có truy vấn tham khảo.

## Mẫu hợp pháp và giới hạn thu thập

`samples/excerpts/manifest.json` có 3 trích đoạn báo Wikinews tiếng Anh (CC BY 2.5) và
1 trích đoạn Wikipedia tiếng Việt (CC BY-SA 4.0, **nguồn bách khoa**, không tính là báo).
Đây là văn bản thật được đọc qua công cụ tra cứu, bọc lại HTML để thử extraction.
Không phải HTML gốc tải toàn trang, không phải dữ liệu báo chí do AI sáng tác.
Mẫu gồm lịch sử 2006/2007/2018; không đại diện tin tức hiện tại.
Nguồn, ngày đăng (nếu biết), thời điểm ghi nhận, giấy phép, tác giả tập thể, history URL,
phương pháp ghi nhận và checksum đều có trong manifest. Giữ ghi công/giấy phép khi chia sẻ mẫu
và văn bản phái sinh; giấy phép MIT của mã nguồn không thay giấy phép dữ liệu.

Lần tải trực tiếp đầu tiên bị HTTP 403 ở robots.txt; chi tiết nằm trong `samples/manifest.json`.
Script không cố vượt chặn. Có thể thử thu thập lại khi truy cập hợp lệ đã được khôi phục:

```powershell
uv run weconomy discover wikinews_en --limit 10 --output candidate-urls.txt
uv run weconomy run --urls candidate-urls.txt
```

VnExpress, Tuổi Trẻ và TechCrunch được bật cho đợt nghiên cứu local có giới hạn theo yêu cầu người dùng;
kiểm tra robots trước mỗi trang. Dữ liệu giữ trong `data/` bị Git bỏ qua, nhãn copyright publisher,
không tự cấp giấy phép mở cho nội dung báo. Reuters/Bloomberg vẫn `allowed: false`.
Quyền đọc/RSS không đồng nghĩa quyền công bố lại toàn văn; không đưa snapshot báo thương mại vào Git.

Katana không cần cho MVP và chưa cài. Chỉ chạy với nguồn đã cho phép, scope đúng host,
giới hạn độ sâu/nhịp/trang và tuân thủ robots; **cổng Python không kiểm soát crawler ngoài**.
Nhập kết quả khám phá đã có (URL mỗi dòng hoặc JSONL `request.endpoint`):

```powershell
uv run weconomy run --urls katana-output.jsonl
```

Không phát lệnh Katana tự động với nguồn bị khóa. Bộ thu thập hiện tuần tự, tối đa 100 bài/run
mặc định; cấu hình có thể đổi sau khi đo thông lượng và quyền truy cập. Chưa có scheduler phân tán.

## Thu thập tiếp và gom corpus

Mỗi run giữ nguyên snapshot của mình. Thu thập tiếp với danh sách các run đã thành công để bỏ qua
URL đã có toàn văn; bài lỗi hoặc chưa qua NER vẫn được thử lại. Giới hạn là số URL **mới** mỗi nguồn,
không phải số bài chắc chắn đạt. Khi feed không còn URL mới, status là `no_new_documents` và exit code 0.

```powershell
uv run --no-sync weconomy collect --source vnexpress --source tuoitre --source techcrunch --limit 10 --skip-run $run --ner models
# Gán $next bằng đường dẫn run trả về. Gom offline, không cộng số đếm của các lần replay.
uv run --no-sync weconomy merge-runs --run $run --run $next --ner models
```

`merge-runs` chỉ chọn capture `body_checked` và NER thành công. Cùng URL xuất hiện nhiều lần thì
capture cuối trong thứ tự `--run` được chọn, sau đó trích xuất/NLP/dedup nội dung chạy lại từ bronze.
Run gốc không bị sửa. Manifest ghi `merged_from`, `skip_runs` và số URL đã biết. Bài trích đoạn,
bài bị cách ly và các lần replay không được cộng vào corpus. Muốn thử sửa bài lỗi, dùng `run --from-run`
trước khi gom. Giới hạn `max_documents` vẫn áp dụng; không tự nâng ngân sách tải.

## Dùng NER thống kê (tùy chọn)

```powershell
uv sync --locked --extra dev --extra nlp
uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
uv run --no-sync weconomy run --manifest samples/excerpts/manifest.json --allow-excerpts --ner models
```

Model spaCy là tài nguyên cài riêng ngoài `uv.lock`; URL được ghim phiên bản, không tự đổi phiên bản.
Dùng `--no-sync` sau khi cài để uv không xóa model ngoài lock. underthesea có thể cần tải tài nguyên
ở lần dùng đầu. Kiểm tra giấy phép model riêng trước khi phân phối. So sánh chất lượng hai backend
trên cùng bộ nhãn; không suy ra chất lượng từ tên model.

Backend `models` dùng thêm dependency parser spaCy cho một số động từ tiếng Anh: chủ ngữ/tân ngữ
phải khớp mention có offset và đúng kiểu. Có mẫu bị động, mẫu chức danh và khử trùng giữa rules/parser.
Mệnh đề dưới động từ tường thuật khẳng định như `announced/reported` có thể được nhận dưới trạng thái
`reported`; phủ định và tình thái ở cả động từ quan hệ lẫn động từ tường thuật đều phải vượt kiểm tra.
Không giải đại từ, không suy quan hệ từ đồng xuất hiện; câu phủ định và giả định vẫn bỏ qua.
Quan hệ hành động trong câu có lời trích dẫn vẫn bỏ qua; mẫu chức danh có thể nhận phần vai trò
tường minh nằm ngoài cặp ngoặc kép, không lấy vai trò nằm bên trong lời trích dẫn.
Tiếng Việt hiện dùng mẫu câu tường minh, chưa có dependency RE. Các quan hệ đều `unreviewed`;
tăng độ bao phủ của bộ trích xuất không chứng minh precision. Underthesea được căn lại một số biến thể
đặt dấu tương đương như `Tuỳ/Tùy`, giữ nguyên text gốc và offset.

## Đánh giá và kiểm định

```powershell
uv run weconomy label-tasks $run --limit 200 --output reports/labels-to-review.json
# Người gán nhãn: đọc mọi câu, đánh dấu complete, điền reviewer và đầy đủ entities/relations.
uv run weconomy evaluate $run --labels reports/labels-to-review.json --output reports/evaluation.json
```

Đọc `docs/ANNOTATION.md`. Nhãn chưa hoàn chỉnh bị từ chối; câu không có quan hệ vẫn được lấy mẫu
để đo false negatives. Không gán `complete=true` chỉ để chạy qua. Pilot do agent gán nhãn được
ghi rõ, không thay bộ test độc lập. Chưa có workflow duyệt ghi ngược Neo4j.

## Neo4j local

Máy này đã có `.env` với mật khẩu ngẫu nhiên và container dự án đang chạy; giữ nguyên tệp này.
Khi triển khai máy mới, tạo `.env` từ `.env.example` và thay mật khẩu trước khi chạy.

```powershell
docker compose up -d
# Nạp mật khẩu từ tệp local, không in ra màn hình.
$env:NEO4J_PASSWORD = ((Get-Content .env | Where-Object { $_ -like 'NEO4J_PASSWORD=*' }) -split '=', 2)[1]
uv run weconomy import-neo4j $run
```

Browser: http://localhost:7474 (localhost only). Volume giữ dữ liệu. Không chạy `down -v` nếu cần giữ DB.
Importer có thể chạy lại cùng run; ID tài liệu bao gồm URL và checksum nên revision mới không xóa revision cũ.
Tổng count toàn DB có thể lớn hơn count một run. Bằng chứng xem qua `Claim → Sentence → Document`;
edge nghiệp vụ được gộp theo `event_id`. Dữ liệu từ Wikipedia và Wikinews có `Document.kind` riêng.

```cypher
MATCH (c:Claim)-[:ABOUT_EVENT]->(e:Event), (c)-[:EVIDENCED_BY]->(s)-[:IN_DOCUMENT]->(d)
RETURN c.predicate, c.review_status, e.event_id, s.text, d.url, d.license LIMIT 25;
```

Dockerfile ứng dụng cài core dependencies từ `requirements.lock` có hash. Chạy container offline:

```powershell
docker build -t weconomy:corpus-v3 .
docker run --rm --network none --mount "type=bind,source=D:\Project\weconomy\data,target=/app/data" weconomy:corpus-v3 run --manifest samples/excerpts/manifest.json --allow-excerpts
```

Image chỉ chứa backend gazetteer; models chạy trong môi trường local có extras NLP.
GDS chưa được bật tự động và chưa được nghiệm thu.

## Cấu trúc và mở rộng

```text
config/             policy nguồn, alias, tham số
src/weconomy/       access, nlp, pipeline, schema, quality, graph, analytics, cli
samples/            trích đoạn thật có ghi công + log thu thập thất bại
tests/              logic và tích hợp offline; câu nhân tạo chỉ nằm ở test
docs/               kiến trúc, schema, hướng dẫn nhãn, lộ trình
reports/            báo cáo sơ bộ và số đo thực
data/runs/<id>/     bronze/, silver/, gold/, manifest + config/policy snapshots (gitignored)
```

Xem `docs/ARCHITECTURE.md`, `docs/SCHEMA.md`, `docs/ROADMAP.md`.
Không thêm orchestration/Kafka/UI cho pilot. Những điểm cần nâng cấp trước khi mở rộng:
NER/linking ngoài từ điển có kiểm định, RE Việt và attribution, entity linking có duyệt, event identity có thời gian,
index dedup tăng dần, annotation độc lập và thu thập nguồn đủ phép ở quy mô lớn hơn.

## Nguồn kỹ thuật chính

- [Trafilatura](https://trafilatura.readthedocs.io/en/latest/usage-python.html)
- [feedparser](https://feedparser.readthedocs.io/en/latest/)
- [spaCy models](https://spacy.io/usage/models)
- [underthesea](https://github.com/undertheseanlp/underthesea)
- [Katana](https://github.com/projectdiscovery/katana)
- [Neo4j Docker](https://neo4j.com/docs/operations-manual/current/docker/introduction/)
- [NetworkX sigma](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.smallworld.sigma.html)
- [Wikinews copyright](https://en.wikinews.org/wiki/Wikinews:Copyright)
