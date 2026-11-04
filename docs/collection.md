# Thu thập dataset chủ đề

Lệnh `collect-dataset` xây một catalog tăng dần từ bài báo đủ thân bài và qua bộ lọc chủ đề. Chủ đề theo [`initial.md`](../initial.md): tập đoàn đa quốc gia, tỷ phú, quỹ đầu tư quốc tế; lãnh đạo công nghệ/tài chính, startup, VC và chính phủ; các sự kiện đầu tư, M&A, chống độc quyền, cùng hợp tác hoặc gián đoạn chuỗi cung ứng.

## Chạy

Trên Windows, dùng trực tiếp `uv`; Makefile chỉ là tiện ích tùy chọn. `--ner models` cần cài NLP extras và model spaCy riêng như trong [hướng dẫn cài đặt](../README.md#cài-đặt-trên-windows):

```powershell
uv sync --locked --extra dev --extra nlp
uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

Sau khi cài model, tiếp tục dùng `--no-sync` để uv không gỡ model ngoài lock:

```powershell
uv run --no-sync weconomy collect-dataset --nodes 2000 --relations 5000 --relation-types 10 --max-candidates 5000 --batch-size 20 --ner models
uv run --no-sync weconomy dataset-status data/datasets/international-business
uv run --no-sync weconomy export-dataset data/datasets/international-business --output data/exports/international-business
```

Makefile là tùy chọn cho máy có GNU Make. `make install` cài NLP extras và model spaCy; `make collect` nhận biến như `DATASET`, `SOURCES`, `ARTICLES`, `NODES`, `RELATIONS`, `RELATION_TYPES`, `MAX_CANDIDATES`, `BATCH_SIZE`, `NER` và `RESUME`. Ví dụ tiếp tục một dataset với ngưỡng:

```powershell
make collect SOURCES="vnexpress tuoitre" NODES=2000 RELATIONS=5000 RELATION_TYPES=10 MAX_CANDIDATES=5000 BATCH_SIZE=20 RESUME=1
```

Nếu `SOURCES` trống, collector dùng các nguồn đủ điều kiện trong policy. Các lệnh `uv` ở trên vẫn là hướng dẫn chính và hoạt động trên Windows PowerShell mà không cần Make.

`collect-dataset` mặc định dùng `config/collection.yaml` và lưu vào `data/datasets/international-business`. Có thể truyền `--dataset PATH`; `--config PATH` phải đặt trước tên lệnh như argparse toàn cục thông thường. Tùy chọn `--source` có thể lặp lại. Thay vào đó, `--urls FILE` nhận mỗi URL trên một dòng; file URL không thể dùng cùng `--source`.

### Phát lại thân bài đã lưu

`--from-run PATH` có thể lặp lại để phát lại body `full_page` từ immutable run theo thứ tự ưu tiên; lần xuất hiện sau cùng của URL trùng được chọn. Cách này đọc bronze cũ và chạy extraction/NLP hiện tại, không tải bài qua HTTP. Chỉ tài liệu từng qua `body_checked` và NLP đủ điều kiện (hoặc lỗi NLP có thể khôi phục) mới được xét lại; bộ lọc thân bài, NLP và chính sách host hiện tại vẫn được áp dụng. Checksum raw cùng source, license, attribution, URL và thời điểm truy xuất được kiểm tra/lưu lại. Các archive phải giữ nguyên trong suốt quá trình.

Ví dụ phát lại các run đã lưu trong batch cũ bằng PowerShell:

```powershell
$archiveRoot = "data/datasets/international-business/batches"
$replayArgs = @()
Get-ChildItem $archiveRoot -Filter manifest.json -File -Recurse |
    Sort-Object FullName |
    ForEach-Object { $replayArgs += @("--from-run", $_.DirectoryName) }
uv run --no-sync weconomy collect-dataset --dataset data/datasets/international-business-v2-20261104 `
    --articles 200 --max-candidates 396 --batch-size 20 @replayArgs
```

Đổi tên đích nếu thư mục phiên bản đó đã tồn tại; collector không ghi đè dataset. Resume phải dùng cùng processing fingerprint và archive đã đăng ký không được thay đổi. Có thể thêm archive mới vào lần `--resume` sau; các archive cũ, queue và ngân sách attempts được giữ nguyên. `FROM_RUNS` trong Makefile nhận danh sách đường dẫn run, ví dụ `make collect DATASET=data/datasets/international-business-v2-20261104 FROM_RUNS="data/.../batch-a/run data/.../batch-b/run" ARTICLES=200 MAX_CANDIDATES=396`.

Ngưỡng `--articles`, `--nodes`, `--relations`, `--relation-types` là tùy chọn. `--max-candidates` là ngân sách tối đa tổng số URL được phân bổ để thử trong dataset, không phải số bài hợp lệ, và được giữ qua các lần chạy `--resume`. `--batch-size` giới hạn URL xử lý mỗi run nội bộ. `--relations` đếm cạnh phân biệt theo bộ `(subject, predicate, object)`; nhiều claim có thể hỗ trợ cùng một cạnh. Nếu đã yêu cầu ngưỡng mà dataset chưa đạt, lệnh trả mã 2; lỗi đầu vào, xử lý hoặc phát hiện nguồn trả mã 1; thành công/đã đạt trả mã 0. Chỉ tiếp tục dataset đã có bằng `--resume`; không có tùy chọn này thì lệnh từ chối ghi lên dataset cũ.

Các ngưỡng đầy đủ theo đề bài là 2.000 node có cạnh, 5.000 cạnh phân biệt và 10 loại quan hệ. Với phạm vi quốc tế hẹp hơn, đề bài cho phép tối thiểu 1.000 node. Có thể thêm `--articles 200` làm mục tiêu bài báo hoặc bỏ mọi cờ ngưỡng để khảo sát hữu hạn candidate.

## Dữ liệu và giới hạn

Candidate đến từ RSS hữu hạn của các nguồn tin được bật trong policy hiện tại hoặc từ URL được chỉ định. RSS không đảm bảo số lượng hay độ liên quan mong muốn. Chỉ bài có `body_checked`, NLP đủ điều kiện và domain heuristic nhận diện đúng phạm vi mới được giữ; bài bị giới hạn/thiếu thân bài hoặc ngoài phạm vi không được tính vào dataset. Heuristic phạm vi giúp lọc chủ đề, không phải phép đo precision. Độ chính xác trên 90% chưa được xác minh; cần bộ nhãn độc lập.

Catalog SQLite lưu queue và bản ghi chấp nhận; mỗi batch tham chiếu tới một run Parquet bất biến trong `batches/`. Resume dùng cùng catalog, kiểm tra fingerprint xử lý và không tải/NER lại các bài đã chấp nhận. Xuất JSONL gồm articles, entities, relations, claims và manifest; export chỉ đọc catalog đã commit và không ghi đè thư mục tồn tại. Dataset không tự đẩy lên dịch vụ từ xa. Hãy giữ nguyên policy bản quyền/robots và kiểm tra quyền chia sẻ trước khi phân phối văn bản.

Thư mục catalog và JSONL export không phải immutable run Parquet: không dùng chúng trực tiếp với `import-neo4j` hoặc `hf-push`. Các lệnh đó tiếp tục nhận đường dẫn run Parquet hợp lệ, ví dụ đường dẫn `batches/<id>/<run-id>` được ghi trong catalog SQLite.

WikiNews bị loại khỏi thu thập dataset. Danh sách nguồn đủ điều kiện phụ thuộc policy đang cấu hình; việc một publisher xuất hiện trong đề bài không chứng minh feed hoạt động hay quyền truy cập đã được xác minh. Kiểm tra bằng `weconomy sources --check` (mỗi nguồn tối đa một trang probe); probe không chứng nhận toàn bộ website hay quyền tái sử dụng.

```powershell
uv run --no-sync weconomy sources
uv run --no-sync weconomy sources --check --source vnexpress_en --source vneconomy_en --source vietnamnews --source thanhnien
```

## Kiểm tra hiện tại — 04/11/2026

Probe một bài trên mỗi nguồn ngày 03/11 cho thấy `vnexpress_en`, `vneconomy_en`, `vietnamnews` và `thanhnien` đều trả nội dung qua kiểm tra thân bài (`body_checked`). Hai bài (`vnexpress_en`, `vietnamnews`) được heuristic đưa vào phạm vi; hai bài còn lại ở ngoài phạm vi. Đây là kết quả của bốn trang đã probe, không phải kiểm chứng toàn website, RSS hay quyền tái sử dụng toàn văn.

Một lượt thu thập thật với bốn lần thử URL ghi nhận 3 bài được nhận, 10 node có cạnh, 5 cạnh phân biệt và 2 loại quan hệ. Resume với ngân sách tối đa 4 giữ tổng attempts ở 4; mục tiêu 2.000 node, 5.000 cạnh và 10 loại quan hệ vẫn chưa đạt. Độ chính xác chưa được đo bằng bộ nhãn độc lập. Probe được lưu tại `data/experiments/team-20261102/source-probes-current.json`; catalog thử nghiệm nằm trong `data/experiments/team-20261102/current-live-relations`, kết quả đối chiếu tại `current-live-graph-verification.json` và phần thiếu tại `current-live-deficits.json` trong cùng thư mục experiments.

Catalog cũ `data/datasets/international-business` đã hoàn tất 396 attempts, với 228 bài được nhận, 31 node, 17 cạnh và 2 loại quan hệ. Sau thay đổi NLP, processing fingerprint mới không tương thích với catalog này; giữ nguyên dữ liệu cũ và dùng một đường dẫn dataset mới khi phát lại body đã lưu.

Dataset `data/datasets/international-business-v4-20261104` đã phát lại 393 bản lưu toàn văn đủ điều kiện từ các batch cũ: 229 bài được nhận, 164 ngoài phạm vi, 31 node có cạnh, 16 cạnh phân biệt, 17 claims và 2 loại quan hệ. Lượt này kết thúc với `sources_exhausted`, không có lỗi xử lý. Một bài lỗi căn chỉnh NER đã được khôi phục; ba claims gán sai người sáng lập bị loại và hai claims CEO có bằng chứng được khôi phục. Cả ba ngưỡng số lượng và precision mục tiêu vẫn chưa được nghiệm thu. Xem snapshot trong [README](../README.md) và `data/experiments/collection-20261104/` trên máy đã chạy.
