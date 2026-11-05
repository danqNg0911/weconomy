# Lệnh CLI bổ sung

Trang [README dự án](../README.md) tập trung quickstart cho collection có thể tiếp tục. Trang này giữ các ví dụ cho immutable run, kiểm định, Neo4j và Docker.

## Chạy fixture offline

Fixture trong `samples/excerpts/` là trích đoạn có ghi nhận giấy phép, dùng chẩn đoán extraction/NLP; không đại diện tin tức hiện hành hay corpus đã thu thập.

```powershell
uv sync --locked --extra dev
$completed = uv run weconomy run --manifest samples/excerpts/manifest.json --allow-excerpts | ConvertFrom-Json
$run = $completed.run
uv run --no-sync weconomy validate $run
uv run --no-sync weconomy analytics $run --output reports/analytics-offline.json
```

Các lệnh ghi output từ chối ghi đè. Đổi tên file output nếu đã tồn tại. Lệnh `analytics` tính thống kê trên run; kết quả này không đo độ chính xác của NER/RE.

## Crawl và rà soát output

Discovery hiện tại dùng Katana. Chạy lệnh crawl trong [hướng dẫn collection](collection.md), lấy một run từ `targets[].run_ids` trong JSON kết quả rồi kiểm tra/xuất bảng:

```powershell
uv run --no-sync weconomy crawl --config config/collection.yaml
$run = "data/runs/RUN_ID"
uv run --no-sync weconomy validate $run
uv run --no-sync weconomy export $run --table articles --output "$run/articles-review.jsonl"
uv run --no-sync weconomy export $run --table entities --output "$run/entities-review.jsonl"
uv run --no-sync weconomy export $run --table relations --output "$run/relations-review.jsonl"
```

Quan hệ là ứng viên chưa duyệt; đọc evidence cùng document/source provenance trước khi dùng.

## Chạy lại NLP không tải lại bài

`run --from-run` đọc HTML đã lưu trong bronze và tạo một run mới. Run nguồn không bị sửa.

```powershell
uv run --no-sync weconomy run --from-run $run --ner models
```

Với catalog nhiều batch, `collect-dataset --from-run` phát lại thân bài offline theo lô, kiểm tra policy host hiện tại và lưu vào catalog mới/resume được. Có thể lặp cờ theo thứ tự ưu tiên; xem [hướng dẫn crawl/replay](collection.md). Ví dụ ngắn:

```powershell
uv run --no-sync weconomy collect-dataset `
    --from-run $run --articles 200 --max-candidates 396 --batch-size 20
```

`collect-dataset` nhận run được lưu bằng `--from-run` để replay offline vào catalog; nó không còn lệnh discover/fetch riêng. `merge-runs` vẫn dùng để gộp các immutable runs đã có, không thực hiện discovery.

## Gán nhãn và đánh giá

Sinh task câu đầy đủ để người gán nhãn hoàn thành trước khi đánh giá. Không đánh dấu complete nếu chưa rà soát câu và quan hệ.

```powershell
uv run --no-sync weconomy label-tasks $run --limit 200 --output reports/labels-to-review.json
# Sau khi hoàn thành nhãn theo docs/ANNOTATION.md:
uv run --no-sync weconomy evaluate $run --labels reports/labels-to-review.json --output reports/evaluation.json
```

Đánh giá yêu cầu nhãn hoàn chỉnh. Precision/recall/F1 chỉ có ý nghĩa khi tập nhãn độc lập và cách chia dữ liệu phù hợp; số câu đã gán nhãn chưa phải bằng chứng đạt ngưỡng precision.

## Neo4j local

Cần Docker. Nếu chưa có `.env`, sao chép `.env.example` thành `.env`, thay password local và giữ tệp này ngoài Git. Khởi động Neo4j, nạp password vào process hiện tại mà không in ra, rồi import một immutable run đã validate:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
# Mở .env và thay giá trị NEO4J_PASSWORD trước khi khởi động dịch vụ.
docker compose up -d
$env:NEO4J_PASSWORD = ((Get-Content .env | Where-Object { $_ -like 'NEO4J_PASSWORD=*' }) -split '=', 2)[1]
uv run --no-sync weconomy validate $run
uv run --no-sync weconomy import-neo4j $run
```

Neo4j Browser chỉ bind vào localhost tại `http://localhost:7474`; cổng Bolt là `7687`. Các volume Docker giữ dữ liệu. `docker compose down` dừng dịch vụ; thêm `-v` sẽ xóa cả volume graph.

Truy vấn claim, câu evidence và document nguồn:

```cypher
MATCH (c:Claim)-[:ABOUT_EVENT]->(e:Event),
      (c)-[:EVIDENCED_BY]->(s:Sentence)-[:IN_DOCUMENT]->(d:Document)
RETURN c.predicate, c.review_status, e.event_id, s.text, d.url, d.license
LIMIT 25;
```

Cạnh trong Neo4j biểu diễn ứng viên máy; `reported` không có nghĩa đã fact-check. Xem thêm [schema/provenance](SCHEMA.md).

## Docker offline

Image core chứa backend gazetteer, không bao gồm GLiNER/model weights. Ví dụ chạy fixture offline, mount thư mục `data/` để giữ run trên host:

```powershell
docker build -t weconomy:corpus-v3 .
$dataPath = (Resolve-Path .\data).Path
docker run --rm --network none --mount "type=bind,source=$dataPath,target=/app/data" `
  weconomy run --manifest samples/excerpts/manifest.json --allow-excerpts
```

`--network none` phù hợp với fixture local. Với nguồn Internet, dùng CLI ngoài container và tuân thủ policy hiện hành. Các lệnh Hugging Face private được ghi riêng trong [HUGGINGFACE.md](HUGGINGFACE.md).
