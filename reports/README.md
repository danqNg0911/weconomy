# Kết quả cần đọc

Kết quả chốt sau sửa review: **FINAL_2026-10-31.md** và **FINAL_2026-10-31.json**.
81 tests qua; 9 bài thật đã import/reimport Neo4j; Docker offline đọc đúng cùng thân bài với Windows.
Các kết quả/lỗi engine trong báo cáo cũ bên dưới phản ánh thời điểm kiểm tra trước, không phải trạng thái hiện tại.

Cập nhật mới nhất 31/10: `FULLTEXT_2026-10-31.md` và `FULLTEXT_2026-10-31.json` —
9 bài thật, 150 thực thể ứng viên, 1 quan hệ thỏa thuận; thay thế tình trạng chỉ có trích đoạn của ngày 30/10.
`body-v2-docker-check.json` ghi trạng thái Engine trong lần kiểm tra bản mới.
Các file pilot bên dưới là bằng chứng lịch sử 30/10, không phải số đo corpus full text hiện tại.

- `SPRINT1.md`: báo cáo sơ bộ cuối, trạng thái chưa đạt nghiệm thu quy mô/chất lượng.
- `pilot-labels-final.json`: nhãn pilot do agent, không phải ground truth người duyệt độc lập.
- `evaluation-gazetteer-final.json`, `evaluation-models-final.json`: P/R/F1 cuối theo nhãn pilot đã sửa kiểu Azyxxi.
- `neo4j-final.json`: import/reimport live, counts và evidence từ Neo4j.
- `analytics-models.json`: analytics trên cùng model graph topology, 22 node / 2 candidate edges.
- `docker-build.log`, `docker-smoke.json`: bằng chứng build và chạy container nếu thành công.

File không có `-final` (ngoại trừ analytics topology không đổi) là vòng thử trước khi phát hiện lỗi
gán sản phẩm Azyxxi thành tổ chức. Giữ lại để truy vết, **không dùng làm báo cáo chất lượng cuối**.
Run IDs cuối có trong báo cáo. `data/runs` chứa các lần chạy cũ, không cộng chúng thành số bài độc lập.
