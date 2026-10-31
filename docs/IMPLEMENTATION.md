# Phạm vi triển khai

Mục tiêu cập nhật: đánh giá truy cập và trích xuất tối đa 10 bài hợp lệ/nguồn. Code bắt buộc `--limit` trong 1–10,
đếm cả bài có sẵn trong SQLite. Giới hạn thử mặc định 30 URL/nguồn/lần chạy; dữ liệu không liên quan vẫn được giữ.

## A — Nền tảng

`pyproject.toml`, `config.py`, `models.py`, `configs/*.yaml`: Python 3.11+, Pydantic article/settings,
CLI Typer, cấu hình nguồn tách khỏi code. Dùng `.venv` do Python mặc định của máy là 3.10.

## B — Discovery

`discovery.py`: tìm RSS từ trang công bố, sitemap từ robots.txt; RSS/Atom, sitemap index/urlset/gzip,
XML không tải external entities/DTD; giới hạn sâu/số sitemap/kích thước. Kiểm tra domain và pattern bài.
Lưu content type, HTTP, số URL, lỗi và thời điểm kiểm tra. XML hợp lệ là tiêu chí quyết định;
content type được ghi nhận vì một số publisher trả XML với MIME không chuẩn.
Sitemap index chỉ được coi available khi tìm được URL bài trong các con đã duyệt.
Không dùng sitemap lastmod làm ngày xuất bản. Queue giữ nhiều endpoint provenance cho cùng URL.

## C — HTTP và extraction

`fetching.py`: AsyncClient chạy tuần tự để dễ kiểm soát tốc độ; kiểm tra robots trên mỗi đích redirect,
không đi ra domain đã cấu hình, giới hạn kích thước body, timeout, backoff; 429 lưu Retry-After và dừng nguồn.
Robots không tải được thì không giả định được phép truy cập. Cache robots trong một lần chạy.
Không giả danh browser/crawler khác. HTTP gzip được giải mã một lần.

`extraction.py`: JSON-LD/HTML metadata, trafilatura, fallback selector; phát hiện paywall/CAPTCHA phổ biến,
kiểm tra title và độ dài. Detector là heuristic, không bảo đảm nhận ra mọi paywall hoặc trang lỗi mới.
Ngày không timezone được để null; không suy đoán từ URL. Canonical ngoài domain bị bỏ qua.
Nguồn hạn chế chỉ giữ metadata discovery trong queue, không ghi article thành công.

## D — Storage và resume

`storage.py`: SQLite WAL, unique URL/canonical/content hash, ID SHA-256, bảng nguồn/endpoint/queue/
provenance/articles/runs/errors. Toàn bộ article JSON được commit cùng trạng thái queue trong một transaction.
JSONL được dựng lại vào file tạm, fsync và replace nguyên tử; khi khởi động dựng lại từ SQLite.
Thiết kế này thay cơ chế append/byte offset trong bản kế hoạch lớn, phù hợp tối đa 50 bài và tránh lệch dữ liệu sau crash.
URL đang fetching khi khởi động được chuyển pending; run đang dở được đánh interrupted.
CLI giữ OS lock tự giải phóng khi tiến trình chết. Không chạy hai writer trên cùng thư mục.

## E — Báo cáo

`processing.py`: normalize URL/text, content hash, keyword relevance có trọng số title/description/content.
`pipeline.py`: điều phối, đếm bài hợp lệ theo nguồn, ghi report JSON từng run; thống kê tổng database tách khỏi số mới.
`cli.py`: init-db, validate-sources, discover, fetch, run, stats, export, retry-failed.
Nguồn thiếu mẫu là một kết quả feasibility hợp lệ; lỗi tham số CLI trả exit code 2.

## F — Kiểm thử và pilot

`tests/test_core.py`, `tests/test_pipeline.py`: fixtures inline cho RSS/Atom, XML gzip/index/cycle, normalization,
metadata/paywall, storage/dedup/recovery, 403/404/429/500/timeout, retry/backoff, redirect robots,
HTTP compression, giới hạn 10 bài và rerun không request thêm. Kết quả live ở `PILOT_REPORT.md`.

## Phần hoãn theo mục tiêu pilot

Không triển khai crawl hàng nghìn bài, CLI lọc ngày, historical crawl, checkpoint sitemap định kỳ,
raw HTML, near-duplicate, giao diện, NLP hay Neo4j. Endpoint được kiểm tra lại thay vì cache vĩnh viễn.
Chỉ khảo sát một số feed public và sitemap trong ngân sách; không kết luận đã tìm hết endpoint của website.
Không lọc chủ đề cứng. Không có bảo đảm đủ 10 bài khi nguồn chặn hoặc thiếu nội dung hợp lệ.

## Điều kiện sử dụng nguồn đã kiểm tra

Trang [VnExpress RSS](https://vnexpress.net/rss) và [Tuổi Trẻ RSS](https://tuoitre.vn/rss.htm)
công bố điều kiện dùng kênh RSS cho cá nhân/tổ chức phi lợi nhuận, yêu cầu thông tin nguồn và quyền yêu cầu ngừng phân phối.
Đây là điều kiện cho RSS, không phải xác nhận quyền tái xuất bản toàn văn. Pilot giữ URL, source và provenance.
Trạng thái kỹ thuật của Reuters/Bloomberg/TechCrunch được ghi theo phản hồi HTTP/robots tại máy chạy;
không coi `available` là giấy phép sử dụng dữ liệu. Chưa xác minh đầy đủ điều khoản tái sử dụng toàn văn của 5 nguồn.
