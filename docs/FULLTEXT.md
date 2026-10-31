# Contract thân bài → NER/quan hệ

Cập nhật body-v2.1: gate được kiểm tra trên trang, không chỉ body; JSON-LD trùng giữ các trường
đồng thuận và restriction của bài chính; bỏ khối phụ theo class/id cụ thể, không xóa substring comment/social.
UTF-8 được xác định trước khi parse để Windows/Linux đọc cùng văn bản, encoding khác giữ khai báo riêng.
Input sai không tạo run; README chọn run hoàn tất có manifest. Bằng chứng: reports/FINAL_2026-10-31.md.

## Dữ liệu nào được xử lý?

CLI `collect` khám phá URL qua RSS, tải trang qua Access có policy/robots/rate/timeout/size limit,
giữ HTML bytes rồi gọi `extract_article`. Adapter DOM của VnExpress/Tuổi Trẻ/TechCrunch chỉ ra vùng
thân bài. RSS title/summary phục vụ discovery, không được ghép vào thân bài để đủ số từ.

Metadata JSON-LD chọn theo canonical URL/@id/mainEntityOfPage; đối tượng bài liên quan có URL khác
không được ghi đè. Nếu không đủ căn cứ phân biệt các đối tượng, không lấy ngày/tác giả tùy tiện.
Ngày thiếu timezone giữ rỗng. Không đổi ngày cập nhật thành ngày xuất bản.

Trước khi ghép văn bản, loại nội dung ẩn (gồm ancestor), scripts, nav/aside/related/comments/ads,
caption ảnh, bảng và khối phụ. Giữ paragraphs/section headings/blockquote/list và khoảng cách inline.
Giữ bytes gốc nên có thể mở rộng trích bảng/caption sau, không mất nguồn.

Trafilatura chạy trên body đã làm sạch; so token của từng đoạn với đầu ra. Khi thiếu bất kỳ đoạn nào,
dùng toàn bộ body DOM sạch (`source_dom_recovery`) thay cho đoạn extract bị cắt.
`trafilatura_coverage` đo tỷ lệ đoạn có đủ chuỗi token trong candidate; `paragraph_coverage`
đo phần body sạch được chọn. Không coi đây là precision hoặc kiểm định của con người.

## Trạng thái nội dung

| content_status | Nghĩa | NLP mặc định |
|---|---|---|
| body_checked | Vùng body đã xác định, đủ dài, không có dấu hạn chế/truncation đã biết; giữ đủ đoạn body sạch | Có |
| partial | Nội dung quá ngắn hoặc có thông báo nội dung bị cắt | Không |
| restricted | Metadata bài chính/khối gate hiển thị/trang challenge chỉ ra hạn chế | Không |
| unknown | Chưa tìm được selector vùng thân bài hoặc chưa rõ capture scope của snapshot | Không |
| excerpt | Snapshot khai báo là trích đoạn, không phải trang đầy đủ | Chỉ với --allow-excerpts, không có dấu hạn chế |

`body_checked` không chứng minh full article trên mọi site: chưa phát hiện mọi phân trang, nội dung
chỉ tải qua JavaScript hay paywall không có dấu hiệu trong HTML. Không tải hoặc vượt các phần đó.
Nếu một publisher đổi layout, thêm/chỉnh adapter + fixture rồi replay raw snapshot để đo lại.

`nlp_eligible` là cổng thật trong pipeline, không chỉ nhãn báo cáo. Document bị cách ly không có
sentence/mention/entity/claim; validator kiểm tra để phát hiện lọt cổng. Nếu NER bị lỗi giữa bài,
không publish nửa tập câu/thực thể của bài đó. Chỉ commit NLP output của một bài sau khi xử lý hết bài.
Precision NER/RE vẫn cần bộ nhãn độc lập; thân bài đầy đủ chỉ giải quyết một nguyên nhân mất bằng chứng.

Khi replay 9 bài thật ngày 31/10, underthesea có token chèn khoảng trắng sau dấu nháy. Alignment mới
chỉ cho phép khác khoảng trắng, đi tuần tự và giữ đúng chữ/ký tự nguồn; không tìm nhảy qua từ khác
để đoán span. Trường hợp không khớp vẫn báo lỗi và cách ly output NLP của bài.
RE có `AGREED_TO_ACQUIRE` cho phát biểu đã thỏa thuận mua lại, với `agreement_reported`; không
gộp vào `ACQUIRED`. Hai alias ORG được duyệt ở pilot (Salesforce/Vingroup) có evidence URL trong config.
Đây là hiệu chỉnh trên pilot đã đọc, không phải điểm kiểm thử held-out hay bảo đảm các tên khác đúng kiểu.

## Lưu trữ và replay

Schema 1.1 thêm:

- Bronze: raw_bytes, raw_path, capture_scope, discovery_endpoint; giữ raw_html cũ để tương thích.
- Silver/articles: canonical_url, content_status, extraction_method, extractor_version,
  word_count, body_paragraphs, paragraph_coverage, trafilatura_coverage, nlp_eligible,
  quality_flags (JSON), authors (JSON), published_at.
- `<run>/bronze/html/<id>.html`: bytes đúng checksum, không tái tạo từ text.
- `<run>/discovery.json`: nguồn discovery và metadata RSS khi dùng collect.

`run --from-run <old>` đọc bronze, kiểm checksum, chạy parser/NLP hiện tại trong run mới, không request
mạng và không ghi đè snapshot. Manifest giữ `reprocessed_from`, config/alias/source snapshots và package versions.
Checksum kiểm bytes gốc, không phải chuỗi decode replacement. Neo4j chỉ nhận metadata; không gửi raw HTML
bytes vào query. Document có content_status/nlp_eligible để phân biệt dữ liệu diagnostic và dữ liệu thu thập.

Run schema 1.0 vẫn được read_table/validator đọc. Nếu không biết capture_scope thì replay cách ly
thành unknown; không tự đổi dữ liệu cũ thành full text. Các mẫu trong samples/excerpts được nhận diện
từ manifest ghi rõ excerpt, chỉ dùng chạy chức năng với --allow-excerpts.

## Giới hạn còn lại

- Kiểm tra body dựa trên HTML/adapter, không render CSS/JavaScript. Visibility từ CSS stylesheet bên ngoài
  chưa xác định được; các trường hợp mơ hồ cần xem snapshot và duyệt.
- Body có pagination/accordion AJAX chưa tự ghép. Trang bị chặn được ghi lỗi, không bypass.
- Dedup văn bản vẫn trong run; event identity và entity resolution chưa được chứng nhận trên corpus lớn.
- `collect --limit N` giới hạn URL thử, không bổ sung vô hạn URL cho đến khi đủ N bài hợp lệ.
- Chưa coi tất cả tin kinh doanh là phù hợp đề tài mạng đa quốc gia; cần tập nhãn relevance/phạm vi riêng.
