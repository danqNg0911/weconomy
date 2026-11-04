# Weconomy

Pipeline nghiên cứu mã nguồn mở chạy local, tạo **đồ thị tri thức ứng viên** từ tin kinh doanh tiếng Việt và tiếng Anh về tập đoàn đa quốc gia, tỷ phú và quỹ đầu tư quốc tế. Phạm vi đề tài kết nối lãnh đạo công nghệ/tài chính, startup, quỹ đầu tư mạo hiểm và chính phủ qua đầu tư, M&A, kiện chống độc quyền, hợp tác hoặc đứt gãy chuỗi cung ứng. Mỗi quan hệ giữ dấu vết về câu, bài và nguồn để người nghiên cứu kiểm tra.

**Cập nhật 04/11/2026:** bộ kiểm thử được hỗ trợ có **214 test pass**. Dataset v4 đã xử lý lại 393 bản lưu toàn văn, nhận 229 bài và kết thúc với `sources_exhausted`, không có lỗi xử lý. [Snapshot JSON của lần chạy](docs/assets/status-current.json) ghi số liệu dưới đây; dùng `dataset-status` để xem một dataset khác.

| Chỉ số | Mục tiêu | Đã ghi nhận ở v4 |
|---|---:|---:|
| Bài được nhận | Tùy chọn | 229 |
| Node có cạnh | 2.000 | 31 |
| Cạnh phân biệt | 5.000 | 16 |
| Loại quan hệ quan sát được | 10 | 2 |
| Precision | Trên 90% | Chưa đo độc lập |

Mục tiêu số lượng **chưa đạt**. So với bản cũ, bản sửa khôi phục một bài lỗi NER, loại ba claims gán sai vai trò người sáng lập và khôi phục hai claims CEO có bằng chứng. Kết quả còn 17 claims hỗ trợ 16 cạnh phân biệt; đây là ứng viên máy trích xuất, chưa được nghiệm thu precision. Dữ liệu cũ được giữ ở dataset riêng. Corpus hiện tại còn hạn chế về phân loại thực thể Việt và độ đa dạng quan hệ; tăng ngân sách URL không bảo đảm đạt các ngưỡng.

![Ví dụ các cạnh ứng viên trong export v4 thực tế](docs/assets/relation-candidates.png)

*Ảnh xem trước 8 trong 16 cạnh của export v4 thực tế tại `data/experiments/collection-20261104/v4-export`. Corpus có 229 bài được nhận, 31 node có cạnh và 2 loại quan hệ. Các cạnh đều là ứng viên tự động, trạng thái `unreviewed`; hình chỉ hiện tên thực thể và predicate, không sao chép câu bài báo.*

![Dấu vết từ một quan hệ ứng viên đến bài nguồn thực tế](docs/assets/provenance-trace.png)

*Một claim trong export v4 được lần ngược về hostname nguồn, document ID và offset evidence trong thân bài; văn bản bài báo không được chép vào ảnh.*

![Phát lại output CLI status thực tế](docs/assets/dataset-status-replay.gif)

*GIF phát lại rút gọn output JSON của `dataset-status` trên dataset v4, cùng số liệu với snapshot phía trên. Đây là minh họa CLI, không phải bản ghi màn hình giao diện.*

## Cài đặt trên Windows

Cần Python 3.11–3.13, `uv` và kết nối mạng cho lần cài đầu. Bộ NLP dùng spaCy tiếng Anh và underthesea tiếng Việt. Cài model spaCy ghim phiên bản riêng; dùng `--no-sync` ở các lần chạy sau để `uv` không gỡ model này.

```powershell
cd D:\Project\weconomy
uv sync --locked --extra nlp --extra dev
uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
uv run --no-sync weconomy sources
```

Lệnh `sources` liệt kê nguồn theo policy hiện tại. Có thể probe tối đa một bài mỗi nguồn bằng `sources --check`; probe không xác nhận toàn bộ publisher, RSS hay quyền tái sử dụng nội dung.

## Thu thập dataset có thể tiếp tục

Mặc định, lệnh dùng `config/collection.yaml` và lưu catalog cùng các batch vào `data/datasets/international-business`. Dòng lệnh dưới đây đặt đúng các ngưỡng chính và ngân sách tối đa 5.000 URL được phân bổ để thử:

```powershell
uv run --no-sync weconomy collect-dataset `
  --dataset data/datasets/international-business `
  --nodes 2000 --relations 5000 --relation-types 10 `
  --max-candidates 5000 --batch-size 20 --ner models
```

`--max-candidates` là giới hạn số URL thử trên toàn dataset, không phải số bài hợp lệ hay cam kết đạt ngưỡng. Có thể chỉ định nguồn bằng cách lặp `--source <id>`; dùng ID đang được bật trong `config/sources.yaml`. Nếu không chỉ định nguồn, collector xét các nguồn tin có feed và được cho phép trong policy hiện tại.

Nếu dataset đã tồn tại, tiếp tục với cùng đường dẫn và thêm `--resume`:

```powershell
uv run --no-sync weconomy collect-dataset `
  --dataset data/datasets/international-business `
  --nodes 2000 --relations 5000 --relation-types 10 `
  --max-candidates 5000 --batch-size 20 --ner models --resume
```

Xem trạng thái và xuất các bảng đã commit thành JSONL:

```powershell
uv run --no-sync weconomy dataset-status data/datasets/international-business
uv run --no-sync weconomy export-dataset data/datasets/international-business `
  --output data/exports/international-business
```

Export gồm `articles.jsonl`, `entities.jsonl`, `relations.jsonl`, `claims.jsonl` và manifest. CLI từ chối ghi đè export đã tồn tại; chọn thư mục đầu ra mới nếu cần xuất lại. Mã thoát `0` nghĩa là hoàn tất hoặc đã đạt mọi ngưỡng được yêu cầu; `2` nghĩa là kết thúc lượt nhưng ngưỡng chưa đạt; `1` báo lỗi. Đọc `counts`, `remaining`, `errors` và `targets_met` trước khi sử dụng kết quả.

GNU Make là tiện ích tùy chọn; trên Windows, các lệnh `uv` ở trên không cần Make. Ví dụ chạy và tiếp tục bằng Make:

```powershell
make collect NODES=2000 RELATIONS=5000 RELATION_TYPES=10 MAX_CANDIDATES=5000 BATCH_SIZE=20 NER=models
make collect NODES=2000 RELATIONS=5000 RELATION_TYPES=10 MAX_CANDIDATES=5000 BATCH_SIZE=20 NER=models RESUME=1
make dataset-status
make export-dataset
```

Có thể đổi đường dẫn bằng `DATASET=...` và `OUTPUT=...`. Xem [toàn bộ tham số và cách đếm](docs/collection.md).

## Cách dữ liệu đi qua pipeline

| Lớp | Nội dung | Vai trò |
|---|---|---|
| Bronze | HTML nhận được, URL, checksum, publisher và thông tin truy xuất | Dấu vết nguồn; không phát hành lại nội dung báo chí |
| Silver | Bài đã chuẩn hóa, câu và mention có offset | Chỉ nội dung qua cổng kiểm tra thân bài mới đủ điều kiện NLP mặc định |
| Gold | Entity, claim, event và relation kèm predicate, evidence và provenance | Đầu ra trích xuất tự động; quan hệ vẫn cần người rà soát |
| Catalog | SQLite theo dõi queue, quyết định nhận và các batch Parquet bất biến | Cho phép tiếp tục bằng `--resume`, xem status và export JSONL |

Schema và ý nghĩa các trường nằm trong [SCHEMA.md](docs/SCHEMA.md), quy trình thân bài trong [FULLTEXT.md](docs/FULLTEXT.md), và kiến trúc trong [ARCHITECTURE.md](docs/ARCHITECTURE.md). Catalog/JSONL export không phải immutable run Parquet; các lệnh `import-neo4j` và `hf-push` nhận run Parquet hợp lệ, không nhận thư mục catalog hay export.

## Xử lý lại HTML đã lưu

`collect-dataset --from-run` trích xuất và chạy NLP lại từ bronze của một run đã lưu, theo từng batch. Lặp cờ này để ghép nhiều run; bản chụp được kiểm tra checksum và policy nguồn hiện tại trước khi xử lý. Đầu ra giữ dấu vết về run, document và checksum gốc. Ví dụ sau dùng đường dẫn run của bạn thay cho `RUN_ID`:

```powershell
uv run --no-sync weconomy collect-dataset `
  --dataset data/datasets/replayed-business `
  --from-run data/runs/RUN_ID --batch-size 20 --max-candidates 1000 --ner models
```

Có thể bổ sung run khác hoặc tiếp tục thu RSS vào cùng dataset bằng `--resume` khi cấu hình xử lý tương thích. Khi đổi NER/rule, tạo dataset mới để giữ kết quả cũ và đo trước–sau. Xem [hướng dẫn replay và ngân sách](docs/collection.md).

## Policy nguồn và giới hạn

Nguồn được chọn từ `config/sources.yaml`; policy có thể thay đổi. Wikinews bị loại khỏi collection dataset; Reuters, Bloomberg và TechCrunch hiện tắt trong policy. Collector tôn trọng allowlist, robots, giới hạn tốc độ/kích thước và redirect; không vượt paywall hay cơ chế chống bot. Hãy kiểm tra lại nguồn trước khi chạy.

Quyền truy cập trang hoặc RSS không cấp quyền tái phân phối toàn văn. Dữ liệu báo được giữ local và không đưa snapshot báo thương mại vào Git. `body_checked` chỉ xác nhận nội dung có trong HTML đã nhận; nó không chứng minh đã lấy được phần ẩn, phân trang hay sau paywall. Bộ lọc chủ đề là heuristic, không phải phép đo độ chính xác.

Các fixture trong `samples/` là trích đoạn có ghi nhận giấy phép, dùng kiểm tra extraction/NLP offline; chúng không đại diện cho tin tức hiện hành hay corpus thu thập đầy đủ. Không dùng chúng thay kết quả thu thập thực.

## Lệnh khác

```powershell
uv run --no-sync weconomy schema
uv run --no-sync weconomy sources --check
uv run --no-sync pytest -q tests --ignore tests/test_core.py
uv run --no-sync ruff check src/weconomy tests --exclude test_core.py
```

Ví dụ run immutable, reprocess, gán nhãn, Neo4j và Docker nằm trong [các lệnh bổ sung](docs/commands.md); trạng thái triển khai và mục lục tài liệu ở [docs/README.md](docs/README.md). Quy trình Hugging Face nằm trong [HUGGINGFACE.md](docs/HUGGINGFACE.md). Bộ test `tests/test_core.py` là pilot suite cũ, cần dependencies riêng.

## Tài liệu

- [Trạng thái, bằng chứng và việc chưa nghiệm thu](docs/STATUS.md)
- [Thu thập dataset, resume và giới hạn ngân sách](docs/collection.md)
- [Toàn văn và cách ly nội dung](docs/FULLTEXT.md)
- [Schema, predicate và provenance](docs/SCHEMA.md)
- [Gán nhãn và đánh giá](docs/ANNOTATION.md)
- [Lộ trình](docs/ROADMAP.md)

Ảnh PNG và GIF có thể tạo lại từ JSONL export và output JSON của `dataset-status` bằng `scripts/render_readme_media.py`. Trên Windows, lưu trạng thái rồi chạy renderer như sau; Pillow chỉ được nạp trong một môi trường tạm, không đổi `pyproject.toml` hay `uv.lock`:

```powershell
$dataset = "data/datasets/international-business"
uv run --no-sync weconomy dataset-status $dataset | Set-Content -Encoding utf8 "$dataset/status.json"
uv run --no-project --with pillow python scripts/render_readme_media.py `
  --export-dir data/exports/international-business `
  --status-json "$dataset/status.json" --output-dir docs/assets --max-edges 8
```

Microsoft Edge được dùng để render SVG; Pillow tạo GIF với 700 ms giữa các bước, dừng 2,5 giây ở trạng thái cuối rồi lặp lại. Ảnh graph mặc định vẽ tối đa 8 cạnh thật, còn header giữ tổng số từ catalog; renderer kiểm tra counts giữa JSON status và export trước khi ghi ảnh.
