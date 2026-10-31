# Schema v1.0

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

`PERSON`, `ORG`, `PLACE`, `GOV`. spaCy/underthesea chuyển nhãn địa danh về PLACE;
GOV cần alias hoặc classifier được duyệt, không tự đổi mọi ORG có chữ ministry thành GOV.
Quỹ và tập đoàn là ORG trong v1; subtype sẽ thêm khi có nhãn và nhu cầu truy vấn rõ ràng.

## Mười quan hệ có hướng

| Predicate | Subject → Object | Định nghĩa |
|---|---|---|
| ACQUIRED | ORG → ORG | Chủ thể mua/thâu tóm tổ chức đích; không suy ra từ mua cổ phần/sản phẩm |
| INVESTED_IN | ORG/PERSON → ORG | Rót vốn, không đồng nghĩa mua toàn công ty |
| MERGED_WITH | ORG → ORG | Sáp nhập được câu mô tả; giữ hướng văn bản, analytics có thể đối xứng hóa |
| SUED | ORG/PERSON/GOV → ORG/PERSON | Bên khởi kiện → bên bị kiện |
| PARTNERED_WITH | ORG → ORG | Quan hệ hợp tác rõ ràng; không suy ra từ cùng ngành |
| SUPPLIES_TO | ORG → ORG | Nhà cung ứng → khách hàng |
| CEO_OF | PERSON → ORG | Người giữ vị trí CEO → tổ chức trong thời điểm câu mô tả |
| FOUNDED | PERSON/ORG → ORG | Người/tổ chức sáng lập → tổ chức được sáng lập |
| SUBSIDIARY_OF | ORG → ORG | Công ty con → công ty mẹ |
| REGULATES | GOV → ORG | Cơ quan quản lý → tổ chức chịu quản lý |

Patterns tiếng Anh/Việt đều có trong code. REGULATES cần GOV seed thực, bộ mẫu hiện chưa có GOV.
Số loại **định nghĩa** không được báo thành số loại **quan sát**.
`assertion_status=reported` nghĩa là câu trình bày khẳng định theo nguồn, không có nghĩa đã fact-check.
`review_status=unreviewed` cho toàn bộ đầu ra tự động. Không có confidence số được hiệu chuẩn nên không đặt điểm giả.

## Provenance và dedup

- `document_id = hash(canonical URL, raw SHA256)`; loại tracking, giữ query có nghĩa như oldid.
- `sentence_id = hash(document_id, start, text)`; `mention_id = hash(sentence_id, start, end)`.
- `entity_id = hash(entity_type, casefold(canonical name))`; alias khác type/đồng danh cần xử lý thủ công.
- Text hash và Jaccard 5-word-shingle loại bài giống trong cùng run; vẫn giữ snapshot bronze/silver.
- `event_id` hiện gắn actor+predicate+assertion_status+document revision khi chưa biết ngày sự kiện.
  Nhiều câu cùng actor/predicate trong một bài chia sẻ event, mỗi câu có claim riêng.
  Đây là quy tắc bảo thủ cho pilot: có thể gộp nhầm hai giao dịch cùng cặp trong một bài;
  có thể đếm trùng cùng giao dịch ở nhiều bài. Chưa dùng để chứng nhận 5.000 sự kiện duy nhất.
- `claim_id = hash(event_id, sentence_id)`. Evidence start/end phủ toàn câu và giữ trigger.

## Neo4j và phép chiếu

```text
(Entity)-[:ACQUIRED|... {event_id, review_status, assertion_status}]->(Entity)
(Claim)-[:ABOUT_EVENT]->(Event)-[:SUBJECT|OBJECT]->(Entity)
(Claim)-[:EVIDENCED_BY]->(Sentence)-[:IN_DOCUMENT]->(Document)
```

Constraint unique trên các ID node. Edge nghiệp vụ MERGE theo event_id.
Full raw HTML không đưa vào Neo4j; truy vết qua document_id đến Parquet.
Đếm node provenance vào quy mô thực thể hoặc đếm hai lần cạnh reciprocal là sai.
Analytics mặc định giữ isolate, loại cạnh lặp/hướng/trọng số bằng undirected simple projection;
đường đi toàn cặp chỉ báo trên LCC, cùng số cặp reachable và tỷ lệ bao phủ.
