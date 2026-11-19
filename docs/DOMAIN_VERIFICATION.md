# Kiểm định domain và bổ sung dữ liệu

## Phạm vi và điều kiện chấp nhận

Domain theo `initial.md`: startup, tập đoàn/công ty kinh doanh, quỹ đầu tư, người sáng lập/điều hành,
tỷ phú và cơ quan chính phủ trong các quan hệ kinh doanh được bài báo mô tả. Một đối tác được mở rộng
vào mạng khi có quan hệ đã qua kiểm định trực tiếp với actor có bằng chứng domain; không mở rộng dây chuyền
qua những cạnh chưa được xác thực.

Chỉ tiêu mặc định kiểm tra **sau normalize**: 2.000 nút có cạnh, 5.000 triple khác nhau và ít nhất 11
loại quan hệ. Triple là bộ `(subject_id, predicate, object_id)`. Nhiều bài chứng minh cùng một triple
được lưu thành nhiều claim, không dùng để tăng số cạnh. Entity chưa có cạnh chỉ xuất hiện trong audit,
không được cộng vào chỉ tiêu nút của mạng.

## Sự kiện quản lý và cấp phép công nghệ (v20)

- Phân biệt `INVESTIGATES`, `CLOSED_INVESTIGATION_INTO` và `LICENSED_TECH_FROM`; không ép điều tra thành SUED,
  đóng điều tra thành đang điều tra, hoặc cấp quyền công nghệ thành ACQUIRED.
- GOV được sửa trước trích xuất khi bài có tên đầy đủ của cơ quan và ngữ cảnh thẩm quyền: hiện chỉ một bộ
  alias có kiểm soát cho SEC/DOJ/FTC của Mỹ. Thiếu tên đầy đủ/ngữ cảnh, tên trùng tổ chức khác hoặc cơ quan
  chưa nằm trong bộ nhận diện thì không tự đổi nhãn. Không thay toàn bộ Commission/Department thành GOV.
- NLP nạp alias theo từng bài, ưu tiên span tên cơ quan đầy đủ. Normalize dùng cùng helper cho dữ liệu legacy;
  các mention ORG nằm trong span cơ quan đã xác định không được che mất endpoint thật.
- `investigating whether ...` nói cuộc điều tra đang/đã diễn ra, không phải nghi vấn cuộc điều tra có tồn tại.
  Rule xét đúng khoảng giữa actor/target, vẫn chặn `not investigating`, `may investigate` và giả định.
- Quá khứ `was investigating/was under investigation` dùng `historical_reported`; không khẳng định vụ việc
  còn mở hiện tại. Điều tra/đóng điều tra không khẳng định có tội/vô tội.
- Nhận cấu trúc thanh toán để cấp quyền như `A paid B $... to license its technology`, với hai tổ chức cụ thể.
  Không suy giao dịch đã hoàn tất từ agreed/offered và không biến tuyển nhân sự hoặc mua IP thành mua cả công ty.

## Chặn và xử lý sớm trong luồng (v19)

Các bản cũ vẫn được giữ nguyên. Bài mới đi qua các bước sau trước khi lưu claim:

1. Policy nguồn, chất lượng body, URL/nội dung trùng và routing chủ đề như trước.
2. `NLP.begin_document` xác định ngữ cảnh tổ chức X trước vòng tách câu/NLP. X của Alphabet và X mạng xã hội
   có ID riêng. Không có bằng chứng rõ hoặc có cả hai nghĩa trong một bài thì X cần review; không suy từ tên đơn lẻ.
   Context được reset cho mỗi bài, kể cả khi có curated alias `X → Twitter`.
3. Tách câu giữ tên viết tắt nhiều dấu chấm như O.H.I.O. Fund và dấu kết thúc trong ngoặc; offset theo nguyên văn.
4. Tách descriptor đầu câu và descriptor sở hữu khỏi tên: `Defense startup Firestorm Labs` → `Firestorm Labs`,
   `David Sacks’ firm Craft Ventures` → `Craft Ventures`. Nhóm chung như European entrepreneurs không thành named actor.
5. Trích vai trò với phủ định theo đúng vùng cặp entity và phần dẫn trước; phủ định trong câu trích dẫn khác không
   làm mất chức danh bên ngoài. Dự báo vai trò, phủ định chức danh và chức danh nằm trong lời trích dẫn vẫn bị chặn.
   Từ May chỉ tháng không tự biến CEO thành vai trò dự kiến.
6. Kiểm tra chủ thể thật trước khi tạo quan hệ: con gái/foundation của một người không phải chính người đó;
   sản phẩm đứng sau cụm `company behind` không tự thành bên nhận vốn; employer của người đầu tư không tự là investor.
7. Phục hồi vốn dùng chung helper: nhận công bố vòng vốn đã có danh sách dẫn vòng, backed-by seed funding,
   descriptor trước tên investor. `The company/startup` chỉ nối về tổ chức duy nhất ở câu liền trước, có vai trò
   chủ thể hoặc được giới thiệu rõ, không phải quỹ vừa dẫn vòng hay một đối tượng được nhắc thoáng qua.
8. Rule mệnh đề chen giữa chỉ chạy khi có cue phù hợp. Không ghép mọi cặp entity chỉ vì cùng câu.
   Mua tài sản/cổ phần, kế hoạch và tin đồn vẫn không thành mua toàn bộ công ty đã hoàn tất.

Normalize dùng lại các helper này để kiểm tra và để phục hồi các bản ghi legacy; không chạy lại model bài cũ.
Các quyết định context có trong model audit; snapshot có `audit/name_resolutions.jsonl` và
`audit/unresolved_contexts.jsonl`. Quy tắc không tăng chi phí model bằng cách gọi lại inference cho cùng câu.

Phạm vi chưa làm: coreference tùy ý nhiều câu, tách hai nghĩa X trong cùng một bài theo từng lần xuất hiện,
mọi loại fragment trong danh sách/caption, mở schema GOV/PRODUCT/PROJECT và sự kiện pháp lý mới. Không dùng
rule rộng để lấp những khoảng trống đó. Vai trò và quan hệ mới vẫn cần kiểm định domain riêng trước công bố.

## Chi tiết thay đổi v18

Các tin nói `raised ... in funding` rồi `Its investors include ...` có thể có bằng chứng đầu tư
nhưng không có nhãn Series/seed. Bộ phục hồi nhận danh sách nhà đầu tư rõ ràng sau một bên nhận
vốn được định danh duy nhất; không coi danh sách đó là cùng vòng vốn. Tham chiếu `Its investors`
chỉ được nối ở câu kế tiếp. Câu có debt/grant/convertible chỉ được dùng cho nhánh này khi có cách
biểu diễn thích hợp khác; nhánh funding chung hiện từ chối. Model và normalize dùng chung helper.

`weconomy.derived.shared_investment_targets` nhận **claim đã qua kiểm định**, xuất quan hệ
`SHARES_INVESTMENT_TARGET` giữa hai nhà đầu tư kèm target ID/type, hai phía claim nguồn, URL,
evidence và offset. Không suy partnership hay cùng vòng vốn; không gộp mục tiêu chỉ trùng tên.
Các hàng suy ra lưu trong `data/analysis/derived`, tách khỏi graph normalize và không cộng vào
chỉ tiêu triple trực tiếp. Một mục tiêu có n nhà đầu tư có thể tạo n(n-1)/2 cặp, nên không dùng
các cặp này để tuyên bố đã tăng lượng bằng chứng độc lập.

Hàm projection hỗ trợ đầu vào PRODUCT/PROJECT đã được xác minh riêng. **Schema trích xuất hiện tại
chưa nhận PRODUCT/PROJECT và chưa trích quan hệ đầu tư tới các loại đó từ raw.** Không biến sản phẩm
thành ORG để lách hạn chế này. Khi mở rộng schema cần giữ các loại riêng, giữ liên kết ownership/product
khi nguồn chứng minh, cập nhật NER/constraints/domain/quality/export/import và kiểm tra trên dữ liệu thật.

Tương tự, điều tra, đóng điều tra, phê duyệt và kiện tụng là các sự kiện khác nhau. Raw cho thấy nhiều
cơ quan bị nhận thành ORG; kiểu GOV và các predicate còn thiếu cần được sửa có bằng chứng, không đổi
mọi tên chứa Department/Commission thành GOV hoặc ép `investigates` thành `SUED`.

## Chi tiết quy tắc dùng chung v17

Các nguyên tắc được tổng quát theo cấu trúc và vai trò, không theo danh sách tên công ty trong mẫu:

| Nhóm lỗi | Quy tắc | Hành vi khi chưa đủ bằng chứng |
|---|---|---|
| Nhóm chung bị coi là tên riêng | Tách named entity khỏi `the company`, VC/LP/GP dạng số nhiều, đại từ, vòng vốn, sản phẩm | Giữ raw prediction và lý do loại |
| Tên đầy đủ và tên rút gọn | Chỉ nối ORG có một tên mở rộng phù hợp trong chính bài đó | Không gộp khi có hai ứng viên; không nối qua bài khác |
| Công ty bị gán hành động của nhân sự | Xét chức danh ngay sau đúng lần xuất hiện của tên công ty | Không suy `công ty A sáng lập B` từ `B do founder của A sáng lập` |
| Vai trò đã kết thúc | Gắn former/ex-/cựu vào đúng cặp người–tổ chức và chức danh | Không xuất thành CEO hiện tại; chờ mô hình thời gian phù hợp |
| Sai loại hoặc chiều quan hệ | Bằng chứng từ vựng, phạm vi mệnh đề, loại endpoint; giữ kiểm tra dự định và phủ định | Không biến cạnh tranh, cùng đầu tư, dùng sản phẩm thành partnership/merger |
| Đúng chủ đề nhưng thiếu neo domain | Topic routing chỉ là bước sơ bộ; normalize cần bằng chứng riêng cho actor | Giữ review, không lấy tên viết hoa hay nguồn báo làm bằng chứng |

Kiểm tra vai trò lịch sử và gán hành động cho công ty thay cá nhân được áp dụng trong `NLP.relations`,
`extract_relations` và `supported_relation`; normalize dùng cùng helper. Quy tắc nối tên ORG dùng chung
giữa pipeline nạp bài và normalize. Bài mới lưu phép nối tên tại `silver/entity_resolutions.jsonl`;
model output và các quyết định loại vẫn được giữ tại `silver/model_predictions.jsonl`.

Đã kiểm tra đường URL bằng HTTP giả lập → lấy body → NLP → nối tên → lưu claim và offset.
Đây là kiểm tra chức năng; không phải bằng chứng precision trên URL thực chưa thấy.

Khi thu bổ sung, dùng catalog hiện có và `--allow-processing-upgrade` cho phiên bản xử lý mới.
Fingerprint/schema/alias gate vẫn được giữ; chỉ URL mới được phân tích bằng phiên bản mới.
Giới hạn vòng/candidate và điều kiện dừng của graph-cycle vẫn áp dụng. Không bỏ kiểm định
để chạy đủ số lượng; chỉ công bố khi bản normalize đạt ngưỡng và đã duyệt chất lượng phù hợp.

## Bổ sung kiểm định v16 sau duyệt mẫu

- Tên ORG rút gọn chỉ nối với một tên đầy đủ xuất hiện trong cùng bài, theo danh sách hậu tố giới hạn.
  Không nối giữa các bài, không dùng fuzzy matching, không gộp Salesforce với Salesforce Foundation.
  Nếu có hai tên mở rộng phù hợp thì giữ nguyên. Audit ghi từng phép nối ở `audit/name_resolutions.jsonl`.
- Mô tả đầu câu như `Fusion startup Inertia Enterprises` được tách khỏi tên. Tên có hậu tố
  `Enterprises/Materials` vẫn cần tham gia quan hệ đã qua kiểm định mới trở thành neo doanh nghiệp.
- `The company/The startup...` chỉ nối về tổ chức duy nhất trong câu ngay trước, không qua dòng trắng;
  chỉ nhận mô tả trực tiếp như `is a robotics startup`, không nhận `invested in a startup`.
- Nhận cách gọi trực tiếp `Tên, công ty con của...` trong tiếng Việt.
- Vai trò `former ... CEO` chuyển sang review để tránh biểu diễn thành chức vụ hiện tại.
- `VCs` là nhóm chung; công ty xuất hiện trước chức danh của một người không tự trở thành người sáng lập
  doanh nghiệp khác. Ví dụ `founded by Spotify co-founder Daniel Ek` không chứng minh Spotify là founder.
- Chưa khôi phục tự động các mục startup bị mất tiêu đề, tham chiếu nhiều câu tùy ý hoặc mọi bí danh thương hiệu.
  Các trường hợp đó cần giữ ranh giới nguồn tốt hơn hoặc duyệt riêng.

## Các bước kiểm định v15

1. **Kiểm tra tên.** Tên viết hoa là tín hiệu hỗ trợ. Cụm chung, đại từ, số tiền, vòng gọi vốn,
   sản phẩm và tên sự kiện bị đưa sang `review` dù có chữ hoa. `Series H` khác `Series X Capital`.
   `xAI`/`eBay` có chữ hoa bên trong vẫn hợp lệ; thương hiệu hoàn toàn viết thường cần alias đã duyệt.
   Bản ghi chưa đủ căn cứ được giữ trong audit và dữ liệu nguồn để xem lại.
   Với dữ liệu đã phân tích, ưu tiên mention/span và loại entity của đúng bài, thay vì tra một tên
   trong danh sách toàn corpus; một tên bị gán sai loại ở bài khác không được làm mất bản ghi đúng.
2. **Tách tên khỏi mô tả.** Ví dụ `AI agent startup Manus` được chuẩn hóa thành `Manus`, giữ tên và ID
   nguồn trong audit, cập nhật đầu mút claim và khử trùng theo ID mới. Cue `startup` sát tên vẫn là
   bằng chứng domain. Không dùng fuzzy matching để tự gộp các công ty có tên gần giống.
3. **Chứng minh domain cho từng actor.** Dùng alias được duyệt hoặc mô tả sát đúng actor trong cùng câu.
   Việc model gán `ORG`, tên có chữ hoa hay xuất hiện trong hai bài chưa đủ chứng minh đó là công ty.
   Tên có hậu tố tổ chức kinh doanh còn phải tham gia một quan hệ đã qua kiểm định.
4. **Chứng minh từng cạnh.** Kiểm tra loại hai đầu mút, tự nối, ID, câu bằng chứng và offset trong bài gốc.
   Từ/cấu trúc mô tả quan hệ phải phù hợp predicate và đúng hướng. Tham gia chương trình không phải
   `SUBSIDIARY_OF`; huy động một Series không phải đầu tư vào một công ty tên Series.
   Mua cổ phần không tự thành mua toàn công ty; cân nhắc sáp nhập không thành đã sáp nhập.
   Trường hợp cấu trúc chưa được hỗ trợ được ghi `unsupported_predicate_or_direction` để rà soát.
   Cấu trúc trực tiếp bị model bỏ sót có thể được phục hồi bằng rule trên các tên đã nhận dạng.
   Với tiếng Anh, tham chiếu `the round/this round` chỉ được nối khi có đúng một công ty đứng trước
   thông báo đã huy động một khoản vốn cụ thể theo Series/equity/seed round. Cửa sổ tối đa 4 câu tiếp theo
   và 1.800 ký tự; thông báo vòng khác thay anchor cũ. Danh sách phải nói rõ người dẫn vòng/nhà đầu tư.
   Actor chưa được NER nhận ra chỉ được thêm khi tên có hậu tố tổ chức rõ trong danh sách đầu tư đó;
   không tự gán mọi tên viết hoa thành ORG. Đơn vị `managed by` không trở thành nhà đầu tư.
5. **Xuất mạng từ claim được chấp nhận.** Tạo lại danh sách triple từ claim đã kiểm định, chuẩn hóa
   ID event/claim, loại trùng và chỉ giữ entity thực sự có cạnh. Không lấy lại cạnh cũ thiếu bằng chứng.

Không cần dùng `OTHER` làm điều kiện lọc trong v15. Các trường hợp ngoài loại actor của mạng có lý do
kiểm định riêng; đổi nhãn thành `OTHER` không chứng minh được chất lượng của quan hệ.

## Các tầng lưu trữ

| Tầng | Vị trí | Nội dung và cách dùng |
|---|---|---|
| Raw | `data/datasets/<dataset>/batches/<batch>/<run>/bronze/` | HTML/bytes gốc, checksum và metadata thu thập; các batch cũ tiếp tục dùng đường dẫn gốc |
| Phân tích | `<run>/silver/`, `<run>/gold/` | Bài đã tách thân, câu, mention, entity và claim; tên `gold` của lớp lưu trữ không có nghĩa là nhãn chuẩn do người gán |
| Dự đoán model | `<run>/silver/model_predictions.jsonl` | Output model trước lọc cùng các quyết định kiểm định cho bài mới; batch lịch sử không có file này không được tự chạy lại |
| Export phân tích | `data/analysis/exports/<snapshot>/` | Article, entity, sentence, mention và claim JSONL của catalog, dùng làm đầu vào normalize |
| Normalize | `data/normalized/<version>/` | Graph được chấp nhận, manifest có checksum đầu vào và `audit/` |
| Chỉ mục | `data/datasets/<dataset>/layers.json` | Tham chiếu các tầng, fingerprint của từng batch, lịch sử phiên bản và các export normalize |

Không di chuyển batch lịch sử vì replay, checksum và provenance đang tham chiếu các đường dẫn đó.
Catalog v15 có thể được tạo bằng SQLite backup từ catalog nguồn, tái sử dụng các kết quả đã commit
mà không chạy NLP lại. Catalog mới vẫn tham chiếu batch của nguồn: **cần giữ các batch nguồn**.

`audit/entities.jsonl` cho biết ID/tên gốc, ID/tên chuẩn, decision, reason, domain types và bằng chứng.
`audit/claims.jsonl` có hai tên actor, URL bài, câu bằng chứng và lý do giữ/đưa sang review.
Manifest thống kê các lý do, số entity đã gộp và claim trùng đã loại.
Export phân tích giữ toàn bộ entity đã phân tích, kể cả isolate; chỉ normalize mới chọn node có cạnh.
Các claim phục hồi ghi `recovery_method` và rule cụ thể. Một evidence window có thể gồm nhiều câu gốc;
ID, offset và mention đều tham chiếu đúng đoạn liên tục trong bài, không ghép văn bản ngoài nguồn.
Với export lịch sử chưa có `mentions.jsonl`, bộ lọc đọc `silver/mentions.parquet` trong run được tham chiếu
nếu còn file; không gọi lại model. Export mới chứa span ngay trong snapshot để kiểm định độc lập dễ hơn.

## Tối ưu phân tích ban đầu

- `collect` chỉ khám phá URL; catalog tải và phân tích bài một lần.
- Loại URL đã biết ngay khi khám phá, trước khi tính hạn mức và trước khi ngừng phân trang.
- So sánh nội dung/checksum và shingle với bài đã lưu trước NLP; bài trùng vẫn có raw để đối chiếu.
- Sàng lọc bài ngoài chủ đề trước NLP. Đây là bước routing rộng, không thay thế kiểm định actor/cạnh.
- Chỉ yêu cầu model các predicate có cue trong câu, rồi kiểm tra độc lập predicate và hướng quan hệ.
- Liên kết tham chiếu vòng vốn theo các điều kiện trên; đây là bước kiểm định/rule trên dữ liệu đã lưu,
  không phải một lượt gọi lại model trên toàn bộ bài cũ.
- Prompt phân biệt người, tổ chức, địa điểm và chính phủ/cơ quan quản lý; các span sai vẫn nằm trong
  archive dự đoán để xem lại, không phải chạy model chỉ để biết nó đã dự đoán gì.

## Chạy kiểm định trên dữ liệu đã có

```powershell
uv run --no-sync weconomy filter-domain `
  data/exports/international-business-gliner-v2-full-20261108T065138-ec4a44 `
  --output data/normalized/international-business-v15-manual-check
```

Đầu ra phải là thư mục chưa tồn tại. Lệnh này đọc kết quả phân tích cũ; không crawl và không gọi model.
Trạng thái `targets_met` trong manifest phản ánh chỉ tiêu normalize, không kế thừa mục tiêu số bài thô.

## Bổ sung khi thiếu chỉ tiêu

```powershell
uv run --no-sync weconomy graph-cycle `
  --dataset data/datasets/international-business-verified-v15 `
  --source-dataset data/datasets/international-business-gliner-v2 `
  --allow-processing-upgrade `
  --nodes 2000 --relations 5000 --relation-types 11 `
  --max-candidates 1000 --max-rounds 3 --batch-size 20
```

Lần đầu sao chép catalog đã commit; các lần sau resume catalog đích. Mỗi vòng tìm URL chưa có,
phân tích bài mới rồi kiểm tra lại mạng normalize. `graph-cycle --max-candidates` là ngân sách **attempt
mới của lần gọi**, phân bổ qua tối đa `max-rounds`; nó không bảo đảm thu được chừng ấy bài hợp lệ.
Riêng `collect-dataset --max-candidates` tiếp tục là trần attempt tích lũy của catalog.

Các điểm dừng: đủ chỉ tiêu, hết ngân sách, hết số vòng, không có URL mới, lỗi khám phá nguồn hoặc
không có tiến triển thu thập. Nếu nguồn bị lỗi, báo lỗi thay vì ghi nhận đã đủ dữ liệu.
Chạy lại cùng lệnh để bổ sung tiếp; URL/thân bài đã có không được đưa lại vào NLP.

Khi code/model thay đổi, resume mặc định vẫn từ chối fingerprint khác. Cờ
`--allow-processing-upgrade` cho phép ghi phiên bản mới **chỉ cho bài mới**, sau khi kiểm tra schema
và alias còn tương thích. Fingerprint batch cũ và chuyển tiếp phiên bản được lưu; thay alias làm đổi
định danh cần migration riêng. Không dùng cờ này để phát lại bài cũ.

Graph-cycle mặc định không import Neo4j. `--publish` là thao tác riêng và chỉ chạy khi đủ các ngưỡng
normalize; lượt kiểm định không sử dụng cờ này. Không tự gửi dữ liệu lên Aura/Hugging Face.

## Đánh giá chất lượng

Kiểm tra cấu trúc, rule và đọc mẫu giúp tìm lỗi nhưng chưa chứng minh precision trên 90%.
Cần gán nhãn độc lập trên mẫu phân tầng theo predicate, nguồn, ngôn ngữ và quyết định giữ/review;
đo precision của cạnh giữ lại và tỷ lệ loại nhầm trên phần review. Giữ một tập chưa dùng để chỉnh rule.
Chỉ báo đạt yêu cầu số lượng khi manifest normalize đủ cả ba ngưỡng; không nới tiêu chuẩn để điền số.
