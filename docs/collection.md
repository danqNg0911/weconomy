# Crawl nguồn và tạo dataset

## Đường thu thập hiện tại

`weconomy crawl` dùng Katana chạy trong Docker để khám phá trang bài từ các danh mục trong `config/collection.yaml`. Mỗi target chỉ nhận URL liên kết trong card bài của trang danh mục đó; menu và link sang danh mục khác bị loại. URL còn được lọc theo host, robots.txt và regex bài. Thân bài dùng selector riêng theo nguồn, sau đó qua pipeline và lưu thành immutable run trong `data/runs/`. Log hiển thị số từ, đoạn và câu NLP theo từng bài. Không có RSS discovery trong đường chạy này.

Collector tự nhận diện liên kết trang kế tiếp từ dấu hiệu trong DOM (`rel`, nhãn, class hoặc `alt` như “next”/“trang sau”), nên không ghim cấu trúc URL phân trang của từng báo vào config. Nó tải tuần tự, lấy bài mới và dừng khi hết liên kết nhận diện được, đạt giới hạn bài target hoặc chạm `crawl.max_pages_per_target`. URL kế tiếp phải cùng host, qua policy và robots; URL đã gặp không tải lại. Nguồn không đánh dấu rõ liên kết trang sau sẽ dừng tại trang hiện tại.

```powershell
uv run --no-sync weconomy sources
uv run --no-sync weconomy sources --check
uv run --no-sync weconomy crawl --config config/collection.yaml
uv run --no-sync weconomy collect
```

Docker Desktop phải chạy và image Katana phải tải được. `sources --check` chỉ kiểm tra policy/robots ở gốc host, không thử khám phá hay tải bài. Có thể giới hạn crawl bằng một hay nhiều `--target ID`.

Các selector card bài, phân trang tùy nguồn và thân bài nằm trong `targets` của `config/collection.yaml`. Selector thân bài cũng được khai báo trong `config/sources.yaml` để khi phát lại run, pipeline tiếp tục dùng đúng vùng nội dung. `body_checked` xác nhận vùng thân bài đạt cổng chất lượng; không thể chứng minh bài không bị chia trang, ẩn bằng JavaScript hoặc khóa sau paywall.

## Tạo catalog có thể tiếp tục

`weconomy collect` là lệnh dùng thường ngày: nó chạy crawl, lấy các run vừa tạo và nạp vào catalog mặc định. Mục tiêu mặc định là 2.000 node, 5.000 cạnh và 11 loại quan hệ (>10). Tiếp tục catalog bằng `--resume`; lọc target bằng `--target ID` lặp lại, hoặc đổi nơi lưu bằng `--dataset PATH`.

```powershell
uv run --no-sync weconomy collect
uv run --no-sync weconomy collect --resume
```

`--resume` kiểm tra fingerprint trước khi crawl, nên catalog không tương thích sẽ dừng sớm và không tạo run mới. `--force` tạo một catalog mới có hậu tố thời gian/ID duy nhất cạnh đường dẫn đã chọn; dataset cũ được giữ nguyên. Batch lỗi được ghi nguyên nhân và collector vẫn xử lý các batch còn lại. Chạy lại với `--resume` để đưa URL lỗi vào hàng đợi thử lại. Trên terminal tương tác, trạng thái hiện ở dòng cuối; lỗi được tô đỏ. JSON tổng kết vẫn ghi ra `stdout`, log tiến độ ghi ra `stderr`.

Trong lúc chạy, terminal in target đang crawl, số URL tìm thấy, URL bài đang xử lý, trạng thái từng bài và số node/cạnh theo batch. Các bước kéo dài phát heartbeat mỗi 10 giây để nhận biết tiến trình còn hoạt động. Log tiến độ ghi vào `stderr`; JSON tổng kết ghi vào `stdout`.

`collect-dataset` vẫn có sẵn cho thao tác thủ công/offline; lệnh này không tự khám phá nguồn và cần `--urls FILE` hoặc `--from-run PATH`:

```powershell
uv run --no-sync weconomy collect-dataset `
  --from-run data/runs/RUN_ID `
  --nodes 2000 --relations 5000 --relation-types 11 `
  --max-candidates 10000 --batch-size 20 --ner models
```

Lượt crawl hiện bị giới hạn ở **500 URL** bởi `max_articles` và `max_documents`; mỗi target có tối đa 100 bài và 100 trang danh mục theo `crawl.max_pages_per_target`, cùng các page/time caps của Katana. Mục tiêu có thể chưa đạt; tăng ngân sách không tự tạo thêm bài hoặc quan hệ. Không dùng `--resume` để đổi processing fingerprint.

`--max-candidates` là số URL tối đa được phân bổ trong catalog, không phải số bài hợp lệ và không tự tạo candidate. `--relations` đếm cạnh phân biệt `(subject, predicate, object)`; `claims` là số câu/bằng chứng hỗ trợ. `nodes` đếm endpoint có cạnh. Các ngưỡng đầy đủ trong đề bài là 2.000 node, 5.000 cạnh và 11 loại quan hệ (>10); phạm vi quốc tế hẹp hơn cho phép tối thiểu 1.000 node. Không có lệnh nào bảo đảm đạt chỉ tiêu khi nguồn/candidate không đủ hoặc extractor không tìm được cạnh.

Khi lượt dừng, kiểm tra số liệu và trạng thái:

```powershell
uv run --no-sync weconomy dataset-status
uv run --no-sync weconomy export-dataset
```

Mặc định catalog ở `data/datasets/international-business-katana`, export ở `data/exports/international-business-katana`. Dùng `--dataset PATH` hoặc `--output PATH` khi muốn chọn vị trí khác. Catalog cũ `data/datasets/international-business` được giữ nguyên; nó được tạo bởi pipeline RSS trước và không thể resume an toàn với fingerprint mới.

Mã thoát `0` nghĩa là đã đạt mục tiêu (hoặc không đặt mục tiêu); `2` là đã xử lý đầu vào nhưng chưa đạt ngưỡng; `1` là lỗi. Xem `counts`, `remaining`, `errors`, `reason` và `targets_met`. Export gồm articles, entities, relations, claims và manifest; nếu thư mục export đã có, CLI tạo thư mục tên duy nhất để giữ bản cũ.

## Đầu vào URL trực tiếp

Mỗi dòng của file là một URL bài; URL vẫn qua policy hiện tại trước khi tải:

```powershell
uv run --no-sync weconomy collect-dataset `
  --urls data/input/article-urls.txt `
  --nodes 2000 --relations 5000 --relation-types 11 `
  --max-candidates 10000 --batch-size 20 --ner models
```

## Giới hạn và kết quả đã ghi nhận

Quan hệ là ứng viên tự động, cần đọc evidence và rà soát thủ công. Độ chính xác trên 90% chưa được xác minh bằng bộ nhãn độc lập. NER tiếng Việt và độ bao phủ predicate còn hạn chế; thêm URL không đồng nghĩa thêm node/cạnh.

Lượt kiểm tra Katana ngày 05/11/2026 đã lấy 100 URL, xử lý 10 bài trong safety cap và dừng khi đạt 100 entity rows (thực tế 219); kết quả có 0 relation. Đây là bằng chứng đường crawl/body hoạt động, đồng thời cho thấy mục tiêu graph hiện chưa đạt. Dataset replay ngày 04/11 ghi nhận 229 bài, 31 node có cạnh, 16 cạnh phân biệt, 2 loại quan hệ; đây là snapshot lịch sử. Không cộng các số liệu giữa các run/replay.

Catalog SQLite theo dõi queue và các batch Parquet bất biến. URL được canonicalize và chống lặp trong catalog; bản sao nội dung được phát hiện khi ingest. Catalog/JSONL export không phải immutable run Parquet; `import-neo4j` và `hf-push` nhận run Parquet hợp lệ.

Collector tuân thủ allowlist, robots, giới hạn tốc độ/kích thước và redirect; không vượt paywall hay cơ chế chống bot. Quyền truy cập trang không đồng nghĩa quyền tái phân phối toàn văn. Xem [schema](SCHEMA.md), [toàn văn](FULLTEXT.md) và [trạng thái triển khai](STATUS.md).
