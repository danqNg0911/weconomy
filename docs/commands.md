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

## Chạy một chu trình graph

Lần đầu, lệnh tự phát lại các run đã commit trong dataset nguồn cũ bằng NLP hiện tại, xuất và lọc domain. Khi cần crawl thêm, lệnh chỉ khám phá URL rồi để catalog tải full body và chạy NLP một lượt; URL có trong catalog bị bỏ trước NLP. Mục tiêu node/cạnh/loại quan hệ chỉ được kiểm tra trên export đã lọc domain, không dừng theo số đếm thô. Dataset đích được resume, run cũ không bị sửa. Nếu dataset nguồn mặc định không phù hợp, đổi `--source-dataset`:

```powershell
uv run --no-sync weconomy graph-cycle `
  --dataset data/datasets/international-business-gliner-coref-v3 `
  --nodes 2000 --relations 5000 --relation-types 11 `
  --max-candidates 10000 --batch-size 20
```

Mặc định nguồn cũ là `data/datasets/international-business-gliner-v1`. Dataset đích chỉ phát lại nguồn này khi được tạo lần đầu; những lần sau tiếp tục catalog đích, không phân tích lại bài đã xử lý. Mỗi lượt tạo export có tên riêng. Nếu bản domain chưa đạt chỉ tiêu, export vẫn được giữ, lệnh trả mã thoát `2`, và không import vào Neo4j. Chạy lại cùng lệnh để tiếp tục; catalog chống URL/nội dung trùng. Importer không xóa entity/cạnh đã có trong AuraDB.

## Gán nhãn và đánh giá

Sinh task câu đầy đủ để người gán nhãn hoàn thành trước khi đánh giá. Không đánh dấu complete nếu chưa rà soát câu và quan hệ.

```powershell
uv run --no-sync weconomy label-tasks $run --limit 200 --output reports/labels-to-review.json
# Sau khi hoàn thành nhãn theo docs/ANNOTATION.md:
uv run --no-sync weconomy evaluate $run --labels reports/labels-to-review.json --output reports/evaluation.json
```

Đánh giá yêu cầu nhãn hoàn chỉnh. Precision/recall/F1 chỉ có ý nghĩa khi tập nhãn độc lập và cách chia dữ liệu phù hợp; số câu đã gán nhãn chưa phải bằng chứng đạt ngưỡng precision.

## Tạo export chỉ gồm node thuộc domain

`filter-domain` đọc export JSONL đầy đủ, gán subtype bằng cue tiếng Việt/Anh ở cấu trúc apposition gần tên entity, giữ node đã phân loại kể cả node chưa có cạnh, và chỉ giữ claim có cả hai đầu mút thuộc domain. Bản v8 loại các alias phổ biến chỉ là đại từ/vai trò, năm, từ chung hoặc tên quốc gia bị NER gán nhầm `ORG`; alias GOV được curated vẫn được giữ. Đây vẫn là heuristic và không kiểm định riêng tính đúng của predicate quan hệ. Lệnh tạo thư mục mới, không sửa export nguồn; kiểm tra `domain_types` và `domain_evidence` trước khi nhập graph.

```powershell
$source = 'data/exports/international-business-gliner-v2-full-20261107T042155-6b3c94'
$domain = 'data/exports/international-business-gliner-v2-domain-v8-recheck'
uv run --no-sync weconomy filter-domain $source --output $domain
```

## Neo4j local

Cần Docker. Nếu chưa có `.env`, sao chép `.env.example` thành `.env`, đặt password và giữ tệp này ngoài Git. Khởi động Neo4j local, ép URI/database về local (vì `.env` có thể đang trỏ Aura), rồi nhập export:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
$dataset = 'data/datasets/international-business-gliner-v1'
$export = "data/exports/international-business-gliner-$(Get-Date -Format yyyyMMdd-HHmmss)"
uv run --no-sync weconomy export-dataset $dataset --output $export
docker compose up -d
$env:NEO4J_PASSWORD = ((Get-Content .env | Where-Object { $_ -like 'NEO4J_PASSWORD=*' }) -split '=', 2)[1].Trim().Trim('"').Trim("'")
$env:NEO4J_URI = 'bolt://localhost:7687'
$env:NEO4J_USERNAME = 'neo4j'
$env:NEO4J_DATABASE = 'neo4j'
uv run --no-sync weconomy import-neo4j $export
```

Neo4j Browser chỉ bind vào localhost tại `http://localhost:7474`; cổng Bolt là `7687`. Các volume Docker giữ dữ liệu. `docker compose down` dừng dịch vụ; thêm `-v` sẽ xóa cả volume graph.

Neo4j chỉ nhận node Entity và cạnh quan hệ. Cạnh giữ type quan hệ, `event_id`, trigger, rule ID, trạng thái và document IDs; document IDs dùng để tra bài ở Hugging Face, còn `collection_ids` phân biệt lần nhập. Không lưu câu evidence hay toàn văn. Import không xóa dữ liệu cũ.

Để nhập cùng export lên AuraDB, nạp cấu hình từ `.env` vào tiến trình PowerShell rồi chạy importer. Đoạn lệnh không in giá trị môi trường:

```powershell
$neo4jSettings = @{}
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#=]+)=(.*)$') {
    $neo4jSettings[$Matches[1].Trim()] = $Matches[2].Trim().Trim('"').Trim("'")
  }
}
$env:NEO4J_URI = $neo4jSettings['NEO4J_URI']
$env:NEO4J_USERNAME = $neo4jSettings['NEO4J_USERNAME']
$env:NEO4J_PASSWORD = $neo4jSettings['NEO4J_PASSWORD']
$env:NEO4J_DATABASE = $neo4jSettings['NEO4J_DATABASE']
uv run --no-sync weconomy import-neo4j $export
Remove-Item Env:NEO4J_URI,Env:NEO4J_USERNAME,Env:NEO4J_PASSWORD,Env:NEO4J_DATABASE
```

`NEO4J_DATABASE` mặc định là `neo4j`; `NEO4J_USERNAME` chấp nhận bí danh cũ `NEO4J_USER`. Import idempotent theo `entity_id` và `event_id`; `collection_ids` trên entity/cạnh ghi nhận các export đã nhập. Importer không xóa graph cũ.

Truy vấn cạnh và tìm tài liệu nguồn trong Hugging Face:

```cypher
MATCH (a:Entity)-[r]->(b:Entity)
RETURN a.name, type(r), b.name, r.triggers, r.rule_ids, r.review_status, r.event_id, r.document_ids
LIMIT 25;
```

Cạnh trong Neo4j biểu diễn ứng viên máy; `reported` không có nghĩa đã fact-check. Dùng `r.document_ids` để tìm bản ghi nguồn trong kho Hugging Face. Xem thêm [schema](SCHEMA.md).

## Docker offline

Image core chứa backend gazetteer, không bao gồm GLiNER/model weights. Ví dụ chạy fixture offline, mount thư mục `data/` để giữ run trên host:

```powershell
docker build -t weconomy:corpus-v3 .
$dataPath = (Resolve-Path .\data).Path
docker run --rm --network none --mount "type=bind,source=$dataPath,target=/app/data" `
  weconomy run --manifest samples/excerpts/manifest.json --allow-excerpts
```

`--network none` phù hợp với fixture local. Với nguồn Internet, dùng CLI ngoài container và tuân thủ policy hiện hành. Các lệnh Hugging Face private được ghi riêng trong [HUGGINGFACE.md](HUGGINGFACE.md).
