# Đồng bộ dữ liệu lên Hugging Face

Đích: `hf://buckets/weconomy235/weconomy` (Storage Bucket, không phải Dataset repository).
CLI chạy riêng, không thay đổi dependencies của pipeline.

```powershell
cd F:\Project\ptmxh
powershell -ExecutionPolicy ByPass -c "irm https://hf.co/cli/install.ps1 | iex"
# Mở terminal mới sau khi cài để nhận PATH.
hf auth login
hf auth whoami
hf sync ./data hf://buckets/weconomy235/weconomy --dry-run
hf sync ./data hf://buckets/weconomy235/weconomy
```

Chỉ đồng bộ thư mục `data`, gồm HTML, Parquet và manifests của các run.
File `.env` của dự án và Docker volume Neo4j không nằm trong thư mục này.
Việc sync không tự thu thập thêm bài, chạy NLP hay import Neo4j.

Sau mỗi lần thu thập/replay, chạy lại `hf sync` để cập nhật bucket.
Đăng nhập trên máy bằng CLI; không đưa token vào source code hoặc gửi token qua chat.

Tài liệu CLI: https://huggingface.co/docs/huggingface_hub/guides/cli

Muốn chỉ đẩy run mới:

```
$runId = Split-Path $run -Leaf
& $hf sync $run "hf://buckets/weconomy235/weconomy/runs/$runId"
```