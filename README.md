# Weconomy

Pipeline nghiên cứu mã nguồn mở chạy local, tạo **đồ thị tri thức ứng viên** từ tin kinh doanh tiếng Việt và tiếng Anh về tập đoàn đa quốc gia, tỷ phú và quỹ đầu tư quốc tế. Phạm vi đề tài kết nối lãnh đạo công nghệ/tài chính, startup, quỹ đầu tư mạo hiểm và chính phủ qua đầu tư, M&A, kiện chống độc quyền, hợp tác hoặc đứt gãy chuỗi cung ứng. Mỗi quan hệ giữ dấu vết về câu, bài và nguồn để người nghiên cứu kiểm tra.

**Cập nhật 05/11/2026:** discovery hiện dùng Katana; đường RSS, `feedparser` và pilot `news_collector` đã được gỡ. Lệnh `collect` tự crawl và nạp vào catalog mặc định; `collect-dataset` vẫn nhận URL/run rõ ràng. Bộ kiểm tra hiện có **236 test pass** và Ruff qua. Dataset v4 bên dưới là snapshot lịch sử ngày 04/11; lượt crawl 05/11 ban đầu có 0 relation, còn phát lại 275 câu bằng code mới tìm được 2 cạnh REQUESTS. Các kết quả này chưa phải phép đo precision độc lập.

| Chỉ số | Mục tiêu | Đã ghi nhận ở v4 |
|---|---:|---:|
| Bài được nhận | Tùy chọn | 229 |
| Node có cạnh | 2.000 | 31 |
| Cạnh phân biệt | 5.000 | 16 |
| Loại quan hệ quan sát được | 10 | 2 |
| Precision | Trên 90% | Chưa đo độc lập |

Mục tiêu số lượng graph **chưa đạt**. So với bản cũ, bản sửa khôi phục một bài lỗi NER, loại ba claims gán sai vai trò người sáng lập và khôi phục hai claims CEO có bằng chứng. Kết quả còn 17 claims hỗ trợ 16 cạnh phân biệt; đây là ứng viên máy trích xuất, chưa được nghiệm thu precision. Dữ liệu cũ được giữ ở dataset riêng. Corpus hiện tại còn hạn chế về phân loại thực thể Việt và độ đa dạng quan hệ; tăng ngân sách URL không bảo đảm đạt các ngưỡng.

Lượt test crawl Katana trên trang VnExpress quốc tế (05/11/2026) lấy 100 URL, xử lý 10 bài trong safety cap, và dừng khi đạt 100 entity rows (đếm thực tế 219). Nhưng số relation bằng 0, vì vậy graph nodes/edges bằng 0; NER có nhiều nhãn sai loại. Đây là xác nhận luồng crawl/body extraction, không phải đạt mục tiêu graph hay precision. Crawl config hiện đặt objectives theo graph (1.000 node, 5.000 cạnh, 10 loại); safety cap 100 bài vẫn giới hạn lượt mặc định. Xem chi tiết ở phần [crawl danh mục](#crawl-danh-mục-bằng-katana).

![Ví dụ các cạnh ứng viên trong export v4 thực tế](docs/assets/relation-candidates.png)

*Ảnh xem trước 8 trong 16 cạnh của export v4 thực tế tại `data/experiments/collection-20261104/v4-export`. Corpus có 229 bài được nhận, 31 node có cạnh và 2 loại quan hệ. Các cạnh đều là ứng viên tự động, trạng thái `unreviewed`; hình chỉ hiện tên thực thể và predicate, không sao chép câu bài báo.*

![Dấu vết từ một quan hệ ứng viên đến bài nguồn thực tế](docs/assets/provenance-trace.png)

*Một claim trong export v4 được lần ngược về hostname nguồn, document ID và offset evidence trong thân bài; văn bản bài báo không được chép vào ảnh.*

![Phát lại output CLI status thực tế](docs/assets/dataset-status-replay.gif)

*GIF phát lại rút gọn output JSON của `dataset-status` trên dataset v4, cùng số liệu với snapshot phía trên. Đây là minh họa CLI, không phải bản ghi màn hình giao diện.*

## Cài đặt trên Windows

Cần Python 3.11–3.13, `uv` và kết nối mạng cho lần cài đầu. Bộ NLP dùng spaCy tiếng Anh, underthesea cho NER tiếng Việt và Stanza cho dependency parsing tiếng Việt. Lần đầu dùng `--ner models` cần cài model spaCy và tải model Stanza một lần. Sau đó dùng `--no-sync` để `uv` không gỡ model spaCy cài riêng.

```powershell
cd D:\Project\weconomy
uv sync --locked --extra nlp --extra dev
uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
uv run python -c "import stanza; stanza.download('vi', processors='tokenize,pos,depparse')"
uv run --no-sync weconomy sources
```

Lệnh `sources` liệt kê nguồn theo policy hiện tại. `sources --check` kiểm tra policy và robots.txt ở host gốc; lệnh này không khám phá/tải bài và không xác minh quyền tái sử dụng nội dung.

## Crawl danh mục bằng Katana

Tool crawl mới đọc danh mục từ `config/collection.yaml`, gọi Katana qua Docker CLI, chỉ theo URL cùng host/path danh mục, rồi kiểm tra robots và lọc URL bài theo regex trước khi chuyển cho pipeline hiện có. Trên Windows cần Docker Desktop đang chạy; image Katana phải tải được. Dùng:

```powershell
uv run --no-sync weconomy crawl --config config/collection.yaml
uv run --no-sync weconomy crawl --config config/collection.yaml --target techcrunch_venture
```

Katana là công cụ discovery hiện tại; không còn RSS discovery. YAML quy định target, objective và các safety cap như `max_articles`, `max_documents`, page cap và timebox. `nodes` đếm entity endpoints có relation; `entities` đếm entity rows. Crawl chạy theo batch và dừng khi đạt objectives hoặc hết giới hạn. Entity rows không đồng nghĩa node/cạnh có ý nghĩa hay precision; NER tiếng Việt hiện cần rà soát và đánh giá độc lập.

## Thu thập dataset có thể tiếp tục

Lệnh thường dùng là `collect`: nó chạy Katana, lấy run vừa tạo và nạp vào catalog mặc định `data/datasets/international-business-katana`. Catalog cũ `data/datasets/international-business` được giữ nguyên vì dùng pipeline trước. Truyền `--dataset PATH` chỉ khi muốn lưu sang chỗ khác.

```powershell
uv run --no-sync weconomy collect
```

Mục tiêu mặc định là 1.000 node, 5.000 cạnh và 10 loại. Safety cap crawl hiện là 100 URL nên lệnh có thể dừng khi mục tiêu chưa đạt. Tiếp tục cùng catalog bằng `--resume`:

Nếu dataset đã tồn tại, tiếp tục với cùng đường dẫn và thêm `--resume`:

```powershell
uv run --no-sync weconomy collect --resume
```

Xem trạng thái và xuất các bảng đã commit thành JSONL:

```powershell
uv run --no-sync weconomy dataset-status
uv run --no-sync weconomy export-dataset
```

Export gồm `articles.jsonl`, `entities.jsonl`, `relations.jsonl`, `claims.jsonl` và manifest. CLI từ chối ghi đè export đã tồn tại; chọn thư mục đầu ra mới nếu cần xuất lại. Mã thoát `0` nghĩa là hoàn tất hoặc đã đạt mọi ngưỡng được yêu cầu; `2` nghĩa là kết thúc lượt nhưng ngưỡng chưa đạt; `1` báo lỗi. Đọc `counts`, `remaining`, `errors` và `targets_met` trước khi sử dụng kết quả.

`dataset-status` và `export-dataset` cũng mặc định dùng catalog nói trên. Export mặc định ở `data/exports/international-business-katana`; dùng `--output PATH` nếu muốn lưu nơi khác hoặc tạo export mới.

GNU Make là tiện ích tùy chọn; `make collect` chạy cùng luồng crawl → dataset:

```powershell
make collect
make collect RESUME=1
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

`collect-dataset --from-run` trích xuất và chạy NLP lại từ bronze của một run đã lưu, theo từng batch. Lặp cờ này để ghép nhiều run; bản chụp được kiểm tra checksum và policy nguồn hiện tại trước khi xử lý. Đầu ra giữ dấu vết về run, document và checksum gốc. Ví dụ trên dùng đường dẫn run của bạn thay cho `RUN_ID`.

```powershell
uv run --no-sync weconomy collect-dataset `
  --from-run data/runs/RUN_ID --batch-size 20 --max-candidates 1000 --ner models
```

Có thể bổ sung run khác vào cùng dataset bằng `--resume` khi cấu hình xử lý tương thích. Khi đổi NER/rule, tạo dataset mới để giữ kết quả cũ và đo trước–sau. Xem [hướng dẫn crawl/replay và ngân sách](docs/collection.md).

## Policy nguồn và giới hạn

Nguồn được chọn từ `config/sources.yaml`; policy có thể thay đổi. Collector tôn trọng allowlist, robots, giới hạn tốc độ/kích thước và redirect; không vượt paywall hay cơ chế chống bot. Hãy kiểm tra policy và target trước khi chạy.

Quyền truy cập trang không cấp quyền tái phân phối toàn văn. Dữ liệu báo được giữ local và không đưa snapshot báo thương mại vào Git. `body_checked` chỉ xác nhận nội dung có trong HTML đã nhận; nó không chứng minh đã lấy được phần ẩn, phân trang hay sau paywall. Bộ lọc chủ đề là heuristic, không phải phép đo độ chính xác.

Các fixture trong `samples/` là trích đoạn có ghi nhận giấy phép, dùng kiểm tra extraction/NLP offline; chúng không đại diện cho tin tức hiện hành hay corpus thu thập đầy đủ. Không dùng chúng thay kết quả thu thập thực.

## Lệnh khác

```powershell
uv run --no-sync weconomy schema
uv run --no-sync weconomy sources --check
uv run --no-sync pytest -q tests
uv run --no-sync ruff check src/weconomy tests
```

Ví dụ run immutable, reprocess, gán nhãn, Neo4j và Docker nằm trong [các lệnh bổ sung](docs/commands.md); trạng thái triển khai và mục lục tài liệu ở [docs/README.md](docs/README.md). Quy trình Hugging Face nằm trong [HUGGINGFACE.md](docs/HUGGINGFACE.md).

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
