# Trạng thái tool và hướng dẫn bàn giao

Cập nhật ngày **04/11/2026, Asia/Saigon**; số liệu corpus tham chiếu ngày 31/10 bên dưới là lịch sử. Đây là trạng thái triển khai và bằng chứng đã chạy,
không phải cam kết đã đạt chỉ tiêu đề bài. Nhánh làm việc: `duy`; các thay đổi hiện còn local,
chưa commit/push. Người clone repository chưa chắc có cùng phiên bản code với máy đã kiểm thử.

## Nên dùng tool vào việc gì lúc này?

Lượt hoàn thiện ngày 04/11 đã sửa căn chỉnh `qui/quy` của underthesea, thêm mẫu vai trò Việt và mẫu vòng gọi vốn Anh có bên tham gia được nêu tên. CLI có thêm `collect-dataset --from-run` để xử lý lại bronze theo batch, giữ checksum và lineage, tiếp tục hoặc bổ sung archive/RSS với cùng cấu hình xử lý. Sau thay đổi NER/rule, dùng dataset mới; fingerprint từ chối trộn kết quả không tương thích. Bộ kiểm thử được hỗ trợ hiện có **214 test pass**, cùng kiểm tra độc lập về xử lý offline, ngân sách cộng dồn và phục hồi batch.

Kiểm tra corpus thật: dataset v4 `data/datasets/international-business-v4-20261104` phát lại 393 body, nhận 229 bài, có 31 node có cạnh / 16 cạnh phân biệt / 17 claims / 2 loại quan hệ và không có lỗi xử lý. Lượt chạy đã kết thúc vì hết candidate; chưa đạt 2.000 / 5.000 / 10. So với bản cũ, một bài lỗi NER được khôi phục; ba claims người sáng lập sai bị loại, hai claims CEO có bằng chứng được khôi phục. Số liệu 31/10 ở các mục dưới là lịch sử của run khác.

Giới hạn đã quan sát: trong corpus này, một số tên tổ chức/nhân vật Việt bị mô hình gán `PLACE` hoặc thiếu span, nên rule có thể bỏ sót quan hệ. Corpus được nhận cũng không có câu gọi vốn thỏa điều kiện của mẫu vòng vốn mới. Các kiểm thử xác nhận logic và lưu trữ, không thay thế bộ nhãn để đo precision/recall.

Có thể dùng để thu thập có giới hạn từ nguồn được bật, lưu HTML gốc, kiểm tra thân bài,
chạy NER/RE baseline và xuất dữ liệu có provenance để kiểm tra thủ công. Có thể chạy lại offline
và nhập ứng viên vào Neo4j. Tool hiện là pipeline nghiên cứu; đầu ra chưa phải knowledge graph đã xác thực.

Với corpus chủ đề có thể tiếp tục, chạy `weconomy collect-dataset` rồi `dataset-status` và
`export-dataset`; xem [các lệnh, tham số và giới hạn](collection.md). Đừng suy ra nguồn nào đang hoạt động
từ tên trong đề tài: `weconomy sources --check` chỉ probe tối đa một bài mỗi nguồn.

## Đã có và đã kiểm tra đến đâu

| Thành phần | Trạng thái thực tế | Giới hạn người dùng cần biết |
|---|---|---|
| CLI/config/schema | Đã chạy; Parquet bronze/silver/gold có schema cố định | Không có web UI/API phục vụ nhiều người |
| Discovery RSS | Các lần chạy lịch sử từng thu từ VnExpress, Tuổi Trẻ và TechCrunch | Là số liệu/lựa chọn cũ, không khẳng định publisher đang bật; policy hiện tại và probe xem bằng `weconomy sources`. Chưa có crawler lịch sử đầy đủ |
| Chính sách truy cập | Host allowlist, robots, redirect, rate/size/timeout; dừng nguồn bị chặn | Không vượt paywall/anti-bot; quyền đọc không cấp quyền phát hành lại toàn văn |
| Adapter và toàn văn | Trafilatura đối chiếu DOM theo nguồn; lưu bytes gốc và SHA256 | `body_checked` chỉ xác minh thân bài có trong HTML được trả về; chưa lấy nội dung ẩn sau JavaScript, phân trang hoặc paywall |
| Cách ly dữ liệu | `partial/restricted/unknown` không vào NLP mặc định | Có HTML hoặc có text chưa đủ để được coi là bài toàn văn |
| Tiền xử lý/routing | Unicode, khoảng trắng, câu/offset; định tuyến Việt/Anh | Chia câu vẫn có quy tắc và giới hạn với viết tắt; chưa hỗ trợ ngôn ngữ khác |
| NER | Gazetteer; spaCy tiếng Anh và underthesea tiếng Việt đã chạy | Có thể bỏ sót/sai kiểu thực thể; chưa có điểm chất lượng độc lập |
| Entity resolution | Alias có kiểm soát và tên chính xác theo kiểu; fuzzy chỉ gợi ý | Chưa entity linking rộng, phân giải đồng danh hoặc coreference |
| RE theo câu | Mẫu Việt/Anh; mẫu bị động/chức danh; dependency RE Anh có kiểm tra phủ định/tình thái và tường thuật | Độ bao phủ còn hạn chế; chưa dependency RE Việt hoặc mô hình RE được kiểm định để thay baseline |
| Provenance | Claim → câu/bài/URL; evidence, offset, trigger, rule ID; snapshot config/policy | `reported` là khẳng định theo nguồn, không phải đã fact-check |
| Luồng immutable run legacy | `collect --skip-run`, `merge-runs`; dedup lại trên corpus đã chọn | Luồng này cần chỉ định run và không có ledger/checkpoint liên tục; dùng catalog dataset ở hàng kế tiếp cho collection tiếp diễn |
| Dataset chủ đề tăng dần | CLI `collect-dataset`, catalog SQLite, batch Parquet bất biến, `--resume`, status và JSONL export | RSS hữu hạn, budget là số URL thử; domain heuristic chưa được đo precision; JSONL/catalog không phải input Parquet cho Neo4j/HF. Xem [collection.md](collection.md) |
| Event dedup | Bảo thủ trong tài liệu khi chưa có ngày sự kiện | Chưa xác định sự kiện xuyên bài theo ngày/giao dịch; chưa chứng nhận số sự kiện thực duy nhất |
| Nhãn và metrics | Sinh task câu đầy đủ; evaluate NER/RE P/R/F1 và Wilson interval | Chưa có nhãn độc lập hoàn chỉnh; không có precision 90% đã kiểm chứng |
| Neo4j | Import/reimport thật, đối chiếu count theo run, MERGE idempotent | Chưa có workflow duyệt accept/reject và lịch sử duyệt; không tự xóa revision cũ |
| NetworkX | Components, degree centrality, PageRank, communities, clustering; shortest paths trên LCC | Phép chiếu hiện vô hướng, đơn, không trọng số; chưa betweenness và các phép chiếu có hướng/trọng số |
| Small-world | Có lệnh sigma và điều kiện từ chối khi graph không phù hợp | Corpus hiện quá nhỏ/thưa ở phần có cạnh; chưa có kết luận small-world |
| GDS | Có query template | Chưa cài/bật và nghiệm thu so sánh với NetworkX |
| Katana | Nhập URL/JSONL khám phá vào cổng policy của Python | Chưa nghiệm thu chạy crawler Katana; crawler ngoài không chịu cổng Python khi tự tải trang |
| Docker | Build và chạy offline đã qua; 80 văn bản trùng Windows | Image core chỉ có gazetteer, không có spaCy/underthesea; không coi kết quả NLP hai môi trường là tương đương |
| Hugging Face | Có `hf-push/hf-pull`, private-only upload, snapshot/checksum và commit pin; kiểm thử local + Hub giả lập | Chưa nghiệm thu tài khoản/repo thật; chưa đồng bộ tự động. Xem [HUGGINGFACE.md](HUGGINGFACE.md) |

## Số liệu đã xác minh

Các số bên dưới mô tả riêng corpus/run lịch sử ngày 31/10; chúng không phải kết quả của `collect-dataset` mới.
Không cộng replay hoặc suy ra dataset mới đã đạt ngưỡng từ các số liệu này.

Run tham chiếu: `20261031T101555-c6e4bee3`, backend `models`, extractor `body-v2.1`, schema `1.1`.

| Chỉ số trong run | Giá trị |
|---|---:|
| Bài qua kiểm tra toàn văn/NLP | 80 |
| Nguồn trong corpus tham chiếu lịch sử | TechCrunch 39; Tuổi Trẻ 20; VnExpress 21 (không phản ánh allowlist hiện tại) |
| Câu/segment | 2.194 |
| Mentions | 2.159 |
| Thực thể ứng viên | 1.199: PERSON 382; ORG 244; PLACE 573 |
| Claims/events ứng viên | 7 / 7 |
| Loại quan hệ quan sát | 4: ACQUIRED, AGREED_TO_ACQUIRE, CEO_OF, FOUNDED |
| Cạnh trên phép chiếu simple NetworkX | 6; một cặp có nhiều loại quan hệ |
| Nhãn chuẩn bị / câu đã gán nhãn hoàn chỉnh | 200 / 0 |
| Precision / Recall / F1 độc lập | Chưa đo; `null` |

Không cộng số liệu của các lần replay. Không coi 1.199 ứng viên, bao gồm địa danh, là 1.199 doanh nghiệp
hoặc thực thể đã duyệt. Có 11 predicate trong schema nhưng mới quan sát 4 loại trong run này.
Corpus gồm cả 2 bài VnExpress năm 2021; không phải toàn bộ là tin mới trong hai tuần.

Ở đợt thử nguồn trước khi gom, 18 trang bị cách ly vì chưa xác minh được selector thân bài;
các trang đó được giữ trong run nguồn, không tính vào 80 bài của corpus này. Feed VnExpress
`doanh-nghiep.rss` đã bỏ khỏi config mặc định vì trả nhiều hồ sơ sản phẩm cũ.

Bằng chứng local (không được đưa vào Git):

- [Manifest corpus](../data/runs/20261031T101555-c6e4bee3/manifest.json): counts, lỗi, phiên bản và lineage.
- [Neo4j verification](../data/runs/20261031T101555-c6e4bee3/neo4j-verification.json): 1.199 Entity, 80 Document, 7 Claim/Event/cạnh nghiệp vụ theo run; import lại không tăng count.
- [Docker verification](../data/docker-corpus-verified/verification.json): 80 văn bản trùng, dataset hợp lệ, image ID; backend NLP khác host.
- [Analytics](../data/runs/20261031T101555-c6e4bee3/analytics.json): sigma `null` do LCC quá nhỏ/thưa hoặc clustering bằng 0.
- Lần kiểm thử code trước khi bàn giao: **126 tests passed**, Ruff và `git diff --check` qua.
  Đây là kết quả lần chạy ngày 31/10; thay code cần chạy lại checks.
- Sau khi thêm luồng Hugging Face ngày 01/11: **139 tests passed**, Ruff/lock check/diff check qua;
  đóng gói/phục hồi offline 80 bài giữ nguyên 7 bảng. Chưa nghiệm thu Hub thật hoặc Docker cho luồng HF.

Các link `data/` chỉ hoạt động trên máy có dữ liệu tương ứng. Clone Git không mang theo corpus,
model đã cài, `.env`, volume Neo4j hay môi trường `.venv`. Không tự công bố lại HTML báo thương mại.

## Người mới bắt đầu như thế nào?

1. Đọc [README](../README.md) để cài Python/uv, dependencies và model spaCy được ghim phiên bản.
   Muốn dùng `--ner models`, cài extras `nlp`; sau khi cài model riêng, dùng `uv run --no-sync`
   để uv không xóa model ngoài lock. Không dùng hoặc ghi đè `.env` của người khác.
2. Chạy mẫu offline `samples/excerpts/manifest.json` với `--allow-excerpts` như README.
   Mẫu này là trích đoạn có ghi công, không dùng để chứng minh đã thu thập toàn văn.
3. Kiểm tra [policy nguồn](../config/sources.yaml) và tham số trong [pipeline config](../config/pipeline.yaml).
   `collect` và `merge-runs` mặc định dùng models; `run` mặc định theo config, hiện là gazetteer.
4. Thu thập ít bài trước, lấy đường dẫn `run` từ JSON đầu ra, đọc `status/counts/errors/content_statuses`.
   Không chọn thư mục cuối cùng rồi mặc định đó là corpus cần dùng.
5. Validate trước khi xuất/nhập graph; đọc [hướng dẫn toàn văn](FULLTEXT.md),
   [schema](SCHEMA.md) và [gán nhãn](ANNOTATION.md) để hiểu đầu ra.

```powershell
cd D:\Project\weconomy
# Sau khi đã cài môi trường/model theo README:
$collected = uv run --no-sync weconomy collect --source vnexpress --source tuoitre --limit 3 --ner models | ConvertFrom-Json
$run = $collected.run
uv run --no-sync weconomy validate $run
uv run --no-sync weconomy export $run --table articles --output "$run/articles-review.jsonl"
uv run --no-sync weconomy export $run --table relations --output "$run/relations-review.jsonl"
```

Nếu dùng máy đang có corpus tham chiếu, có thể gán `$run = 'data/runs/20261031T101555-c6e4bee3'`
và validate trực tiếp. Đầu ra `--output` từ chối ghi đè; chọn tên mới khi file đã tồn tại.
HTML ở `bronze/html/`, toàn văn ở `silver/articles.parquet` hoặc JSONL `articles`,
thực thể/quan hệ ở `gold/`. Các thư mục này nằm trong `data/runs/<id>/`.

`status=completed` chỉ là hoàn tất xử lý batch, không phải đạt chất lượng đề bài.
`partial`/lỗi trả exit code 1; `no_new_documents` trả 0 và không có corpus mới để thay run cũ.
Ngân sách mặc định **100 documents** áp dụng cả input khi gom corpus; 80 bài cũ cộng 30 URL mới
có thể vượt ngân sách. Xem lại config/phạm vi trước khi gom, không coi lỗi này là đã mất dữ liệu.

## Những việc chưa làm hoặc chưa nghiệm thu

- [ ] Corpus đại diện đủ doanh nghiệp, tỷ phú/startup/quỹ/chính phủ và đủ hai ngôn ngữ.
- [ ] Kết nối và nghiệm thu upload/download thật với private dataset repo của nhóm trên Hugging Face.
- [ ] 2.000 thực thể, 5.000 sự kiện quan hệ đã kiểm định, 10 loại quan hệ quan sát thực.
- [ ] Bộ nhãn độc lập, split theo bài/sự kiện/thời gian; đo NER, RE và entity resolution.
- [ ] Xác minh precision ≥90% cùng recall/F1, per-type/per-language và khoảng tin cậy.
- [ ] Cải thiện độ bao phủ RE và NER trên tên doanh nghiệp mới; kiểm định mô hình thay thế.
- [ ] Coreference, entity linking có duyệt, event-time extraction và event dedup xuyên bài.
- [ ] Workflow duyệt gold/Neo4j, audit trail và quản lý phiên bản dataset/materialization.
- [ ] Checkpoint/job ledger, index dedup tăng dần/LSH, source/date partitions, theo dõi drift và scheduler.
- [ ] Nghiệm thu directed/weighted analytics, betweenness, GDS, null models và độ nhạy small-world.
- [ ] Khả năng vận hành dài hạn/hiệu năng ở quy mô mục tiêu; chưa benchmark để gọi production-ready.
- [ ] Báo cáo nộp và phân công nhóm: đang tạm hoãn theo yêu cầu người dùng.

GLiNER2 đã được thử riêng trên 44 câu tiếng Anh, có dự đoán quan hệ sai rõ ràng; chưa tích hợp vào
pipeline chính và không dùng số dự đoán thử nghiệm để cộng vào graph. Chưa có API trả phí bắt buộc.
Reuters/Bloomberg vẫn tắt chờ quyền truy cập phù hợp. Nguồn mở Wikipedia/Wikinews từng gặp 403;
không coi registry nguồn là bằng chứng đã tải được toàn văn từ nguồn đó.

Ưu tiên tiếp: hoàn thiện nhãn độc lập và phân tích lỗi NER/RE, cải thiện trên dev set rồi đo test đã khóa;
sau đó mở rộng nguồn/corpus có quyền và kiểm định lại. Không tăng số cạnh bằng đồng xuất hiện hoặc
nâng số đếm từ các lần replay. Xem [ROADMAP](ROADMAP.md) cho checklist theo giai đoạn.
