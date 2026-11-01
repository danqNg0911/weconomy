# IMPLEMENTATION PLAN — News Collection Pipeline

## 1. Mục tiêu

Xây dựng hệ thống thu thập bài báo tự động bằng Python, phục vụ đề tài:

**Mạng lưới Tập đoàn Đa quốc gia, Tỷ phú và Quỹ Đầu tư Quốc tế (Báo Kinh tế Thế giới).**

Dữ liệu sẽ được sử dụng trong các giai đoạn sau để thực hiện:

- Named Entity Recognition (NER).
- Entity Linking và Entity Resolution.
- Relation Extraction.
- Event Extraction.
- Xây dựng Knowledge Graph bằng Neo4j.

**Phạm vi của implementation này chỉ gồm discovery, download, extraction, validation, deduplication, storage và reporting.**

Không triển khai NLP, LLM agents, Neo4j, giao diện web hoặc hệ thống phân tán trong giai đoạn này.

### Mục tiêu vận hành

- Thu thập từ 5 nguồn báo.
- Hỗ trợ cả tiếng Việt và tiếng Anh.
- Sử dụng RSS Feed và Sitemap XML để phát hiện URL.
- Thu thập được cả dữ liệu lịch sử nếu sitemap cung cấp.
- Có khả năng chạy lại mà không xử lý trùng các bài đã hoàn thành.
- Lưu metadata, nội dung bài báo và nguồn gốc dữ liệu.
- Có thể dừng và tiếp tục sau khi chương trình gặp lỗi.
- Có CLI để chạy theo nguồn, theo phương pháp và theo thời gian.
- Hỗ trợ mở rộng tới hàng nghìn bài báo.

**Mục tiêu hiện tại (điều chỉnh): kiểm tra khả năng crawl của từng nguồn, tối đa 10 bài hợp lệ/nguồn, tối đa 50 bài cho 5 nguồn.** Không yêu cầu đủ 50 bài nếu có nguồn bị chặn hoặc thiếu endpoint công khai.

Giới hạn 10 bài tính trên tổng số bài đã lưu của mỗi nguồn trong cùng database, kể cả khi chạy lại. Mỗi lần chạy thử tối đa 30 URL/nguồn; bài lỗi, bị hạn chế hoặc trùng không tính là bài hợp lệ. Không lọc bỏ bài theo chủ đề trong pilot; chỉ ghi điểm relevance.

Các yêu cầu quy mô lớn, crawl lịch sử theo thời gian, checkpoint sitemap định kỳ và lưu raw HTML được hoãn. Bản pilot dùng SQLite làm nguồn dữ liệu chính, tái tạo JSONL nguyên tử để phục hồi sau gián đoạn; triển khai các nhóm chức năng bằng module gọn thay vì nhiều package nhỏ. Xem `docs/IMPLEMENTATION.md` và `docs/PILOT_REPORT.md` để biết phạm vi thực tế và kết quả.

---

## 2. Nguồn dữ liệu

| Source ID | Website | Discovery methods | Ngôn ngữ |
|---|---|---|---|
| `vnexpress` | https://vnexpress.net | RSS, Sitemap XML | vi |
| `tuoitre` | https://tuoitre.vn | RSS, Sitemap XML | vi |
| `reuters` | https://www.reuters.com | RSS, Sitemap XML nếu khả dụng | en |
| `bloomberg` | https://www.bloomberg.com | RSS, Sitemap XML nếu khả dụng | en |
| `techcrunch` | https://techcrunch.com | RSS, Sitemap XML | en |

**Quan trọng:**

Không hardcode các URL RSS/sitemap chưa được xác minh.

Codex phải xây dựng bước kiểm tra endpoint cho từng nguồn:

1. Kiểm tra `robots.txt` và các điều khoản truy cập liên quan.
2. Tìm RSS URL hoặc sitemap URL công khai.
3. Kiểm tra HTTP status, content type và XML hợp lệ.
4. Xác định endpoint có thực sự chứa URL bài báo không.
5. Lưu endpoint đã xác minh vào `configs/sources.yaml`.
6. Ghi rõ trạng thái `available`, `unavailable`, `restricted` hoặc `unknown`.

Nếu một nguồn không có RSS hoặc sitemap khả dụng thì ghi nhận trong báo cáo, không tự động chuyển sang scraping tìm kiếm hay bypass.

Đối với Reuters và Bloomberg, chỉ trích xuất nội dung được phép truy cập. Nếu bài báo bị hạn chế, lưu metadata được phép sử dụng và trạng thái `restricted`, không coi đó là một bài báo có nội dung đầy đủ.

---

## 3. Technology Stack

Sử dụng Python 3.11+.

Các thư viện chính:

| Library | Chức năng |
|---|---|
| `httpx` | HTTP client, timeout, retry orchestration |
| `feedparser` | Đọc RSS và Atom |
| `lxml` | Parse XML sitemap |
| `beautifulsoup4` | Phân tích HTML, metadata |
| `trafilatura` | Trích xuất nội dung chính |
| `pydantic` | Schema và validation |
| `PyYAML` | Đọc cấu hình |
| `typer` | CLI |
| `rich` | Logging và thống kê CLI |
| `pytest` | Unit/integration tests |
| `pytest-httpx` | Mock HTTP requests |

Sử dụng Python standard library cho SQLite, JSONL, hashing, datetime, URL normalization và logging khi phù hợp.

Không dùng Scrapy, Selenium hoặc Playwright trong phiên bản đầu tiên.

---

## 4. Project Structure

```text
news-collection/
├── README.md
├── PLAN.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── configs/
│   ├── sources.yaml
│   ├── keywords.yaml
│   └── settings.yaml
│
├── data/
│   ├── raw/
│   │   ├── vnexpress/
│   │   ├── tuoitre/
│   │   ├── reuters/
│   │   ├── bloomberg/
│   │   └── techcrunch/
│   ├── html/
│   ├── exports/
│   ├── reports/
│   └── crawler.db
│
├── src/
│   └── news_collector/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── models.py
│       │
│       ├── discovery/
│       │   ├── rss.py
│       │   ├── sitemap.py
│       │   ├── endpoint_validator.py
│       │   └── url_filter.py
│       │
│       ├── fetching/
│       │   ├── client.py
│       │   ├── rate_limiter.py
│       │   └── robots.py
│       │
│       ├── extraction/
│       │   ├── extractor.py
│       │   ├── metadata.py
│       │   └── site_rules.py
│       │
│       ├── processing/
│       │   ├── normalize.py
│       │   ├── deduplicate.py
│       │   ├── relevance.py
│       │   └── validate.py
│       │
│       ├── storage/
│       │   ├── database.py
│       │   ├── repositories.py
│       │   └── jsonl.py
│       │
│       └── reporting/
│           └── statistics.py
│
└── tests/
    ├── fixtures/
    ├── test_rss.py
    ├── test_sitemap.py
    ├── test_extractor.py
    ├── test_deduplicate.py
    ├── test_storage.py
    └── test_pipeline.py
```

---

## 5. Data Schema

### 5.1. Article Schema

Mỗi bài báo hợp lệ phải có cấu trúc:

```json
{
  "article_id": "string",
  "source": "vnexpress",
  "url": "string",
  "canonical_url": "string",
  "title": "string",
  "description": "string|null",
  "authors": [],
  "published_at": "ISO8601|null",
  "updated_at": "ISO8601|null",
  "collected_at": "ISO8601",
  "language": "vi",
  "category": "string|null",
  "tags": [],
  "content": "string",
  "word_count": 0,
  "content_hash": "string",
  "discovery_method": "rss",
  "discovery_endpoint": "string",
  "extraction_method": "trafilatura",
  "extraction_version": "1.0",
  "http_status": 200,
  "crawl_status": "success",
  "relevance_status": "pending",
  "duplicate_of": null,
  "raw_file_path": null
}
```

### Quy tắc dữ liệu

- `article_id`: ID ổn định, sinh từ canonical URL đã chuẩn hóa.
- `content_hash`: SHA-256 của nội dung đã chuẩn hóa.
- `published_at`: giữ timezone nếu có, chuẩn hóa về UTC khi lưu.
- Không tự suy đoán ngày xuất bản khi thiếu.
- `content`: chỉ chứa nội dung chính, không gồm menu, quảng cáo, footer hoặc bình luận.
- `authors`: danh sách tác giả, có thể rỗng.
- `discovery_method`: `rss` hoặc `sitemap`.
- Nếu cùng một bài được tìm thấy từ nhiều endpoint, giữ đầy đủ nguồn discovery trong SQLite.
- Bài thiếu nội dung không được đánh dấu `success`.
- Metadata không chắc chắn phải để `null`, không tạo dữ liệu giả.

### 5.2. SQLite Tables

Thiết kế tối thiểu gồm:

**`sources`**

- `source_id`
- `base_url`
- `language`
- `enabled`
- `created_at`

**`discovery_endpoints`**

- `endpoint_id`
- `source_id`
- `url`
- `method`
- `status`
- `last_checked_at`
- `last_success_at`
- `last_error`

**`url_queue`**

- `url_id`
- `normalized_url`
- `source_id`
- `status`
- `priority`
- `discovered_at`
- `last_attempt_at`
- `retry_count`
- `next_retry_at`
- `http_status`
- `last_error`

Đặt unique constraint trên `normalized_url`.

**`url_discoveries`**

- `url_id`
- `endpoint_id`
- `discovered_at`

Dùng để ghi nhận một URL xuất hiện trong nhiều RSS hoặc sitemap mà không tạo nhiều công việc tải xuống.

**`articles`**

- `article_id`
- `url_id`
- `canonical_url`
- `source_id`
- `title`
- `published_at`
- `language`
- `content_hash`
- `word_count`
- `jsonl_path`
- `jsonl_offset`
- `raw_file_path`
- `relevance_status`
- `created_at`

Đặt unique constraint trên `canonical_url`.

**`crawl_runs`**

- `run_id`
- `started_at`
- `finished_at`
- `status`
- `sources`
- `urls_discovered`
- `urls_processed`
- `articles_saved`
- `articles_failed`

**`crawl_errors`**

- `error_id`
- `run_id`
- `url`
- `error_type`
- `message`
- `created_at`

Tạo index trên các trường dùng thường xuyên: `source_id`, `status`, `published_at`, `content_hash`.

Sử dụng SQLite WAL mode và một cơ chế ghi tuần tự để hạn chế lỗi khóa database.

---

## 6. RSS Discovery

Module: `discovery/rss.py`

### Chức năng

1. Đọc danh sách RSS endpoint từ config.
2. Gửi HTTP request với timeout và User-Agent định danh.
3. Parse RSS hoặc Atom.
4. Lấy URL, title, publication date và category nếu có.
5. Chuẩn hóa URL.
6. Kiểm tra domain và loại trang không phải bài báo.
7. Upsert vào `url_queue`.
8. Lưu liên kết giữa URL và endpoint trong `url_discoveries`.

### Yêu cầu

- Hỗ trợ RSS 2.0 và Atom.
- Không giả định RSS chứa toàn bộ nội dung bài báo.
- Không sử dụng ngày của feed làm ngày xuất bản bài báo nếu thiếu ngày của entry.
- Không tải lại URL đã hoàn thành nếu không có chế độ refresh.
- Ghi log số entry đọc được, số URL mới và số URL trùng.
- Nếu RSS lỗi, chỉ đánh dấu lỗi endpoint, không làm dừng các nguồn khác.

---

## 7. Sitemap Discovery

Module: `discovery/sitemap.py`

### Chức năng

1. Đọc sitemap URL đã cấu hình.
2. Parse XML.
3. Hỗ trợ `sitemapindex` và `urlset`.
4. Duyệt sitemap con theo giới hạn cấu hình.
5. Hỗ trợ sitemap XML nén gzip.
6. Trích xuất URL và `lastmod` nếu có.
7. Lọc URL bài báo theo domain và quy tắc nguồn.
8. Upsert URL vào SQLite.

### Yêu cầu

- Có giới hạn độ sâu sitemap.
- Có giới hạn tổng số sitemap và URL mỗi lần chạy.
- Có cơ chế tránh duyệt lặp sitemap.
- Không coi `lastmod` là `published_at`.
- Có thể lọc theo thời gian nếu sitemap cung cấp metadata phù hợp.
- Không giả định URL có ngày trong path thì đó là ngày xuất bản.
- Có checkpoint để tránh xử lý lại toàn bộ sitemap trong các lần chạy định kỳ khi không cần thiết.
- Lưu trạng thái sitemap đã kiểm tra.

---

## 8. Article Fetching

Module: `fetching/client.py`

Sử dụng `httpx.AsyncClient` để tải bài báo.

### Cấu hình mặc định

```yaml
http:
  timeout_seconds: 20
  max_retries: 3
  max_connections: 10
  max_connections_per_domain: 2
  user_agent: "AcademicNewsCollector/0.1 (contact: configure-before-running)"

crawl:
  min_delay_per_domain_seconds: 3
  max_urls_per_run: 500
  respect_robots_txt: true
  store_raw_html: false
```

Các giá trị là mặc định ban đầu, phải giảm tốc độ hoặc dừng khi chính sách nguồn yêu cầu.

### Xử lý HTTP

- `200`: thử bóc tách.
- `301/302`: theo redirect hợp lệ và kiểm tra lại domain.
- `403`: đánh dấu `restricted`, không cố bypass.
- `404/410`: đánh dấu lỗi không thể phục hồi.
- `429`: tuân thủ `Retry-After`, tạm dừng nguồn.
- `5xx`: retry với exponential backoff có giới hạn.
- Timeout/network error: retry có giới hạn.
- HTML trả về là trang yêu cầu đăng nhập, CAPTCHA hoặc paywall: đánh dấu `restricted`.

Không sử dụng proxy rotation, CAPTCHA solver, giả lập đăng nhập hoặc cơ chế vượt hạn chế truy cập.

---

## 9. Article Extraction

Module: `extraction/extractor.py`

### Extraction strategy

Thực hiện theo thứ tự:

1. Parse metadata HTML và JSON-LD `NewsArticle`/`Article` nếu có.
2. Dùng `trafilatura` để lấy nội dung chính.
3. Dùng `BeautifulSoup` để lấy các metadata còn thiếu.
4. Áp dụng site-specific extraction rules nếu parser chung không đạt yêu cầu.
5. Chuẩn hóa kết quả về một Pydantic schema thống nhất.

### Metadata cần trích xuất

- Title.
- Description/sapo.
- Author.
- Published date.
- Updated date.
- Canonical URL.
- Language.
- Category.
- Tags.
- Main content.

### Site-specific rules

Có thể viết rule riêng cho:

- VnExpress.
- Tuổi Trẻ.
- Reuters.
- Bloomberg.
- TechCrunch.

Không hardcode giả định rằng cấu trúc HTML của một website sẽ không thay đổi.

Nếu extraction thất bại, lưu loại lỗi và cho phép thử lại sau khi sửa parser.

---

## 10. Validation và Deduplication

### 10.1. URL deduplication

- Chuẩn hóa scheme và hostname.
- Loại bỏ fragment.
- Loại bỏ tracking parameters đã biết như `utm_*`.
- Giữ lại query parameters có ý nghĩa định danh bài viết.
- Ưu tiên canonical URL hợp lệ.
- Không gộp hai URL khác nhau chỉ vì tiêu đề giống nhau.

### 10.2. Content deduplication

Sử dụng SHA-256 trên nội dung đã chuẩn hóa để tìm các bản trùng hoàn toàn.

Nếu có bài trùng:

- Không tạo thêm bài báo chính.
- Ghi `duplicate_of`.
- Giữ thông tin URL nguồn và provenance.
- Không tự động xóa dữ liệu đã thu thập.

### 10.3. Validation

Một bài được đánh dấu `success` khi:

- Có URL hợp lệ.
- Có source.
- Có title.
- Có main content.
- Nội dung vượt ngưỡng độ dài tối thiểu có thể cấu hình.
- Không phải trang lỗi, CAPTCHA, trang chủ hoặc trang đăng nhập.

Nếu thiếu `published_at`, đánh dấu `missing_metadata` hoặc lưu cờ chất lượng, thay vì bịa ngày.

Phân biệt rõ:

- `success`: lấy được nội dung hợp lệ.
- `duplicate`: bài trùng.
- `restricted`: bị hạn chế truy cập.
- `extraction_failed`: tải được nhưng không bóc tách được.
- `fetch_failed`: không tải được.
- `irrelevant`: bài đã được xác định không phù hợp.
- `pending`: chưa xử lý.

---

## 11. Topic Relevance Filtering

Module: `processing/relevance.py`

Ở giai đoạn 1, chỉ triển khai **keyword-based relevance filtering**, không dùng LLM.

Nhóm từ khóa:

- Đầu tư: investment, funding, venture capital, rót vốn, gọi vốn.
- M&A: acquisition, merger, takeover, mua lại, sáp nhập.
- Lãnh đạo: CEO, founder, chairman, nhà sáng lập.
- Sở hữu: shareholder, stake, subsidiary, cổ phần.
- Pháp lý: antitrust, lawsuit, investigation, chống độc quyền.
- Chuỗi cung ứng: supplier, partnership, supply chain.
- Chính phủ/chính sách: sanctions, tariffs, regulation, cấm vận, áp thuế.

### Cách thực hiện

- Đọc keywords từ `configs/keywords.yaml`.
- Tính điểm dựa trên title, description và content.
- Ưu tiên title và description.
- Ghi `relevance_score`.
- Ghi `matched_keywords`.
- Gán `relevance_status`: `relevant`, `irrelevant` hoặc `review`.

**Không xóa bài chỉ vì không khớp từ khóa.** Giữ khả năng đánh giá lại bằng NLP ở giai đoạn tiếp theo.

---

## 12. Storage Strategy

### 12.1. SQLite

Lưu:

- Source và discovery endpoint.
- URL queue.
- Crawl status.
- Retry/error logs.
- Metadata và vị trí bản ghi bài báo.
- Thống kê crawl.

### 12.2. JSONL

Lưu nội dung đầy đủ của từng bài báo đã trích xuất thành công.

Ví dụ:

```text
data/raw/vnexpress/2026-10.jsonl
data/raw/tuoitre/2026-10.jsonl
data/raw/reuters/2026-10.jsonl
```

Mỗi dòng là một JSON object.

Đảm bảo:

- UTF-8.
- Có thể append.
- Ghi an toàn khi chương trình bị dừng.
- Có thể truy xuất bản ghi từ SQLite.
- Không ghi trùng bài khi retry.
- Có cơ chế phục hồi nếu SQLite và JSONL bị lệch trạng thái sau crash.

Có thể dùng một writer duy nhất và lưu offset theo byte. Khi khởi động, kiểm tra và khôi phục các bản ghi ghi dở.

### 12.3. Raw HTML

Mặc định `store_raw_html = false`.

Nếu nguồn cho phép lưu HTML:

- Lưu HTML gốc dạng nén.
- Đặt tên bằng article ID hoặc hash.
- Ghi đường dẫn vào SQLite.

Không lưu HTML của các nguồn hạn chế khi không được phép.

### 12.4. Neo4j

**Không ghi dữ liệu vào Neo4j trong giai đoạn này.**

Chỉ đảm bảo dữ liệu có:

- Article ID ổn định.
- Canonical URL.
- Source.
- Publication date.
- Main content.

Đây là dữ liệu đầu vào cho pipeline NLP và xây dựng graph sau này.

---

## 13. CLI Requirements

Sử dụng Typer.

Các lệnh cần triển khai:

```bash
# Khởi tạo database
python -m news_collector.cli init-db

# Kiểm tra RSS và sitemap endpoints
python -m news_collector.cli validate-sources

# Phát hiện URL từ toàn bộ nguồn
python -m news_collector.cli discover --all

# Chỉ chạy RSS
python -m news_collector.cli discover --all --method rss

# Chỉ chạy sitemap
python -m news_collector.cli discover --all --method sitemap

# Chạy một nguồn
python -m news_collector.cli discover --source vnexpress

# Tải và bóc tách URL đang chờ
python -m news_collector.cli fetch --limit 10

# Chạy toàn bộ pipeline
python -m news_collector.cli run --source techcrunch --limit 10

# Thử nghiệm nhỏ
python -m news_collector.cli run --all --limit 10

# Xem thống kê
python -m news_collector.cli stats

# Xuất bài báo
python -m news_collector.cli export --format jsonl

# Thử lại các lỗi có thể phục hồi
python -m news_collector.cli retry-failed
```

CLI cần hỗ trợ `--help`, logging rõ ràng và exit code hợp lý.

---

## 14. Reporting

Sau mỗi lần chạy, tạo báo cáo JSON hoặc Markdown trong `data/reports/`.

Các chỉ số:

| Metric | Ý nghĩa |
|---|---|
| `urls_discovered` | Tổng URL phát hiện |
| `unique_urls` | Tổng URL duy nhất |
| `fetch_success` | Số URL tải thành công |
| `fetch_failed` | Số URL tải thất bại |
| `restricted` | Số URL bị hạn chế |
| `extraction_success` | Số bài bóc tách thành công |
| `extraction_failed` | Số bài lỗi bóc tách |
| `duplicates` | Số bài trùng |
| `missing_published_at` | Số bài thiếu ngày xuất bản |
| `relevant_articles` | Số bài liên quan |
| `articles_by_source` | Số bài theo nguồn |
| `articles_by_month` | Số bài theo tháng |

Cần có thống kê riêng cho từng nguồn để biết nguồn nào hoạt động tốt, nguồn nào không có endpoint hoặc bị hạn chế.

---

## 15. Implementation Phases

### Phase A — Foundation

- [ ] Tạo project Python và `pyproject.toml`.
- [ ] Tạo cấu trúc thư mục.
- [ ] Tạo Pydantic models.
- [ ] Tạo YAML configuration.
- [ ] Thiết kế SQLite schema.
- [ ] Viết database initialization.
- [ ] Viết logging và CLI skeleton.

**Deliverable:** CLI khởi động được, database được tạo, config load được.

### Phase B — Source Discovery

- [ ] Implement RSS parser.
- [ ] Implement sitemap parser.
- [ ] Implement nested sitemap traversal.
- [ ] Implement endpoint validation.
- [ ] Implement URL normalization.
- [ ] Implement URL filtering.
- [ ] Implement queue upsert.
- [ ] Kiểm tra từng nguồn báo.

**Deliverable:** URL queue chứa các URL hợp lệ, có thống kê theo nguồn.

### Phase C — Fetching & Extraction

- [ ] Implement async HTTP client.
- [ ] Implement rate limiting.
- [ ] Implement retry/backoff.
- [ ] Implement robots policy checks.
- [ ] Implement article extractor.
- [ ] Implement metadata extraction.
- [ ] Implement site-specific fallback rules khi cần.
- [ ] Implement extraction validation.

**Deliverable:** Tải và bóc tách được bài báo hợp lệ.

### Phase D — Storage & Deduplication

- [ ] Implement SQLite repositories.
- [ ] Implement JSONL writer.
- [ ] Implement URL deduplication.
- [ ] Implement content hash deduplication.
- [ ] Implement crash recovery.
- [ ] Implement crawl state transitions.
- [ ] Implement export.

**Deliverable:** Dữ liệu được lưu ổn định, không nhân bản khi chạy lại.

### Phase E — Filtering & Reporting

- [ ] Implement keyword relevance scoring.
- [ ] Implement per-source statistics.
- [ ] Implement crawl run reports.
- [ ] Implement failure reports.
- [ ] Implement CLI stats.
- [ ] Viết README hướng dẫn sử dụng.

**Deliverable:** Có thể đánh giá chất lượng dữ liệu thu thập.

### Phase F — Testing & Pilot

- [ ] Unit tests cho RSS.
- [ ] Unit tests cho sitemap index và gzip.
- [ ] Unit tests cho URL normalization.
- [ ] Unit tests cho metadata extraction.
- [ ] Unit tests cho duplicate detection.
- [ ] Tests cho HTTP 403, 404, 429, 500 và timeout.
- [ ] Tests cho retry và resume.
- [ ] Integration test bằng fixture HTML/XML.
- [ ] Pilot tối đa 10 bài/nguồn; báo cáo riêng nguồn bị hạn chế hoặc không khả dụng.
- [ ] Kiểm tra thủ công một mẫu bài đã bóc tách.

**Deliverable:** Pipeline có kiểm thử và báo cáo pilot.

---

## 16. Acceptance Criteria

Implementation được coi là hoàn thành khi:

1. Có thể chạy `validate-sources` để xác định RSS/sitemap khả dụng của năm nguồn.
2. Có thể discovery URL bằng RSS và sitemap mà không dùng phương pháp ngoài phạm vi.
3. Có thể tải và trích xuất title, content, canonical URL, source và các metadata có sẵn.
4. Có SQLite database lưu trạng thái và chống trùng URL.
5. Có JSONL lưu bài báo đã bóc tách.
6. Có thể chạy lại pipeline mà không tạo bản sao của bài đã lưu.
7. Có thể resume sau khi dừng hoặc lỗi.
8. Có cơ chế rate limiting, retry và xử lý nguồn bị hạn chế.
9. Có CLI và báo cáo thống kê.
10. Unit tests và integration tests chạy thành công.
11. README mô tả cách cài đặt, cấu hình, vận hành và giới hạn truy cập từng nguồn.
12. Không có dữ liệu giả hoặc metadata được suy đoán.
13. Không có chức năng vượt paywall, CAPTCHA hoặc các hạn chế truy cập.
14. Có thể xuất dữ liệu cho giai đoạn NLP tiếp theo.

---

## 17. Hướng dẫn bắt buộc dành cho Codex

**Implementation instructions:**

- Build this project incrementally, phase by phase.
- Before writing site-specific code, inspect the current repository and identify existing conventions.
- Do not overwrite unrelated existing files.
- Prefer simple, maintainable Python modules.
- Use type hints, Pydantic models and clear error handling.
- Keep discovery, fetching, extraction, processing and storage separate.
- Make all sources configurable rather than embedding endpoint URLs in code.
- Verify live RSS/sitemap endpoints before marking them operational.
- If network access is unavailable, implement and test with fixtures; explicitly mark live endpoints as unverified.
- Never invent successful crawl results.
- Do not implement bypasses for restricted content.
- Use deterministic identifiers and idempotent database operations.
- Make every command safe to rerun.
- Add tests for every core component.
- Run the relevant tests after each phase.
- At the end of each phase, report changed files, commands executed, test results and outstanding issues.
- Do not add NLP, AI agents, Neo4j or web UI to this implementation.
- Begin with Phase A, then proceed sequentially through Phase F.
