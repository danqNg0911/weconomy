# Crawl nguồn và tạo dataset

## Đường thu thập hiện tại

`weconomy crawl` dùng Katana chạy trong Docker để khám phá trang bài từ các danh mục trong `config/collection.yaml`. URL được lọc theo host, robots.txt và mẫu URL bài; nội dung sau đó đi qua pipeline, lưu thành immutable run trong `data/runs/`. Không có RSS discovery trong đường chạy này.

```powershell
uv run --no-sync weconomy sources
uv run --no-sync weconomy sources --check
uv run --no-sync weconomy crawl --config config/collection.yaml
uv run --no-sync weconomy collect
```

Docker Desktop phải chạy và image Katana phải tải được. `sources --check` chỉ kiểm tra policy/robots ở gốc host, không thử khám phá hay tải bài. Có thể giới hạn crawl bằng một hay nhiều `--target ID`.

## Tạo catalog có thể tiếp tục

`weconomy collect` là lệnh dùng thường ngày: nó chạy crawl, lấy các run vừa tạo và nạp vào catalog mặc định. Mục tiêu mặc định là 1.000 node, 5.000 cạnh và 10 loại. Tiếp tục catalog bằng `--resume`; lọc target bằng `--target ID` lặp lại, hoặc đổi nơi lưu bằng `--dataset PATH`.

```powershell
uv run --no-sync weconomy collect
uv run --no-sync weconomy collect --resume
```

`collect-dataset` vẫn có sẵn cho thao tác thủ công/offline; lệnh này không tự khám phá nguồn và cần `--urls FILE` hoặc `--from-run PATH`:

```powershell
uv run --no-sync weconomy collect-dataset `
  --from-run data/runs/RUN_ID `
  --nodes 1000 --relations 5000 --relation-types 10 `
  --max-candidates 10000 --batch-size 20 --ner models
```

Lượt crawl hiện bị giới hạn ở **100 URL** bởi `max_articles` và `max_documents`, cùng giới hạn từng target và page/time caps trong config. Mục tiêu có thể chưa đạt; thêm URL không bảo đảm thêm quan hệ. Không dùng `--resume` để đổi processing fingerprint.

`--max-candidates` là số URL tối đa được phân bổ trong catalog, không phải số bài hợp lệ và không tự tạo candidate. `--relations` đếm cạnh phân biệt `(subject, predicate, object)`; `claims` là số câu/bằng chứng hỗ trợ. `nodes` đếm endpoint có cạnh. Các ngưỡng đầy đủ trong đề bài là 2.000 node, 5.000 cạnh và 10 loại; phạm vi quốc tế hẹp hơn cho phép tối thiểu 1.000 node. Không có lệnh nào bảo đảm đạt chỉ tiêu khi nguồn/candidate không đủ hoặc extractor không tìm được cạnh.

Khi lượt dừng, kiểm tra số liệu và trạng thái:

```powershell
uv run --no-sync weconomy dataset-status
uv run --no-sync weconomy export-dataset
```

Mặc định catalog ở `data/datasets/international-business-katana`, export ở `data/exports/international-business-katana`. Dùng `--dataset PATH` hoặc `--output PATH` khi muốn chọn vị trí khác. Catalog cũ `data/datasets/international-business` được giữ nguyên; nó được tạo bởi pipeline RSS trước và không thể resume an toàn với fingerprint mới.

Mã thoát `0` nghĩa là đã đạt mục tiêu (hoặc không đặt mục tiêu); `2` là đã xử lý đầu vào nhưng chưa đạt ngưỡng; `1` là lỗi. Xem `counts`, `remaining`, `errors`, `reason` và `targets_met`. Export gồm articles, entities, relations, claims và manifest; lệnh không ghi đè thư mục export đã có.

## Đầu vào URL trực tiếp

Mỗi dòng của file là một URL bài; URL vẫn qua policy hiện tại trước khi tải:

```powershell
uv run --no-sync weconomy collect-dataset `
  --urls data/input/article-urls.txt `
  --nodes 1000 --relations 5000 --relation-types 10 `
  --max-candidates 10000 --batch-size 20 --ner models
```

## Giới hạn và kết quả đã ghi nhận

Quan hệ là ứng viên tự động, cần đọc evidence và rà soát thủ công. Độ chính xác trên 90% chưa được xác minh bằng bộ nhãn độc lập. NER tiếng Việt và độ bao phủ predicate còn hạn chế; thêm URL không đồng nghĩa thêm node/cạnh.

Lượt kiểm tra Katana ngày 05/11/2026 đã lấy 100 URL, xử lý 10 bài trong safety cap và dừng khi đạt 100 entity rows (thực tế 219); kết quả có 0 relation. Đây là bằng chứng đường crawl/body hoạt động, đồng thời cho thấy mục tiêu graph hiện chưa đạt. Dataset replay ngày 04/11 ghi nhận 229 bài, 31 node có cạnh, 16 cạnh phân biệt, 2 loại quan hệ; đây là snapshot lịch sử. Không cộng các số liệu giữa các run/replay.

Catalog SQLite theo dõi queue và các batch Parquet bất biến. URL được canonicalize và chống lặp trong catalog; bản sao nội dung được phát hiện khi ingest. Catalog/JSONL export không phải immutable run Parquet; `import-neo4j` và `hf-push` nhận run Parquet hợp lệ.

Collector tuân thủ allowlist, robots, giới hạn tốc độ/kích thước và redirect; không vượt paywall hay cơ chế chống bot. Quyền truy cập trang không đồng nghĩa quyền tái phân phối toàn văn. Xem [schema](SCHEMA.md), [toàn văn](FULLTEXT.md) và [trạng thái triển khai](STATUS.md).
