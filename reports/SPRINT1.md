# Báo cáo sơ bộ Sprint 1 — News Knowledge Graph

Ngày thực thi: **30/10/2026 (Asia/Saigon)**. Dự án: `D:\Project\weconomy`.
Trạng thái: **nền tảng kỹ thuật đã chạy end-to-end; chưa nghiệm thu đủ Sprint 1 về dữ liệu/quy mô/chất lượng**.

## 1. Phạm vi đã thực thi

Đã đọc đề bài `initial.md`, kiểm tra thư mục và Git: ban đầu chỉ có tài liệu đề bài và repository.
Giữ nguyên tài liệu gốc; không tác động thư mục `sources/` của ChatGPT project.
Đã tạo môi trường Python 3.11.9, cài package local và lock dependencies bằng uv.
Đã viết discovery RSS/feedparser, nhập URL Katana tùy chọn, registry adapter các nguồn Việt/Anh,
kiểm tra policy/robots/redirect/rate/size; extraction Trafilatura, preprocessing, language routing,
NER hai backend, alias resolution, RE theo câu có bằng chứng, Parquet bronze/silver/gold,
schema/CLI/quality/analytics/Neo4j importer/tests/Compose/Dockerfile và tài liệu.

Đây là package batch chạy local; chưa phải hệ thống crawler production hoặc bộ NLP đã được chứng nhận.
Không tạo tin giả, không tạo thực thể/cạnh nhân tạo để đạt chỉ tiêu. Các câu nhân tạo chỉ dùng trong test,
được ghi rõ và không nhập corpus/Neo4j.

## 2. Dữ liệu thật và quyền truy cập

Mẫu gồm ba trích đoạn báo Wikinews tiếng Anh và một trích đoạn bách khoa Wikipedia tiếng Việt.
Wikinews cho phép tái sử dụng văn bản của các bài 2006/2007/2018 theo CC BY 2.5;
nguồn có chính sách đổi giấy phép theo ngày đăng, nên không gán cùng một license cho mọi bài mới.
Xem [chính sách Wikinews](https://en.wikinews.org/wiki/Wikinews:Copyright).
Trích đoạn tiếng Việt giữ giấy phép/ghi công riêng của Wikipedia; không tính là báo tiếng Việt.
Manifest có URL, contributors/history URL, license, ngày đăng nếu biết, thời điểm ghi nhận,
phương pháp ghi nhận và checksum. Không tải hình ảnh.

| Nguồn mẫu | Ngày bài | Ngôn ngữ / loại |
|---|---|---|
| Disney buys Pixar | 24/01/2006 | Anh / báo Wikinews |
| Microsoft to acquire health information search engine | 27/02/2007 | Anh / báo Wikinews |
| Technology giant Microsoft completes acquisition of GitHub | 29/10/2018 | Anh / báo Wikinews |
| Microsoft | không xác định ngày xuất bản một lần | Việt / Wikipedia bách khoa |

Mẫu là trích đoạn thật đọc qua công cụ tra cứu và bọc HTML local để thử extraction,
**không phải snapshot toàn trang tải trực tiếp**. Lần thu thập HTTP trực tiếp bị 403 ở robots.txt của cả
hai host: 0/4 trang được tải. Giữ log ở `samples/manifest.json`; không vượt chặn.
Do đó chưa có corpus báo chí song ngữ toàn văn hay thống kê extraction theo nguồn đại diện.
VnExpress, Tuổi Trẻ, Reuters, Bloomberg, TechCrunch mặc định bị khóa, chưa xác nhận quyền thu thập.

## 3. Các lần chạy dùng làm kết quả cuối

| Backend | Run |
|---|---|
| Gazetteer | `data/runs/20261030T085421-cfa10843` |
| spaCy + underthesea | `data/runs/20261030T085427-bff128ea` |

Các lần chạy cũ vẫn giữ nguyên trong `data/runs`; không cộng tất cả run để báo số bài độc lập.
Các file đánh giá không có hậu tố `-final` là kết quả vòng trước, có nhãn/mapping cũ;
không dùng cho kết luận hiện tại. Đây là pilot/dev, đã dùng quan sát lỗi để chỉnh mapping, không held-out test.

| Số đo thực | Gazetteer | Models |
|---|---:|---:|
| Tài liệu bronze / silver | 4 / 4 | 4 / 4 |
| Segment silver (có cả heading) | 23 | 23 |
| Mentions | 32 | 43 |
| Entity nodes (gồm isolate, machine candidates) | 10 | 22 |
| Claim / event edges | 1 / 1 | 2 / 2 |
| Loại quan hệ thực quan sát | 1 (`FOUNDED`) | 2 (`ACQUIRED`, `FOUNDED`) |
| Lỗi pipeline / bài trùng | 0 / 0 | 0 / 0 |
| Validation provenance / FK / offsets | đạt | đạt |

Schema và pattern đã có **10 loại**; chỉ 1–2 loại xuất hiện trong output này. Đặc biệt, một cạnh ACQUIRED
ở backend models là sai theo kiểm nhãn pilot: Azyxxi được nguồn mô tả là hệ thống phần mềm, không phải ORG.
Đã bỏ tên đó khỏi từ điển tổ chức; spaCy vẫn có thể gán ORG. Giữ kết quả lỗi để đánh giá trung thực,
không coi hai cạnh machine candidates là hai cạnh đã được xác thực.

## 4. Đo chất lượng pilot

`pilot-labels-final.json`: 23 segment, **40 entity spans và 5 quan hệ tham chiếu**, do agent đọc và gán nhãn
theo `docs/ANNOTATION.md`. Chưa có người gán nhãn độc lập, chưa agreement, chưa test set giữ kín.
Các số dưới đây chỉ kiểm tra vòng đánh giá và chẩn đoán baseline.

| Backend / task | TP / FP / FN | Precision | Recall | F1 |
|---|---|---:|---:|---:|
| Gazetteer NER exact-span | 32 / 0 / 8 | 100% | 80% | 88,89% |
| Models NER exact-span | 34 / 9 / 6 | 79,07% | 85% | 81,93% |
| Gazetteer relations exact-triple | 1 / 0 / 4 | 100% | 20% | 33,33% |
| Models relations exact-triple | 1 / 1 / 4 | 50% | 20% | 28,57% |

100% trên **một prediction** của gazetteer không đủ chứng minh precision ≥90%:
Wilson 95% chỉ khoảng **20,65%–100%**. Models relations có khoảng **9,45%–90,55%**.
Nguồn nhỏ, từ điển được chuẩn bị cho pilot và nhãn do agent tự kiểm làm giảm mạnh khả năng suy rộng.
Mọi metric production trong run manifest vẫn null vì chưa có kiểm định độc lập.

Các lỗi chính: thiếu tên ngoài từ điển; sai kiểu sản phẩm/tổ chức; apposition CEO; đồng sáng lập có phối hợp;
nominal acquisition không khớp mẫu động từ; tên viết tắt/surname; ngữ nghĩa dự định/hoàn tất.
Chưa giải quyết coreference giữa câu, event time, event dedup xuyên bài và đồng danh thực thể.

## 5. Neo4j và analytics

Docker Engine ban đầu chưa hoạt động; đã khởi động Docker Desktop và tạo container Neo4j riêng cho dự án.
Neo4j local healthy, chỉ mở `127.0.0.1:7474/7687`. Mật khẩu ngẫu nhiên lưu `.env` (gitignored), không ghi báo cáo.
`neo4j-final.json` xác nhận import model run **hai lần**, count không tăng:
**22 Entity, 4 Document, 23 Sentence, 2 Event, 2 Claim, 2 cạnh nghiệp vụ**.
Có truy vấn evidence/URL/license thành công. Đây là graph **unreviewed candidates**, chứa cả lỗi Azyxxi
đã nêu. Không báo thành graph đạt precision. Importer không xóa và giữ review_status đã có khi nhập lại.

NetworkX đã chạy với projection undirected/unweighted/simple và giữ isolate.
Trên model candidate graph: 20 components, LCC 3 nút, 6 ordered reachable pairs,
tổng shortest-path LCC = 8, trung bình = 1,3333; clustering = 0.
LCC chỉ chiếm 13,64% số nút; không diễn giải số này là khoảng cách trung bình toàn mạng.
Không tính small-world sigma vì graph quá nhỏ/thưa. Chưa có kết luận kinh tế từ pilot này.
GDS có template truy vấn cho Sprint 2, chưa cài/chạy GDS và chưa đối chiếu với NetworkX.

## 6. Kiểm thử và khả năng tái lập

- 41 tests đã qua tại thời điểm chốt baseline, ruff không có lỗi.
- Test bao gồm extraction end-to-end trên mẫu thật, schema rỗng, checksum hỏng, Unicode offsets,
  immutable runs, dedup tài liệu, alias boundaries, phủ định/điều kiện/lời đồn, type constraints,
  RSS, policy/robots, redirect ra host lạ, đánh giá FP/FN và whitelist tên cạnh Neo4j.
- NER models đã chạy thật: spaCy 3.8.18, en_core_web_sm 3.8.0, underthesea 8.3.0.
- `uv.lock` lưu dependencies; `requirements.lock` xuất bản core có hash cho Docker.
- Model spaCy là tài nguyên ghim URL ngoài lock; README có lệnh cài và lưu ý `--no-sync`.
- Docker image `weconomy:sprint1` đã build thành công với dependencies có hash. Đã chạy container
  **không có mạng**, mount đầu ra vào thư mục data của dự án: 4 tài liệu, 23 segment, 32 mentions,
  10 entities, 1 claim/event, 0 lỗi; khớp backend gazetteer trên Windows.
  Bằng chứng: `docker-build.log`, `docker-smoke.json`; run host
  `data/runs/20261030T090041-ad0a6fc0` (trong container hiển thị prefix `/app/data`).

## 7. Đối chiếu mục tiêu nghiệm thu

| Mục tiêu | Hiện tại | Kết luận |
|---|---|---|
| 2.000 thực thể | 10 baseline / 22 model candidates | Chưa đạt, nhiều isolate và có NER errors |
| 5.000 cạnh sự kiện thật | 1 / 2 candidates; model có 1 FP pilot | Chưa đạt |
| 10 loại quan hệ thật | 10 định nghĩa, 1–2 quan sát | Chưa đạt |
| Precision ≥90% | Không có test độc lập; model pilot 50% relations | Chưa chứng minh/không đạt pilot models |
| Thu thập đủ tin Việt/Anh | 3 trích đoạn báo Anh + 1 bách khoa Việt; tải toàn văn 0 | Chưa đạt |
| Graph lưu DB và truy vết | Neo4j import/reimport/query đã kiểm tra | Đạt chức năng pilot |
| Báo cáo nộp ≥10 trang/GitHub/phân công | Báo cáo sơ bộ Markdown; chưa thông tin nhóm/remote | Chưa phải bản nộp cuối |

## 8. Rủi ro khi mở rộng và việc cần làm tiếp

1. **Nguồn và giấy phép:** cần corpus tin kinh tế thật, đủ quyền và đủ độ phủ. RSS không bảo đảm quyền toàn văn;
   tỷ lệ 403 hiện tại ngăn thu thập tự động. Ưu tiên nguồn mở/corpus được cấp phép, không lách paywall.
2. **Recall và kiểu thực thể:** model NER không tự tăng chất lượng; cần nhãn độc lập, kiểm tra lỗi theo ngôn ngữ,
   source/type, chuẩn hóa quỹ/tổ chức/người/sản phẩm và RE cú pháp trước khi mở rộng volume.
3. **Event identity:** luật bảo thủ trong bài chưa chứng minh 5.000 sự kiện khác nhau; nhiều bài cùng sự kiện
   và nhiều giao dịch cùng cặp actor cần ngày/thương vụ/evidence review riêng.
4. **Hiệu năng:** pairwise shingle dedup O(n²), toàn bộ batch ở RAM và all-pairs paths chưa benchmark lớn.
   Trước scale: ledger/checkpoint, partition Parquet, LSH/index xuyên run; đo thay vì đoán throughput.
5. **Tính hợp lệ mạng:** số node NER không đồng nghĩa node đúng/có cạnh. Đếm node provenance, duplicate events
   hoặc xuất hiện nhiều lần sẽ làm phồng chỉ tiêu. Chốt projection và approved subset trước analytics.
6. **Nghiệm thu:** xác nhận “2000 nghìn nút” với giảng viên; bổ sung phân công thành viên thật và remote GitHub
   được phép. Không tự nhận đã có các thông tin này.

Sprint 2 đã có đường dùng dữ liệu gold và module NetworkX; kế hoạch 4 tuần ở `docs/ROADMAP.md`.
Chưa thêm scheduler phân tán, paid API, UI hoặc orchestration khi chưa có bottleneck và nguồn dữ liệu hợp lệ.
