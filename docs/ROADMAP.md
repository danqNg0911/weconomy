# Lộ trình và checklist nghiệm thu

Khởi đầu 30/10/2026, múi giờ Asia/Saigon. Checklist thể hiện việc có bằng chứng đã chạy,
không dùng dấu hoàn thành cho mục tiêu tương lai.

## Sprint 1 — 30/10 đến 12/11/2026

- [x] Đọc initial.md, kiểm tra Git/thư mục/môi trường, giữ tài liệu cũ.
- [x] Tạo package Python, lock, config, schema và CLI.
- [x] Có cổng policy/robots/redirect/rate/size và registry nguồn Việt/Anh.
- [x] Chạy mẫu thật có giấy phép mở từ snapshot trích đoạn, xuất Parquet 3 lớp.
- [x] NER gazetteer, alias resolution và RE có evidence/offset/type constraints.
- [x] Viết nhãn task và phép đo Precision/Recall/F1, từ chối nhãn chưa duyệt.
- [x] Viết test tích hợp offline và các trường hợp từ chối trích xuất.
- [x] Chuẩn bị NetworkX, schema Neo4j, importer, Docker Compose và tài liệu.
- [x] Chạy NER spaCy/underthesea trên mẫu, kiểm định pilot (chưa độc lập).
- [x] Neo4j live import/reimport/query; Docker build và chạy mẫu offline đã xác minh.
- [ ] Thu thập toàn văn tin Việt/Anh ở quy mô đại diện với quyền truy cập đã xác minh.
- [ ] Xác nhận chính thức với giảng viên “2000 nghìn nút” là 2.000 hay 2 triệu.
- [ ] Đạt 2.000 entity nodes, 5.000 distinct validated event edges, 10 observed predicates.
- [ ] Bộ nhãn độc lập ≥150–200 câu, đủ loại, đo ≥90% precision cùng recall/F1 và khoảng tin cậy.
- [ ] Báo cáo nộp ≥10 trang, phân công nhóm thực, liên kết GitHub thật và phân tích số liệu đủ quy mô.

Kiểm tra live Neo4j/NLP/Docker xem kết quả cụ thể ở `reports/SPRINT1.md`; roadmap không thay run log.
Chưa có danh sách thành viên/remote GitHub được cung cấp; không tự tạo phân công hoặc đẩy repository.

| Khoảng ngày | Công việc tiếp theo | Bằng chứng cần có |
|---|---|---|
| 30/10–01/11 | Chốt scope kinh tế/công nghệ, nguồn được phép, chạy pilot và đo extraction | source register, checksum, test/run manifests |
| 02–05/11 | Thu thập có quyền, lấy mẫu đánh giá, mở rộng NER/alias theo lỗi | corpus đủ hai ngôn ngữ, nhãn độc lập và nhật ký lỗi |
| 06–09/11 | Cải thiện RE, phân biệt planned/completed/denied, review entity/event resolution | dev scores theo nguồn/loại, kiểm tra event duplicates |
| 10–12/11 | Khóa corpus/test, duyệt chất lượng, nhập graph, viết báo cáo | counts DB vs Parquet, P/R/F1 held-out, báo cáo và GitHub |

## Sprint 2 — 13 đến 26/11/2026

| Tuần | Thực thi | Điều kiện nghiệm thu |
|---|---|---|
| 3 | Phép chiếu directed/undirected và weighted; degree, PageRank, betweenness, communities, components | Định nghĩa node/edge/weight rõ, tái lập cùng dataset version |
| 3 | Tổng/độ dài đường đi ngắn nhất; disconnected và LCC riêng | Báo ordered vs unordered pairs, reachable coverage; không gọi kết quả LCC là toàn mạng |
| 4 | Small-world so với random/degree-preserving null, sigma và độ nhạy theo projection | Null models, seeds, nhiều lần chạy, bất định; không khẳng định vì clustering cao đơn lẻ |
| 4 | So sánh NetworkX/GDS, trực quan hóa, diễn giải kinh tế, hoàn thiện báo cáo | Count/mapping thống nhất, kiểm tra sai số do NLP và thiên lệch nguồn |

## Sau 4 tuần

Checkpoint/job ledger, source/date partitions, dedup xuyên run bằng LSH, model registry và model cards,
review accept/reject có audit trail, theo dõi drift theo source/language và refresh terms.
Chỉ thêm orchestration hoặc xử lý phân tán sau khi benchmark chỉ ra bottleneck thực tế.

## Chỉ tiêu chất lượng để quyết định tiếp tục mở rộng

- Mỗi claim truy được về câu, bài, URL và giấy phép: validation phải 100%.
- Không đếm PERSON/ORG từ số lần xuất hiện thành nhiều node; không đếm provenance node vào target.
- Đếm 10 loại trên các quan hệ thật được duyệt; không bịa thêm predicate/câu để đủ số.
- Đo lại khi đổi NER, alias hoặc rules; test được giữ kín, không dùng test labels để chỉnh rules.
- Nếu nguồn bị chặn/không được phép, thay nguồn được phép hoặc xin cấp phép; không lách chặn.
