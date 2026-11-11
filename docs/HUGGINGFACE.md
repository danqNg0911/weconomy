# Chia sẻ corpus qua Hugging Face Dataset Hub

Luồng bổ sung ngày 01/11/2026: **run local → validate → ZIP + SHA256 → private dataset repo →
download theo commit → kiểm tra checksum + validate → run local trên máy thành viên**.
Không thay đổi pipeline thu thập hoặc chuyển Neo4j lên cloud.

## Trạng thái triển khai

- [x] CLI `hf-push`, có `--dry-run` không gọi mạng hoặc yêu cầu token.
- [x] CLI `hf-pull`, nhận commit SHA và không ghi đè run local đã có.
- [x] Upload chỉ nhận run `completed`, không rỗng, qua validate và khớp counts trong manifest.
- [x] Từ chối repo public; không có tùy chọn tự chuyển repo thành public.
- [x] Ghi ZIP và metadata trong một commit, kiểm tra parent commit để tránh ghi đè cập nhật đồng thời.
- [x] Từ chối run ID đã tồn tại trên nhánh mặc định; không cập nhật run cũ tại chỗ.
- [x] Download ghim một commit cho cả hai file, kiểm tra archive/file SHA256, kích thước và dataset.
- [x] Giải nén vào staging, chặn path không hợp lệ; chỉ công bố thư mục run khi validate thành công.
- [ ] Chưa nghiệm thu upload/download với tài khoản và dataset repo thật của nhóm.

Bằng chứng local ngày 01/11/2026: **139 tests passed**, Ruff/lock check/diff check qua.
Dry-run corpus `20261031T101555-c6e4bee3` gồm 91 file, ZIP 12.802.611 bytes (~12,21 MiB).
Đóng gói và phục hồi offline cho kết quả 7 bảng giống bản gốc, validator hợp lệ:
[kiểm tra roundtrip](../data/hf-local-roundtrip-20261101.json). Link này chỉ có trên máy đã chạy,
không đi kèm Git. Không gọi mạng trong kiểm tra này. Build Docker cho bản HF chưa nghiệm thu vì
Docker Engine không khả dụng lúc kiểm tra ngày 01/11; không suy ra đã thử HF trên image cũ.

`hf-push` là lệnh gửi dữ liệu thật nếu không có `--dry-run`. Việc cài tính năng không tự đồng bộ bất kỳ
dữ liệu nào. Repo private là kiểm soát truy cập, không cấp thêm quyền chia sẻ nội dung báo.

## Chia sẻ private cho thành viên

Nên tạo **Organization của nhóm**, ví dụ tên minh họa `your-team`, rồi tạo dataset private
`your-team/weconomy-corpus`. Tên trong ví dụ phải thay bằng namespace/repo thật.
Mời tài khoản Hugging Face của từng người vào Organization:

| Vai trò | Dùng cho |
|---|---|
| `read` | Người chỉ tải và đọc corpus |
| `write` | Người xuất bản run mới; quyền này rộng hơn chỉ upload một file |
| `admin` | Người quản lý thành viên và cấu hình Organization |

Mỗi thành viên dùng tài khoản và token riêng. Người tải cần token có quyền đọc repo;
người upload cần quyền ghi. Token không thể cấp vượt quyền tài khoản trong Organization.
Repo dưới tài khoản cá nhân không phải cách bàn giao quyền ghi cho cả nhóm; chọn namespace
Organization ngay từ đầu. Phân quyền chi tiết hơn bằng Resource Groups thuộc các gói trả phí.
Xem [phân quyền Organization](https://huggingface.co/docs/hub/organizations-security).

## Cài đặt và xác thực trên Windows

Từ thư mục gốc dự án:

```powershell
uv sync --locked --extra dev --extra nlp --extra hub
uv run --no-sync hf auth login
```

Nếu chỉ upload/download và validate Parquet, không chạy NER, có thể chỉ cài `--extra hub`.
Đăng nhập ở prompt của CLI; không đặt token trong lệnh, source code, file config được commit hoặc chat.
SDK cũng đọc `HF_TOKEN` từ biến môi trường của tiến trình. Tool không tự đọc `HF_TOKEN` từ `.env`;
chọn `hf auth login` để tránh phải tự nạp biến này. Các lệnh dưới đây dùng `--no-sync` để giữ model riêng.

## Kiểm tra gói rồi upload

```powershell
$run = 'data/runs/20261031T101555-c6e4bee3'
$repo = 'your-team/weconomy-corpus'

# Chỉ kiểm tra local và hiển thị danh sách file/counts/dung lượng/hash, không gọi Hugging Face.
uv run --no-sync weconomy hf-push $run --repo $repo --dry-run

# Lệnh này mới gửi dữ liệu lên repo.
uv run --no-sync weconomy hf-push $run --repo $repo
```

Run ID là tên thư mục run, chỉ nhận chữ, số, `-`, `_`. Repo ID bắt buộc dạng `namespace/name`.
Nếu repo chưa tồn tại, tool yêu cầu API tạo repo **private**; tài khoản phải có quyền tạo trong namespace.
Nếu repo đã tồn tại, tool kiểm tra private trước khi gửi file, không thay đổi visibility.
Nếu không thấy repo do thiếu quyền, kiểm tra quyền/token trước khi thử lại.
JSON kết quả upload gồm `repo_id`, `run_id`, `commit`, URL commit, counts và SHA256 archive.
Lưu **commit SHA** đó để các thành viên lấy cùng phiên bản.

Mỗi lần upload thêm hai file, không ghi đè cây dữ liệu các run khác:

```text
runs/<run_id>.zip    payload phục hồi run
runs/<run_id>.json   inventory, kích thước và SHA256 archive/từng file, counts, schema version
```

ZIP chỉ chứa 7 bảng Parquet bronze/silver/gold, HTML được bronze tham chiếu, `manifest.json`
và snapshot `config.yaml/sources.yaml/aliases.yaml`. Có cả bytes HTML trong bronze và file HTML riêng
để phục hồi nguyên run. Không quét toàn bộ `data/`, không đưa `.env`, model cache, Docker volume,
file JSONL xuất thêm hoặc nhãn reviewer vào gói. Các bảng Parquet vẫn chứa toàn văn/evidence;
kiểm tra phạm vi được phép chia sẻ trước khi chạy upload thật.

## Thành viên tải đúng phiên bản

Sau khi được cấp quyền và đăng nhập tài khoản riêng:

```powershell
$repo = 'your-team/weconomy-corpus'
$runId = '20261031T101555-c6e4bee3'
$commit = 'THAY_BANG_COMMIT_SHA_TRA_VE_KHI_UPLOAD'
uv run --no-sync weconomy hf-pull --repo $repo --run-id $runId --revision $commit --output data/runs
uv run --no-sync weconomy validate "data/runs/$runId"

# Có thể chạy NLP lại offline với config/môi trường của máy này, tạo một run mới.
uv run --no-sync weconomy run --from-run "data/runs/$runId" --ner models
```

Không truyền `--revision` thì tool lấy `main`, sau đó tự ghim SHA của nhánh một lần cho cả hai file.
Ghim SHA tường minh vẫn là cách tái lập được khuyến nghị. Nếu run local đã tồn tại, chọn thư mục
cha khác, ví dụ `--output data/from-hf`, không cần xóa bản local cũ.
Snapshot config trong bundle giữ nguyên đường dẫn từ máy gốc để truy vết; khi replay, dùng config
ở checkout hiện tại của bạn, không mặc định đưa snapshot config có đường dẫn máy khác vào `--config`.

## Giới hạn và xử lý lỗi

- Giới hạn 1 GiB cho ZIP và tổng dung lượng giải nén; metadata tối đa 1 MiB khi tải.
- Mỗi run là snapshot đầy đủ; chưa có đồng bộ tăng dần/dedup giữa các ZIP, scheduler hoặc resume riêng
  ở cấp ứng dụng. SDK quản lý phần truyền tải; nếu mất phản hồi sau commit, kiểm tra repo trước khi retry.
- Run đã có từ xa bị từ chối. Nếu lần trước thành công nhưng CLI mất kết nối, dùng `hf-pull` theo commit
  đã có; không sửa/xóa run đó để ép upload qua. Nếu nhánh bị người khác sửa đồng thời, kiểm tra remote rồi thử lại.
- ZIP/checksum/dataset lỗi: không xuất bản thư mục đích; staging được dọn. Cache download tạm cũng không
  trộn vào thư mục run. SHA256 phát hiện lỗi toàn vẹn, không thay thế việc tin cậy chủ repo và commit đã chọn.
- Lệnh không giữ khóa nhiều tiến trình trên thư mục đích; tránh chạy nhiều download cùng run/output đồng thời.
- Docker image core hiện không cài extra `hub`; dùng môi trường host có extra này cho upload/download.
- Đây là gói snapshot ZIP để pipeline dùng lại, chưa cấu hình Dataset Viewer xem các bảng trên web,
  chưa đồng bộ nhãn duyệt hoặc Neo4j. Người dùng vẫn có thể dùng `export` sau khi pull.

Tài liệu SDK: [upload](https://huggingface.co/docs/huggingface_hub/guides/upload),
[download theo revision](https://huggingface.co/docs/huggingface_hub/guides/download).
# Đồng bộ dữ liệu lên Hugging Face

Đích: `hf://buckets/weconomy235/weconomy` (Storage Bucket, không phải Dataset repository).
CLI chạy riêng, không thay đổi dependencies của pipeline.

```powershell
# Chạy ở thư mục gốc repo. Chỉ cần cài hub extra một lần nếu `uv run hf` chưa có.
uv sync --locked --extra hub
uv run --no-sync hf auth login
uv run --no-sync hf auth whoami
uv run --no-sync hf sync ./data hf://buckets/weconomy235/weconomy --exclude '*.writer.lock' --dry-run
uv run --no-sync hf sync ./data hf://buckets/weconomy235/weconomy --exclude '*.writer.lock'
```

Chỉ đồng bộ thư mục `data`, gồm HTML, Parquet, catalog, export JSONL và manifests; cấu trúc `datasets/<dataset-id>`, `exports/<dataset-id>` và `runs/<run-id>` được giữ trên bucket. File khóa tạm `.writer.lock` bị loại trừ.
File `.env` của dự án và Docker volume Neo4j không nằm trong thư mục này.
Việc sync không tự thu thập thêm bài, chạy NLP hay import Neo4j.

Sau mỗi lần thu thập/replay/export, chạy lại lệnh `hf sync` để thêm/cập nhật file trên cùng bucket. Mặc định không xóa file từ xa.
Đăng nhập trên máy bằng CLI; không đưa token vào source code hoặc gửi token qua chat.

Tài liệu CLI: https://huggingface.co/docs/huggingface_hub/guides/cli

Muốn chỉ đẩy run mới:

```
$runId = Split-Path $run -Leaf
& $hf sync $run "hf://buckets/weconomy235/weconomy/runs/$runId"
```
