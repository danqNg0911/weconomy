# Kết quả cần đọc

- `SPRINT1.md`: báo cáo sơ bộ cuối, trạng thái chưa đạt nghiệm thu quy mô/chất lượng.
- `pilot-labels-final.json`: nhãn pilot do agent, không phải ground truth người duyệt độc lập.
- `evaluation-gazetteer-final.json`, `evaluation-models-final.json`: P/R/F1 cuối theo nhãn pilot đã sửa kiểu Azyxxi.
- `neo4j-final.json`: import/reimport live, counts và evidence từ Neo4j.
- `analytics-models.json`: analytics trên cùng model graph topology, 22 node / 2 candidate edges.
- `docker-build.log`, `docker-smoke.json`: bằng chứng build và chạy container nếu thành công.

File không có `-final` (ngoại trừ analytics topology không đổi) là vòng thử trước khi phát hiện lỗi
gán sản phẩm Azyxxi thành tổ chức. Giữ lại để truy vết, **không dùng làm báo cáo chất lượng cuối**.
Run IDs cuối có trong báo cáo. `data/runs` chứa các lần chạy cũ, không cộng chúng thành số bài độc lập.
