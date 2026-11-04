# Tài liệu sử dụng và phát triển

Người mới nên đọc theo thứ tự:

1. [Trạng thái hiện tại và bàn giao](STATUS.md): đã chạy gì, bằng chứng, giới hạn và những việc chưa làm.
2. [README dự án](../README.md): phạm vi đề tài, trạng thái collection mới nhất, cài đặt và quickstart dataset có thể tiếp tục.
3. [Thu thập dataset](collection.md): catalog tăng dần, resume, budget ứng viên và JSONL export.
4. [Toàn văn](FULLTEXT.md): `body_checked`, cách ly bài và giới hạn phạm vi HTML.
5. [Schema](SCHEMA.md): bronze/silver/gold, ID, provenance, event và graph.
6. [Gán nhãn](ANNOTATION.md): quy ước nhãn, đánh giá và cách diễn giải P/R/F1.
7. [Kiến trúc](ARCHITECTURE.md): luồng xử lý, ranh giới module và đường mở rộng.
8. [Roadmap](ROADMAP.md): checklist nghiệm thu và công việc các giai đoạn.
9. [Hugging Face](HUGGINGFACE.md): kết nối, chia sẻ private qua Organization, upload/download corpus theo commit.
10. [Các lệnh CLI bổ sung](commands.md): run legacy, fixture offline, reprocess, gán nhãn, Neo4j và Docker.

[gds.cypher](gds.cypher) là template chưa nghiệm thu, không phải bằng chứng GDS đã chạy.
Số liệu trong báo cáo pilot là lịch sử của từng lần chạy; đọc STATUS và manifest corpus tương ứng
trước khi dùng số liệu mới. Corpus local trong `data/` không đi kèm khi clone Git.
