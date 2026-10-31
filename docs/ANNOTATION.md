# Gán nhãn và đo chất lượng

## Đơn vị và quy trình

Một task là một câu/segment trong silver, kèm article URL, document ID và sentence ID.
Có thể có title/heading và segment không chứa quan hệ. Gán toàn bộ entities/relations trong các loại
đã định nghĩa, không chỉ xác nhận cạnh máy dự đoán. `complete=true` là xác nhận câu đã được đọc hết.
Để giảm anchoring, file tasks không hiển thị prediction. File label hiện là JSON riêng, chưa phải native
Label Studio export. Có thể chuyển sang Label Studio sau; không quảng cáo đã có integration chưa viết.

1. Chia train/dev/test theo article và event, ưu tiên tách theo thời gian và source; không chia ngẫu nhiên
   các câu trong cùng một bài sang hai tập. Cross-source syndicated copies phải cùng split.
2. Lấy 150–200 câu ban đầu, phân tầng vi/en, source, loại thực thể/quan hệ; có câu không quan hệ,
   phủ định, dự định, phủ nhận, trích dẫn và đồng danh. Tăng mẫu cho loại hiếm.
3. Hai người gán nhãn độc lập một phần đủ lớn (ít nhất 20–30%), ghi reviewer thật, phân xử bất đồng;
   báo agreement theo span/triple, không tự tạo tên thành viên hay giả có hai người đã duyệt.
4. Khóa test trước khi sửa rules. Báo source distribution, n, TP/FP/FN, per-predicate và per-language.
   CLI hiện báo micro và per-predicate; muốn per-language, tạo file nhãn tách vi/en rồi evaluate từng file.
5. Duyệt entity resolution riêng: alias đúng, đồng danh, tổ chức đổi tên, người cùng tên. Entity IDs
   trong relation label phải lấy canonical mapping đã duyệt; có thể tính bằng stable_id(type,name.casefold()).

## Quy ước pilot

- NER: ORG, PERSON, PLACE, GOV, exact Unicode character span trong task.text. Không gán sản phẩm,
  chức danh, ngày tháng là thực thể của mạng v1. Tên viết tắt/surname có chỉ định người vẫn được gán span.
- Quan hệ: một triple có hướng subject_id/predicate/object_id; actors phải được câu chứng minh rõ.
  Không gán quan hệ qua coreference sang câu khác cho bài đo sentence-only này.
- ACQUIRED chỉ mua tổ chức đích; quyết định mua, đề nghị mua, đạt thỏa thuận chờ hoàn tất chưa được
  coi là giao dịch hoàn tất. Headline fragment không có câu thân bài đầy đủ: không gán triple.
- AGREED_TO_ACQUIRE (bổ sung 31/10): câu nêu rõ đã đạt thỏa thuận mua tổ chức đích; không gán
  ACQUIRED thay thế. Dự định/đề nghị đơn thuần không có thỏa thuận chưa thuộc loại này.
- CEO_OF là chức vụ hiện hữu trong câu; “will become/was to become” chưa phải đã giữ chức vụ.
- Vai trò đồng sáng lập: mỗi founder có một triple. Apposition “current Pixar and Apple CEO”
  chứng minh hai CEO_OF. Baseline có thể bỏ sót: đó là false negatives cần đo.
- Không dùng hiểu biết ngoài câu để gán quan hệ. Câu Wikipedia “Công ty được sáng lập bởi ...”
  thiếu tên công ty ngay trong câu: không gán triple trong bài đo sentence-only, vẫn gán person spans.

## Định dạng

```json
{
  "format": "weconomy-labels-v1",
  "tasks": [{
    "sentence_id": "ID từ task",
    "text": "câu gốc",
    "reviewer": "tên người gán nhãn thật",
    "split": "test",
    "complete": true,
    "entities": [{"surface": "tên", "start": 0, "end": 3, "entity_type": "ORG"}],
    "relations": [{"subject_id": "ID chủ thể", "predicate": "ACQUIRED", "object_id": "ID đối tượng"}]
  }]
}
```

Ví dụ trên chỉ mô tả format, không phải tin bài hay nhãn đã duyệt. Offset end exclusive.
CLI từ chối thiếu reviewer, incomplete, trùng sentence ID, text không khớp run hoặc span sai.
Nhãn rỗng `relations: []` chỉ hợp lệ khi đã đọc và xác nhận câu không có quan hệ trong scope.

## Metrics và cách diễn giải

Relations exact match theo (sentence ID, subject ID, predicate, object ID); tập label là toàn bộ ground truth
trong câu, nên quan hệ bị bỏ sót làm giảm recall. Entity resolution sai làm relation mismatch.
NER exact match theo (sentence ID, start, end, type), độc lập với canonical name.
Precision = TP/(TP+FP), Recall = TP/(TP+FN), F1 = 2TP/(2TP+FP+FN).
Mẫu không có denominator thì metric là null, không tự gán 100%.
Wilson 95% cho precision được in để thấy bất định do mẫu nhỏ; không chứng minh chất lượng toàn bộ corpus.

`reports/pilot-labels.json` nếu có là nhãn **agent-pilot**, không phải người gán nhãn độc lập,
không held-out và không dùng để công bố đạt ≥90%. Một prediction đúng trong hai prediction
khác hoàn toàn với 90% trên nhiều loại quan hệ và hai ngôn ngữ. Precision cao nhưng recall thấp
vẫn không đủ tạo mạng lớn đúng deadline. Báo thêm số entity có cạnh và độ đa dạng quan hệ thực.
