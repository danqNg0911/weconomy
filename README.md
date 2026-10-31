# News Collector — kiểm tra khả năng crawl

Pilot Python 3.11+, kiểm tra VnExpress, Tuổi Trẻ, Reuters, Bloomberg và TechCrunch.
Mỗi nguồn lưu **tối đa 10 bài hợp lệ trong cùng database**, tối đa 50 bài tổng cộng.
Nguồn bị hạn chế có thể thu được 0 bài; báo cáo ghi rõ lý do, không coi metadata/RSS summary là bài đầy đủ.

## Cài đặt trên Windows PowerShell

Chạy tại thư mục dự án `F:\Project\ptmxh`:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Không cần activate môi trường nên không phụ thuộc ExecutionPolicy của PowerShell.
Lệnh `python` của máy này mặc định là 3.10; dùng Python trong `.venv` như các ví dụ dưới đây.

## Chạy pilot

```powershell
.\.venv\Scripts\python.exe -m news_collector.cli run --all --limit 10
```

Lệnh tự tạo database, kiểm tra endpoint, tìm URL, tải và bóc tách, lưu dữ liệu, xuất báo cáo.
`--max-articles 10` là đích **mỗi nguồn**, tính cả bài đã lưu từ lần trước. Dùng `--max-attempts` để giới hạn tổng URL thử và `--max-consecutive-restricted` để tạm dừng nguồn sau chuỗi lỗi hạn chế. Chạy lại khi nguồn đã có 10 bài sẽ bỏ qua nguồn đó.
Không có endpoint sử dụng được hoặc hết ngân sách thử URL thì kết thúc với số bài thực tế.
Thông thường mất vài phút vì có khoảng nghỉ tối thiểu 3 giây giữa các request cùng hostname.

Chạy một nguồn hoặc riêng một phương pháp:

```powershell
.\.venv\Scripts\python.exe -m news_collector.cli run --source vnexpress --limit 10
.\.venv\Scripts\python.exe -m news_collector.cli run --source tuoitre --method rss --limit 10
```

Kiểm tra độc lập và xem kết quả:

```powershell
.\.venv\Scripts\python.exe -m news_collector.cli validate-sources --all
.\.venv\Scripts\python.exe -m news_collector.cli stats
.\.venv\Scripts\python.exe -m news_collector.cli export --format jsonl
```

`validate-sources` chỉ tải robots/trang giới thiệu RSS/XML, không tải bài. Nó lưu URL vào hàng đợi và cập nhật trạng thái endpoint trong `configs/sources.yaml`.

## Các file kết quả

| File | Nội dung |
|---|---|
| `data/exports/articles.jsonl` | Toàn bộ bài thành công, mỗi dòng là một JSON UTF-8 |
| `data/raw/<source>/<YYYY-MM>.jsonl` | Bài theo nguồn/tháng thu thập, không phải HTML thô |
| `data/crawler.db` | SQLite: nội dung, queue, provenance, trạng thái lỗi, lịch sử run |
| `data/reports/latest.json` | Báo cáo lần chạy gần nhất |
| `data/reports/<run_id>.json` | Báo cáo từng lần, endpoint, HTTP, robots và lỗi |
| `docs/PILOT_REPORT.md` | Kết quả thử thực tế khi triển khai |

Trong báo cáo, `saved_this_run` là bài mới của lần chạy; `saved_total` là tổng bài của nguồn;
`target_reached` cho biết đủ mẫu hay chưa. `source_status=available` chỉ xác nhận có endpoint chứa URL bài,
không bảo đảm tất cả bài đều truy cập được. `statistics` là thống kê toàn database.
Exit code 0 nghĩa là quy trình đánh giá hoàn tất, **không có nghĩa cả 5 nguồn đều đủ 10 bài**.

## Dừng và tiếp tục

Ctrl+C để dừng. Chạy lại `run` để tiếp tục các URL còn chờ. Không xóa database nếu muốn giữ lịch sử và chống trùng.
Để thử lại lỗi mạng/5xx/429 hoặc extraction sau khi sửa parser:

```powershell
.\.venv\Scripts\python.exe -m news_collector.cli retry-failed
.\.venv\Scripts\python.exe -m news_collector.cli fetch --all --limit 10
```

`retry-failed` chỉ xếp hàng lại, không tải ngay. Không retry 403/404/410 và không chạy trước `Retry-After`;
mỗi URL tối đa 3 lượt xử lý qua hàng đợi. HTTP timeout/5xx có thêm tối đa 2 lần retry nội bộ mỗi lượt.
429 dừng request tới hostname đó trong lần chạy hiện tại. Một tiến trình ghi cho mỗi thư mục dữ liệu.

## Cấu hình

- `configs/settings.yaml`: giới hạn 10 bài, tối đa 30 URL thử/nguồn/lần chạy, 100 URL discovery/nguồn,
  tối đa 2 sitemap gốc/nguồn, 6 sitemap/endpoint và sâu 2 cấp, độ dài tối thiểu 100 từ, timeout, tốc độ và `data_dir`.
- `configs/sources.yaml`: domain, quy tắc URL, trang công bố RSS và endpoint đã kiểm tra. `unknown` nghĩa là chưa xác nhận.
- `configs/keywords.yaml`: chấm điểm relevance; **không loại bỏ** bài không khớp từ khóa trong pilot.

Có thể điền thông tin liên hệ của bạn vào `user_agent`. Thay `data_dir` để làm một pilot độc lập;
giới hạn 10 bài áp dụng riêng từng database. `--config <thư-mục>` đặt trước tên lệnh để dùng bộ cấu hình khác.

## Kiểm thử và phạm vi

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m news_collector.cli --help
```

Tests dùng HTTP/XML/HTML giả lập, không cần Internet. Xem [chi tiết triển khai](docs/IMPLEMENTATION.md).
Không vượt paywall/CAPTCHA, không dùng proxy hay trình duyệt tự động. Ngày thiếu timezone hoặc không xác định để null.
Không có NLP, Neo4j, lọc thời gian/historical crawl hay lưu HTML trong pilot này.
