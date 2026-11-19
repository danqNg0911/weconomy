# Schema v1.1

Schema Arrow thực thi ở `src/weconomy/schema.py`; in bằng `uv run weconomy schema`.
Trường chuỗi vắng thông tin dùng chuỗi rỗng; không bịa ngày đăng/ngày sự kiện.

| Lớp / bảng | Khóa | Nội dung |
|---|---|---|
| bronze/bronze | document_id | URL, raw HTML, SHA256, source_id, kind, license, attribution, retrieved_at, published_at, language_hint, headers |
| silver/articles | document_id | title, normalized text, language, routing_method, content_sha256, duplicate_of |
| silver/sentences | sentence_id | document_id, text, start/end (silver text) |
| silver/mentions | mention_id | document_id, sentence_id, entity_id, surface, entity_type, method, start/end (silver text) |
| gold/entities | entity_id | canonical name, entity_type, resolution_method |
| gold/relations | claim_id | subject_id, predicate, object_id, event_id, document_id, sentence_id, evidence, trigger, rule_id, assertion_status, review_status, event_date, evidence_start/end |
| gold/events | event_id | subject_id, predicate, object_id, assertion_status, event_date, dedup_scope |

`entities` gồm mọi thực thể được NER nhận dạng, kể cả isolate. Chỉ tiêu graph phải báo cả số thực thể có cạnh
và toàn bộ thực thể. Số cạnh phải phân biệt claims, events và cặp simple projection.
`relations` là tập claims trích xuất, không phải gold labels của đánh giá. Tên lớp gold chỉ biểu thị lớp dữ liệu.

## Loại thực thể

`PERSON`, `ORG`, `PLACE`, `GOV`. GLiNER dùng nhãn tương ứng; GOV có nhãn riêng cho chính phủ/cơ quan quản lý
và alias đã duyệt. Không tự đổi mọi ORG có chữ ministry thành GOV; bản ghi nghi sai loại được đưa sang review.
Quỹ và tập đoàn vẫn là ORG trong schema gốc. `filter-domain` v15 tạo export riêng, kiểm tra tên,
bằng chứng domain sát actor và predicate/hướng của từng claim. Chỉ entity có cạnh đã kiểm định được
tính vào ngưỡng node. Entity chưa đủ căn cứ vẫn nằm trong source và `audit/entities.jsonl`; claim được
giữ hoặc đưa sang review có lý do trong `audit/claims.jsonl`. Xem [quy trình](DOMAIN_VERIFICATION.md).
Các kiểm tra này chưa phải nhãn chuẩn hay phép đo precision; `OTHER` không phải điều kiện lọc v15.
Rule tham chiếu vòng vốn có thể tạo evidence window gồm vài câu liên tục. Window có offset thật và
mention của cả hai actor, được lưu dưới schema Sentence; rule_id phân biệt nó với một câu NLP thông thường.

## Quan hệ có hướng

| Predicate | Subject → Object | Định nghĩa |
|---|---|---|
| ACQUIRED | ORG → ORG | Chủ thể mua/thâu tóm tổ chức đích; không suy ra từ mua cổ phần/sản phẩm |
| AGREED_TO_ACQUIRE | ORG → ORG | Đã đạt thỏa thuận mua tổ chức đích, chưa đồng nghĩa thương vụ hoàn tất; assertion_status=agreement_reported |
| INVESTED_IN | ORG/PERSON → ORG | Rót vốn, không đồng nghĩa mua toàn công ty |
| MERGED_WITH | ORG → ORG | Sáp nhập được câu mô tả; giữ hướng văn bản, analytics có thể đối xứng hóa |
| SUED | ORG/PERSON/GOV → ORG/PERSON | Bên khởi kiện → bên bị kiện |
| PARTNERED_WITH | ORG → ORG | Quan hệ hợp tác rõ ràng; không suy ra từ cùng ngành |
| SUPPLIES_TO | ORG → ORG | Nhà cung ứng → khách hàng |
| CEO_OF | PERSON → ORG | Người giữ vị trí CEO → tổ chức trong thời điểm câu mô tả |
| FOUNDED | PERSON/ORG → ORG | Người/tổ chức sáng lập → tổ chức được sáng lập |
| SUBSIDIARY_OF | ORG → ORG | Công ty con → công ty mẹ |
| REGULATES | GOV → ORG | Cơ quan quản lý → tổ chức chịu quản lý |
| OWNS_STAKE_IN | PERSON/ORG → ORG | Cá nhân/tổ chức nắm cổ phần tại tổ chức; không suy ra từ việc mua tài sản |
| BOARD_MEMBER_OF | PERSON → ORG | Thành viên hội đồng quản trị → tổ chức |
| CONTRACTED_WITH | ORG → ORG | Hai tổ chức ký hợp đồng; chỉ lấy khi câu nêu rõ hành động ký |
| AWARDED_CONTRACT_TO | GOV/ORG → ORG | Bên trao/giao hợp đồng → bên nhận |
| ANTITRUST_ACTION_AGAINST | GOV → ORG | Hành động pháp lý chống độc quyền được nêu rõ; không suy từ một cuộc điều tra bất kỳ |
| SANCTIONED | GOV → ORG/PERSON | Chính phủ áp đặt trừng phạt → tổ chức/cá nhân |
| DISRUPTED_SUPPLY_TO | GOV/ORG → ORG | Tác nhân làm gián đoạn nguồn cung → tổ chức chịu ảnh hưởng |
| SPUN_OFF_FROM | ORG → ORG | Công ty tách ra → công ty mẹ/đơn vị gốc |
| INVESTIGATES | GOV → ORG/PERSON | Cơ quan tiến hành điều tra đối tượng; không khẳng định đối tượng vi phạm |
| CLOSED_INVESTIGATION_INTO | GOV → ORG/PERSON | Cơ quan đã kết thúc/đóng cuộc điều tra; không đồng nghĩa phán quyết vô tội |
| LICENSED_TECH_FROM | ORG → ORG | Bên nhận quyền sử dụng công nghệ → bên cấp quyền; không đồng nghĩa mua công ty |

Có 22 predicate trong schema; các predicate quan hệ mới có rule song ngữ và nhãn model tương ứng.
Ba predicate bổ sung ở v20 không đổi cấu trúc Arrow 1.1: nhãn vẫn là chuỗi và các trường giữ nguyên.
Điều tra được diễn đạt ở quá khứ dùng `historical_reported`; trạng thái hiện tại phải đọc cùng ngày bài và bằng chứng,
không coi một cạnh INVESTIGATES cũ là cuộc điều tra vẫn đang mở hôm nay. Trường hợp đóng điều tra có predicate riêng.
LICENSED_TECH_FROM chỉ nhận giao dịch cấp quyền được nguồn khẳng định; thỏa thuận/dự định cấp quyền chưa có
predicate riêng và không được nâng thành đã cấp quyền. `HIRED_TEAM_FROM`/mua IP cũng chưa được suy từ đó.
Các rule mới chỉ khớp một số cách diễn đạt tường minh. REGULATES và quan hệ cần GOV vẫn phụ thuộc GOV seed/model.
AGREED_TO_ACQUIRE giữ riêng trạng thái thỏa thuận. Không nâng
thỏa thuận/dự định thành ACQUIRED đã hoàn tất để tăng số cạnh.
Số loại **định nghĩa** không được báo thành số loại **quan sát**.
`assertion_status=reported` nghĩa là câu trình bày khẳng định theo nguồn, không có nghĩa đã fact-check.
Các trường kiểm định thân bài và raw_bytes/schema 1.1 được mô tả ở `FULLTEXT.md`.
`review_status=unreviewed` cho toàn bộ đầu ra tự động. Không có confidence số được hiệu chuẩn nên không đặt điểm giả.

## Provenance và dedup

- `document_id = hash(canonical URL, raw SHA256)`; loại tracking, giữ query có nghĩa như oldid.
- `sentence_id = hash(document_id, start, text)`; `mention_id = hash(sentence_id, start, end)`.
- `entity_id = hash(entity_type, casefold(canonical name))`; alias khác type/đồng danh cần xử lý thủ công. Trong cùng một bài, surname/tước xưng được gộp vào PERSON tên đầy đủ chỉ khi có đúng một anchor khớp; nhiều người cùng họ thì giữ riêng.
- Text hash và Jaccard 5-word-shingle loại bài giống trong cùng run; vẫn giữ snapshot bronze/silver.
  `merge-runs` chọn một capture toàn văn/NLP thành công mỗi URL theo thứ tự input (cuối thắng),
  rồi chạy lại cùng phép dedup trên toàn bộ corpus đã chọn. Không cộng số liệu của các run nguồn.
- `event_id` hiện gắn actor+predicate+assertion_status+document revision khi chưa biết ngày sự kiện.
  Nhiều câu cùng actor/predicate trong một bài chia sẻ event, mỗi câu có claim riêng.
  Đây là quy tắc bảo thủ cho pilot: có thể gộp nhầm hai giao dịch cùng cặp trong một bài;
  có thể đếm trùng cùng giao dịch ở nhiều bài. Chưa dùng để chứng nhận 5.000 sự kiện duy nhất.
- `claim_id = hash(event_id, sentence_id)`. Evidence start/end phủ toàn câu và giữ trigger.

## Neo4j và phép chiếu

```text
(Entity)-[:ACQUIRED|... {relation_id, collection_id, event_ids, review_status,
                          assertion_status, triggers, rule_ids, document_ids,
                          event_details_json}]->(Entity)
                          rule_ids, document_ids, collection_ids}]->(Entity)
```

Neo4j chỉ lưu node Entity và cạnh quan hệ trực tiếp. Mỗi bộ ba đã chuẩn hóa là một cạnh trong từng collection; predicate đối xứng có thứ tự endpoint chuẩn. Các event và claim nguồn được giữ trong `event_ids`, `event_count`, `claim_count` và `event_details_json`; cạnh cũng lưu trigger, rule và `document_ids` để tra bài trong kho Hugging Face. Khóa cạnh gồm `relation_id` và `collection_id`, nên import lặp cùng collection là idempotent và các snapshot khác nhau vẫn tách biệt. Không tạo node Document, Sentence, Event, Claim hay Collection; không lưu câu evidence, raw HTML hay toàn văn trong graph.
Analytics mặc định giữ isolate, loại cạnh lặp/hướng/trọng số bằng undirected simple projection;
đường đi toàn cặp chỉ báo trên LCC, cùng số cặp reachable và tỷ lệ bao phủ.
