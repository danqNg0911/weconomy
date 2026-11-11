# Kiến trúc và các quyết định Sprint 1

## Luồng dữ liệu

```mermaid
flowchart LR
    K[Katana category discovery] --> Gate[Policy + robots + rate limit]
    U[Explicit article URLs] --> Gate
    Gate --> B[Bronze: HTML + nguồn + giấy phép]
    Local[Trích đoạn thật có ghi công] --> B
    B --> T[Trafilatura + normalization]
    T --> S[Silver: article / sentence / mention]
    S --> L[Language routing + NER]
    L --> ER[Alias resolution]
    ER --> RE[Sentence rules + type constraints]
    RE --> G[Gold: Entity / Event / Claim]
    G --> Q[Validation + annotation + P/R/F1]
    G --> N[Neo4j]
    G --> A[NetworkX / Sprint 2 GDS]
```

Đơn vị dữ liệu trung tâm là **claim có câu bằng chứng**, không phải cặp tên cùng xuất hiện.
Một sự kiện có thể có nhiều claims từ nhiều câu. Machine candidates chưa đồng nghĩa với sự thật đã duyệt.
Neo4j chỉ có node Entity và cạnh quan hệ trực tiếp giữa các entity. Event ID, trạng thái, trigger, rule ID và document IDs là thuộc tính của cạnh; raw HTML/toàn văn được lưu ở Hugging Face, không đưa vào graph.

## Những quyết định đã thực thi

| Quyết định | Lý do | Giới hạn cần theo dõi |
|---|---|---|
| Python 3.11 + uv.lock | Wheels NLP trên Windows, môi trường tái lập | GLiNER weights tải lần đầu vào Hugging Face cache; cần mạng và vài GB dung lượng |
| Katana khám phá danh mục | Dùng target URL, giới hạn scope/page/time và policy hiện tại | Phụ thuộc cấu trúc trang danh mục và các cap hữu hạn |
| Registry adapter theo host | Cùng extractor, mỗi nguồn có policy/language/body selector riêng | Chưa thử parser toàn trang từng báo thương mại |
| Trafilatura | Tái sử dụng extractor có sẵn thay viết parser từng báo | Chưa kiểm tra chất lượng full-page thực tế do 403 |
| Gazetteer mặc định, models tùy chọn | Chạy offline nhẹ ngay; models dùng GLiNER-Relex với model ID riêng theo ngôn ngữ, một lượt lấy entities và relations | Nhãn business tiếng Việt truyền cho Barb là zero-shot; chưa đo trên tin kinh doanh |
| Alias xác định, fuzzy chỉ đề xuất; surname PERSON được resolve theo anchor duy nhất trong cùng bài | Gộp các cách gọi như “Elon Musk”/“ông Musk” mà không gộp họ chung xuyên bài | Nếu bài nhắc nhiều người cùng họ, hệ thống giữ riêng mention dạng họ |
| 19 predicate với type constraints | Bao phủ đầu tư, sở hữu, vai trò lãnh đạo, hợp đồng, M&A, chống độc quyền và chuỗi cung ứng; tách acquisition agreement khỏi completed acquisition | Rule là mẫu tường minh, chưa đo precision/recall trên nhãn thật; số predicate định nghĩa khác số loại quan sát |
| Parquet + immutable run | Debug/reprocess có thể truy vết và không ghi đè | Chưa catalog/version table nhiều người ghi |
| Event identity bảo thủ | Tránh gộp những vòng đầu tư khác nhau | Chưa dedup sự kiện xuyên bài/run khi không có ngày sự kiện |
| Neo4j Community | Lưu entity và cạnh quan hệ để truy vấn/visualize local | Raw và toàn văn nằm ở Hugging Face; truy vết từ cạnh qua document IDs |
| NetworkX trước GDS | Không phụ thuộc plugin server để phân tích pilot | Thuật toán toàn cặp chưa tối ưu cho graph lớn |

## Contracts giữa module

- `access.py` là cổng cho mọi request tải bằng Python. Katana chỉ khám phá URL; URL tải bài vẫn qua policy, robots và rate limit trong pipeline.
  Chuyển hướng phải qua policy lại. robots không tải được thì dừng, không tự suy ra cho phép.
- Manifest offline là đầu vào do người dùng quản lý, phải có giấy phép/ghi công/source/kind/thời điểm;
  không dùng nó để hợp thức hóa tập dữ liệu không có quyền. Snapshot có SHA thì kiểm tra SHA.
- Offset là index ký tự Unicode Python trong **văn bản silver đã normalize**, không phải byte HTML.
  NER giữ surface gốc; tên canonical không thay văn bản bằng chứng.
- `nlp.py` nhận một câu và language. `unknown` không tự route sang tiếng Anh.
- `schema.py` giữ kiểu Arrow và danh sách predicate. Thêm predicate cần cập nhật pattern,
  ràng buộc kiểu, nhãn, test và query; không thêm tùy tiện để đủ chỉ tiêu.
- `pipeline.py` tạo run mới. URL hash + raw checksum xác định revision tài liệu; sentence ID gắn revision
  và offset; entity ID gắn canonical name + type. Hàm `stable_id` dùng JSON để tránh nhập nhằng nối chuỗi.
- Import Neo4j chỉ nhận dữ liệu qua validate. Tham số hóa toàn bộ giá trị; tên loại cạnh từ whitelist.
  Tạo constraint trước, transaction dữ liệu sau. Không tự xóa dữ liệu đã tồn tại.

## Đường mở rộng sau pilot

1. Thu thập đủ quyền từ nguồn thật, đo extraction theo nguồn/ngôn ngữ; giữ metadata xuất bản và snapshot.
2. Thêm tập nhãn theo article/event/time split; bổ sung alias đã duyệt, định danh ngoài (Wikidata/LEI)
   khi có bằng chứng đồng nhất. Chỉ fuzzy/embedding không đủ kết luận cùng thực thể.
3. Backend models dùng GLiNER-Relex chung adapter và rule determinist làm fallback.
   Kiểm định cả hai trên nhãn độc lập. Tách reported/planned/
   denied/rumoured, vai trò chủ thể/đối tượng, thời gian quan hệ và attribution. Không nâng số cạnh bằng co-occurrence.
4. Khi batch tăng, thay pairwise shingles hiện O(n²) bằng MinHash/LSH; index xuyên run, partition Parquet
   theo source/date/language. Không cần Kafka để đạt vài nghìn thực thể; SQLite job ledger + batch là bước kế.
5. Chuẩn hóa event identity bằng actor+predicate+transaction/date/value với human review cho trường hợp mơ hồ.
   Không dùng publication date thay event date; không gộp chỉ dựa vào một cặp actor.
6. Khi cần tái dựng graph nhiều lần, thêm dataset version/materialization và kiểm tra count trong Neo4j;
   không coi mọi revision là sự kiện mới thật. Gold xuất bản cần quy trình accept/reject và lịch sử duyệt.

Giới hạn hiện tại: đơn tiến trình, chưa checkpoint từng request, không retry tự động 403/429,
chưa pin DNS đến socket (chỉ dùng registry đáng tin, không mở crawler nhận URL Internet tùy ý),
chưa coreference, chưa event-time extraction, chưa inference phủ định phức tạp, chưa UI annotation.
