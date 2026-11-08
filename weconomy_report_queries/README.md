# Weconomy — bộ truy vấn phục vụ báo cáo (AuraDB + Hugging Face)

Bộ tệp được thiết kế theo báo cáo Codex của dự án Weconomy, **không phải một kết quả thống kê đã được xác nhận**. Số liệu chỉ có giá trị sau khi chạy trên đúng dataset/run cuối cùng. Tất cả câu Cypher thống kê đều chỉ đọc; không tạo, sửa hoặc xóa node và relationship.

## File nào dùng để làm gì?

| File | Mục đích |
|---|---|
| `auradb_queries.cypher` | ~60 câu truy vấn Cypher theo mã Q01–Q60, chia nhóm core/extended/heavy |
| `collect_auradb.py` | Chạy tự động truy vấn read-only và ghi kết quả JSON/Markdown |
| `analyze_networkx.py` | Tính PageRank, degree, density, connected components, community, clustering, approximate betweenness |
| `inspect_hf_parquet.py` | Tải từ repo Hugging Face hoặc dùng thư mục local; đọc Parquet/ZIP và thống kê |
| `hf_parquet_queries.sql` | SQL DuckDB tham khảo để phân tích từng bảng Parquet |
| `sample_quality.py` | Lấy mẫu claim phân tầng theo predicate và tính precision theo nhãn do con người cung cấp |

## A. Chuẩn bị trên Windows PowerShell

Nên chạy bằng môi trường Python riêng. Các lệnh bên dưới chạy tại thư mục `F:\Project\ptmxh\weconomy_report_queries`:

```powershell
python -m pip install neo4j networkx scipy huggingface_hub pyarrow duckdb
```

Tạo hoặc cập nhật file `.env` tại thư mục gốc dự án (`F:\Project\ptmxh\.env`). Ví dụ dưới đây dùng thông tin giả; thay bằng thông tin kết nối của bạn:

```dotenv
NEO4J_URI="neo4j+s://example-instance.databases.neo4j.io"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="example-password-change-me"
```

`collect_auradb.py` và `analyze_networkx.py` tự tìm file `.env` gần nhất từ thư mục chứa script lên các thư mục cha. Biến môi trường đã đặt trong terminal được ưu tiên hơn giá trị trong `.env`. Có thể dùng `NEO4J_USERNAME` thay cho `NEO4J_USER`.

Không ghi password thật trong báo cáo, GitHub, log hoặc gửi cho ChatGPT. Có thể cài phụ thuộc bằng `uv` nếu dự án đã dùng `uv`.

## B. Thu thập thống kê AuraDB

Chạy **core** trước, xem kết quả tại thư mục `reports`:

```powershell
python collect_auradb.py --level core --output reports
```

Sau khi xem Q05 và Q06 để đối chiếu tên trường thực tế, chạy mở rộng:

```powershell
python collect_auradb.py --level extended --output extended-reports
```

Chạy một vài câu cụ thể:

```powershell
python collect_auradb.py --only Q14 Q15 Q27 Q30 Q32 Q37 --output selected-reports
```

Kết quả:

- `reports/auradb_results.json`
- `reports/auradb_results.md`
- `reports/auradb_errors.json`

Lần chạy `extended` ghi ba file cùng tên vào `extended-reports/`. Ví dụ `--only` ghi vào `selected-reports/` (thư mục được tạo khi chạy). Mỗi lần chạy ghi lại các file kết quả trong thư mục `--output`, nên dùng thư mục riêng để giữ kết quả trước đó.

Câu lỗi do không có quyền hoặc không khớp schema sẽ được bỏ qua và ghi lý do. Q59 là câu trực quan hóa thủ công trong Neo4j Browser; Q60 chỉ là mẫu shortest path có chú thích. Nếu Aura có hạn chế tài nguyên, không chạy nhiều phép toán nặng cùng một lúc.

## C. Các chỉ số mạng từ NetworkX, không cần GDS trên Aura

```powershell
python analyze_networkx.py --output pagerank-reports
python analyze_networkx.py --advanced --output pagerank-reports
```

`--advanced` bổ sung trung bình hệ số gom cụm, tam giác, cộng đồng greedy-modularity, shortest path trong thành phần liên thông lớn nhất, approximate betweenness. Đồ thị được chiếu về đơn có hướng và đơn vô hướng để phân tích; số cạnh tại hai đồ thị có thể thấp hơn số relationship gốc của Aura.

Kết quả: `pagerank-reports/networkx_metrics.json` và `pagerank-reports/networkx_metrics.md`. Chọn một trong hai lệnh trên; chạy `--advanced` vào cùng thư mục sẽ ghi lại kết quả cơ bản và bổ sung các chỉ số nâng cao.

Các thư mục kết quả hiện tại (đường dẫn tính từ `weconomy_report_queries/`):

| Thư mục | Nội dung |
|---|---|
| `reports/` | Kết quả AuraDB core: `auradb_results.json`, `auradb_results.md`, `auradb_errors.json` |
| `extended-reports/` | Kết quả AuraDB extended: ba file cùng tên như core |
| `pagerank-reports/` | Phân tích NetworkX: `networkx_metrics.json`, `networkx_metrics.md` |

## D. Thống kê Parquet từ Hugging Face

Nếu repo private, trước tiên xác thực trên máy của bạn:

```powershell
hf auth login
```

Nếu repo chứa Parquet và/hoặc ZIP run bundle:

```powershell
python inspect_hf_parquet.py --repo "OWNER/REPO" --download-to hf_snapshot --output reports
```

Nếu đã tải run xuống máy:

```powershell
python inspect_hf_parquet.py --local "F:\\Path\\To\\Weconomy\\FinalRun" --output reports
```

Nếu có nhiều run cũ, chỉ lựa chọn một thư mục run cuối bằng `--subdir` hoặc `--local` phù hợp. Khi đọc toàn bộ HF repo, **đừng cộng số bài giữa các run chồng lấn**. Script đọc metadata Parquet, đếm dòng, danh sách cột, phân bố các trường có mặt, nguồn, ngôn ngữ, predicate và các ví dụ ngắn. Các cột nào không tồn tại sẽ tự được bỏ qua.

Kết quả: `reports/hf_parquet_summary.json` và `.md`.

Nếu muốn tự query DuckDB, dùng `hf_parquet_queries.sql`, sửa đường dẫn và xác minh field bằng `DESCRIBE`/`SELECT * LIMIT 3` trước khi chạy các phần thống kê theo cột.

## E. Mẫu đánh giá chính xác quan hệ

Sau khi có thư mục một run cuối chứa `relations.parquet`:

```powershell
python sample_quality.py --local "F:\\Path\\To\\FinalRun" --per-predicate 15 --out reports/annotation_sample.csv
```

Mở `annotation_sample.csv`, điền `is_correct` = 1 (đúng toàn bộ subject/predicate/object/evidence) hoặc 0 (sai) cho các hàng được kiểm tra bằng chứng. Sau đó:

```powershell
python sample_quality.py --evaluate reports/annotation_sample.csv
```

Script cung cấp precision theo predicate, precision chung, và khoảng tin cậy Wilson 95%. Để tính **recall/F1**, cần thêm bộ gold-standard có cả quan hệ mô hình đã bỏ sót; chỉ lấy mẫu từ các quan hệ mô hình đã trích xuất **không đủ** để tính recall.

## F. Gửi gì để viết báo cáo?

Ưu tiên các file sau:

1. `reports/auradb_results.json`
2. `pagerank-reports/networkx_metrics.json`
3. `reports/hf_parquet_summary.json`
4. `reports/auradb_errors.json` (nếu có lỗi, để chỉnh đúng schema)

Nếu dùng lần chạy mở rộng, gửi thêm `extended-reports/auradb_results.json` và `extended-reports/auradb_errors.json`. `reports/hf_parquet_summary.json` chỉ có sau khi chạy bước D.

Nếu đã gán nhãn thủ công, gửi thêm báo cáo precision từ `sample_quality.py` (không cần gửi credential). Ngoài ra cần **GitHub URL**, danh sách thành viên và nhiệm vụ thật, và xác nhận run/dataset nào được dùng để ghi số liệu cuối cùng.

## G. Thang đánh giá/diễn giải

- `COUNT(*)` của mối quan hệ Neo4j là số **edge thực tế**, không phải số predicate hay số claim trong Parquet.
- `relations.parquet` theo mô tả Codex lưu các **claim có bằng chứng**; export JSONL có thể tách `claims.jsonl` và `relations.jsonl`, không được coi là cùng mức tổng hợp.
- Chỉ tiêu cấu hình 2.000 node, 5.000 quan hệ, 11 loại quan hệ **không phải kết quả**, cần so với đếm thực tế; schema có 19 predicate ràng buộc kiểu, nhưng không có nghĩa cả 19 đều xuất hiện.
- Độ chính xác >90% cần gán nhãn độc lập và công bố cách lấy mẫu, cỡ mẫu, số đúng/sai, cách tính.
- Dữ liệu thu thập hiện mô tả là báo chí Việt/Anh; **không tự ghi là đã crawl Wikipedia** nếu chưa có module và bằng chứng thu thập.
- Chỉ số NetworkX của đồ thị đơn vô hướng là một **phép chiếu**; không gán nhầm thành đặc tính trực tiếp của đồ thị có hướng đa cạnh trong Neo4j.
