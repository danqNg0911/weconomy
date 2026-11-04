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

## Thu thập run nhỏ và xuất để rà soát

Cài extras và model spaCy theo [README](../README.md#cài-đặt-trên-windows). Dùng publisher ID đang bật trong `config/sources.yaml`; ví dụ dưới đây giới hạn mỗi nguồn ở tối đa ba URL thử.

```powershell
$collected = uv run --no-sync weconomy collect --source vnexpress --source tuoitre --limit 3 --ner models | ConvertFrom-Json
$run = $collected.run
uv run --no-sync weconomy validate $run
uv run --no-sync weconomy export $run --table articles --output "$run/articles-review.jsonl"
uv run --no-sync weconomy export $run --table entities --output "$run/entities-review.jsonl"
uv run --no-sync weconomy export $run --table relations --output "$run/relations-review.jsonl"
```

`--limit` là số URL tối đa thử ở mỗi nguồn, không đảm bảo số bài được nhận. Xem `status`, `counts`, `errors` và `content_statuses` trong kết quả. Quan hệ là ứng viên chưa duyệt; đọc evidence cùng document/source provenance trước khi dùng.

## Chạy lại NLP không tải lại bài

`run --from-run` đọc HTML đã lưu trong bronze và tạo một run mới. Run nguồn không bị sửa.

```powershell
uv run --no-sync weconomy run --from-run $run --ner models
```

Với catalog nhiều batch, `collect-dataset --from-run` phát lại thân bài offline theo lô, kiểm tra policy host hiện tại và lưu vào catalog mới/resume được. Có thể lặp cờ theo thứ tự ưu tiên; xem [hướng dẫn phát lại dataset](collection.md#phát-lại-thân-bài-đã-lưu). Ví dụ ngắn:

```powershell
uv run --no-sync weconomy collect-dataset --dataset data/datasets/international-business-v2 `
    --from-run $run --articles 200 --max-candidates 396 --batch-size 20
```

## Gộp các run legacy

Dùng `--skip-run` để không thử lại URL đã có toàn văn ở run trước, sau đó gộp offline:

```powershell
$nextResult = uv run --no-sync weconomy collect --source vnexpress --source tuoitre --limit 10 --skip-run $run --ner models | ConvertFrom-Json
$next = $nextResult.run
uv run --no-sync weconomy merge-runs --run $run --run $next --ner models
```

`merge-runs` giữ capture toàn văn hợp lệ, chọn revision theo thứ tự `--run` và chạy lại extraction/NLP/dedup. Không cộng số đếm của các lần replay. Với collection tiếp tục lâu dài, dùng catalog `collect-dataset` trong README thay cho luồng này.

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

Image core chứa backend gazetteer, không bao gồm spaCy/underthesea. Ví dụ chạy fixture offline, mount thư mục `data/` để giữ run trên host:

```powershell
docker build -t weconomy:corpus-v3 .
$dataPath = (Resolve-Path .\data).Path
docker run --rm --network none --mount "type=bind,source=$dataPath,target=/app/data" `
  weconomy run --manifest samples/excerpts/manifest.json --allow-excerpts
```

`--network none` phù hợp với fixture local. Với nguồn Internet, dùng CLI ngoài container và tuân thủ policy hiện hành. Các lệnh Hugging Face private được ghi riêng trong [HUGGINGFACE.md](HUGGINGFACE.md).
