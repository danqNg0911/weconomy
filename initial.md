1. Yêu cầu

Xây dựng mạng xã hội dựa trên kỹ thuật phân tích xử lý ngôn ngữ tự nhiên theo danh sách các đề tài được phân công theo nhóm ở dưới:

Yêu cầu: mạng tối thiểu 2000 nghìn nút, 5000 cạnh và 10 loại quan hệ chi tiết giữa các cạnh, độ chính xác trên 90%

(Lưu ý: Các đề tài liên quan Quốc tế có thể lựa chọn một phạm vi nhỏ hơn (ví dụ cầu thủ có thể chọn chỉ ngoại hạng Anh), các phạm vi nhỏ tối thiểu 1000 nút.)
Ưu tiên tạo ra mạng chất lượng (node và cạnh có ý nghĩa cụ thể, rõ ràng, ví dụ mối quan hệ giữa các diễn viên thông qua các bộ phim hay mối quan hệ giữa các cầu thủ thông qua danh sách đội bóng hoặc mối quan hệ HLV)
Dữ liệu sử dụng là các bài báo tiếng Anh/Việt.

Yêu cầu kỹ thuật:
Các nhóm lưu trữ dữ liệu graph vào 1 trong các hệ quản trị CSDL sau:
- Neo4j
- ElasticSearch/OpenSearch
- ArrangoDB
- Dgraph
... (các em có thể đề xuất riêng 1 hệ quản trị CSDL phù hợp, việc lựa chọn cần đánh giá có thể chạy các thuật toán cho bài tập cuối kỳ)
Kết quả báo cáo:

Một báo cáo tối thiểu 10 trang bao gồm các nội dung:

- Phân công công việc trong nhóm
- Giới thiệu về mạng đã xây dựng được, lựa chọn node thế nào và lựa chọn cạnh ra sao
- Giới thiệu stack công nghệ sử dụng để thu thập, xử lý dữ liệu 
- Các bước tiền xử lý dữ liệu
- Các thống kê về mạng đã xây dựng được
- Kết luận về các vấn đề đạt được và chưa đạt được
- Link github code xử lý

2. Đề tài

Mạng lưới Tập đoàn Đa quốc gia, Tỷ phú và Quỹ Đầu tư Quốc tế (Báo Kinh tế Thế giới):

Nguồn dữ liệu phổ biến: Chuyên mục Kinh doanh quốc tế (VnExpress, Tuổi Trẻ) hoặc Reuters, Bloomberg, TechCrunch.

Phân tích nội dung & Phân loại cạnh: Kết nối các 
- CEO công nghệ/tài chính
- Startup
- Quỹ đầu tư mạo hiểm (VC)
- Chính phủ các nước 

qua các cạnh: 
- Rót vốn đầu tư
- Sáp nhập (M&A)
- Kiện chống độc quyền
- Đứt gãy/Hợp tác chuỗi cung ứng.

