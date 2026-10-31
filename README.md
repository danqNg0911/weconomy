# Weconomy — News Knowledge Graph

Pipeline mã nguồn mở, chạy local cho mạng tập đoàn, cá nhân và quỹ đầu tư từ văn bản Việt/Anh.
Mục tiêu nghiệm thu là **2.000 thực thể / 5.000 sự kiện quan hệ / 10 loại quan hệ / precision ≥90%**.
Các mục tiêu này **chưa đạt**. Xem số đo và bằng chứng ở `reports/SPRINT1.md`.
`initial.md` là đề bài gốc, được giữ nguyên.

## Chạy ngay trên Windows (PowerShell)

```powershell
cd D:\Project\weconomy
uv sync --locked --extra dev
uv run weconomy run --manifest samples/excerpts/manifest.json
$run = (Get-ChildItem data/runs -Directory | Sort-Object Name | Select-Object -Last 1).FullName
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
- NER mặc định: từ điển thực thể có kiểm soát, **không phải open-world NER**.
  Chế độ `models`: spaCy cho Anh, underthesea cho Việt; lỗi thiếu model được báo rõ.
- Entity resolution bằng alias rõ ràng + loại thực thể. RapidFuzz chỉ gợi ý, không tự gộp gần giống.
- 10 loại quan hệ có ràng buộc kiểu và mẫu trực tiếp Việt/Anh. Không sinh cạnh chỉ vì cùng câu.
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

VnExpress, Tuổi Trẻ, Reuters, Bloomberg, TechCrunch mặc định `allowed: false`.
Chỉ đổi cấu hình sau khi có căn cứ cho phép cụ thể, ghi vào `permission_basis` và rà soát terms/robots.
RSS công khai không chứng minh quyền thu thập hoặc tái phân phối toàn văn. Danh sách terms URL của
nguồn bị khóa là điểm bắt đầu rà soát, chưa phải kết luận pháp lý hay xác nhận quyền truy cập.

Katana không cần cho MVP và chưa cài. Chỉ chạy với nguồn đã cho phép, scope đúng host,
giới hạn độ sâu/nhịp/trang và tuân thủ robots; **cổng Python không kiểm soát crawler ngoài**.
Nhập kết quả khám phá đã có (URL mỗi dòng hoặc JSONL `request.endpoint`):

```powershell
uv run weconomy run --urls katana-output.jsonl
```

Không phát lệnh Katana tự động với nguồn bị khóa. Bộ thu thập hiện tuần tự, tối đa 100 bài/run
mặc định; cấu hình có thể đổi sau khi đo thông lượng và quyền truy cập. Chưa có scheduler phân tán.

## Dùng NER thống kê (tùy chọn)

```powershell
uv sync --locked --extra dev --extra nlp
uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
uv run --no-sync weconomy run --manifest samples/excerpts/manifest.json --ner models
```

Model spaCy là tài nguyên cài riêng ngoài `uv.lock`; URL được ghim phiên bản, không tự đổi phiên bản.
Dùng `--no-sync` sau khi cài để uv không xóa model ngoài lock. underthesea có thể cần tải tài nguyên
ở lần dùng đầu. Kiểm tra giấy phép model riêng trước khi phân phối. So sánh chất lượng hai backend
trên cùng bộ nhãn; không suy ra chất lượng từ tên model.

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
docker build -t weconomy:sprint1 .
docker run --rm --network none --mount "type=bind,source=D:\Project\weconomy\data,target=/app/data" weconomy:sprint1 run --manifest samples/excerpts/manifest.json
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
NER ngoài từ điển, RE có cú pháp/negation/attribution, entity linking có duyệt, event identity có thời gian,
dedup xuyên run, annotation độc lập, thu thập nguồn đủ phép và importer đã chạy trên DB thật.

## Nguồn kỹ thuật chính

- [Trafilatura](https://trafilatura.readthedocs.io/en/latest/usage-python.html)
- [feedparser](https://feedparser.readthedocs.io/en/latest/)
- [spaCy models](https://spacy.io/usage/models)
- [underthesea](https://github.com/undertheseanlp/underthesea)
- [Katana](https://github.com/projectdiscovery/katana)
- [Neo4j Docker](https://neo4j.com/docs/operations-manual/current/docker/introduction/)
- [NetworkX sigma](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.smallworld.sigma.html)
- [Wikinews copyright](https://en.wikinews.org/wiki/Wikinews:Copyright)
