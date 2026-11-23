# Phiếu review thủ công: 300 cạnh

**Mục tiêu:** ước lượng precision quan hệ bằng review người trên mẫu ngẫu nhiên.
**Export:** `D:\Project\weconomy\data\normalized\international-business-v15-manual-20261112-global-business-only`
**Quần thể:** 5046 cạnh | **Mẫu:** 300 | **Seed:** 20261123 (ngẫu nhiên, không hoàn lại)
**SHA-256 packet:** `25c13430222a605389b34b342db59ca624891e3e5ed8e59b9e13107eb6925db9`

**Reviewer ID:** TODO

## Hướng dẫn chấm

- `correct`: evidence hỗ trợ đúng subject, object, chiều/predicate, trạng thái sự kiện và phạm vi đề tài.
- `incorrect`: có ít nhất một lỗi rõ ràng; ghi lý do ngắn trong Note.
- `uncertain`: chưa đủ evidence/ngữ cảnh để kết luận; không đoán, ghi lý do.
- Tin đồn, kế hoạch hoặc đàm phán không chứng minh giao dịch đã hoàn tất.
- Thay `TODO` tại Verdict bằng đúng một nhãn: `correct`, `incorrect`, `uncertain`. Note bắt buộc cho hai nhãn cuối.
- Không sửa task ID, triple, evidence hay URL. Điền Reviewer ID ở đầu phiếu.
- Sau khi đủ nhãn, lưu phiếu. Nhãn sẽ được chuyển sang JSONL, kiểm tra coverage rồi tính precision và Wilson 95%.
- Với n=300, cần ít nhất **281 correct** để cận dưới Wilson 95% đạt 90%; `uncertain` tính là chưa đúng. Point precision 90% cần 270 correct.

> Hoàn tất phiếu này là review xong mẫu 300 cạnh, không phải review thủ công toàn bộ 5.046 cạnh.

<!-- task_id: edge-0001 -->
## 001. edge-0001

**Triple:** Cobalt Capital (ORG) —CO_INVESTED_WITH→ Agility Global (ORG)
**Assertion status:** reported
**Evidence:**
> Parallel Systems, a startup developing a rail vehicle capable of moving over several tons of freight as far as 500 miles without an operator, raised $100 million in a Series C round led by AVP, with participation from Hillspire, Agility Global, Cobalt Capital, Anthos Capital, Congruent Ventures, Riot Ventures, and Collaborative Fund.

**Article:** [TechCrunch Mobility: A roadblock clears for self-driving trucks](https://techcrunch.com/2026/10/11/techcrunch-mobility-a-roadblock-clears-for-self-driving-trucks/) | en | techcrunch.com
**Ngữ cảnh:**
>  Ventures, and the Michigan Outdoor Innovation Fund.
> Flai, a startup that developed AI software for dealerships, raised $27 million in a Series A funding round led by automation-focused firm Base10 Partners. The round included funding from dealers (Friedkin Group and Findlay Automotive), Toyota’s venture arm, Y Combinator, and First Round Capital.
> Parallel Systems, a startup developing a rail vehicle capable of moving over several tons of freight as far as 500 miles without an operator, raised $100 million in a Series C round led by AVP, with participation from Hillspire, Agility Global, Cobalt Capital, Anthos Capital, Congruent Ventures, Riot Ventures, and Collaborative Fund.
> Uber has agreed to buy catering company ezCater in an all-cash transaction valued at $2.3 billion.
> Notable reads and other tidbits
> Surveillance camera maker Flock cut its workforce by 18%, or around 270 employees, as the company faces ongoing and growing backlash to its license plate readers and people-tracking technology. FYI: Flock founder and C

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0002 -->
## 002. edge-0002

**Triple:** D1 Capital Partners (ORG) —CO_INVESTED_WITH→ Bessemer Venture Partners (ORG)
**Assertion status:** reported
**Evidence:**
> If finalized, the deal would nearly triple Anthropic’s valuation, which was $61.5 billion after a $3.5 billion funding round led by Lightspeed Venture Partners announced in March. Other participants in the startup’s last round included Bessemer Venture Partners, Cisco Investments, D1 Capital Partners, Fidelity Management & Research Company, General Catalyst, Jane Street, Menlo Ventures, and Salesforce Ventures.

**Article:** [Anthropic reportedly nears $170B valuation with potential $5B round](https://techcrunch.com/2025/07/29/anthropic-reportedly-nears-170b-valuation-with-potential-5b-round/) | en | techcrunch.com
**Ngữ cảnh:**
> llion in funding, valuing the large language model developer at $170 billion, Bloomberg reported.
> Iconiq Capital is leading this funding round, but there’s a possibility of a second lead investor joining the deal. The company has also been in talks with Qatar Investment Authority and GIC, Singapore’s sovereign wealth fund, according to the report.
> If finalized, the deal would nearly triple Anthropic’s valuation, which was $61.5 billion after a $3.5 billion funding round led by Lightspeed Venture Partners announced in March. Other participants in the startup’s last round included Bessemer Venture Partners, Cisco Investments, D1 Capital Partners, Fidelity Management & Research Company, General Catalyst, Jane Street, Menlo Ventures, and Salesforce Ventures.
> Despite Anthropic’s mission as a safety-conscious AI model developer, the company’s CEO, Dario Amodei, recently confessed in a memo to employees, reported by Wired, that he’s “not thrilled” about taking money from sovereign wealth funds of dictatorial governments.
> To keep pace with the massive capital requirements of developing AI models, the comp

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0003 -->
## 003. edge-0003

**Triple:** Shinhan Bank (ORG) —CO_FINANCED_WITH→ The Export-Import Bank of China (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> Tham gia giao dịch còn có các định chế tài chính phát triển gồm IFC, DEG (Đức), Proparco (Pháp) và Norfund (Na Uy); các ngân hàng xuất nhập khẩu China Eximbank, Korea Eximbank cùng nhóm ngân hàng thương mại và tổ chức tài chính như SMBC, Punjab National Bank, Commercial Bank of Ceylon, ICBC, Shinhan Bank, Woori Bank và KEXIM Asia Limited.

**Article:** [VPBank huy động 730 triệu USD vốn quốc tế](https://vnexpress.net/vpbank-huy-dong-730-trieu-usd-von-quoc-te-5143246.html) | vi | vnexpress.net
**Ngữ cảnh:**
> y động thành công khoản vay hợp vốn quốc tế 730 triệu USD, tương đương gần 19.000 tỷ đồng, do IFC và SMBC thu xếp, ngày 10/11.
> Giao dịch do Tổ chức Tài chính Quốc tế (IFC) và Ngân hàng Sumitomo Mitsui Banking Corporation (SMBC) đồng điều phối, thu xếp, gồm các khoản vay có kỳ hạn 3 năm, 5 năm và 7 năm, được giải ngân theo nhiều đợt trong năm 2026.
> Tham gia giao dịch còn có các định chế tài chính phát triển gồm IFC, DEG (Đức), Proparco (Pháp) và Norfund (Na Uy); các ngân hàng xuất nhập khẩu China Eximbank, Korea Eximbank cùng nhóm ngân hàng thương mại và tổ chức tài chính như SMBC, Punjab National Bank, Commercial Bank of Ceylon, ICBC, Shinhan Bank, Woori Bank và KEXIM Asia Limited. Sự tham gia của các tổ chức đến từ nhiều quốc gia giúp VPBank đa dạng hóa đối tác và mở rộng khả năng tiếp cận thị trường vốn quốc tế.
> Theo VPBank, nguồn vốn này sẽ được sử dụng để mở rộng tín dụng cho doanh nghiệp vừa và nhỏ (SME), đặc biệt là doanh nghiệp do phụ nữ làm chủ hoặc lãnh đạo (WSME) và doanh nghiệp hoạt động trong lĩnh vực nông nghiệp

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0004 -->
## 004. edge-0004

**Triple:** Commerzbank (ORG) —CO_FINANCED_WITH→ Sumitomo Mitsui Banking Corporation (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> Sumitomo Mitsui Banking Corporation (SMBC) played a central role in the transaction as Coordinator, Mandated Lead Arranger, Underwriter and Bookrunner, Facility Agent and Sustainability Coordinator.
> This collaboration further reinforces the long-standing strategic partnership between VPBank and SMBC, while enhancing VPBank’s standing in regional and international financial markets.
> The transaction attracted several financial institutions taking on lead roles for the first time or expanding their existing participation, with these banks accounting for nearly half of all participating institutions.
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).

**Article:** [VPBank and 15 international financial institutions sign maiden US$1.44 billion sustainability-linked syndicated loan facility](https://vietnamnews.vn/economy/1784501/vpbank-and-15-international-financial-institutions-sign-maiden-us-1-44-billion-sustainability-linked-syndicated-loan-facility.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> mitted by VPBank throughout the tenor, which are defined at the portfolio level and include annual targets related to expanding lending to green and social sectors.
> The assessment of VPBank’s performance against these SPTs will serve as the basis for making any adjustments to the financial terms, in accordance with the agreements with the lenders.
> Sumitomo Mitsui Banking Corporation (SMBC) played a central role in the transaction as Coordinator, Mandated Lead Arranger, Underwriter and Bookrunner, Facility Agent and Sustainability Coordinator.
> This collaboration further reinforces the long-standing strategic partnership between VPBank and SMBC, while enhancing VPBank’s standing in regional and international financial markets.
> The transaction attracted several financial institutions taking on lead roles for the first time or expanding their existing participation, with these banks accounting for nearly half of all participating institutions.
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).
> With the partnership of 15 international financial institutions, this facility represents VPBank’s largest-ever transaction in terms of the number of MLAUBs involved. The scale of the transaction and the breadth of participation underscore the strong confidence of the international financial community in VPBank’s financial strength, growth prospec

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0005 -->
## 005. edge-0005

**Triple:** Camber Partners (ORG) —INVESTED_IN→ Respond.io (ORG)
**Assertion status:** reported
**Evidence:**
> In 2017, Respond.io set out to solve a simple problem: Businesses couldn’t keep up with customers who had moved to messaging apps. Today, Respond, with its customer conversation management software, has become one of the tech success stories of Malaysia.
> The startup, headquartered in Kuala Lumpur, has raised a $62.5 million Series B round led by Camber Partners, with participation from Endeavor Catalyst and existing investors. It last raised a $7 million Series A in 2022. The company has grown to $35 million in annual recurring revenue (ARR), growing 169% year-over-year, at a 30% profit margin, it tells TechCrunch.

**Article:** [Malaysia&#8217;s AI agent-powered messaging app Respond.io raises $62.5M, eyes acquisitions](https://techcrunch.com/2026/06/15/malaysias-respond-io-raises-62-5m-eyes-acquisitions-in-north-america-and-europe/) | en | techcrunch.com
**Ngữ cảnh:**
> In 2017, Respond.io set out to solve a simple problem: Businesses couldn’t keep up with customers who had moved to messaging apps. Today, Respond, with its customer conversation management software, has become one of the tech success stories of Malaysia.
> The startup, headquartered in Kuala Lumpur, has raised a $62.5 million Series B round led by Camber Partners, with participation from Endeavor Catalyst and existing investors. It last raised a $7 million Series A in 2022. The company has grown to $35 million in annual recurring revenue (ARR), growing 169% year-over-year, at a 30% profit margin, it tells TechCrunch.
> Co-founder and CEO Gerardo Salandra, who worked at IBM and Google before joining Runtastic, a fitness tracking app that was sold to Adidas in 2015, founded Respond in Hong Kong in 2017 alongside Hassan Ahmed (CTO) and Iaroslav Kudritskiy (COO). The team relocated the business to Malaysia two years later.
> The platform helps mid- to large-sized B2C 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0006 -->
## 006. edge-0006

**Triple:** Carlsberg (ORG) —COOPERATES_WITH→ Chính quyền thành phố Đà Nẵng (GOV)
**Assertion status:** reported
**Evidence:**
> Trong lĩnh vực công nghiệp, Carlsberg trao ý định thư với chính quyền thành phố Huế về mở rộng nhà máy bia tại Khu công nghiệp Phú Bài và với thành phố Đà Nẵng về cam kết đầu tư giai đoạn 2026-2030.

**Article:** [Loạt thỏa thuận hợp tác năng lượng, logistics, công nghệ của Việt Nam - Đan Mạch - Báo VnExpress Kinh doanh](https://vnexpress.net/loat-thoa-thuan-hop-tac-nang-luong-logistics-cong-nghe-cua-viet-nam-dan-mach-5134816.html) | vi | vnexpress.net
**Ngữ cảnh:**
> à vận hành ga hàng hóa đường sắt tại Hải Phòng.
> 
> Vietjet ký biên bản ghi nhớ với Satair về vật tư, chuỗi cung ứng và dịch vụ hàng không. Vietnam Airlines trao ba biên bản ghi nhớ với Copenhagen Airport, Danish Industry và Scandinavian Airlines (SAS), hướng tới mở rộng hợp tác vận hành sân bay, vận tải hành khách, hàng hóa và liên danh chuyến bay.
> 
> Trong lĩnh vực công nghiệp, Carlsberg trao ý định thư với chính quyền thành phố Huế về mở rộng nhà máy bia tại Khu công nghiệp Phú Bài và với thành phố Đà Nẵng về cam kết đầu tư giai đoạn 2026-2030.
> 
> Các thỏa thuận khác liên quan đến nghiên cứu công nghệ lượng tử giữa FPT và Viện Niels Bohr thuộc Đại học Copenhagen; giáo dục STEAM giữa Hà Nội và LEGO; hợp tác y sinh giữa Bệnh viện 19-8 và Bệnh viện Đại học Aalborg; phát triển du lịch giữa Vietravel và Nordic Travel Associates.
> 
> Phát biểu tại diễn đàn, Tổng Bí thư, Chủ tịch nước Tô Lâm đề nghị

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0007 -->
## 007. edge-0007

**Triple:** Tiger Global (ORG) —CO_INVESTED_WITH→ Greycroft (ORG)
**Assertion status:** reported
**Evidence:**
> Electric truck startup Harbinger has raised a $240 million Series D funding round as it expands its portfolio of products, including battery storage and defense applications.
> The funding comes almost one year to the day after the Los Angeles-based company announced a $160 million Series C, which included an initial truck order from FedEx. Harbinger has now raised more than $650 million to date, according to Bloomberg News, which first reported the round.
> The Series D was co-led by Tiger Global, Capricorn’s “technology impact fund,” and defense-focused firm Ridgeline. FedEx invested again after leading last year’s round, and other repeat investors included Maniv, Greycroft, and Leitmotif, a VC firm backed by Volkswagen. Also investing this time was institutional giant Fidelity Management, which tends to invest in pre-IPO startups. (Harbinger is reportedly weighing going public.)

**Article:** [Harbinger raises $240M after expanding into defense](https://techcrunch.com/2026/11/05/harbinger-raises-240m-after-expanding-into-defense/) | en | techcrunch.com
**Ngữ cảnh:**
> Electric truck startup Harbinger has raised a $240 million Series D funding round as it expands its portfolio of products, including battery storage and defense applications.
> The funding comes almost one year to the day after the Los Angeles-based company announced a $160 million Series C, which included an initial truck order from FedEx. Harbinger has now raised more than $650 million to date, according to Bloomberg News, which first reported the round.
> The Series D was co-led by Tiger Global, Capricorn’s “technology impact fund,” and defense-focused firm Ridgeline. FedEx invested again after leading last year’s round, and other repeat investors included Maniv, Greycroft, and Leitmotif, a VC firm backed by Volkswagen. Also investing this time was institutional giant Fidelity Management, which tends to invest in pre-IPO startups. (Harbinger is reportedly weighing going public.)
> While it didn’t lead this round, FedEx’s relationship with Harbinger continues to deepen. The shipping giant’s senior vice president of safety and transportation, Paul Melander, has joined Harbinger’s board of directors. FedEx also recently placed its first large order with Harbinger — a deal for 2,000 trucks valued at more than $300 million.
> Foun

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0008 -->
## 008. edge-0008

**Triple:** General Catalyst (ORG) —CO_INVESTED_WITH→ Elad Gil (PERSON)
**Assertion status:** reported
**Evidence:**
> Cognition, the makers of the autonomous AI software engineer named Devin, has raised more than $1 billion at a $25 billion pre-money valuation ($26 billion post money), the company announced on Wednesday.
> That’s a major leap from its $10.2 billion post-money valuation when it closed a $400 million funding round just eight months ago in September.
> The round was led by Lux Capital, General Catalyst and 8VC, with a host of existing investors pouring in, including Elad Gil, Soma Capital, Omri Casspi, Founders Fund, and a long list of others. The round also included new investors like Ribbit Capital, Atreides, and Layer Global.

**Article:** [AI coding startup Cognition raises $1B at $25B pre-money valuation](https://techcrunch.com/2026/05/27/ai-coding-startup-cognition-raises-1b-at-25b-pre-money-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Cognition, the makers of the autonomous AI software engineer named Devin, has raised more than $1 billion at a $25 billion pre-money valuation ($26 billion post money), the company announced on Wednesday.
> That’s a major leap from its $10.2 billion post-money valuation when it closed a $400 million funding round just eight months ago in September.
> The round was led by Lux Capital, General Catalyst and 8VC, with a host of existing investors pouring in, including Elad Gil, Soma Capital, Omri Casspi, Founders Fund, and a long list of others. The round also included new investors like Ribbit Capital, Atreides, and Layer Global.
> This is a giant vote of confidence from top-tier VCs that there will be room for independent AI software coding startups. Last year, all signs pointed to model makers swallowing this hot market themselves. Certainly Anthropic’s Claude Code, OpenAI’s Codex, and maybe even Google’s coding agent Jules (after Google’s acqui-hire deal of Windsurf last 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0009 -->
## 009. edge-0009

**Triple:** Khosla Ventures (ORG) —CO_INVESTED_WITH→ Terrain Capital (ORG)
**Assertion status:** reported
**Evidence:**
> Parallel Web Systems, the AI agent-tool startup founded by former Twitter CEO Parag Agrawal, has raised a $100 million Series B at a $2 billion valuation led by Sequoia. Existing investors Kleiner Perkins, Index Ventures, Khosla Ventures, First Round Capital, Spark Capital, and Terrain Capital also participated, the company said.

**Article:** [Parallel Web Systems hits $2B valuation five months after its last big raise](https://techcrunch.com/2026/04/29/parallel-web-systems-hits-2b-valuation-five-months-after-its-last-big-raise/) | en | techcrunch.com
**Ngữ cảnh:**
> Parallel Web Systems, the AI agent-tool startup founded by former Twitter CEO Parag Agrawal, has raised a $100 million Series B at a $2 billion valuation led by Sequoia. Existing investors Kleiner Perkins, Index Ventures, Khosla Ventures, First Round Capital, Spark Capital, and Terrain Capital also participated, the company said.
> This raise comes just five months after the startup announced its $100 million Series A at a $740 million valuation led by Kleiner and Index, and brings the total capital it raised to $230 million.
> Parallel offers a suite of web search and research APIs specifically for AI agents and names customers such as Clay, Harvey, Notion, and Opendoor. It s

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0010 -->
## 010. edge-0010

**Triple:** Maybank Securities (ORG) —CO_FINANCED_WITH→ Cathay United Bank (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).

**Article:** [VPBank and 15 international financial institutions sign maiden US$1.44 billion sustainability-linked syndicated loan facility](https://vietnamnews.vn/economy/1784501/vpbank-and-15-international-financial-institutions-sign-maiden-us-1-44-billion-sustainability-linked-syndicated-loan-facility.html) | en | vietnamnews.vn
**Ngữ cảnh:**
>  strategic partnership between VPBank and SMBC, while enhancing VPBank’s standing in regional and international financial markets.
> The transaction attracted several financial institutions taking on lead roles for the first time or expanding their existing participation, with these banks accounting for nearly half of all participating institutions.
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).
> With the partnership of 15 international financial institutions, this facility represents VPBank’s largest-ever transaction in terms of the number of MLAUBs involved. The scale of the transaction and the breadth of participation underscore the strong confidence of the international financial community in VPBank’s financial strength, growth prospec

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0011 -->
## 011. edge-0011

**Triple:** WTI (ORG) —INVESTED_IN→ Lucra (ORG)
**Assertion status:** reported
**Evidence:**
> Lucra announced on Wednesday that it raised a $20 million Series B, led by the ARK fund, with participation from Alumni Ventures, Astralis Capital, Harlo Equity Partners, Simplex Ventures, SeventySix Capital, and WTI.

**Article:** [Cathie Wood’s ARK makes its first lead investment in startup Lucra — and it isn’t AI](https://techcrunch.com/2026/04/22/cathie-woods-ark-makes-its-first-lead-investment-in-startup-lucra-and-it-isnt-ai/) | en | techcrunch.com
**Ngữ cảnh:**
> ding the investment in the startup.
> Lucra developed a software platform that reimagines corporate loyalty programs into interactive, esports-like events such as tournaments where customers can play each other, even betting or winning cash or company giveaways. The startup said its customers include Five Iron Golf, Chess Kings, and Dave & Buster’s.
> Lucra announced on Wednesday that it raised a $20 million Series B, led by the ARK fund, with participation from Alumni Ventures, Astralis Capital, Harlo Equity Partners, Simplex Ventures, SeventySix Capital, and WTI.
> There are a few reasons why the famed financial company has never led a startup deal before. For one, the ARK Invest Venture Fund is not a typical VC fund. It’s an SEC-regulated interval fund (also known as a closed-end mutual fund), meaning anyone can invest in it, for as little as $500. However, it is not traded on a public exchange, so investor

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0012 -->
## 012. edge-0012

**Triple:** Sequoia (ORG) —INVESTED_IN→ OpenAI (ORG)
**Assertion status:** reported
**Evidence:**
> Yet here’s Sequoia, already invested in both OpenAI and Elon Musk’s xAI, now throwing its weight behind Anthropic, too.

**Article:** [Sequoia to invest in Anthropic, breaking VC taboo on backing rivals: FT](https://techcrunch.com/2026/01/18/sequoia-to-invest-in-anthropic-breaking-vc-taboo-on-backing-rivals-ft/) | en | techcrunch.com
**Ngữ cảnh:**
> ia Capital is reportedly joining a blockbuster funding round for Anthropic, the AI startup behind Claude, according to the Financial Times. It’s a move sure to turn heads in Silicon Valley.
> Why? Because venture capital firms have historically avoided backing competing companies in the same sector, preferring to place their bets on a single winner. Yet here’s Sequoia, already invested in both OpenAI and Elon Musk’s xAI, now throwing its weight behind Anthropic, too.
> The timing is particularly surprising given what OpenAI CEO Sam Altman said under oath last year. As part of OpenAI’s defense against a high-profile lawsuit by Musk, Altman addressed earlier rumors about restrictions in OpenAI’s 2024 funding round. While he denied that OpenAI investors were broadly prohibited from backing rivals, he did acknowledg

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0013 -->
## 013. edge-0013

**Triple:** Ocean Edu (ORG) —PARTNERED_WITH→ Pearson (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> Hệ thống Anh ngữ Ocean Edu ký biên bản ghi nhớ hợp tác (MOU) với Tập đoàn giáo dục Pearson nhằm mở rộng hợp tác đào tạo, đánh giá năng lực tiếng Anh cho học sinh.

**Article:** [Ocean Edu mở rộng hợp tác đào tạo với tập đoàn giáo dục Anh](https://vnexpress.net/ocean-edu-mo-rong-hop-tac-dao-tao-voi-tap-doan-giao-duc-anh-5131421.html) | vi | vnexpress.net
**Ngữ cảnh:**
> Ocean Edu mở rộng hợp tác đào tạo với tập đoàn giáo dục Anh
> Hệ thống Anh ngữ Ocean Edu ký biên bản ghi nhớ hợp tác (MOU) với Tập đoàn giáo dục Pearson nhằm mở rộng hợp tác đào tạo, đánh giá năng lực tiếng Anh cho học sinh.
> Lễ ký kết diễn ra trong khuôn khổ Hội nghị quốc tế về hợp tác giáo dục trong kỷ nguyên số và Triển lãm giáo dục và công nghệ giáo dục (IECEE), ngày 8/10, tại Hà Nội.
> Đại diện hai bên ký kết là bà Vũ Thị Thanh Loan - Tổng giám đốc Hệ thống Anh ngữ Quốc tế Ocean Edu và ông David Lyons - quyền Chủ tịch khu vực Châu Á - Thái Bình Dương của Pearson. Th

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0014 -->
## 014. edge-0014

**Triple:** Index Ventures (ORG) —INVESTED_IN→ Mistral AI (ORG)
**Assertion status:** reported
**Evidence:**
> In September 2025, Mistral closed a €1.7 billion Series C round (about $2 billion) led by ASML at a €11.7 billion valuation (approximately $13.8 billion), with participation from existing backers DST Global, a16z, Bpifrance, General Catalyst, Index Ventures, Lightspeed, and Nvidia.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
>  presented as a Series A extension, implying an unchanged valuation.
> In June 2024, Mistral raised €600 million (about $640 million) in a mix of equity and debt. The long-rumored round was led by General Catalyst at a $6 billion valuation, with notable investors including Cisco, IBM, Nvidia, and Samsung Venture Investment Corporation participating.
> In September 2025, Mistral closed a €1.7 billion Series C round (about $2 billion) led by ASML at a €11.7 billion valuation (approximately $13.8 billion), with participation from existing backers DST Global, a16z, Bpifrance, General Catalyst, Index Ventures, Lightspeed, and Nvidia.
> What companies has Mistral AI acquired?
> In addition to infrastructure startup Koyeb, Mistral has also bought Emmi, an Austrian startup focusing on physics AI, with the ambition to better support industrial enterprises in their AI transformation.
> Will Mistral AI make its own chips?
> While Mistral has yet to design its own chips, Mensch isn’t ruling 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0015 -->
## 015. edge-0015

**Triple:** Bessemer Venture Partners (ORG) —INVESTED_IN→ Box (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Bessemer has been well-known as a leading VC in the SaaS era, with a particular knack for picking enterprise winners, like Box, Docusign, and Gainsight. Since 2022, it has invested in more than 260 AI-native companies. So far, the firm has invested $3 billion into AI-related startups, it says, including those focused on compute, infrastructure, foundation models, dev tools, app-layer startups, and agentic tech.

**Article:** [VC firm Bessemer now has another $5.75B to invest in (what else?) AI](https://techcrunch.com/2026/09/23/vc-firm-bessemer-now-has-another-5-75b-to-invest-in-what-else-ai/) | en | techcrunch.com
**Ngữ cảnh:**
>  Wednesday that it has raised $5.75 billion across two new funds to accelerate its investment across all parts of the AI stack. The firm, which has backed companies such as Anthropic, Cognition, Legora, Perplexity, Ramp, Shopify, and Waymo, dedicated $1.75 billion for seed and early-stage investing and the remaining $4 billion for growth startups.
> Bessemer has been well-known as a leading VC in the SaaS era, with a particular knack for picking enterprise winners, like Box, Docusign, and Gainsight. Since 2022, it has invested in more than 260 AI-native companies. So far, the firm has invested $3 billion into AI-related startups, it says, including those focused on compute, infrastructure, foundation models, dev tools, app-layer startups, and agentic tech.
> Now, Bessemer positions all things AI as the opportunity of a lifetime — a common sentiment, until the next big trendy tech revolution comes around, of course.
> “AI-native companies are scaling faster than any category of technology we’ve backed before,” Bessemer Partner Byron Deeter said in the company’s funding announcement. VC firms also need to

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0016 -->
## 016. edge-0016

**Triple:** M??ng Thanh Vientiane Hotel (ORG) —PARTNERED_WITH→ Green SM (ORG)
**Assertion status:** reported
**Evidence:**
> Green SM also signed comprehensive cooperation agreements with major banks, including VietinBank Laos, JDB, MB Bank Laos and Sacombank Laos; Lao telecom operator ETL; e-wallet providers U-Money and M-Money; and leading hotel and tourism groups such as Bawanli, Mường Thanh Vientiane Hotel and Latsavong Wanda Vista Hotel.

**Article:** [Việt Nam, Laos step up cooperation on green transition, digital economy](https://vietnamnews.vn/economy/1803930/viet-nam-laos-step-up-cooperation-on-green-transition-digital-economy.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> referential rates to roaming customers travelling from Việt Nam to Laos; integrating ride-hailing services directly into the Lao Travel national tourism app; providing green-transition vouchers to customers purchasing Unitel tourist SIM cards; and deploying Green SM’s Green Business corporate mobility solution across Unitel’s internal operations.
> 
> Green SM also signed comprehensive cooperation agreements with major banks, including VietinBank Laos, JDB, MB Bank Laos and Sacombank Laos; Lao telecom operator ETL; e-wallet providers U-Money and M-Money; and leading hotel and tourism groups such as Bawanli, Mường Thanh Vientiane Hotel and Latsavong Wanda Vista Hotel.
> 
> The agreements focus on integrating payment technology infrastructure, introducing joint promotional programmes and promoting environmentally friendly mobility solutions to a wider audience of tourists and local residents.
> 
> Speaking at the event, Tâm lauded Green SM Laos for its efforts and impressive achievements. He said the company’s investmen

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0017 -->
## 017. edge-0017

**Triple:** Tidal Venture Partners (ORG) —INVESTED_IN→ Floqer (ORG)
**Assertion status:** reported
**Evidence:**
> Floqer was founded in 2024 and has raised $2 million in pre-seed funding, with participation from investors such as Perplexity’s F7 Fund, N49P, Tidal Venture Partners, and Perplexity co-founder Denis Yarats.

**Article:** [Floqer&#8217;s AI agents research sales prospects so teams don&#8217;t have to](https://techcrunch.com/2026/10/14/floqers-ai-agents-help-b2b-revenue-teams-research-customers/) | en | techcrunch.com
**Ngữ cảnh:**
> y platform. Others want to modify the technology or build on top of it.
> “Our mission is to really enable every team to build their central source of growth,” Mahajan said.
> Before releasing the database publicly, Floqer is conducting security reviews because the database can contain sensitive customer information and large companies already use it.
> Floqer was founded in 2024 and has raised $2 million in pre-seed funding, with participation from investors such as Perplexity’s F7 Fund, N49P, Tidal Venture Partners, and Perplexity co-founder Denis Yarats. It says it now has eight employees and more than 1,000 customers, including Perplexity, Wise, and AngelList.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0018 -->
## 018. edge-0018

**Triple:** Stripe (ORG) —CO_INVESTED_WITH→ Square Peg (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The Series A round was led by General Catalyst, with participation from existing investors Square Peg, Stripe, Lightspeed, and Moore Capital, while PayPal Ventures joined as a new backer. The all-equity round values the Bengaluru-based startup at $85 million post-investment and brings its total funding to more than $32 million to date.

**Article:** [Stripe, PayPal Ventures bet on India&#8217;s Xflow to fix cross-border B2B payments](https://techcrunch.com/2026/02/23/stripe-paypal-ventures-bet-on-indias-xflow-to-fix-cross-border-b2b-payments/) | en | techcrunch.com
**Ngữ cảnh:**
> Xflow, an Indian fintech startup, has secured backing from both Stripe and PayPal Ventures in a $16.6 million funding round. The investment comes as the company works to carve out a position in cross-border B2B payments, a market still dominated by banks and manual processes.
> The Series A round was led by General Catalyst, with participation from existing investors Square Peg, Stripe, Lightspeed, and Moore Capital, while PayPal Ventures joined as a new backer. The all-equity round values the Bengaluru-based startup at $85 million post-investment and brings its total funding to more than $32 million to date.
> Despite rapid digitization in domestic payments, cross-border B2B transfers for Indian exporters remain heavily reliant on banks, often with limited visibility into fees, settlement timelines, and the final amount received in rupees. The friction is particularly acute for larger exporters moving millions of dollars into India to fund salaries and 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0019 -->
## 019. edge-0019

**Triple:** Flybridge (ORG) —CO_INVESTED_WITH→ 84I90 (ORG)
**Assertion status:** reported
**Evidence:**
> Maka Kids is building a streaming app for children ages zero to six featuring content designed for healthy development. The startup has now raised $3 million in pre-seed funding to scale its platform, and is currently accepting waitlist sign-ups.
> Unlike traditional streaming platforms, Maka Kids doesn’t have recommendation algorithms, ads, or auto-play. Instead, it is designed to offer a predictable experience that supports learning, creativity, and emotional growth.
> Maka Kids was founded by Isabel Sheinman and Tanyella Leta, who previously founded Nabu, a non-profit venture that brought children’s books to more than 15 million children across 26 countries.
> Sheinman and Leta were introduced at a dinner back in 2013 through a mutual friend and immediately hit it off, the pair told TechCrunch in an email. They said they initially over the fact that they both came from families of educators and entrepreneurs, an experience that first inspired Nabu and later fueled their passion for Maka Kids.
> They began dreaming up the concept of Maka Kids after discussions with their friends, families, and customers at Nabu. They heard from parents who felt increasingly anxious about the effects of screen time on their children. Building on those concerns, the duo conducted hundreds of user interviews, which ultimately shaped their solution: a children’s streaming app designed with well-being at its core.
> “We were seeing parents get completely overwhelmed trying to weigh decisions about what was unsafe, what was good, and understand why their kid was melting down every time screen time ended,” Sheinman said. “At the same time, we watched the children’s media ecosystem get louder, faster, more algorithmically driven. Looking at this problem, we felt uniquely positioned to deliver the relief that parents craved.”
> All of the content on Maka Kids is evaluated using Maka Imprint, the startup’s patent-pending developmental framework created through two years of R&D in collaboration with researchers at the Yale Child Study Center. The framework maps seven core domains of early childhood development across more than 650 developmental indicators, including language, creativity, emotional skills, and growth mindset.
> Maka Kids licenses content directly from IP holders and individual creators. The startup is also partnering directly with studios and animators to produce original content.
> Every show on the platform goes through an analysis of pacing, stimulation levels, color contrast, and narrative structure. Its catalog features slower-paced, lower-stimulation content with genuine narrative arcs and stories from around the world.
> The duo believes an important factor often missing from the screen time debate for kids is how much the right story, delivered at the right moment, can positively support a young child.
> “Stories can support language development, emotional regulation, curiosity, and give kids a sense of how wide the world is,” Leta said. “Children’s media at its best is one of the most powerful developmental tools families have, when it’s designed with this intention. Most of the platforms children watch on today were designed for adult audiences, with a kids experience crudely bolted on as an afterthought. The incentive for the majority of kids’ streaming platforms is watch time, not well-being.”
> When parents create a profile for their child, they can select channels focused on a variety of topics, such as kindness, STEM, emotional regulation, or movement, and then set preferred session lengths. From there, Maka Kids delivers curated, developmentally vetted content tailored to those selections.
> The session then ends naturally, with wind-down cues from characters to help children calmly transition away from screen time without a meltdown.
> Maka Kids is running a private beta on iOS this summer and plans to launch publicly this fall on iPhone and iPad, with casting support via AirPlay. Maka Kids says it already has thousands of families on its waitlist.
> As for the startup’s business model, the app will operate on a subscription model, priced at $11.99 per month, with a discounted annual option.
> In terms of the new funding, the startup plans to use it to grow its catalog of vetted shows. The round was led by Michigan Rise, with participation from Union Heritage Ventures, Flybridge, Also Capital, Detroit Venture Partners, Song United, Invest Detroit, Ann Arbor Spark Capital, 84I90, Georgetown Gain, and Segal Ventures, as well as angel investors.

**Article:** [Maka Kids is redefining kids’ screen time with a streaming app optimized for well-being, not engagement](https://techcrunch.com/2026/05/21/maka-kids-is-redefining-kids-screen-time-with-a-streaming-app-optimized-for-well-being-not-engagement/) | en | techcrunch.com
**Ngữ cảnh:**
> In a media landscape dominated by Baby Shark and Skibidi Toilet, one startup is reimagining children’s media by focusing on well-being, not watch time.
> Maka Kids is building a streaming app for children ages zero to six featuring content designed for healthy development. The startup has now raised $3 million in pre-seed funding to scale its platform, and is currently accepting waitlist sign-ups.
> Unlike traditional streaming platforms, Maka Kids doesn’t have recommendation algorithms, ads, or auto-play. Instead, it is designed to offer a predictable experience that supports learning, creativity, and emotional growth.
> Maka Kids was founded by Isabel Sheinman and Tanyella Leta, who previously founded Nabu, a non-profit venture that brought children’s books to more than 15 million children across 26 countries.
> Sheinman and Leta were introduced at a dinner back in 2013 through a mutual friend and immediately hit it off, the pair told TechCrunch in an email. They said they initially over the fact that they both came from families of educators and entrepreneurs, an experience that first inspired Nabu and later fueled their passion for Maka Kids.
> They began dreaming up the concept of Maka Kids after discussions with their friends, families, and customers at Nabu. They heard from parents who felt increasingly anxious about the effects of screen time on their children. Building on those concerns, the duo conducted hundreds of user interviews, which ultimately shaped their solution: a children’s streaming app designed with well-being at its core.
> “We were seeing parents get completely overwhelmed trying to weigh decisions about what was unsafe, what was good, and understand why their kid was melting down every time screen time ended,” Sheinman said. “At the same time, we watched the children’s media ecosystem get louder, faster, more algorithmically driven. Looking at this problem, we felt uniquely positioned to deliver the relief that parents craved.”
> All of the content on Maka Kids is evaluated using Maka Imprint, the startup’s patent-pending developmental framework created through two years of R&D in collaboration with researchers at the Yale Child Study Center. The framework maps seven core domains of early childhood development across more than 650 developmental indicators, including language, creativity, emotional skills, and growth mindset.
> Maka Kids licenses content directly from IP holders and individual creators. The startup is also partnering directly with studios and animators to produce original content.
> Every show on the platform goes through an analysis of pacing, stimulation levels, color contrast, and narrative structure. Its catalog features slower-paced, lower-stimulation content with genuine narrative arcs and stories from around the world.
> The duo believes an important factor often missing from the screen time debate for kids is how much the right story, delivered at the right moment, can positively support a young child.
> “Stories can support language development, emotional regulation, curiosity, and give kids a sense of how wide the world is,” Leta said. “Children’s media at its best is one of the most powerful developmental tools families have, when it’s designed with this intention. Most of the platforms children watch on today were designed for adult audiences, with a kids experience crudely bolted on as an afterthought. The incentive for the majority of kids’ streaming platforms is watch time, not well-being.”
> When parents create a profile for their child, they can select channels focused on a variety of topics, such as kindness, STEM, emotional regulation, or movement, and then set preferred session lengths. From there, Maka Kids delivers curated, developmentally vetted content tailored to those selections.
> The session then ends naturally, with wind-down cues from characters to help children calmly transition away from screen time without a meltdown.
> Maka Kids is running a private beta on iOS this summer and plans to launch publicly this fall on iPhone and iPad, with casting support via AirPlay. Maka Kids says it already has thousands of families on its waitlist.
> As for the startup’s business model, the app will operate on a subscription model, priced at $11.99 per month, with a discounted annual option.
> In terms of the new funding, the startup plans to use it to grow its catalog of vetted shows. The round was led by Michigan Rise, with participation from Union Heritage Ventures, Flybridge, Also Capital, Detroit Venture Partners, Song United, Invest Detroit, Ann Arbor Spark Capital, 84I90, Georgetown Gain, and Segal Ventures, as well as angel investors.
> “Longer term, our vision is to become the trust layer for every digital experience children have,” Sheinman said. “Embedded into games, edtech products, and shows, Maka Imprint can help developers align their products to what is actually good for kids and families. The kids category deserves a trusted industry standard, and that’s what we are buil

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0020 -->
## 020. edge-0020

**Triple:** Battery Ventures (ORG) —CO_INVESTED_WITH→ Seligman Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Article:** [AI chip maker SambaNova raises $1B at $11B valuation, 5 months after last mega round](https://techcrunch.com/2026/07/08/sambanova-draws-1b-at-11b-valuation-in-series-f-first-close/) | en | techcrunch.com
**Ngữ cảnh:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0021 -->
## 021. edge-0021

**Triple:** Starwood Capital (ORG) —INVESTED_IN→ Legora (ORG)
**Assertion status:** reported
**Evidence:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.

**Article:** [Legora reaches $5.55 billion valuation as AI legal tech boom endures](https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/) | en | techcrunch.com
**Ngữ cảnh:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.
> There are other signs that investors are bullish about AI legal tech. Legora’s Series D and valuation jump come just a few months after its October 2025 $150 million Series C round led at a $1.8 billion valuation. Its competitor, Harvey, which is backed by a16z, is already valued at $8 billion, and is now reportedly seeking to raise at an $11 bill

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0022 -->
## 022. edge-0022

**Triple:** IBM (ORG) —PARTNERED_WITH→ Ferrari (ORG)
**Assertion status:** reported
**Evidence:**
> In that time, Oracle became the title sponsor of Red Bull Racing team, the Mercedes-AMG Petronas F1 team struck a multi-year partnership with Microsoft, CoreWeave became Aston Martin Aramco’s official AI cloud partner, Anthropic began working with Williams Racing, Palantir and IBM partnered with Ferrari, AWS began providing data analytics to F1, and the audio app ElevenLabs and fintech Revolut have teamed up with Audi.

**Article:** [The hottest place for startups to strike a deal? The F1 paddock](https://techcrunch.com/2026/05/10/the-hottest-place-for-startups-to-strike-a-deal-the-f1-paddock/) | en | techcrunch.com
**Ngữ cảnh:**
> ts of folks missed Milken for F1 Miami.”
> F1 teams, once sponsored by major oil, tobacco, banks, and alcohol companies, have embraced the new railroad giants. The F1 team liveries this season — plastered with AI, cloud computing, and enterprise company logos — is a literal sign pointing to where the money is.
> The past five years reflects the shift. In that time, Oracle became the title sponsor of Red Bull Racing team, the Mercedes-AMG Petronas F1 team struck a multi-year partnership with Microsoft, CoreWeave became Aston Martin Aramco’s official AI cloud partner, Anthropic began working with Williams Racing, Palantir and IBM partnered with Ferrari, AWS began providing data analytics to F1, and the audio app ElevenLabs and fintech Revolut have teamed up with Audi.
> Some VC and PE firms also own stakes in F1 teams, including Dorilton Capital’s 2020 acquisition of Williams Racing and the 200-million-euro investment into Alpine by backers Otro Capital, RedBird Capital Partners, and Maximum Effort Investments.
> Hannan Happi, founder of the climate startup Exowatt, credits the 2020 Netflix F1 show “Drive to Surviv

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0023 -->
## 023. edge-0023

**Triple:** Oura (ORG) —AGREED_TO_ACQUIRE→ Counsel Health (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> Oura announced on Tuesday that it’s acquiring AI-native primary care company Counsel Health for $625 million.

**Article:** [Oura to acquire AI-native primary care startup Counsel Health for $625M](https://techcrunch.com/2026/11/10/oura-to-acquire-ai-native-primary-care-startup-counsel-health-for-625m/) | en | techcrunch.com
**Ngữ cảnh:**
> Oura announced on Tuesday that it’s acquiring AI-native primary care company Counsel Health for $625 million. The deal comes a few weeks after Oura postponed its up to $2.2 billion IPO indefinitely, citing “uncertainty in the IPO market.”
> Counsel Health is an AI-powered healthcare platform that combines a chat-based medical experience with access to licensed physicians. Its service was integrated into the Oura app in June.
> Users can connect with Counsel’s

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0024 -->
## 024. edge-0024

**Triple:** Celesta Capital (ORG) —FOUNDED→ India Deep Tech Alliance (ORG)
**Assertion status:** historical_reported
**Evidence:**
> In September, Silicon Valley- and India-based Celesta Capital spearheaded the launch of the India Deep Tech Alliance (IDTA) to bridge that gap, bringing together seven major U.S. and Indian investors — Accel, Blume Ventures, Premji Invest, Gaja Capital, Ideaspring Capital, Tenacity Ventures, and Venture Catalysts. The latest addition includes Indian venture firms Activate AI, Chiratae Ventures, InfoEdge Ventures, Kalaari Capital, Singularity Holdings, and YourNest Venture Capital.

**Article:** [Nvidia, Qualcomm join US, Indian VCs to help build India&#8217;s next deep tech startups](https://techcrunch.com/2025/11/04/nvidia-qualcomm-join-u-s-indian-vcs-to-help-build-indias-next-deep-tech-startups/) | en | techcrunch.com
**Ngữ cảnh:**
> satellites and electrifying transportation to designing semiconductors.
> The Indian government has sought to accelerate this shift as major economies race to secure technological sovereignty. Yet capital for such ventures remains scarce, as they require a longer gestation period than traditional sectors and most VCs favor proven, lower-risk models.
> In September, Silicon Valley- and India-based Celesta Capital spearheaded the launch of the India Deep Tech Alliance (IDTA) to bridge that gap, bringing together seven major U.S. and Indian investors — Accel, Blume Ventures, Premji Invest, Gaja Capital, Ideaspring Capital, Tenacity Ventures, and Venture Catalysts. The latest addition includes Indian venture firms Activate AI, Chiratae Ventures, InfoEdge Ventures, Kalaari Capital, Singularity Holdings, and YourNest Venture Capital.
> The coalition aims to invest capital and provide mentorship and network access to Indian deep tech startups over the next five to 10 years. It also plans to collaborate with the Indian government on its policy initiatives, including the recently introduced Research, Development and Innovation (RDI) scheme.
> “It’s a coalition of the willing, wanting

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0025 -->
## 025. edge-0025

**Triple:** SV Angel (ORG) —INVESTED_IN→ AI research lab (ORG)
**Assertion status:** reported
**Evidence:**
> humans& — $4.5 billion: This AI research lab, which focuses on creating AI that collaborates with humans, last raised a $480 million seed round led by SV Angel and Georges Harik, per Crunchbase.

**Article:** [Almost 90 new unicorns have been minted so far this year — here they are](https://techcrunch.com/2026/07/05/almost-40-new-unicorns-have-been-minted-so-far-this-year-here-they-are/) | en | techcrunch.com
**Ngữ cảnh:**
> rprises, according to PitchBook.
> Arena — $1.7 billion: This AI platform helps business leaders make decisions. It was founded in 2022 and last raised a $150 million Series A, valuing the company at $1.7 billion. The company has raised $250 million in funding to date, from investors including Andreessen Horowitz and Felicis, according to PitchBook.
> humans& — $4.5 billion: This AI research lab, which focuses on creating AI that collaborates with humans, last raised a $480 million seed round led by SV Angel and Georges Harik, per Crunchbase.
> webAI — $2.5 billion: This company lets organizations build their own private enterprise models. It was founded in 2019 and last raised an undisclosed Series A round, per PitchBook.
> Tandem — $1 billion: This company helps doctors effectively fill prescriptions. Founded in 2013, it last raised a $100 million Series B from investors including Accel,

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0026 -->
## 026. edge-0026

**Triple:** Volantis (ORG) —CO_INVESTED_WITH→ A&E Investment (ORG)
**Assertion status:** reported
**Evidence:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Article:** [AI chip maker SambaNova raises $1B at $11B valuation, 5 months after last mega round](https://techcrunch.com/2026/07/08/sambanova-draws-1b-at-11b-valuation-in-series-f-first-close/) | en | techcrunch.com
**Ngữ cảnh:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0027 -->
## 027. edge-0027

**Triple:** Corazon Capital (ORG) —CO_INVESTED_WITH→ BAM Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> The company raised $6.2 million in funding in a round led by Chicago Ventures, with participation from BAM Ventures, Aglaé Ventures, Corazon Capital, Press On Ventures, Tusk Ventures, Yonder Ventures, Rule 30, and Brown Angel Group.

**Article:** [Siri co-founder backs Helix for its voice ID tech](https://techcrunch.com/2026/11/11/siri-co-founder-backs-helix-for-its-voice-id-tech/) | en | techcrunch.com
**Ngữ cảnh:**
> otos or videos to verify users’ identities. Now, a startup called Helix is betting that voice technology can do the same job, without requiring users to hand over sensitive personal information.
> The voice technology, which can run directly on a user’s device, has attracted backing from Siri co-founder Dag Kittlaus, who will also act as an adviser.
> The company raised $6.2 million in funding in a round led by Chicago Ventures, with participation from BAM Ventures, Aglaé Ventures, Corazon Capital, Press On Ventures, Tusk Ventures, Yonder Ventures, Rule 30, and Brown Angel Group.
> The startup was founded by Alex Oberg, Anna Dorofiyenko, and Mike Hall in 2025. Oberg previously worked at Ticketmaster, which acquired his startup; Dorofiyenko led data science teams at Live Nation and Zillow; and Hall has worked at Nike and Tinder, where he helped develop the initial matching algorithm.
> At Ticketmaster, Oberg played a role in cr

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0028 -->
## 028. edge-0028

**Triple:** China Railway Sixth Group Viet Nam Company Limited (ORG) —PART_OF→ Cát Linh–Hà Đông Urban Railway Project (PROJECT)
**Assertion status:** reported
**Evidence:**
> Zhang Qiang, general director of China Railway Sixth Group Viet Nam Company Limited, said his company had participated in the Cát Linh – Hà Đông urban railway project, Việt Nam's first urban rail line, under an engineering, procurement, and construction contract.

**Article:** [HCM City welcomes Chinese investments in logistics](https://vietnamnews.vn/economy/1803189/hcm-city-welcomes-chinese-investments-in-logistics.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> id Chinese agricultural suppliers, Vietnamese importers, seaports, and logistics companies could establish long-term partnerships to improve efficiency and reduce cargo handling times.
> 
> She called on authorities in both countries to facilitate business cooperation, improve transport connections beyond ports, and simplify import-export procedures.
> 
> Zhang Qiang, general director of China Railway Sixth Group Viet Nam Company Limited, said his company had participated in the Cát Linh – Hà Đông urban railway project, Việt Nam's first urban rail line, under an engineering, procurement, and construction contract.
> 
> "It serves as clear proof that Chinese rail transit technology, construction standards, and equipment are fully capable of adapting to the complex urban environment of Việt Nam."
> 
> He described how the company had adapted the project to Việt Nam's climate, environmental conditions, and urban landscape.
> 
> It had also worked closely with Hanoi Metro 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0029 -->
## 029. edge-0029

**Triple:** Iconiq (ORG) —CO_INVESTED_WITH→ Nikesh Arora (PERSON)
**Assertion status:** reported
**Evidence:**
> The round was led by Iconiq’s Murali Joshi, who helped lead the firm’s investments in companies like Anthropic, Datadog, Drata, 1Password, among others.
> Angels who invested include Microsoft CEO Satya Nadella; Palo Alto Networks CEO Nikesh Arora; Pershing Square Holdings CEO Bill Ackman; Palantir CTO Shyam Sankar; Anduril co-founder Trae Stephens; Former OpenAI VP Bob McGrew; Vercel CEO Guillermo Rauch, and Former AT&T CEO John Donovan. Whew!

**Article:** [AI security startup Outtake raises $40M from Iconiq, Satya Nadella, Bill Ackman, and other big names](https://techcrunch.com/2026/01/28/ai-security-startup-outtake-raises-40m-from-iconiq-satya-nadella-bill-ackman-and-other-big-names/) | en | techcrunch.com
**Ngữ cảnh:**
> Outtake, which makes an agentic cybersecurity platform to help enterprises detect, investigate, and take down identity fraud, has raised a $40 million Series B round of funding.
> While that might not sound like a lot given the huge sums some AI companies are raising, the names involved in this financing reads like a tech industry who’s who.
> The round was led by Iconiq’s Murali Joshi, who helped lead the firm’s investments in companies like Anthropic, Datadog, Drata, 1Password, among others.
> Angels who invested include Microsoft CEO Satya Nadella; Palo Alto Networks CEO Nikesh Arora; Pershing Square Holdings CEO Bill Ackman; Palantir CTO Shyam Sankar; Anduril co-founder Trae Stephens; Former OpenAI VP Bob McGrew; Vercel CEO Guillermo Rauch, and Former AT&T CEO John Donovan. Whew!
> The reason for the excitement? Outtake, founded in 2023 by a former Palantir engineer, Alex Dhillon, has found a way to automate what has largely been the manual problem of spotting and taking down digital identity posers: impersonation accounts, malicious domains posing as the company’s, rogue apps, fraudulent ads, and more. This problem has grow

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0030 -->
## 030. edge-0030

**Triple:** TPG (ORG) —CO_INVESTED_WITH→ Dragoneer Investment Group (ORG)
**Assertion status:** reported
**Evidence:**
> ChatGPT-maker OpenAI has raised $8.3 billion at a $300 billion valuation, reports The New York Times. The deal is part of OpenAI’s broader strategy to secure $40 billion this year.
> The oversubscribed round came months ahead of schedule, per the NYT. OpenAI initially raised $2.5 billion from VC firms in March when it announced its intention to raise $40 billion in a round spearheaded by SoftBank. The AI giant had planned to take on an additional $7.5 billion by the end of the year, but beat itself to the punch as investors clamber to get onto its cap table amid impressive growth.
> On Thursday, The Information reported OpenAI hit $12 billion in annualized revenue and surpassed 700 million ChatGPT weekly active users. The Times today said that the number is closer to $13 billion, with projections to reach $20 billion by the end of the year. Other tailwinds include the Trump administration’s AI Action Plan and talks with Microsoft that could help the startup reach its goal of becoming a true for-profit company.
> The Times reported that Dragoneer Investment Group, an under-the-radar investor, led the round with a startling $2.8 billion check. Many new investors participated in the round, including private equity giants Blackstone and TPG, and mutual fund manager T. Rowe Price. Other participants include Altimeter Capital, Andreessen Horowitz, Coatue Management, D1 Capital Partners, Fidelity Management, Founders Fund, Sequoia Capital, Tiger Global, and Thrive Capital.

**Article:** [OpenAI reportedly raises $8.3B at $300B valuation](https://techcrunch.com/2025/08/01/openai-reportedly-raises-8-3b-at-300b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> ChatGPT-maker OpenAI has raised $8.3 billion at a $300 billion valuation, reports The New York Times. The deal is part of OpenAI’s broader strategy to secure $40 billion this year.
> The oversubscribed round came months ahead of schedule, per the NYT. OpenAI initially raised $2.5 billion from VC firms in March when it announced its intention to raise $40 billion in a round spearheaded by SoftBank. The AI giant had planned to take on an additional $7.5 billion by the end of the year, but beat itself to the punch as investors clamber to get onto its cap table amid impressive growth.
> On Thursday, The Information reported OpenAI hit $12 billion in annualized revenue and surpassed 700 million ChatGPT weekly active users. The Times today said that the number is closer to $13 billion, with projections to reach $20 billion by the end of the year. Other tailwinds include the Trump administration’s AI Action Plan and talks with Microsoft that could help the startup reach its goal of becoming a true for-profit company.
> The Times reported that Dragoneer Investment Group, an under-the-radar investor, led the round with a startling $2.8 billion check. Many new investors participated in the round, including private equity giants Blackstone and TPG, and mutual fund manager T. Rowe Price. Other participants include Altimeter Capital, Andreessen Horowitz, Coatue Management, D1 Capital Partners, Fidelity Management, Founders Fund, Sequoia Capital, Tiger Global, and Thrive Capital.
> Some early investors in OpenAI were reportedly dismayed by the smaller allocations they got in the round as the AI behemoth prioritized bringing on new strategic backers.
> TechCrunch has reached out to OpenAI for comment.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0031 -->
## 031. edge-0031

**Triple:** Yodar Shafrir (PERSON) —FOUNDED→ ScaleOps (ORG)
**Assertion status:** reported
**Evidence:**
> ScaleOps was co-founded in 2022 by Yodar Shafrir, a former engineer at Run:ai, a GPU orchestration startup acquired by Nvidia, after seeing firsthand how difficult it was for companies to manage increasingly complex AI workloads. While tools like Kubernetes help run applications across large clusters of machines, they often rely on static configurations that struggle to keep up with fast-changing demand, leading to underused GPUs, performance issues, and costly inefficiencies.

**Article:** [ScaleOps raises $130M to improve computing efficiency amid AI demand](https://techcrunch.com/2026/03/30/scaleops-130m-series-c-kubernetes-efficiency-ai-demand-funding/) | en | techcrunch.com
**Ngữ cảnh:**
> sed $130 million at an $800 million valuation, ScaleOps said Monday. The Series C funding round was led by Insight Partners, with participation from existing investors, including Lightspeed Venture Partners, NFX, Glilot Capital Partners, and Picture Capital. The company says its software reduces cloud and AI infrastructure costs by as much as 80%.
> ScaleOps was co-founded in 2022 by Yodar Shafrir, a former engineer at Run:ai, a GPU orchestration startup acquired by Nvidia, after seeing firsthand how difficult it was for companies to manage increasingly complex AI workloads. While tools like Kubernetes help run applications across large clusters of machines, they often rely on static configurations that struggle to keep up with fast-changing demand, leading to underused GPUs, performance issues, and costly inefficiencies.
> “As part of my role [at Run:ai], I met many customers, especially DevOps teams,” Shafrir, who is the company’s CEO, told TechCrunch. “While they really liked what Run:ai provided, they still struggled to manage their production workloads, especially as inference workloads became more common in the AI era. When I zoomed out, I realized the problem 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0032 -->
## 032. edge-0032

**Triple:** Elad Gil (ORG) —INVESTED_IN→ Mistral (ORG)
**Assertion status:** reported
**Evidence:**
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
> nd led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.
> Microsoft’s $16.3 million convertible investment in Mistral as part of a partnership announced in February 2024 was presented as a Series A extension, implying an unchanged valuation.
> In June 2024, Mistral raised €600 million (about $640 million) in a mix of equity and debt. The long-rumored round was led by General Catalyst at a $6 billion valuat

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0033 -->
## 033. edge-0033

**Triple:** BoxGroup (ORG) —CO_INVESTED_WITH→ SoftBank Vision Fund 2 (ORG)
**Assertion status:** reported
**Evidence:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.

**Article:** [Helion, the Sam Altman-backed fusion startup, raises $465M to build a power plant for Microsoft](https://techcrunch.com/2026/06/04/helion-the-sam-altman-backed-fusion-startup-raises-465m-to-build-a-power-plant-for-microsoft/) | en | techcrunch.com
**Ngữ cảnh:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.
> Helion’s approach to fusion power differs from many of its peers. Some use magnets to contain the superheated plasma required for fusion conditions, while others use lasers to compress fusion fuel until it reacts. In both cases, the majority of startups plan to use steam turbines to transform the intense heat into electricity.
> But Helion, which us

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0034 -->
## 034. edge-0034

**Triple:** JCDecaux Holding (ORG) —CO_INVESTED_WITH→ Lightspeed Venture Partners (ORG)
**Assertion status:** reported
**Evidence:**
> In June 2023, just one month after being founded, Mistral AI raised a record $113 million seed round led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
> rmy and job agency, Luxembourg, shipping giant CMA, German defense tech startup Helsing, IBM, Orange, and Stellantis.
> How much funding has Mistral AI raised to date?
> Most of Mistral AI’s funding to date was debt financing, but the company has also raised several venture funding rounds, with a grand total around $4 billion, according to Crunchbase.
> In June 2023, just one month after being founded, Mistral AI raised a record $113 million seed round led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.
> Microsoft’s $16.3 million convertible investment 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0035 -->
## 035. edge-0035

**Triple:** Redpoint Ventures (ORG) —CO_INVESTED_WITH→ Bain Capital Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.

**Article:** [Kevin Mandia&#8217;s new &#8216;agent swarm&#8217; security startup Armadin raises $255.5M at $2.5B valuation](https://techcrunch.com/2026/10/01/kevin-mandias-new-agent-swarm-security-startup-armadin-raises-255-5m-at-2-5b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.
> The new round comes just six months after Armadin raised a $190 million Series A in March. It has now raised more than $445 million.
> Armadin is offering enterprises a new kind of always-on security by reimagining defense testing for the AI era. Instead of traditional penetration tests, where hired guns attempt to break in and report on the weaknes

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0036 -->
## 036. edge-0036

**Triple:** Notable Capital (ORG) —CO_INVESTED_WITH→ Iconiq (ORG)
**Assertion status:** reported
**Evidence:**
> In a sea of massive valuations for early-stage AI startups, today we have a bit of rare news: a jumbo round and valuation step-up for an e-commerce company. Quince announced on Wednesday that it raised a $500 million Series E round at a $10.1 billion valuation.
> The round was led by previous investor Iconiq, which also led Quince’s $200 million Series D in early 2025 at a reported $4.5 billion valuation. That’s more than double the valuation in less than a year.
> Quince rose to fame on Instagram with its $50 cashmere sweater, but has since amassed a wider range of product offerings, including apparel, home, accessories, beauty, and wellness. Unlike typical e-commerce retail sites, the company manufactures its products and sells them to consumers directly.
> Quince, which launched out of beta in 2020, calls its business model “manufacturer-to-consumer.” And because it owns most of its own tech stack and controls its designs and manufacturing, Quince can more accurately predict its sales, according to a blog post by Iconiq. This allows smaller batch manufacturing with less waste.
> Quince and its investors argue that, unlike fast fashion, Quince can produce higher-quality products at low costs.
> Not that the company has been without controversy. It has faced several lawsuits from brands alleging Quince is selling dupes of their designs. Coach parent Tapestry is suing, as is Williams Sonoma, Puck reported. Deckers also sued over footwear designs, but a court ruled in Quince’s favor.
> If such scuffles have given Quince a copycat reputation, as Puck describes, the site’s customers are apparently unphased. The company says that its top-line revenue has now surpassed $1 billion. In January, it also expanded to Canada.
> Other participating investors include Basis Set Ventures, Wellington Management, WndrCo, MarcyPen Capital Partners, Ballie Gifford, Notable Capital, and DST Global.

**Article:** [Quince hits $10B valuation with giant $500M round led by Iconiq](https://techcrunch.com/2026/03/11/quince-series-e-10b-valuation-with-500m-round-led-by-iconiq/) | en | techcrunch.com
**Ngữ cảnh:**
> In a sea of massive valuations for early-stage AI startups, today we have a bit of rare news: a jumbo round and valuation step-up for an e-commerce company. Quince announced on Wednesday that it raised a $500 million Series E round at a $10.1 billion valuation.
> The round was led by previous investor Iconiq, which also led Quince’s $200 million Series D in early 2025 at a reported $4.5 billion valuation. That’s more than double the valuation in less than a year.
> Quince rose to fame on Instagram with its $50 cashmere sweater, but has since amassed a wider range of product offerings, including apparel, home, accessories, beauty, and wellness. Unlike typical e-commerce retail sites, the company manufactures its products and sells them to consumers directly.
> Quince, which launched out of beta in 2020, calls its business model “manufacturer-to-consumer.” And because it owns most of its own tech stack and controls its designs and manufacturing, Quince can more accurately predict its sales, according to a blog post by Iconiq. This allows smaller batch manufacturing with less waste.
> Quince and its investors argue that, unlike fast fashion, Quince can produce higher-quality products at low costs.
> Not that the company has been without controversy. It has faced several lawsuits from brands alleging Quince is selling dupes of their designs. Coach parent Tapestry is suing, as is Williams Sonoma, Puck reported. Deckers also sued over footwear designs, but a court ruled in Quince’s favor.
> If such scuffles have given Quince a copycat reputation, as Puck describes, the site’s customers are apparently unphased. The company says that its top-line revenue has now surpassed $1 billion. In January, it also expanded to Canada.
> Other participating investors include Basis Set Ventures, Wellington Management, WndrCo, MarcyPen Capital Partners, Ballie Gifford, Notable Capital, and DST Global.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0037 -->
## 037. edge-0037

**Triple:** Databricks Ventures (ORG) —INVESTED_IN→ Replit (ORG)
**Assertion status:** reported
**Evidence:**
> Vibe-coding sensation Replit has hit another funding milestone. The company announced Wednesday that it raised a $400 million Series D at a $9 billion valuation, led by previous investor Georgian Partners. Other participating investors include G Squared, Prysm Capital, Coatue, Andreessen Horowitz, Craft Ventures, Y Combinator, Accenture Ventures, Okta Ventures, and Databricks Ventures.

**Article:** [Replit snags $9B valuation 6 months after hitting $3B](https://techcrunch.com/2026/03/11/replit-snags-9b-valuation-6-months-after-hitting-3b/) | en | techcrunch.com
**Ngữ cảnh:**
> Vibe-coding sensation Replit has hit another funding milestone. The company announced Wednesday that it raised a $400 million Series D at a $9 billion valuation, led by previous investor Georgian Partners. Other participating investors include G Squared, Prysm Capital, Coatue, Andreessen Horowitz, Craft Ventures, Y Combinator, Accenture Ventures, Okta Ventures, and Databricks Ventures.
> Founder and CEO Amjad Masad also said in a post on X that backers include angel investors Shaquille O’Neal and Jared Leto.
> This follows the $3 billion valuation the startup hit in September, when it raised a $250 million round. At that time, Replit said it was on track for $150 million in annualized revenue. Replit did not release updated, current

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0038 -->
## 038. edge-0038

**Triple:** Craft Ventures (ORG) —INVESTED_IN→ 8090 Labs (ORG)
**Assertion status:** reported
**Evidence:**
> The company, 8090 Labs, closed a $135 million round led by Salesforce Ventures with participation from Jeffrey Katzenberg’s WndrCo; David Sacks’ Craft Ventures; fellow All-In hosts and “besties” David Friedberg (The Production Board) and Jason Calacanis (Launch); and angel investors like Palo Alto Networks CEO Nikesh Arora and Quora CEO Adam D’Angelo.

**Article:** [Chamath Palihapitiya raises $135M Series A for his AI coding startup, takes CEO role](https://techcrunch.com/2026/06/29/chamath-palihapitiya-raises-135m-series-a-for-his-ai-coding-startup-takes-ceo-role/) | en | techcrunch.com
**Ngữ cảnh:**
> Chamath Palihapitiya, best known for his venture capital firm Social Capital and the All-In podcast, announced Monday that the AI coding startup he founded raised a sizable Series A.
> The company, 8090 Labs, closed a $135 million round led by Salesforce Ventures with participation from Jeffrey Katzenberg’s WndrCo; David Sacks’ Craft Ventures; fellow All-In hosts and “besties” David Friedberg (The Production Board) and Jason Calacanis (Launch); and angel investors like Palo Alto Networks CEO Nikesh Arora and Quora CEO Adam D’Angelo.
> Palihapitiya founded 8090 Labs in January 2024 to offer an AI coding agent specifically for corporate programming teams. Its product, Software Factory, helps corporate coders use AI to build production-quality software, not just vibe-coded prototypes, with all the controls enterprises need, such as audit trails, the company promises.
> With the rais

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0039 -->
## 039. edge-0039

**Triple:** Elad Gil (PERSON) —INVESTED_IN→ Mistral AI (ORG)
**Assertion status:** reported
**Evidence:**
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
> nd led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.
> Microsoft’s $16.3 million convertible investment in Mistral as part of a partnership announced in February 2024 was presented as a Series A extension, implying an unchanged valuation.
> In June 2024, Mistral raised €600 million (about $640 million) in a mix of equity and debt. The long-rumored round was led by General Catalyst at a $6 billion valuat

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0040 -->
## 040. edge-0040

**Triple:** Geodesic Capital (ORG) —INVESTED_IN→ Portal (ORG)
**Assertion status:** reported
**Evidence:**
> Portal, founded in 2021, announced a $50 million Series A funding round Thursday that values the company at $250 million. The round was led by Geodesic Capital and Mach33, alongside Booz Allen Ventures, ARK Invest, AlleyCorp, and FUSE.

**Article:** [This founder helped build SpaceX&#8217;s most powerful rocket engine. Now he&#8217;s building a &#8216;fighter jet for orbit.&#8217;](https://techcrunch.com/2026/04/09/portal-raises-50-million-to-build-a-new-kind-of-high-power-rocket-engine/) | en | techcrunch.com
**Ngữ cảnh:**
> Jeff Thornburg helped turn a government research project into SpaceX’s most powerful rocket engine. Now, he’s trying to do the same thing at his startup Portal Space Systems, which is taking an idea set aside by NASA and turning it into high-powered propulsion for the next generation of spacecraft.
> Portal, founded in 2021, announced a $50 million Series A funding round Thursday that values the company at $250 million. The round was led by Geodesic Capital and Mach33, alongside Booz Allen Ventures, ARK Invest, AlleyCorp, and FUSE.
> The company is developing a technology called solar thermal propulsion. Today’s standard satellite engines either burn chemical fuel or convert the sun’s energy to electricity, using that to power efficient but low-powered thrusters. Portal’s engines would instead concentrate the heat of the sun, using that to heat propellant and move the spacecra

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0041 -->
## 041. edge-0041

**Triple:** Dario Amodei (PERSON) —CEO_OF→ Anthropic (ORG)
**Assertion status:** reported
**Evidence:**
> The seven co-founders are Dario Amodei, CEO; Daniela Amodei, president and chair of the board; Tom Brown, chief compute officer; Jack Clark, head of public benefit; Jared Kaplan, chief science officer (pictured above); Sam McCandlish, chief architect; and Christopher Olah, interpretability research lead.

**Article:** [All 7 Anthropic founders will each cash out about $250M in IPO](https://techcrunch.com/2026/11/10/all-7-anthropic-founders-will-each-cash-out-about-250m-in-ipo/) | en | techcrunch.com
**Ngữ cảnh:**
> ever, in an IPO as eagerly anticipated as this one, companies can often price shares above the initial range.
> The S-1 is already hinting at high demand. Board member Reed Hastings has indicated he wants to buy $300 million worth of shares through his donor-advised fund. Board member Christopher Liddell also wants to buy $3 million worth of shares.
> The seven co-founders are Dario Amodei, CEO; Daniela Amodei, president and chair of the board; Tom Brown, chief compute officer; Jack Clark, head of public benefit; Jared Kaplan, chief science officer (pictured above); Sam McCandlish, chief architect; and Christopher Olah, interpretability research lead.
> After the sale, each of them will own about 3.2% of the total outstanding Class A shares, the S-1 says, or roughly 22% collectively. That’s not their share of the company overall. Class A is just one of Anthropic’s share classes, and other holders, including Amazon and Google, hold nonvoting Class N shares, so the founders’ stake in the company’s 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0042 -->
## 042. edge-0042

**Triple:** Altimeter Capital (ORG) —CO_INVESTED_WITH→ Deutsche Telekom Capital Partners (ORG)
**Assertion status:** reported
**Evidence:**
> AI chip startup Groq confirmed Wednesday that it raised a fresh $750 million in funding at a post-money valuation of $6.9 billion.
> This topped the rumored numbers when word leaked in July that Groq was raising. At that time, reports suggested that the raise would be about $600 million, at near a $6 billion valuation.
> Groq, which also sells data center computing power, previously raised $640 million at a $2.8 billion valuation in August 2024, making this more than double the valuation in about a year. Groq has now raised over $3 billion to date, PitchBook estimates.
> Groq has been a hot commodity because it is working on breaking the chokehold that AI chip maker Nvidia has over the tech industry. Groq’s chips are not GPUs, the graphics processing units that typically power AI systems. Instead, Groq calls them LPUs (language processing units) and calls its hardware an inference engine — specialized computers optimized for running AI models quickly and efficiently.
> Its products are geared toward developers and enterprises, available as either a cloud service or an on-premises hardware cluster. The on-prem hardware is a server rack outfitted with a stack of its integrated hardware/software nodes. Both the cloud and on-prem hardware run open versions of popular models, like those from Meta, DeepSeek, Qwen, Mistral, Google, and OpenAI. Groq says its offerings maintain, or in some cases improve, AI performance at significantly less cost than alternatives.
> Groq’s founder, Jonathan Ross, has a particularly relevant pedigree for this work. Ross previously worked at Google developing its Tensor Processing Unit chip, which are specialized processors designed for machine learning tasks. The TPU was announced in 2016, the same year Groq emerged from stealth. TPUs still power Google Cloud’s AI services.
> Groq says it now powers the AI apps of more than 2 million developers, up from 356,000 developers when the company talked to TechCrunch a year ago.
> The new round was led by investment firm Disruptive, with additional funding from BlackRock, Neuberger Berman, Deutsche Telekom Capital Partners, and others. Existing investors, including Samsung, Cisco, D1, and Altimeter, also joined the round.

**Article:** [Nvidia AI chip challenger Groq raises even more than expected, hits $6.9B valuation](https://techcrunch.com/2025/09/17/nvidia-ai-chip-challenger-groq-raises-even-more-than-expected-hits-6-9b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> AI chip startup Groq confirmed Wednesday that it raised a fresh $750 million in funding at a post-money valuation of $6.9 billion.
> This topped the rumored numbers when word leaked in July that Groq was raising. At that time, reports suggested that the raise would be about $600 million, at near a $6 billion valuation.
> Groq, which also sells data center computing power, previously raised $640 million at a $2.8 billion valuation in August 2024, making this more than double the valuation in about a year. Groq has now raised over $3 billion to date, PitchBook estimates.
> Groq has been a hot commodity because it is working on breaking the chokehold that AI chip maker Nvidia has over the tech industry. Groq’s chips are not GPUs, the graphics processing units that typically power AI systems. Instead, Groq calls them LPUs (language processing units) and calls its hardware an inference engine — specialized computers optimized for running AI models quickly and efficiently.
> Its products are geared toward developers and enterprises, available as either a cloud service or an on-premises hardware cluster. The on-prem hardware is a server rack outfitted with a stack of its integrated hardware/software nodes. Both the cloud and on-prem hardware run open versions of popular models, like those from Meta, DeepSeek, Qwen, Mistral, Google, and OpenAI. Groq says its offerings maintain, or in some cases improve, AI performance at significantly less cost than alternatives.
> Groq’s founder, Jonathan Ross, has a particularly relevant pedigree for this work. Ross previously worked at Google developing its Tensor Processing Unit chip, which are specialized processors designed for machine learning tasks. The TPU was announced in 2016, the same year Groq emerged from stealth. TPUs still power Google Cloud’s AI services.
> Groq says it now powers the AI apps of more than 2 million developers, up from 356,000 developers when the company talked to TechCrunch a year ago.
> The new round was led by investment firm Disruptive, with additional funding from BlackRock, Neuberger Berman, Deutsche Telekom Capital Partners, and others. Existing investors, including Samsung, Cisco, D1, and Altimeter, also joined the round.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0043 -->
## 043. edge-0043

**Triple:** K5 Global (ORG) —CO_INVESTED_WITH→ Eniac Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> “My whole life has been preparing me for this moment,” Ben Sanders said when asked about why he launched his emergency response startup Hyper. The company announced Monday a $6.3 million seed round led by Eniac Ventures, as well as an official emergence from stealth.
> As a child, he so wanted to become a police officer that he had his mother sew yellow stripes on his navy sweatpants. He wore that with an officer’s rain hat for an entire year. As he grew up, he worked at the intersection of tech and government and once ran for federal office.
> Around a year ago, he read a news article about how his hometown was looking to use AI to reduce the wait time for emergency services. Sanders, who once launched an AI voice for drive-through restaurants, suddenly had an idea. Though he didn’t think AI was quite ready to help with 911 calls, he felt this was a space for innovation, especially after realizing that most calls made to the emergency line are not considered emergency calls at all.
> Sanders teamed up with his friend Damian McCabe. The duo officially launched Hyper on Monday, offering an AI voice company that can handle some 911 calls. Sanders, who is CEO, said the product is to deal with the non-emergency calls that take time away from those critical calls that determine the “difference between life and death.” McCabe is the company’s CPO.
> Right now, even if a person looked to call their local police department, they would most often find a 10-digit number that routes them to the same people who take 911 calls.
> “Imagine getting stuck talking to someone for eight minutes about a neighbor’s dog barking, only to answer the next call late, because of that noise complaint, and hear the trembling voice of a 5-year-old whose dad has just collapsed on the floor,” Sanders said.
> Hyper answers questions, texts links, forwards calls, and even takes non-emergency police reports. “Hyper always plays it safe, so if any calls fall outside the approved scope, or if one sounds slightly more emergency, we can automatically escalate those to a human expert just in case.”
> Sanders described the fundraising process as “frenetic, manic, and fast.” It took him less than two months to raise the whole round, which was ultimately oversubscribed and included follow-on capital. Ripple Ventures, GreatPoint Ventures, VSC Ventures, Tusk Venture Partners, and K5 Global also participated in the round. Sanders said he met his connection at Eniac Ventures through a mutual acquaintance.

**Article:** [AI voice company Hyper raises $6.3M to help automate 911 calls](https://techcrunch.com/2025/07/21/ai-voice-company-hyper-raises-6-3m-to-help-automate-911-calls/) | en | techcrunch.com
**Ngữ cảnh:**
> “My whole life has been preparing me for this moment,” Ben Sanders said when asked about why he launched his emergency response startup Hyper. The company announced Monday a $6.3 million seed round led by Eniac Ventures, as well as an official emergence from stealth.
> As a child, he so wanted to become a police officer that he had his mother sew yellow stripes on his navy sweatpants. He wore that with an officer’s rain hat for an entire year. As he grew up, he worked at the intersection of tech and government and once ran for federal office.
> Around a year ago, he read a news article about how his hometown was looking to use AI to reduce the wait time for emergency services. Sanders, who once launched an AI voice for drive-through restaurants, suddenly had an idea. Though he didn’t think AI was quite ready to help with 911 calls, he felt this was a space for innovation, especially after realizing that most calls made to the emergency line are not considered emergency calls at all.
> Sanders teamed up with his friend Damian McCabe. The duo officially launched Hyper on Monday, offering an AI voice company that can handle some 911 calls. Sanders, who is CEO, said the product is to deal with the non-emergency calls that take time away from those critical calls that determine the “difference between life and death.” McCabe is the company’s CPO.
> Right now, even if a person looked to call their local police department, they would most often find a 10-digit number that routes them to the same people who take 911 calls.
> “Imagine getting stuck talking to someone for eight minutes about a neighbor’s dog barking, only to answer the next call late, because of that noise complaint, and hear the trembling voice of a 5-year-old whose dad has just collapsed on the floor,” Sanders said.
> Hyper answers questions, texts links, forwards calls, and even takes non-emergency police reports. “Hyper always plays it safe, so if any calls fall outside the approved scope, or if one sounds slightly more emergency, we can automatically escalate those to a human expert just in case.”
> Sanders described the fundraising process as “frenetic, manic, and fast.” It took him less than two months to raise the whole round, which was ultimately oversubscribed and included follow-on capital. Ripple Ventures, GreatPoint Ventures, VSC Ventures, Tusk Venture Partners, and K5 Global also participated in the round. Sanders said he met his connection at Eniac Ventures through a mutual acquaintance.
> Hyper hopes to use the fresh capital to help scale across the country, integrate more into existing 911 systems, hire a head of engineering, and build its next product. There is some competition in this space, like Aurelian, which also sorts non-emergency calls. Sanders said what makes Hyper different from the rest is its focus on 911.
> “We train o

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0044 -->
## 044. edge-0044

**Triple:** Wellington Management (ORG) —CO_INVESTED_WITH→ Iconiq (ORG)
**Assertion status:** reported
**Evidence:**
> In a sea of massive valuations for early-stage AI startups, today we have a bit of rare news: a jumbo round and valuation step-up for an e-commerce company. Quince announced on Wednesday that it raised a $500 million Series E round at a $10.1 billion valuation.
> The round was led by previous investor Iconiq, which also led Quince’s $200 million Series D in early 2025 at a reported $4.5 billion valuation. That’s more than double the valuation in less than a year.
> Quince rose to fame on Instagram with its $50 cashmere sweater, but has since amassed a wider range of product offerings, including apparel, home, accessories, beauty, and wellness. Unlike typical e-commerce retail sites, the company manufactures its products and sells them to consumers directly.
> Quince, which launched out of beta in 2020, calls its business model “manufacturer-to-consumer.” And because it owns most of its own tech stack and controls its designs and manufacturing, Quince can more accurately predict its sales, according to a blog post by Iconiq. This allows smaller batch manufacturing with less waste.
> Quince and its investors argue that, unlike fast fashion, Quince can produce higher-quality products at low costs.
> Not that the company has been without controversy. It has faced several lawsuits from brands alleging Quince is selling dupes of their designs. Coach parent Tapestry is suing, as is Williams Sonoma, Puck reported. Deckers also sued over footwear designs, but a court ruled in Quince’s favor.
> If such scuffles have given Quince a copycat reputation, as Puck describes, the site’s customers are apparently unphased. The company says that its top-line revenue has now surpassed $1 billion. In January, it also expanded to Canada.
> Other participating investors include Basis Set Ventures, Wellington Management, WndrCo, MarcyPen Capital Partners, Ballie Gifford, Notable Capital, and DST Global.

**Article:** [Quince hits $10B valuation with giant $500M round led by Iconiq](https://techcrunch.com/2026/03/11/quince-series-e-10b-valuation-with-500m-round-led-by-iconiq/) | en | techcrunch.com
**Ngữ cảnh:**
> In a sea of massive valuations for early-stage AI startups, today we have a bit of rare news: a jumbo round and valuation step-up for an e-commerce company. Quince announced on Wednesday that it raised a $500 million Series E round at a $10.1 billion valuation.
> The round was led by previous investor Iconiq, which also led Quince’s $200 million Series D in early 2025 at a reported $4.5 billion valuation. That’s more than double the valuation in less than a year.
> Quince rose to fame on Instagram with its $50 cashmere sweater, but has since amassed a wider range of product offerings, including apparel, home, accessories, beauty, and wellness. Unlike typical e-commerce retail sites, the company manufactures its products and sells them to consumers directly.
> Quince, which launched out of beta in 2020, calls its business model “manufacturer-to-consumer.” And because it owns most of its own tech stack and controls its designs and manufacturing, Quince can more accurately predict its sales, according to a blog post by Iconiq. This allows smaller batch manufacturing with less waste.
> Quince and its investors argue that, unlike fast fashion, Quince can produce higher-quality products at low costs.
> Not that the company has been without controversy. It has faced several lawsuits from brands alleging Quince is selling dupes of their designs. Coach parent Tapestry is suing, as is Williams Sonoma, Puck reported. Deckers also sued over footwear designs, but a court ruled in Quince’s favor.
> If such scuffles have given Quince a copycat reputation, as Puck describes, the site’s customers are apparently unphased. The company says that its top-line revenue has now surpassed $1 billion. In January, it also expanded to Canada.
> Other participating investors include Basis Set Ventures, Wellington Management, WndrCo, MarcyPen Capital Partners, Ballie Gifford, Notable Capital, and DST Global.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0045 -->
## 045. edge-0045

**Triple:** Earlybird (ORG) —INVESTED_IN→ Marvel Fusion (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The inertial confinement fusion startup is building a demonstration facility in collaboration with Colorado State University, which it expects to have operational by 2027. Munich-based Marvel has raised a total of $208 million from investors, including b2venture, Deutsche Telekom, Earlybird, and HV Capital with Taavet Hinrikus and Albert Wenger as angels.

**Article:** [Every fusion startup that has raised over $100M](https://techcrunch.com/2026/08/15/every-fusion-startup-that-has-raised-over-100m/) | en | techcrunch.com
**Ngữ cảnh:**
> eded to kick them off. Marvel fires powerful lasers at a target embedded with silicon nanostructures that cascade under the bombardment, compressing the fuel to the point of ignition. Because the target is made using silicon, it should be relatively simple to manufacture, leaning on the semiconductor manufacturing industry’s decades of experience.
> The inertial confinement fusion startup is building a demonstration facility in collaboration with Colorado State University, which it expects to have operational by 2027. Munich-based Marvel has raised a total of $208 million from investors, including b2venture, Deutsche Telekom, Earlybird, and HV Capital with Taavet Hinrikus and Albert Wenger as angels.
> Stellarator startup Type One Energy is planning to build a fusion reactor on the site of a retired Tennessee Valley Authority (TVA) coal power plant. The magnetic confinement device is expected to generate 350 megawatts of electricity, and the company hopes to bring it online by the mid-2030s.
> Unlike other fusion startups, Type One plans to sell k

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0046 -->
## 046. edge-0046

**Triple:** CPE Yuanfeng (ORG) —CO_INVESTED_WITH→ Tsinghua Capital (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Moonshot AI, the Beijing-based AI lab developing the popular Kimi series of open-weight large language models, has raised about $2 billion at a valuation of $20 billion, according to a post by Huafeng Capital, which advised some investors who participated in the round.
> The round was led by Chinese food delivery company Meituan’s VC arm, Long-Z Investments, a spokesperson told TechCrunch. Also participating were Tsinghua Capital, China Mobile, and CPE Yuanfeng, according to the post.

**Article:** [China&#8217;s Moonshot AI raises $2B at $20B valuation as demand for open source AI skyrockets](https://techcrunch.com/2026/05/07/chinas-moonshot-ai-raises-2b-at-20b-valuation-as-demand-for-open-source-ai-skyrockets/) | en | techcrunch.com
**Ngữ cảnh:**
> Chinese AI companies may not be swimming in as much cash as their Western rivals, but their open source models are still facing no shortage of interest from those who don’t mind a performance hit in exchange for cheap inference. And investors are taking notice.
> Moonshot AI, the Beijing-based AI lab developing the popular Kimi series of open-weight large language models, has raised about $2 billion at a valuation of $20 billion, according to a post by Huafeng Capital, which advised some investors who participated in the round.
> The round was led by Chinese food delivery company Meituan’s VC arm, Long-Z Investments, a spokesperson told TechCrunch. Also participating were Tsinghua Capital, China Mobile, and CPE Yuanfeng, according to the post.
> The company raised $3.9 billion over the past six months, according to Huafeng Capital. Moonshot was valued at $4.3 billion at the end of 2025, per reports, and by early 2026, that figure had more than doubled to $10 billion following a $700 million raise.
> Moonshot AI was founded in 2023 by Yang Zhilin, a former Meta AI and Google Brain researcher

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0047 -->
## 047. edge-0047

**Triple:** Dream Ventures (ORG) —CO_INVESTED_WITH→ Point72 (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Valar Atomics confirmed the whisperings that it was raising a giant round led by Sequoia on Monday. The startup’s founder and CEO Isaiah Taylor announced that the company has raised $1 billion in equity, with Sequoia partner Shaun Maguire joining its board, and that it also secured a $200 million line of credit from Erebor and other banks.
> While the nuclear startup did not disclose its valuation, Bloomberg reported that it was $6 billion.
> Valar is building small modular nuclear reactors (SMRs) — essentially miniaturized, factory-built power plants intended to be cheaper and faster to build than traditional reactors. In June, it demonstrated its Ward 250 reactor successfully powering an Nvidia Blackwell system, the company said, and announced a deal with Nvidia to develop a waterless 30MW AI factory.
> Valar says its reactors generate the engineering, manufacturing, and operational data needed to improve next-generation reactors, speeding its development cycles.
> “It took two years to complete the NOVA core. It took seven months to take Ward 250 critical. With each reactor built, the tick rate will become smaller until Valar is producing tens, then hundreds, then thousands of reactors per year,” it said, adding that this funding will allow it to reach its next milestone: manufacturing fleets of its SMRs.
> It certainly isn’t the only nuclear startup pursuing such ambitions. Over the past few months, Antares raised $470 million, and X-energy raised $1 billion through its IPO.
> As for Valar’s new round, other investors include Apandion Capital, Atreides Management, Conviction, Dream Ventures, HOF Capital, Point72, Riot Ventures, Snowpoint Ventures, and Valor Equity Partners.

**Article:** [Sequoia&#8217;s Shaun Maguire leads $1B round for nuclear startup Valar Atomics](https://techcrunch.com/2026/08/03/sequoias-shaun-maguire-leads-1b-round-for-nuclear-startup-valar-atomics/) | en | techcrunch.com
**Ngữ cảnh:**
> Valar Atomics confirmed the whisperings that it was raising a giant round led by Sequoia on Monday. The startup’s founder and CEO Isaiah Taylor announced that the company has raised $1 billion in equity, with Sequoia partner Shaun Maguire joining its board, and that it also secured a $200 million line of credit from Erebor and other banks.
> While the nuclear startup did not disclose its valuation, Bloomberg reported that it was $6 billion.
> Valar is building small modular nuclear reactors (SMRs) — essentially miniaturized, factory-built power plants intended to be cheaper and faster to build than traditional reactors. In June, it demonstrated its Ward 250 reactor successfully powering an Nvidia Blackwell system, the company said, and announced a deal with Nvidia to develop a waterless 30MW AI factory.
> Valar says its reactors generate the engineering, manufacturing, and operational data needed to improve next-generation reactors, speeding its development cycles.
> “It took two years to complete the NOVA core. It took seven months to take Ward 250 critical. With each reactor built, the tick rate will become smaller until Valar is producing tens, then hundreds, then thousands of reactors per year,” it said, adding that this funding will allow it to reach its next milestone: manufacturing fleets of its SMRs.
> It certainly isn’t the only nuclear startup pursuing such ambitions. Over the past few months, Antares raised $470 million, and X-energy raised $1 billion through its IPO.
> As for Valar’s new round, other investors include Apandion Capital, Atreides Management, Conviction, Dream Ventures, HOF Capital, Point72, Riot Ventures, Snowpoint Ventures, and Valor Equity Partners.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0048 -->
## 048. edge-0048

**Triple:** Seligman Ventures (ORG) —INVESTED_IN→ Smallest.ai (ORG)
**Assertion status:** reported
**Evidence:**
> To fuel this mission, Smallest.ai has raised $13 million in a Series A round, led by Seligman Ventures with participation from Sierra Ventures and 3one4 Capital.

**Article:** [Smallest.ai raises $13M to build ultra-fast voice AI that sounds genuinely human](https://techcrunch.com/2026/07/31/smallest-ai-raises-13m-to-build-ultra-fast-voice-ai-that-sounds-genuinely-human/) | en | techcrunch.com
**Ngữ cảnh:**
> imic how humans process information by listening, thinking, and speaking simultaneously.
> “While I’m speaking to you, you’re already thinking, and you might interrupt me if I talk for too long,” Sudarshan Kamath (pictured left), founder and CEO of Smallest.ai, told TechCrunch, adding that this is exactly how the startup’s model is designed to work.
> To fuel this mission, Smallest.ai has raised $13 million in a Series A round, led by Seligman Ventures with participation from Sierra Ventures and 3one4 Capital. The fresh capital brings the startup’s total funding to over $21 million.
> “The way an LLM works is you give it an entire prompt, and then it starts thinking,” Kamath said. While that latency is acceptable in a text chat, in a voice conversation, even a short pause feels unnatural. “If you think about how we are talking, I’m not giving you like a l

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0049 -->
## 049. edge-0049

**Triple:** Aziz Akhmedkhodjaev (PERSON) —CEO_OF→ Cerberus (ORG)
**Assertion status:** reported
**Evidence:**
> Competing against 726 applications from 39 countries is valuable in itself, whatever the outcome,” said Aziz Akhmedkhodjaev, founder and CEO of Cerberus.

**Article:** [Central Eurasia names its 2026 Road to Battlefield winners: Cerberus, WeGlobal AI, and LOOQ](https://techcrunch.com/2026/09/11/central-eurasia-names-its-2026-road-to-battlefield-winners-cerberus-weglobal-ai-and-looq/) | en | techcrunch.com
**Ngữ cảnh:**
> : Many rely heavily on general-purpose language models that can hallucinate, with potentially serious consequences when given access to corporate systems. Cerberus has already gone through 500 Global Eurasia and has been accepted into the Alchemist Silkroad — Silicon Valley Residency program.
> “We were simply glad to be part of Road to Battlefield. Competing against 726 applications from 39 countries is valuable in itself, whatever the outcome,” said Aziz Akhmedkhodjaev, founder and CEO of Cerberus. “What made our pitch unique is that we’re solving a problem the market is already feeling. Everyone is writing code with AI now, vulnerabilities are appearing faster than teams can find them, and there’s no established way to let an AI agent test real infrastructure safely. We believe the judges recognized that, and we’ll do our best, treating it 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0050 -->
## 050. edge-0050

**Triple:** Redpoint Ventures (ORG) —CO_INVESTED_WITH→ Bessemer Venture Partners (ORG)
**Assertion status:** reported
**Evidence:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.

**Article:** [Legora reaches $5.55 billion valuation as AI legal tech boom endures](https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/) | en | techcrunch.com
**Ngữ cảnh:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.
> There are other signs that investors are bullish about AI legal tech. Legora’s Series D and valuation jump come just a few months after its October 2025 $150 million Series C round led at a $1.8 billion valuation. Its competitor, Harvey, which is backed by a16z, is already valued at $8 billion, and is now reportedly seeking to raise at an $11 bill

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0051 -->
## 051. edge-0051

**Triple:** Mach33 (ORG) —CO_INVESTED_WITH→ ARK Invest Venture Fund (ORG)
**Assertion status:** reported
**Evidence:**
> Portal, founded in 2021, announced a $50 million Series A funding round Thursday that values the company at $250 million. The round was led by Geodesic Capital and Mach33, alongside Booz Allen Ventures, ARK Invest, AlleyCorp, and FUSE.

**Article:** [This founder helped build SpaceX&#8217;s most powerful rocket engine. Now he&#8217;s building a &#8216;fighter jet for orbit.&#8217;](https://techcrunch.com/2026/04/09/portal-raises-50-million-to-build-a-new-kind-of-high-power-rocket-engine/) | en | techcrunch.com
**Ngữ cảnh:**
> Jeff Thornburg helped turn a government research project into SpaceX’s most powerful rocket engine. Now, he’s trying to do the same thing at his startup Portal Space Systems, which is taking an idea set aside by NASA and turning it into high-powered propulsion for the next generation of spacecraft.
> Portal, founded in 2021, announced a $50 million Series A funding round Thursday that values the company at $250 million. The round was led by Geodesic Capital and Mach33, alongside Booz Allen Ventures, ARK Invest, AlleyCorp, and FUSE.
> The company is developing a technology called solar thermal propulsion. Today’s standard satellite engines either burn chemical fuel or convert the sun’s energy to electricity, using that to power efficient but low-powered thrusters. Portal’s engines would instead concentrate the heat of the sun, using that to heat propellant and move the spacecra

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0052 -->
## 052. edge-0052

**Triple:** Jane Street (ORG) —CO_INVESTED_WITH→ Cisco Investments (ORG)
**Assertion status:** reported
**Evidence:**
> If finalized, the deal would nearly triple Anthropic’s valuation, which was $61.5 billion after a $3.5 billion funding round led by Lightspeed Venture Partners announced in March. Other participants in the startup’s last round included Bessemer Venture Partners, Cisco Investments, D1 Capital Partners, Fidelity Management & Research Company, General Catalyst, Jane Street, Menlo Ventures, and Salesforce Ventures.

**Article:** [Anthropic reportedly nears $170B valuation with potential $5B round](https://techcrunch.com/2025/07/29/anthropic-reportedly-nears-170b-valuation-with-potential-5b-round/) | en | techcrunch.com
**Ngữ cảnh:**
> llion in funding, valuing the large language model developer at $170 billion, Bloomberg reported.
> Iconiq Capital is leading this funding round, but there’s a possibility of a second lead investor joining the deal. The company has also been in talks with Qatar Investment Authority and GIC, Singapore’s sovereign wealth fund, according to the report.
> If finalized, the deal would nearly triple Anthropic’s valuation, which was $61.5 billion after a $3.5 billion funding round led by Lightspeed Venture Partners announced in March. Other participants in the startup’s last round included Bessemer Venture Partners, Cisco Investments, D1 Capital Partners, Fidelity Management & Research Company, General Catalyst, Jane Street, Menlo Ventures, and Salesforce Ventures.
> Despite Anthropic’s mission as a safety-conscious AI model developer, the company’s CEO, Dario Amodei, recently confessed in a memo to employees, reported by Wired, that he’s “not thrilled” about taking money from sovereign wealth funds of dictatorial governments.
> To keep pace with the massive capital requirements of developing AI models, the comp

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0053 -->
## 053. edge-0053

**Triple:** Andreessen Horowitz (ORG) —CO_INVESTED_WITH→ Human Capital (ORG)
**Assertion status:** reported
**Evidence:**
> The round was led by the United Arab Emirates. The Boring Company said Thursday that it now plans to dig more than 150 kilometers of tunnels in the Middle Eastern country. Andreessen Horowitz, Sequoia Capital, Human Capital, Vy Capital, and Valor Equity Partners also participated.

**Article:** [The Boring Company raises $3B in round led by UAE](https://techcrunch.com/2026/09/10/the-boring-company-raises-3b-in-round-led-by-uae/) | en | techcrunch.com
**Ngữ cảnh:**
> Elon Musk’s tunneling company, The Boring Company, has raised a $3 billion Series D funding round that pushes its valuation to $23 billion.
> 
> The round was led by the United Arab Emirates. The Boring Company said Thursday that it now plans to dig more than 150 kilometers of tunnels in the Middle Eastern country. Andreessen Horowitz, Sequoia Capital, Human Capital, Vy Capital, and Valor Equity Partners also participated.
> 
> The Wall Street Journal reported in July that The Boring Company was looking to raise as much as $4 billion.
> 
> The Boring Company has done most of its digging to date in Las Vegas, Nevada, where it operates a handful of tunnels that connect hotel casinos and the convention center. It recently started work on a project in Nashville, Tennessee, that

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0054 -->
## 054. edge-0054

**Triple:** Fritz Lanman (PERSON) —FOUNDED→ Playlist (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Playlist announced on Tuesday that the transaction is officially complete after first disclosing the agreement in January. With everything now finalized, EGYM will operate under Playlist alongside its other brands, and leadership will be shared between Playlist co-founder Fritz Lanman and EGYM CEO Philipp Roesch-Schlanderer.

**Article:** [The company behind ClassPass and Mindbody just got a lot bigger with a $7.5B merger](https://techcrunch.com/2026/03/31/the-company-behind-classpass-and-mindbody-just-got-a-lot-bigger-with-a-7-5b-merger/) | en | techcrunch.com
**Ngữ cảnh:**
> The fitness industry is consolidating fast — and the latest deal is one of the biggest yet. Playlist, the parent company behind fitness brands Booker, ClassPass, and Mindbody, has officially merged with EGYM, a startup known for its smart gym equipment, AI-driven workout plans, and corporate wellness marketplace Wellpass.
> Playlist announced on Tuesday that the transaction is officially complete after first disclosing the agreement in January. With everything now finalized, EGYM will operate under Playlist alongside its other brands, and leadership will be shared between Playlist co-founder Fritz Lanman and EGYM CEO Philipp Roesch-Schlanderer.
> The deal values the combined company at $7.5 billion.
> The merger is expected to create a fitness and wellness powerhouse. By bringing EGYM into the mix alongside B2B platforms like Booker, which supports spas and salons, and Mindbody, which offers software widely used by gyms and studios, plus the consumer app ClassPass, Playlist is stitching toge

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0055 -->
## 055. edge-0055

**Triple:** Menlo Ventures (ORG) —INVESTED_IN→ Stanford (ORG)
**Assertion status:** reported
**Evidence:**
> Stanford adjunct professor and successfully exited founder Zain Asgar just raised an $80 million Series A for a startup that solve the AI inference bottleneck problem in an astute way. The round was led by Menlo Ventures.

**Article:** [Startup Gimlet Labs is solving the AI inference bottleneck in a surprisingly elegant way](https://techcrunch.com/2026/03/23/startup-gimlet-labs-is-solving-the-ai-inference-bottleneck-in-a-surprisingly-elegant-way/) | en | techcrunch.com
**Ngữ cảnh:**
> Stanford adjunct professor and successfully exited founder Zain Asgar just raised an $80 million Series A for a startup that solve the AI inference bottleneck problem in an astute way. The round was led by Menlo Ventures.
> The company, Gimlet Labs, has created what it claims is the first and only “multi-silicon inference cloud” which is software that allows an AI workload to be simultaneously run across diverse types of hardware. It can split an AI app’s work across both traditional CPUs and AI-tuned GPUs, as well as high-memory systems.
> “We basically run across wha

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0056 -->
## 056. edge-0056

**Triple:** General Catalyst (ORG) —CO_INVESTED_WITH→ Salesforce (ORG)
**Assertion status:** reported
**Evidence:**
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
> nd led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.
> Microsoft’s $16.3 million convertible investment in Mistral as part of a partnership announced in February 2024 was presented as a Series A extension, implying an unchanged valuation.
> In June 2024, Mistral raised €600 million (about $640 million) in a mix of equity and debt. The long-rumored round was led by General Catalyst at a $6 billion valuat

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0057 -->
## 057. edge-0057

**Triple:** T. Rowe Price (ORG) —CO_INVESTED_WITH→ BlackRock (ORG)
**Assertion status:** reported
**Evidence:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Article:** [AI chip maker SambaNova raises $1B at $11B valuation, 5 months after last mega round](https://techcrunch.com/2026/07/08/sambanova-draws-1b-at-11b-valuation-in-series-f-first-close/) | en | techcrunch.com
**Ngữ cảnh:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0058 -->
## 058. edge-0058

**Triple:** Shell Ventures (ORG) —CO_INVESTED_WITH→ Centaurus Capital (ORG)
**Assertion status:** reported
**Evidence:**
> Geothermal startup Mazama Energy raised $135 million in an oversubscribed Series B, the startup said Thursday.
> The fresh funding will help the company develop horizontal wells in superhot rocks capable of generating 15 megawatts of electricity per well.
> Mazama plans to start generating electricity sometime next year and said its first site in Oregon is capable of producing 10 gigawatts of electricity. That’s a sharp upward revision from the company’s estimate last year, when investor Vinod Khosla said the site had the potential to produce 5 gigawatts.
> Enhanced geothermal startups are shaping up to be the dark horse in the battle to power AI data centers and other large loads on the grid. While tech companies and data center developers have been throwing their weight behind natural gas, geothermal startups have been quickly advancing their technology.
> Unlike previous geothermal projects, enhanced geothermal startups are targeting deeper and hotter rock. Mazama, for example, has drilled past 10,000 feet in 15 days on its way to about 15,000 feet deep. At those depths, the company can access 750˚ F (400˚ C) heat, which at high pressures turns water into a “supercritical” fluid that’s neither fully liquid nor fully gas — a state that lets it absorb far more energy than ordinary steam. Mazama said that will allow each well to produce up to 10 times more power than traditional geothermal technologies.
> Given the depths Mazama is targeting, the potential payoff is significant. Tapping just 1% of superhot rock worldwide could generate more than 63 terawatts of electricity, according to the University of Twente and the Clean Air Task Force.
> While work at its Oregon site is still in the early stages, the startup has already secured land for a second development. Mazama aims to complete development of the first site by 2030, at which point it says it should generate 200 megawatts of electricity.
> The new round was led by Centaurus Capital and Doerr Capital, with participation from ConocoPhillips and Shell Ventures. Existing investors including Khosla Ventures and Gates Frontier returned, and new investors SiteGround Capital, H. Barton Asset Management, and the Jeffrey and Marieke Rothschild Foundation also joined the round.

**Article:** [Khosla-backed Mazama Energy just raised $135M to drill deeper into superhot-rock geothermal](https://techcrunch.com/2026/09/17/khosla-backed-mazama-energy-just-raised-135m-to-drill-deeper-into-super-hot-rock-geothermal/) | en | techcrunch.com
**Ngữ cảnh:**
> Geothermal startup Mazama Energy raised $135 million in an oversubscribed Series B, the startup said Thursday.
> The fresh funding will help the company develop horizontal wells in superhot rocks capable of generating 15 megawatts of electricity per well.
> Mazama plans to start generating electricity sometime next year and said its first site in Oregon is capable of producing 10 gigawatts of electricity. That’s a sharp upward revision from the company’s estimate last year, when investor Vinod Khosla said the site had the potential to produce 5 gigawatts.
> Enhanced geothermal startups are shaping up to be the dark horse in the battle to power AI data centers and other large loads on the grid. While tech companies and data center developers have been throwing their weight behind natural gas, geothermal startups have been quickly advancing their technology.
> Unlike previous geothermal projects, enhanced geothermal startups are targeting deeper and hotter rock. Mazama, for example, has drilled past 10,000 feet in 15 days on its way to about 15,000 feet deep. At those depths, the company can access 750˚ F (400˚ C) heat, which at high pressures turns water into a “supercritical” fluid that’s neither fully liquid nor fully gas — a state that lets it absorb far more energy than ordinary steam. Mazama said that will allow each well to produce up to 10 times more power than traditional geothermal technologies.
> Given the depths Mazama is targeting, the potential payoff is significant. Tapping just 1% of superhot rock worldwide could generate more than 63 terawatts of electricity, according to the University of Twente and the Clean Air Task Force.
> While work at its Oregon site is still in the early stages, the startup has already secured land for a second development. Mazama aims to complete development of the first site by 2030, at which point it says it should generate 200 megawatts of electricity.
> The new round was led by Centaurus Capital and Doerr Capital, with participation from ConocoPhillips and Shell Ventures. Existing investors including Khosla Ventures and Gates Frontier returned, and new investors SiteGround Capital, H. Barton Asset Management, and the Jeffrey and Marieke Rothschild Foundation also joined the round.
> Mazama was incubated at Khosla Ventures.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0059 -->
## 059. edge-0059

**Triple:** Jamie Foxx (PERSON) —INVESTED_IN→ ElevenLabs (ORG)
**Assertion status:** reported
**Evidence:**
> Voice AI company ElevenLabs revealed new investors that are part of its $500 million Series D fundraise, which was first announced in February. The additions include institutions such as BlackRock, Wellington, D.E. Shaw, and Schroders; enterprises like Nvidia, Salesforce Ventures, Santander, KPN, and Deutsche Telekom; and individual investors such as Jamie Foxx, Eva Longoria, and Squid Game creator Hwang Dong-hyuk.

**Article:** [ElevenLabs lists BlackRock, Jamie Foxx, and Eva Longoria as new investors](https://techcrunch.com/2026/05/05/elevenlabs-lists-blackrock-jamie-foxx-and-eva-longoria-as-new-investors/) | en | techcrunch.com
**Ngữ cảnh:**
> Voice AI company ElevenLabs revealed new investors that are part of its $500 million Series D fundraise, which was first announced in February. The additions include institutions such as BlackRock, Wellington, D.E. Shaw, and Schroders; enterprises like Nvidia, Salesforce Ventures, Santander, KPN, and Deutsche Telekom; and individual investors such as Jamie Foxx, Eva Longoria, and Squid Game creator Hwang Dong-hyuk.
> The startup also noted that it surpassed $500 million in ARR (annual recurring revenue), after ending last year with nearly $350 million in ARR. The company’s co-founder and CEO, Mati Staniszewski, said last month that ElevenLabs added $100 million in net new ARR in Q1 2026, ending the quarter at roughly $450 million in ARR.
> The company has also a

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0060 -->
## 060. edge-0060

**Triple:** Riot Ventures (ORG) —CO_INVESTED_WITH→ Snowpoint Ventures (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Valar Atomics confirmed the whisperings that it was raising a giant round led by Sequoia on Monday. The startup’s founder and CEO Isaiah Taylor announced that the company has raised $1 billion in equity, with Sequoia partner Shaun Maguire joining its board, and that it also secured a $200 million line of credit from Erebor and other banks.
> While the nuclear startup did not disclose its valuation, Bloomberg reported that it was $6 billion.
> Valar is building small modular nuclear reactors (SMRs) — essentially miniaturized, factory-built power plants intended to be cheaper and faster to build than traditional reactors. In June, it demonstrated its Ward 250 reactor successfully powering an Nvidia Blackwell system, the company said, and announced a deal with Nvidia to develop a waterless 30MW AI factory.
> Valar says its reactors generate the engineering, manufacturing, and operational data needed to improve next-generation reactors, speeding its development cycles.
> “It took two years to complete the NOVA core. It took seven months to take Ward 250 critical. With each reactor built, the tick rate will become smaller until Valar is producing tens, then hundreds, then thousands of reactors per year,” it said, adding that this funding will allow it to reach its next milestone: manufacturing fleets of its SMRs.
> It certainly isn’t the only nuclear startup pursuing such ambitions. Over the past few months, Antares raised $470 million, and X-energy raised $1 billion through its IPO.
> As for Valar’s new round, other investors include Apandion Capital, Atreides Management, Conviction, Dream Ventures, HOF Capital, Point72, Riot Ventures, Snowpoint Ventures, and Valor Equity Partners.

**Article:** [Sequoia&#8217;s Shaun Maguire leads $1B round for nuclear startup Valar Atomics](https://techcrunch.com/2026/08/03/sequoias-shaun-maguire-leads-1b-round-for-nuclear-startup-valar-atomics/) | en | techcrunch.com
**Ngữ cảnh:**
> Valar Atomics confirmed the whisperings that it was raising a giant round led by Sequoia on Monday. The startup’s founder and CEO Isaiah Taylor announced that the company has raised $1 billion in equity, with Sequoia partner Shaun Maguire joining its board, and that it also secured a $200 million line of credit from Erebor and other banks.
> While the nuclear startup did not disclose its valuation, Bloomberg reported that it was $6 billion.
> Valar is building small modular nuclear reactors (SMRs) — essentially miniaturized, factory-built power plants intended to be cheaper and faster to build than traditional reactors. In June, it demonstrated its Ward 250 reactor successfully powering an Nvidia Blackwell system, the company said, and announced a deal with Nvidia to develop a waterless 30MW AI factory.
> Valar says its reactors generate the engineering, manufacturing, and operational data needed to improve next-generation reactors, speeding its development cycles.
> “It took two years to complete the NOVA core. It took seven months to take Ward 250 critical. With each reactor built, the tick rate will become smaller until Valar is producing tens, then hundreds, then thousands of reactors per year,” it said, adding that this funding will allow it to reach its next milestone: manufacturing fleets of its SMRs.
> It certainly isn’t the only nuclear startup pursuing such ambitions. Over the past few months, Antares raised $470 million, and X-energy raised $1 billion through its IPO.
> As for Valar’s new round, other investors include Apandion Capital, Atreides Management, Conviction, Dream Ventures, HOF Capital, Point72, Riot Ventures, Snowpoint Ventures, and Valor Equity Partners.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0061 -->
## 061. edge-0061

**Triple:** Commerzbank (ORG) —CO_FINANCED_WITH→ Arab Bank for Investment and Foreign Trade (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).
> With the partnership of 15 international financial institutions, this facility represents VPBank’s largest-ever transaction in terms of the number of MLAUBs involved. The scale of the transaction and the breadth of participation underscore the strong confidence of the international financial community in VPBank’s financial strength, growth prospects and sustainable development orientation.
> In addition to the MLAUBs, the transaction also received strong market support, with participation from 19 international financial institutions following a series of investor roadshows in two major regional financial markets, Singapore and Taiwan (China).
> Speaking at the signing ceremony, Nguyễn Đức Vinh, CEO of VPBank, said: “The $1.44 billion syndicated loan, supported by 15 leading global financial institutions, is a clear testament to the strong confidence that the international financial community places in VPBank.
> "It also marks an important step forward in the bank’s implementation of sustainability-linked financing instruments, serving both as an affirmation of our commitment and as a catalyst for VPBank to further contribute to sustainable growth objectives, institutionalise Environmental, Social and Governance (ESG) goals, create long-term value for shareholders and customers and make positive contributions to society.”
> Notably, despite ongoing geopolitical uncertainties, escalating tensions in the Middle East and tighter liquidity conditions in global financial markets, the transaction secured commitments from several leading financial institutions in the Middle East, including FAB, Mashreq, NBK, Arab Bank for Investment and Foreign Trade and Doha Bank. Their participation is a strong testament to VPBank’s growing reputation and standing in international capital markets.

**Article:** [VPBank and 15 international financial institutions sign maiden US$1.44 billion sustainability-linked syndicated loan facility](https://vietnamnews.vn/economy/1784501/vpbank-and-15-international-financial-institutions-sign-maiden-us-1-44-billion-sustainability-linked-syndicated-loan-facility.html) | en | vietnamnews.vn
**Ngữ cảnh:**
>  strategic partnership between VPBank and SMBC, while enhancing VPBank’s standing in regional and international financial markets.
> The transaction attracted several financial institutions taking on lead roles for the first time or expanding their existing participation, with these banks accounting for nearly half of all participating institutions.
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).
> With the partnership of 15 international financial institutions, this facility represents VPBank’s largest-ever transaction in terms of the number of MLAUBs involved. The scale of the transaction and the breadth of participation underscore the strong confidence of the international financial community in VPBank’s financial strength, growth prospects and sustainable development orientation.
> In addition to the MLAUBs, the transaction also received strong market support, with participation from 19 international financial institutions following a series of investor roadshows in two major regional financial markets, Singapore and Taiwan (China).
> Speaking at the signing ceremony, Nguyễn Đức Vinh, CEO of VPBank, said: “The $1.44 billion syndicated loan, supported by 15 leading global financial institutions, is a clear testament to the strong confidence that the international financial community places in VPBank.
> "It also marks an important step forward in the bank’s implementation of sustainability-linked financing instruments, serving both as an affirmation of our commitment and as a catalyst for VPBank to further contribute to sustainable growth objectives, institutionalise Environmental, Social and Governance (ESG) goals, create long-term value for shareholders and customers and make positive contributions to society.”
> Notably, despite ongoing geopolitical uncertainties, escalating tensions in the Middle East and tighter liquidity conditions in global financial markets, the transaction secured commitments from several leading financial institutions in the Middle East, including FAB, Mashreq, NBK, Arab Bank for Investment and Foreign Trade and Doha Bank. Their participation is a strong testament to VPBank’s growing reputation and standing in international capital markets.
> The successful completion of the transaction marks an important milestone in VPBank’s strategy to diversify its medium- and long-term funding sources, providing momentum for the bank to pursue its ambitious growth objectives in 2026.
> It also significantly expands VPBank’s network of financial partners, laying a strong foundation for the bank to ac

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0062 -->
## 062. edge-0062

**Triple:** Sembcorp Development (ORG) —OWNS_STAKE_IN→ Starmason (ORG)
**Assertion status:** reported
**Evidence:**
> Starmason was established in November 2025 with registered capital of VNĐ50 billion, with Việt Nam's BB Investment and Development Co Ltd holding a stake of 98 per cent. In December 2025, Singapore's Sembcorp Development acquired a 49 per cent stake in Starmason.

**Article:** [Starmason secures land for $480 million data centre in HCM City](https://vietnamnews.vn/economy/1799608/starmason-secures-land-for-480-million-data-centre-in-hcm-city.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> Large Data Centre Complex received its investment registration certificate on March 24, 2026, and the land lease is valid until March 24, 2076.
> The data centre is designed initially with about 60 MW of IT load to support cloud computing, artificial intelligence, big-data processing and high-performance computing, with potential expansion to 90 MW.
> Starmason was established in November 2025 with registered capital of VNĐ50 billion, with Việt Nam's BB Investment and Development Co Ltd holding a stake of 98 per cent. In December 2025, Singapore's Sembcorp Development acquired a 49 per cent stake in Starmason.
> Starmason is one of three large-scale data centre projects being developed in HCM City's High-Tech Park, with combined registered capital of nearly $1.15 billion. — VNS

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0063 -->
## 063. edge-0063

**Triple:** A&E Investment (ORG) —CO_INVESTED_WITH→ Vista Equity Partners (ORG)
**Assertion status:** reported
**Evidence:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Article:** [AI chip maker SambaNova raises $1B at $11B valuation, 5 months after last mega round](https://techcrunch.com/2026/07/08/sambanova-draws-1b-at-11b-valuation-in-series-f-first-close/) | en | techcrunch.com
**Ngữ cảnh:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0064 -->
## 064. edge-0064

**Triple:** Intuit Ventures (ORG) —CO_INVESTED_WITH→ Greyhound Capital (ORG)
**Assertion status:** reported
**Evidence:**
> On Tuesday, Doss announced that it raised a $55 million Series B co-led by Madrona and Premji Invest, with participation from Intuit Ventures. Other new and existing inventors in the round include Theory Ventures, General Catalyst, Contrary Capital, and Greyhound Capital.

**Article:** [Doss raises $55M for AI inventory management that plugs into ERP](https://techcrunch.com/2026/03/24/doss-raises-55m-for-ai-inventory-management-that-plugs-into-erp/) | en | techcrunch.com
**Ngữ cảnh:**
> ey Jones, many new AI ERPs lack robust inventory management, the process of ensuring that the data on physical goods remains synced with the accounting ledger.
> Doss claims to solve this by providing an AI-native inventory management layer that integrates with existing accounting systems, whether traditional ERPs or ones built by AI-based startups.
> On Tuesday, Doss announced that it raised a $55 million Series B co-led by Madrona and Premji Invest, with participation from Intuit Ventures. Other new and existing inventors in the round include Theory Ventures, General Catalyst, Contrary Capital, and Greyhound Capital.
> Doss, founded in 2022, originally focused on a core accounting product similar to those offered by AI-native startups like Rillet and Campfire. But last year, the startup decided instead of competing with these companies, “we would rather partner with them, and play a different game,” Jones told TechCrunch.
> Jones explained that AI-native ERP compa

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0065 -->
## 065. edge-0065

**Triple:** GSV (ORG) —CO_INVESTED_WITH→ Shine Capital (ORG)
**Assertion status:** reported
**Evidence:**
> The Series A round was led by Shine Capital, with participation from Ada Ventures, Seek Investments, GSV, and NFX, which previously led Gizmo’s $3.5 million seed round.

**Article:** [AI learning app Gizmo levels up with 13M users and a $22M investment](https://techcrunch.com/2026/04/15/ai-learning-app-gizmo-levels-up-with-13m-users-and-a-22m-investment/) | en | techcrunch.com
**Ngữ cảnh:**
>  Quizlet, and Nibble, alongside newer entrants such as Yuno and Knowt, which have all attempted to redirect screen-time habits into productive learning. However, for a young learning app like Gizmo to grow this much interest in just a few years is notable. For comparison, Yuno touts 1 million app downloads, and Knowt has more than 7 million users.
> The Series A round was led by Shine Capital, with participation from Ada Ventures, Seek Investments, GSV, and NFX, which previously led Gizmo’s $3.5 million seed round.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0066 -->
## 066. edge-0066

**Triple:** Marissa Mayer (PERSON) —CO_INVESTED_WITH→ Dick Costolo (PERSON)
**Assertion status:** reported
**Evidence:**
> “Eugenia has a unique sense for where AI is headed and a track record of great taste in building it,” said Alex Lim, general partner at IVP, which led the new round, in a statement. “She has a clear vision for how people will interact with AI, one that goes far beyond the text box or command line. Wabi is the expression of that vision, and we’re thrilled to support her.”
> Other participants in the round included Andreessen Horowitz (a16z), Forerunner, Amazon Alexa Fund, and angel investors like Shopify CEO Tobi Lütke, Salesforce CEO Marc Benioff, former Yahoo! head Marissa Mayer, former Twitter CEO Dick Costolo, and one half of The Chainsmokers, Alex Pall.

**Article:** [Wabi, the AI agent that builds mini apps, now valued at $1.25B after latest round](https://techcrunch.com/2026/10/29/wabi-the-ai-agent-that-builds-mini-apps-now-valued-at-1-25b-after-latest-round/) | en | techcrunch.com
**Ngữ cảnh:**
> es that Wabi’s investors agree that its new agentic angle has some potential, especially given the market around AI agents is hot right now, with viral AI agent Instinct pulling in another billion at a $10 billion valuation in September.
> Even Tolan, which makes a cute, Muppet-like AI companion to help people navigate life, just raised $30 million.
> “Eugenia has a unique sense for where AI is headed and a track record of great taste in building it,” said Alex Lim, general partner at IVP, which led the new round, in a statement. “She has a clear vision for how people will interact with AI, one that goes far beyond the text box or command line. Wabi is the expression of that vision, and we’re thrilled to support her.”
> Other participants in the round included Andreessen Horowitz (a16z), Forerunner, Amazon Alexa Fund, and angel investors like Shopify CEO Tobi Lütke, Salesforce CEO Marc Benioff, former Yahoo! head Marissa Mayer, former Twitter CEO Dick Costolo, and one half of The Chainsmokers, Alex Pall.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0067 -->
## 067. edge-0067

**Triple:** Google Ventures (ORG) —CO_INVESTED_WITH→ Kleiner Perkins (ORG)
**Assertion status:** reported
**Evidence:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.

**Article:** [Kevin Mandia&#8217;s new &#8216;agent swarm&#8217; security startup Armadin raises $255.5M at $2.5B valuation](https://techcrunch.com/2026/10/01/kevin-mandias-new-agent-swarm-security-startup-armadin-raises-255-5m-at-2-5b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.
> The new round comes just six months after Armadin raised a $190 million Series A in March. It has now raised more than $445 million.
> Armadin is offering enterprises a new kind of always-on security by reimagining defense testing for the AI era. Instead of traditional penetration tests, where hired guns attempt to break in and report on the weaknes

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0068 -->
## 068. edge-0068

**Triple:** Einride (ORG) —INVESTED_IN→ Public Equity (ORG)
**Assertion status:** reported
**Evidence:**
> Einride has secured an oversubscribed $113 million PIPE (private investment in public equity) ahead of its public debut, which is expected for the first half of 2026.

**Article:** [Self-driving truck startup Einride raises $113M PIPE ahead of public debut](https://techcrunch.com/2026/02/26/self-driving-truck-startup-einride-raises-113m-pipe-ahead-of-public-debut/) | en | techcrunch.com
**Ngữ cảnh:**
> Einride has secured an oversubscribed $113 million PIPE (private investment in public equity) ahead of its public debut, which is expected for the first half of 2026.
> The Swedish startup is most well-known for building both electric trucks and autonomous pods that are designed to carry freight with no room for a human driver. Einride announced its plans to go public via a merger with a special purpose acquisition company, Legato Merger Corp., last November.
> The deal values Einride at a pre-money valuation of $1

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0069 -->
## 069. edge-0069

**Triple:** Databricks (ORG) —ACQUIRED→ Quotient AI (ORG)
**Assertion status:** reported
**Evidence:**
> In March, Databricks bought two startups, Quotient AI, which does evaluation and reinforcement learning for AI agents, and very early-stage interactive notebook SiftD.ai.

**Article:** [Databricks buys Row Zero and is scouting for more startups to acquire](https://techcrunch.com/2026/09/24/databricks-buys-row-zero-and-is-scouting-for-more-startups-to-acquire/) | en | techcrunch.com
**Ngữ cảnh:**
>  2025, at an estimated $40 million valuation at the time, according to PitchBook.
> Databricks, which closed another $5 billion in funding in August and hit $7 billion in annualized revenue run rate, has been busy shopping in 2026 and is eager to keep doing so. “We intend to do many more acquisitions like this in the future,” Ghodsi told TechCrunch.
> In March, Databricks bought two startups, Quotient AI, which does evaluation and reinforcement learning for AI agents, and very early-stage interactive notebook SiftD.ai. In June, the company bought AI security operations center startup Panther, previously valued at $1.4 billion in 2021. Last month, it bought Electric, makers of a small, lite Postgres database known as PGlite, useful for agents running locally on devices.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0070 -->
## 070. edge-0070

**Triple:** Deerfield Management (ORG) —INVESTED_IN→ Shine Technologies (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The company has raised a total of $1 billion, according to PitchBook. Investors include Energy Ventures Group, Koch Disruptive Technologies, Nucleation Capital, and the Wisconsin Alumni Research Foundation. The company most recently raised a $240 million round in February led by NantWorks with participation from investors, including Deerfield Management, Fidelity Management & Research Company, Oaktree Capital Management, Pelican Energy Partners, and the Sumitomo Corporation of Americas.

**Article:** [Every fusion startup that has raised over $100M](https://techcrunch.com/2026/08/15/every-fusion-startup-that-has-raised-over-100m/) | en | techcrunch.com
**Ngữ cảnh:**
> r. Selling electrons from a fusion power plant is years off, so instead, it’s starting by selling neutron testing and medical isotopes. More recently, it has been developing a way to recycle radioactive waste. Shine hasn’t picked an approach for a future fusion reactor, instead saying that it’s developing necessary skills for when that time comes.
> The company has raised a total of $1 billion, according to PitchBook. Investors include Energy Ventures Group, Koch Disruptive Technologies, Nucleation Capital, and the Wisconsin Alumni Research Foundation. The company most recently raised a $240 million round in February led by NantWorks with participation from investors, including Deerfield Management, Fidelity Management & Research Company, Oaktree Capital Management, Pelican Energy Partners, and the Sumitomo Corporation of Americas.
> Only one fusion experiment, the National Ignition Facility (NIF), has surpassed scientific breakeven, and the chief scientist of that endeavor, Annie Kritcher, is part of Inertia Enterprises‘ founding team. She’s joined by Mike Dunne, a Stanford professor, and Jeff Lawson, who co-founded Twilio and currently owns The Onion. In April, the startup s

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0071 -->
## 071. edge-0071

**Triple:** Kuan Yen Tan (PERSON) —FOUNDED→ IQM (ORG)
**Assertion status:** reported
**Evidence:**
> On the quantum side, there’s IQM co-founder Kuan Yen Tan and board member Antti Vasara, also chair at SemiQon, a Finnish semiconductor startup focused on quantum chips.

**Article:** [Before quantum computing arrives, this startup wants enterprises already running on it](https://techcrunch.com/2026/03/12/before-quantum-computing-arrives-this-startup-wants-enterprises-already-running-on-it/) | en | techcrunch.com
**Ngữ cảnh:**
> is that it is already viable today, because it uses classical hardware while simulating quantum behavior, working around the hurdles that still hinder quantum hardware. Meanwhile, Qutwo OS is designed to be flexible, supporting quantum or non-quantum algorithms and chips alike.
> Qutwo’s team brings experience on both sides of the quantum-AI divide. On the quantum side, there’s IQM co-founder Kuan Yen Tan and board member Antti Vasara, also chair at SemiQon, a Finnish semiconductor startup focused on quantum chips. The enterprise side is equally represented, by Sarlin himself and Kaj-Mikael Björk, one of his former co-founders at Silo AI. Pekka Lundmark, the former CEO of Finnish telecom giant Nokia, also joined Qutwo’s board.
> Across both areas, the team counts over 30 quantum and AI scientists, and Sarlin is clear where the company stands. “We’re building f

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0072 -->
## 072. edge-0072

**Triple:** Anthropic (ORG) —INVESTED_IN→ Sapiom (ORG)
**Assertion status:** reported
**Evidence:**
> Kumar has met with dozens of startups in the AI payments space, but he believes Zerbib’s focus on the financial layer for enterprises, rather than consumers, is what’s truly needed to make AI agents work. That’s why Accel is leading Sapiom’s $15 million seed round, with participation from Okta Ventures, Gradient Ventures, Array Ventures, Menlo Ventures, Anthropic, and Coinbase Ventures.

**Article:** [Sapiom raises $15M to help AI agents buy their own tech tools](https://techcrunch.com/2026/02/05/sapiom-raises-15m-to-help-ai-agents-buy-their-own-tech-tools/) | en | techcrunch.com
**Ngữ cảnh:**
> entication and a micro-payment. Sapiom’s goal is to make this whole process seamless, letting the AI agent decide what to buy and when without human intervention.
> “In the future, apps are going to consume services which require payments. Right now, there’s no easy way for agents to actually access all of that,” said Amit Kumar, a partner at Accel.
> Kumar has met with dozens of startups in the AI payments space, but he believes Zerbib’s focus on the financial layer for enterprises, rather than consumers, is what’s truly needed to make AI agents work. That’s why Accel is leading Sapiom’s $15 million seed round, with participation from Okta Ventures, Gradient Ventures, Array Ventures, Menlo Ventures, Anthropic, and Coinbase Ventures.
> “If you really think about it, every API call is a payment. Every time you send a text message, it’s a payment. Every time you spin up a server for AWS, it’s a payment,” Kumar told TechCrunch.
> While it’s still early days for Sapiom, the startup hopes that its infrastructure solution will be adopted by vibe-coding companies and other companies crea

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0073 -->
## 073. edge-0073

**Triple:** Korea Development Bank (ORG) —INVESTED_IN→ Unastella (ORG)
**Assertion status:** reported
**Evidence:**
> One of them is Unastella, a four-year-old South Korean startup that just closed a $24 million Series B, bringing its total funding to $44 million. The company launched its own rocket, the UNA EXPRESS-I, from South Korean soil in May 2025.
> The Seoul-based rocket startup is developing its own launch vehicles and engines, with an initial focus on small satellite launch services. Unastella’s near-term focus is validating its technology and business model through orbital launches, with crewed suborbital spaceflight as a longer-term goal, founder and CEO Jae Park told TechCrunch.
> Unastella uses a kerosene and liquid oxygen propulsion system, one of the most proven combinations in rocket history, and one that is also used by SpaceX’s Falcon series. On top of that, the company swapped out the traditional turbo pump for an electric motor pump, a simpler and cheaper alternative that Rocket Lab has already validated in flight.
> The tradeoff is payload. Electric motor pumps are heavier, which means less room for satellites. But Park said that’s a deliberate decision.
> “We’re not an R&D group trying to build the most impressive rocket,” Park said. “We’re a commercial launch company trying to get to market fast.”
> Park also notes that Unastella handles everything in-house, such as design, manufacturing, ground operations, and flight data. The UNA EXPRESS-I launch last year was the first real-world test of the entire system end-to-end, Park said.
> The CEO has spent his entire career working on rocket engines. Before founding Unastella, Park worked on combustion systems for Korea’s Nuri rocket — the country’s first indigenously developed orbital launch vehicle, built by the Korea Aerospace Research Institute (KARI). He then moved to the German Aerospace Center in Berlin to work on European launch vehicle engines, and returned to Korea to join another rocket startup before deciding to build his own.
> Unastella isn’t generating revenue yet, but investors appear to be backing the startup’s roadmap. Altos Ventures led the Series B, joined by Korea Development Bank, Strong Ventures, and Hana Ventures, among others.

**Article:** [Unastella, a South Korean rocket startup that launched from home, raises $24M](https://techcrunch.com/2026/06/01/unastella-a-south-korean-rocket-startup-that-launched-from-home-raises-24m/) | en | techcrunch.com
**Ngữ cảnh:**
> As SpaceX counts down to what could be the largest IPO in history, the race to build the next generation of launch vehicles is heating up. Asia wants in. Startups across Australia, India, Japan, and South Korea are racing to establish themselves in a market long dominated by the U.S. and China.
> One of them is Unastella, a four-year-old South Korean startup that just closed a $24 million Series B, bringing its total funding to $44 million. The company launched its own rocket, the UNA EXPRESS-I, from South Korean soil in May 2025.
> The Seoul-based rocket startup is developing its own launch vehicles and engines, with an initial focus on small satellite launch services. Unastella’s near-term focus is validating its technology and business model through orbital launches, with crewed suborbital spaceflight as a longer-term goal, founder and CEO Jae Park told TechCrunch.
> Unastella uses a kerosene and liquid oxygen propulsion system, one of the most proven combinations in rocket history, and one that is also used by SpaceX’s Falcon series. On top of that, the company swapped out the traditional turbo pump for an electric motor pump, a simpler and cheaper alternative that Rocket Lab has already validated in flight.
> The tradeoff is payload. Electric motor pumps are heavier, which means less room for satellites. But Park said that’s a deliberate decision.
> “We’re not an R&D group trying to build the most impressive rocket,” Park said. “We’re a commercial launch company trying to get to market fast.”
> Park also notes that Unastella handles everything in-house, such as design, manufacturing, ground operations, and flight data. The UNA EXPRESS-I launch last year was the first real-world test of the entire system end-to-end, Park said.
> The CEO has spent his entire career working on rocket engines. Before founding Unastella, Park worked on combustion systems for Korea’s Nuri rocket — the country’s first indigenously developed orbital launch vehicle, built by the Korea Aerospace Research Institute (KARI). He then moved to the German Aerospace Center in Berlin to work on European launch vehicle engines, and returned to Korea to join another rocket startup before deciding to build his own.
> Unastella isn’t generating revenue yet, but investors appear to be backing the startup’s roadmap. Altos Ventures led the Series B, joined by Korea Development Bank, Strong Ventures, and Hana Ventures, among others.
> UNA EXPRESS-II, targeted for next year, is the launch Park is really building toward. Reaching 100 kilometers would mark a significant milestone, one he believes will open the door to partnerships with South Korea’s major aerospace and defense firms.
> The 22-person startup has already laid the foundation and developed institutional relationships. K

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0074 -->
## 074. edge-0074

**Triple:** AEON Group (ORG) —INVESTED_IN→ AEON Mall Bắc Ninh Project (PROJECT)
**Assertion status:** reported
**Evidence:**
> Retailer AEON received a licence for a US$149 million shopping mall project in Bắc Ninh Province, while railway and property developer Nishitetsu said it planned to develop around 22,000 affordable homes in Việt Nam.

**Article:** [Japanese firms bet on Việt Nam as a strategic growth hub](https://vietnamnews.vn/economy/1781972/japanese-firms-bet-on-viet-nam-as-a-strategic-growth-hub.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> HÀ NỘI — Japanese companies are accelerating investment in Việt Nam, expanding beyond manufacturing into retail, housing and consumer sectors as they reposition the Southeast Asian nation as a strategic growth hub in Asia.
> 
> In the first weeks of the second quarter, several Japanese firms announced new projects in Việt Nam.
> 
> Retailer AEON received a licence for a US$149 million shopping mall project in Bắc Ninh Province, while railway and property developer Nishitetsu said it planned to develop around 22,000 affordable homes in Việt Nam.
> 
> Meanwhile, confectionery maker Fujiya has selected Tây Ninh Province as a production base for its Country Ma’am biscuit line for distribution across Asian markets, including Japan.
> 
> The investments highlight how Japanese businesses are upgrading their approach to Việt Nam, viewing the country not only as a low-cost manufacturing base or emerging 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0075 -->
## 075. edge-0075

**Triple:** Also Capital (ORG) —CO_INVESTED_WITH→ Michigan Rise (ORG)
**Assertion status:** reported
**Evidence:**
> Maka Kids is building a streaming app for children ages zero to six featuring content designed for healthy development. The startup has now raised $3 million in pre-seed funding to scale its platform, and is currently accepting waitlist sign-ups.
> Unlike traditional streaming platforms, Maka Kids doesn’t have recommendation algorithms, ads, or auto-play. Instead, it is designed to offer a predictable experience that supports learning, creativity, and emotional growth.
> Maka Kids was founded by Isabel Sheinman and Tanyella Leta, who previously founded Nabu, a non-profit venture that brought children’s books to more than 15 million children across 26 countries.
> Sheinman and Leta were introduced at a dinner back in 2013 through a mutual friend and immediately hit it off, the pair told TechCrunch in an email. They said they initially over the fact that they both came from families of educators and entrepreneurs, an experience that first inspired Nabu and later fueled their passion for Maka Kids.
> They began dreaming up the concept of Maka Kids after discussions with their friends, families, and customers at Nabu. They heard from parents who felt increasingly anxious about the effects of screen time on their children. Building on those concerns, the duo conducted hundreds of user interviews, which ultimately shaped their solution: a children’s streaming app designed with well-being at its core.
> “We were seeing parents get completely overwhelmed trying to weigh decisions about what was unsafe, what was good, and understand why their kid was melting down every time screen time ended,” Sheinman said. “At the same time, we watched the children’s media ecosystem get louder, faster, more algorithmically driven. Looking at this problem, we felt uniquely positioned to deliver the relief that parents craved.”
> All of the content on Maka Kids is evaluated using Maka Imprint, the startup’s patent-pending developmental framework created through two years of R&D in collaboration with researchers at the Yale Child Study Center. The framework maps seven core domains of early childhood development across more than 650 developmental indicators, including language, creativity, emotional skills, and growth mindset.
> Maka Kids licenses content directly from IP holders and individual creators. The startup is also partnering directly with studios and animators to produce original content.
> Every show on the platform goes through an analysis of pacing, stimulation levels, color contrast, and narrative structure. Its catalog features slower-paced, lower-stimulation content with genuine narrative arcs and stories from around the world.
> The duo believes an important factor often missing from the screen time debate for kids is how much the right story, delivered at the right moment, can positively support a young child.
> “Stories can support language development, emotional regulation, curiosity, and give kids a sense of how wide the world is,” Leta said. “Children’s media at its best is one of the most powerful developmental tools families have, when it’s designed with this intention. Most of the platforms children watch on today were designed for adult audiences, with a kids experience crudely bolted on as an afterthought. The incentive for the majority of kids’ streaming platforms is watch time, not well-being.”
> When parents create a profile for their child, they can select channels focused on a variety of topics, such as kindness, STEM, emotional regulation, or movement, and then set preferred session lengths. From there, Maka Kids delivers curated, developmentally vetted content tailored to those selections.
> The session then ends naturally, with wind-down cues from characters to help children calmly transition away from screen time without a meltdown.
> Maka Kids is running a private beta on iOS this summer and plans to launch publicly this fall on iPhone and iPad, with casting support via AirPlay. Maka Kids says it already has thousands of families on its waitlist.
> As for the startup’s business model, the app will operate on a subscription model, priced at $11.99 per month, with a discounted annual option.
> In terms of the new funding, the startup plans to use it to grow its catalog of vetted shows. The round was led by Michigan Rise, with participation from Union Heritage Ventures, Flybridge, Also Capital, Detroit Venture Partners, Song United, Invest Detroit, Ann Arbor Spark Capital, 84I90, Georgetown Gain, and Segal Ventures, as well as angel investors.

**Article:** [Maka Kids is redefining kids’ screen time with a streaming app optimized for well-being, not engagement](https://techcrunch.com/2026/05/21/maka-kids-is-redefining-kids-screen-time-with-a-streaming-app-optimized-for-well-being-not-engagement/) | en | techcrunch.com
**Ngữ cảnh:**
> In a media landscape dominated by Baby Shark and Skibidi Toilet, one startup is reimagining children’s media by focusing on well-being, not watch time.
> Maka Kids is building a streaming app for children ages zero to six featuring content designed for healthy development. The startup has now raised $3 million in pre-seed funding to scale its platform, and is currently accepting waitlist sign-ups.
> Unlike traditional streaming platforms, Maka Kids doesn’t have recommendation algorithms, ads, or auto-play. Instead, it is designed to offer a predictable experience that supports learning, creativity, and emotional growth.
> Maka Kids was founded by Isabel Sheinman and Tanyella Leta, who previously founded Nabu, a non-profit venture that brought children’s books to more than 15 million children across 26 countries.
> Sheinman and Leta were introduced at a dinner back in 2013 through a mutual friend and immediately hit it off, the pair told TechCrunch in an email. They said they initially over the fact that they both came from families of educators and entrepreneurs, an experience that first inspired Nabu and later fueled their passion for Maka Kids.
> They began dreaming up the concept of Maka Kids after discussions with their friends, families, and customers at Nabu. They heard from parents who felt increasingly anxious about the effects of screen time on their children. Building on those concerns, the duo conducted hundreds of user interviews, which ultimately shaped their solution: a children’s streaming app designed with well-being at its core.
> “We were seeing parents get completely overwhelmed trying to weigh decisions about what was unsafe, what was good, and understand why their kid was melting down every time screen time ended,” Sheinman said. “At the same time, we watched the children’s media ecosystem get louder, faster, more algorithmically driven. Looking at this problem, we felt uniquely positioned to deliver the relief that parents craved.”
> All of the content on Maka Kids is evaluated using Maka Imprint, the startup’s patent-pending developmental framework created through two years of R&D in collaboration with researchers at the Yale Child Study Center. The framework maps seven core domains of early childhood development across more than 650 developmental indicators, including language, creativity, emotional skills, and growth mindset.
> Maka Kids licenses content directly from IP holders and individual creators. The startup is also partnering directly with studios and animators to produce original content.
> Every show on the platform goes through an analysis of pacing, stimulation levels, color contrast, and narrative structure. Its catalog features slower-paced, lower-stimulation content with genuine narrative arcs and stories from around the world.
> The duo believes an important factor often missing from the screen time debate for kids is how much the right story, delivered at the right moment, can positively support a young child.
> “Stories can support language development, emotional regulation, curiosity, and give kids a sense of how wide the world is,” Leta said. “Children’s media at its best is one of the most powerful developmental tools families have, when it’s designed with this intention. Most of the platforms children watch on today were designed for adult audiences, with a kids experience crudely bolted on as an afterthought. The incentive for the majority of kids’ streaming platforms is watch time, not well-being.”
> When parents create a profile for their child, they can select channels focused on a variety of topics, such as kindness, STEM, emotional regulation, or movement, and then set preferred session lengths. From there, Maka Kids delivers curated, developmentally vetted content tailored to those selections.
> The session then ends naturally, with wind-down cues from characters to help children calmly transition away from screen time without a meltdown.
> Maka Kids is running a private beta on iOS this summer and plans to launch publicly this fall on iPhone and iPad, with casting support via AirPlay. Maka Kids says it already has thousands of families on its waitlist.
> As for the startup’s business model, the app will operate on a subscription model, priced at $11.99 per month, with a discounted annual option.
> In terms of the new funding, the startup plans to use it to grow its catalog of vetted shows. The round was led by Michigan Rise, with participation from Union Heritage Ventures, Flybridge, Also Capital, Detroit Venture Partners, Song United, Invest Detroit, Ann Arbor Spark Capital, 84I90, Georgetown Gain, and Segal Ventures, as well as angel investors.
> “Longer term, our vision is to become the trust layer for every digital experience children have,” Sheinman said. “Embedded into games, edtech products, and shows, Maka Imprint can help developers align their products to what is actually good for kids and families. The kids category deserves a trusted industry standard, and that’s what we are buil

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0076 -->
## 076. edge-0076

**Triple:** Electronic Arts (ORG) —INVESTED_IN→ Stability AI (ORG)
**Assertion status:** reported
**Evidence:**
> The company announced the round Tuesday, saying the new capital comes partly from a number of prominent entertainment industry organizations, including Universal Music Group, Sony Music Group, Warner Music Group, and gaming giant Electronic Arts (EA). Two investment firms, AMD Ventures and Pacific Alliance Ventures, also took part.

**Article:** [Stability AI, maker of image generator Stable Diffusion, raises $76 million in fresh funding](https://techcrunch.com/2026/08/25/stability-ai-maker-of-image-generator-stable-diffusion-raises-76-million-in-fresh-funding/) | en | techcrunch.com
**Ngữ cảnh:**
> Stability AI, the startup behind AI image generation model Stable Diffusion, has raised $76 million in Series B funding. The new haul brings the company’s fundraising total to $232 million.
> The company announced the round Tuesday, saying the new capital comes partly from a number of prominent entertainment industry organizations, including Universal Music Group, Sony Music Group, Warner Music Group, and gaming giant Electronic Arts (EA). Two investment firms, AMD Ventures and Pacific Alliance Ventures, also took part.
> It’s an unusual roster and a less typical venture round than a lineup of the companies Stability now depends on for content licensing and distribution deals.
> Stability AI CEO Prem Akkaraju, who joined the company in 2024, called the funding “an affirmation of our vision where generative AI empowers every producer, musician, and storyteller.”
> The c

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0077 -->
## 077. edge-0077

**Triple:** Dream Ventures (ORG) —INVESTED_IN→ Valar Atomics (ORG)
**Assertion status:** historical_reported
**Evidence:**
> As for Valar’s new round, other investors include Apandion Capital, Atreides Management, Conviction, Dream Ventures, HOF Capital, Point72, Riot Ventures, Snowpoint Ventures, and Valor Equity Partners.

**Article:** [Sequoia&#8217;s Shaun Maguire leads $1B round for nuclear startup Valar Atomics](https://techcrunch.com/2026/08/03/sequoias-shaun-maguire-leads-1b-round-for-nuclear-startup-valar-atomics/) | en | techcrunch.com
**Ngữ cảnh:**
> oducing tens, then hundreds, then thousands of reactors per year,” it said, adding that this funding will allow it to reach its next milestone: manufacturing fleets of its SMRs.
> It certainly isn’t the only nuclear startup pursuing such ambitions. Over the past few months, Antares raised $470 million, and X-energy raised $1 billion through its IPO.
> As for Valar’s new round, other investors include Apandion Capital, Atreides Management, Conviction, Dream Ventures, HOF Capital, Point72, Riot Ventures, Snowpoint Ventures, and Valor Equity Partners.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0078 -->
## 078. edge-0078

**Triple:** Ryan Dahl (PERSON) —FOUNDED→ Deno (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Deno — which was co-founded by Bert Belder and Node.js creator Ryan Dahl — recently launched celld, an open source implementation of Workers, which Varda wrote “delighted” the Cloudflare team. Varda argued that contrary to “a popular theory” that the company “made Cloudflare Workers work differently from other cloud platforms in order to create ‘lock-in,’” the company believes “being open source and giving people an escape hatch is good business .”

**Article:** [Cloudflare acquires Deno to improve its Workers programming model](https://techcrunch.com/2026/10/10/cloudflare-acquires-deno-to-improve-its-workers-programming-model/) | en | techcrunch.com
**Ngữ cảnh:**
>  that it’s acquiring Deno, the startup behind the programming runtime of the same name.
> 
> According to Cloudflare’s Kenton Varda, Cloudflare will use this acquisition to improve its Workers programming model and platform, which allows customers to build and run software on Cloudflare’s network. (Varda is principal engineer for Cloudflare Workers.)
> 
> Deno — which was co-founded by Bert Belder and Node.js creator Ryan Dahl — recently launched celld, an open source implementation of Workers, which Varda wrote “delighted” the Cloudflare team. Varda argued that contrary to “a popular theory” that the company “made Cloudflare Workers work differently from other cloud platforms in order to create ‘lock-in,’” the company believes “being open source and giving people an escape hatch is good business .”
> 
> Dahl, meanwhile, wrote that his team is “joining Cloudflare to make the Workers programming model a mainstream way to build servers.”
> 
> The financial terms of the acquisition were not disclosed. Deno had raised a total of $26 million , including a Series A led by Sequoia.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0079 -->
## 079. edge-0079

**Triple:** Iconiq (ORG) —CO_INVESTED_WITH→ Baillie Gifford (ORG)
**Assertion status:** reported
**Evidence:**
> In a sea of massive valuations for early-stage AI startups, today we have a bit of rare news: a jumbo round and valuation step-up for an e-commerce company. Quince announced on Wednesday that it raised a $500 million Series E round at a $10.1 billion valuation.
> The round was led by previous investor Iconiq, which also led Quince’s $200 million Series D in early 2025 at a reported $4.5 billion valuation. That’s more than double the valuation in less than a year.
> Quince rose to fame on Instagram with its $50 cashmere sweater, but has since amassed a wider range of product offerings, including apparel, home, accessories, beauty, and wellness. Unlike typical e-commerce retail sites, the company manufactures its products and sells them to consumers directly.
> Quince, which launched out of beta in 2020, calls its business model “manufacturer-to-consumer.” And because it owns most of its own tech stack and controls its designs and manufacturing, Quince can more accurately predict its sales, according to a blog post by Iconiq. This allows smaller batch manufacturing with less waste.
> Quince and its investors argue that, unlike fast fashion, Quince can produce higher-quality products at low costs.
> Not that the company has been without controversy. It has faced several lawsuits from brands alleging Quince is selling dupes of their designs. Coach parent Tapestry is suing, as is Williams Sonoma, Puck reported. Deckers also sued over footwear designs, but a court ruled in Quince’s favor.
> If such scuffles have given Quince a copycat reputation, as Puck describes, the site’s customers are apparently unphased. The company says that its top-line revenue has now surpassed $1 billion. In January, it also expanded to Canada.
> Other participating investors include Basis Set Ventures, Wellington Management, WndrCo, MarcyPen Capital Partners, Ballie Gifford, Notable Capital, and DST Global.

**Article:** [Quince hits $10B valuation with giant $500M round led by Iconiq](https://techcrunch.com/2026/03/11/quince-series-e-10b-valuation-with-500m-round-led-by-iconiq/) | en | techcrunch.com
**Ngữ cảnh:**
> In a sea of massive valuations for early-stage AI startups, today we have a bit of rare news: a jumbo round and valuation step-up for an e-commerce company. Quince announced on Wednesday that it raised a $500 million Series E round at a $10.1 billion valuation.
> The round was led by previous investor Iconiq, which also led Quince’s $200 million Series D in early 2025 at a reported $4.5 billion valuation. That’s more than double the valuation in less than a year.
> Quince rose to fame on Instagram with its $50 cashmere sweater, but has since amassed a wider range of product offerings, including apparel, home, accessories, beauty, and wellness. Unlike typical e-commerce retail sites, the company manufactures its products and sells them to consumers directly.
> Quince, which launched out of beta in 2020, calls its business model “manufacturer-to-consumer.” And because it owns most of its own tech stack and controls its designs and manufacturing, Quince can more accurately predict its sales, according to a blog post by Iconiq. This allows smaller batch manufacturing with less waste.
> Quince and its investors argue that, unlike fast fashion, Quince can produce higher-quality products at low costs.
> Not that the company has been without controversy. It has faced several lawsuits from brands alleging Quince is selling dupes of their designs. Coach parent Tapestry is suing, as is Williams Sonoma, Puck reported. Deckers also sued over footwear designs, but a court ruled in Quince’s favor.
> If such scuffles have given Quince a copycat reputation, as Puck describes, the site’s customers are apparently unphased. The company says that its top-line revenue has now surpassed $1 billion. In January, it also expanded to Canada.
> Other participating investors include Basis Set Ventures, Wellington Management, WndrCo, MarcyPen Capital Partners, Ballie Gifford, Notable Capital, and DST Global.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0080 -->
## 080. edge-0080

**Triple:** Iconiq (ORG) —CO_INVESTED_WITH→ Starwood Capital (ORG)
**Assertion status:** reported
**Evidence:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.

**Article:** [Legora reaches $5.55 billion valuation as AI legal tech boom endures](https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/) | en | techcrunch.com
**Ngữ cảnh:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.
> There are other signs that investors are bullish about AI legal tech. Legora’s Series D and valuation jump come just a few months after its October 2025 $150 million Series C round led at a $1.8 billion valuation. Its competitor, Harvey, which is backed by a16z, is already valued at $8 billion, and is now reportedly seeking to raise at an $11 bill

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0081 -->
## 081. edge-0081

**Triple:** Accel (ORG) —CO_INVESTED_WITH→ Andreessen Horowitz (ORG)
**Assertion status:** reported
**Evidence:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.

**Article:** [Kevin Mandia&#8217;s new &#8216;agent swarm&#8217; security startup Armadin raises $255.5M at $2.5B valuation](https://techcrunch.com/2026/10/01/kevin-mandias-new-agent-swarm-security-startup-armadin-raises-255-5m-at-2-5b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.
> The new round comes just six months after Armadin raised a $190 million Series A in March. It has now raised more than $445 million.
> Armadin is offering enterprises a new kind of always-on security by reimagining defense testing for the AI era. Instead of traditional penetration tests, where hired guns attempt to break in and report on the weaknes

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0082 -->
## 082. edge-0082

**Triple:** Mashreq Bank (ORG) —CO_FINANCED_WITH→ Cathay United Bank (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).

**Article:** [VPBank and 15 international financial institutions sign maiden US$1.44 billion sustainability-linked syndicated loan facility](https://vietnamnews.vn/economy/1784501/vpbank-and-15-international-financial-institutions-sign-maiden-us-1-44-billion-sustainability-linked-syndicated-loan-facility.html) | en | vietnamnews.vn
**Ngữ cảnh:**
>  strategic partnership between VPBank and SMBC, while enhancing VPBank’s standing in regional and international financial markets.
> The transaction attracted several financial institutions taking on lead roles for the first time or expanding their existing participation, with these banks accounting for nearly half of all participating institutions.
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).
> With the partnership of 15 international financial institutions, this facility represents VPBank’s largest-ever transaction in terms of the number of MLAUBs involved. The scale of the transaction and the breadth of participation underscore the strong confidence of the international financial community in VPBank’s financial strength, growth prospec

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0083 -->
## 083. edge-0083

**Triple:** Fidelity Management (ORG) —CO_INVESTED_WITH→ Ridgeline (ORG)
**Assertion status:** reported
**Evidence:**
> Electric truck startup Harbinger has raised a $240 million Series D funding round as it expands its portfolio of products, including battery storage and defense applications.
> The funding comes almost one year to the day after the Los Angeles-based company announced a $160 million Series C, which included an initial truck order from FedEx. Harbinger has now raised more than $650 million to date, according to Bloomberg News, which first reported the round.
> The Series D was co-led by Tiger Global, Capricorn’s “technology impact fund,” and defense-focused firm Ridgeline. FedEx invested again after leading last year’s round, and other repeat investors included Maniv, Greycroft, and Leitmotif, a VC firm backed by Volkswagen. Also investing this time was institutional giant Fidelity Management, which tends to invest in pre-IPO startups. (Harbinger is reportedly weighing going public.)

**Article:** [Harbinger raises $240M after expanding into defense](https://techcrunch.com/2026/11/05/harbinger-raises-240m-after-expanding-into-defense/) | en | techcrunch.com
**Ngữ cảnh:**
> Electric truck startup Harbinger has raised a $240 million Series D funding round as it expands its portfolio of products, including battery storage and defense applications.
> The funding comes almost one year to the day after the Los Angeles-based company announced a $160 million Series C, which included an initial truck order from FedEx. Harbinger has now raised more than $650 million to date, according to Bloomberg News, which first reported the round.
> The Series D was co-led by Tiger Global, Capricorn’s “technology impact fund,” and defense-focused firm Ridgeline. FedEx invested again after leading last year’s round, and other repeat investors included Maniv, Greycroft, and Leitmotif, a VC firm backed by Volkswagen. Also investing this time was institutional giant Fidelity Management, which tends to invest in pre-IPO startups. (Harbinger is reportedly weighing going public.)
> While it didn’t lead this round, FedEx’s relationship with Harbinger continues to deepen. The shipping giant’s senior vice president of safety and transportation, Paul Melander, has joined Harbinger’s board of directors. FedEx also recently placed its first large order with Harbinger — a deal for 2,000 trucks valued at more than $300 million.
> Foun

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0084 -->
## 084. edge-0084

**Triple:** Caffeinated Capital (ORG) —INVESTED_IN→ Antares (ORG)
**Assertion status:** reported
**Evidence:**
> Nuclear power startup Antares Nuclear said Monday that it has raised $470 million to build small reactors for U.S. military bases.
> The Series C round, which was led by Paradigm and Caffeinated Capital with participation from Industrious Ventures, Point72 Ventures, and Shine Capital, underscores investors’ growing interest in advanced nuclear startups — a trend fueled by an AI data center building boom and demand for new sources of power. The Series C round included $370 million in equity and $100 million in debt.

**Article:** [Antares raises $470M to build nuclear reactors for the US military](https://techcrunch.com/2026/07/27/antares-raises-470m-to-build-nuclear-reactors-for-the-u-s-military/) | en | techcrunch.com
**Ngữ cảnh:**
> Nuclear power startup Antares Nuclear said Monday that it has raised $470 million to build small reactors for U.S. military bases.
> The Series C round, which was led by Paradigm and Caffeinated Capital with participation from Industrious Ventures, Point72 Ventures, and Shine Capital, underscores investors’ growing interest in advanced nuclear startups — a trend fueled by an AI data center building boom and demand for new sources of power. The Series C round included $370 million in equity and $100 million in debt.
> Antares has been developing a small modular reactor (SMR) capable of producing between 100 kilowatts and 1 megawatt of electricity, enough to power up to 750 homes.
> Like many other advanced nuclear startups, Antares’ reactor uses TRISO fuel, which encapsulates uranium in carbon and ceramic shells. TRISO has been touted for years as a safer alterna

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0085 -->
## 085. edge-0085

**Triple:** China Mobile (ORG) —INVESTED_IN→ Moonshot AI (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The round was led by Chinese food delivery company Meituan’s VC arm, Long-Z Investments, a spokesperson told TechCrunch. Also participating were Tsinghua Capital, China Mobile, and CPE Yuanfeng, according to the post.

**Article:** [China&#8217;s Moonshot AI raises $2B at $20B valuation as demand for open source AI skyrockets](https://techcrunch.com/2026/05/07/chinas-moonshot-ai-raises-2b-at-20b-valuation-as-demand-for-open-source-ai-skyrockets/) | en | techcrunch.com
**Ngữ cảnh:**
> rformance hit in exchange for cheap inference. And investors are taking notice.
> Moonshot AI, the Beijing-based AI lab developing the popular Kimi series of open-weight large language models, has raised about $2 billion at a valuation of $20 billion, according to a post by Huafeng Capital, which advised some investors who participated in the round.
> The round was led by Chinese food delivery company Meituan’s VC arm, Long-Z Investments, a spokesperson told TechCrunch. Also participating were Tsinghua Capital, China Mobile, and CPE Yuanfeng, according to the post.
> The company raised $3.9 billion over the past six months, according to Huafeng Capital. Moonshot was valued at $4.3 billion at the end of 2025, per reports, and by early 2026, that figure had more than doubled to $10 billion following a $700 million raise.
> Moonshot AI was founded in 2023 by Yang Zhilin, a former Meta AI and Google Brain researcher

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0086 -->
## 086. edge-0086

**Triple:** Felicis (ORG) —INVESTED_IN→ Arena (ORG)
**Assertion status:** reported
**Evidence:**
> - Arena, a large language model evaluation platform, raised a $150 million Series A round that was co-led by Felicis and UC Investments. This round valued the one-year-old startup at $1.7 billion and was announced on January 6.

**Article:** [Here are the 17 US-based AI companies that have raised $100M or more in 2026](https://techcrunch.com/2026/02/17/here-are-the-17-us-based-ai-companies-that-have-raised-100m-or-more-in-2026/) | en | techcrunch.com
**Ngữ cảnh:**
> alued the startup at $14 billion. The round was announced on January 14 and was led by SoftBank and Nvidia.
> - Voice AI platform Deepgram raised a $130 million Series C round led by AVP, with participation from Tiger Global, ServiceNow Ventures, and Madrona, among others. The round was announced on January 13 and valued the company at $1.3 billion.
> - Arena, a large language model evaluation platform, raised a $150 million Series A round that was co-led by Felicis and UC Investments. This round valued the one-year-old startup at $1.7 billion and was announced on January 6.
> - Elon Musk’s xAI started the new year with a bang. The AI research lab announced a $20 billion Series E round on January 6. Valor Equity Partners, Fidelity, and the Qatar Investment Authority participated in the round, among others. The company was acquired by Musk’s SpaceX a few weeks later.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0087 -->
## 087. edge-0087

**Triple:** Liquid 2 Ventures (ORG) —INVESTED_IN→ Altara (ORG)
**Assertion status:** reported
**Evidence:**
> San Francisco-based startup Altara, which just secured $7 million in seed funding, says it has built an AI layer designed to bridge these data gaps and bring fragmented technical information into a single platform. The round was led by Greylock, with participation from Neo, BoxGroup, Liquid 2 Ventures, and Jeff Dean.

**Article:** [Altara secures $7M to bridge the data gap that&#8217;s slowing down physical sciences](https://techcrunch.com/2026/05/05/altara-secures-7m-to-bridge-the-data-gap-thats-slowing-down-physical-sciences/) | en | techcrunch.com
**Ngữ cảnh:**
> Companies working on batteries, semiconductors, and medical devices generate vast amounts of data — and much of it ends up scattered across spreadsheets and legacy systems, making it hard to use to improve products or understand failures.
> San Francisco-based startup Altara, which just secured $7 million in seed funding, says it has built an AI layer designed to bridge these data gaps and bring fragmented technical information into a single platform. The round was led by Greylock, with participation from Neo, BoxGroup, Liquid 2 Ventures, and Jeff Dean.
> Altara was founded in 2025 by Eva Tuecke (pictured right), who previously conducted particle physics research at Fermilab and worked at SpaceX; and Catherine Yeo (pictured left), a former AI engineer at Warp. The two met while studying computer science at Harvard University.
> “Imagine if you’re a company building next-generation batteries, and a ba

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0088 -->
## 088. edge-0088

**Triple:** Accel (ORG) —CO_INVESTED_WITH→ Ballistic Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.

**Article:** [Kevin Mandia&#8217;s new &#8216;agent swarm&#8217; security startup Armadin raises $255.5M at $2.5B valuation](https://techcrunch.com/2026/10/01/kevin-mandias-new-agent-swarm-security-startup-armadin-raises-255-5m-at-2-5b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.
> The new round comes just six months after Armadin raised a $190 million Series A in March. It has now raised more than $445 million.
> Armadin is offering enterprises a new kind of always-on security by reimagining defense testing for the AI era. Instead of traditional penetration tests, where hired guns attempt to break in and report on the weaknes

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0089 -->
## 089. edge-0089

**Triple:** Orvia Vietnam (ORG) —JOINT_VENTURE_OF→ De Heus Group (ORG)
**Assertion status:** reported
**Evidence:**
> Orvia Vietnam is a joint venture between De Heus Group of the Netherlands, Orvia Group of France and Lan Chi Livestock Company of Việt Nam, combining three complementary areas of expertise.

**Article:** [Orvia Vietnam inaugurates US$10 million duck hatchery in Tây Ninh](https://vietnamnews.vn/brandinfo/1801798/orvia-vietnam-inaugurates-us-10-million-duck-hatchery-in-tay-ninh.html) | vi | vietnamnews.vn
**Ngữ cảnh:**
> rtners, including Orvia France, De Heus and Lan Chi.
> 
> Việt Nam’s duck industry is shifting from smallholder farming towards more structured operations and integrated value chains, increasing demand for high-quality genetics, uniform ducklings, technical support and consistent production performance under different farming and climatic conditions.
> 
> Orvia Vietnam is a joint venture between De Heus Group of the Netherlands, Orvia Group of France and Lan Chi Livestock Company of Việt Nam, combining three complementary areas of expertise.
> 
> Orvia is the exclusive partner in Pekin duck genetics and technical support, building on nearly 50 years of experience in genetics, breeding, reproduction and hatchery performance, initially developed in France and progressively extended across the main duck-producing regions worldwide.
> 
> Lan Chi, Orvia’s long-standing local partner and exclusive 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0090 -->
## 090. edge-0090

**Triple:** Bcons (ORG) —ACQUIRED→ Dự án Phú Định Riverside (PROJECT)
**Assertion status:** reported
**Evidence:**
> Cuối tháng 8, Saigonres chuyển nhượng dự án Phú Định Riverside cho Bcons với giá 245 tỷ đồng.

**Article:** [Chủ đầu tư ồ ạt bán lại dự án](https://vnexpress.net/chu-dau-tu-o-at-ban-lai-du-an-5139588.html) | vi | vnexpress.net
**Ngữ cảnh:**
>  2 tại TP HCM cho Big Gain, giá trị hơn 5.225 tỷ đồng.
> Tập đoàn DIC (DIC Corp) cũng thông qua các thủ tục chuyển nhượng hai phần dự án Đại Phước, gồm phân khu 8 rộng hơn 134.300 m2 cho DCP Châu Á và phần diện tích hơn 19.100 m2 thuộc các phân khu 1, 2, 3 cho Quốc tế Việt Nét. Trước đó DIC Corp cũng chuyển nhượng phân khu 7.1 cho Everland An Giang.
> Cuối tháng 8, Saigonres chuyển nhượng dự án Phú Định Riverside cho Bcons với giá 245 tỷ đồng. Long Thành Riverside mua 93,4% cổ phần Amata Township Long Thành với giá hơn 492 tỷ đồng. Doanh nghiệp này là chủ đầu tư dự án khu đô thị quy mô 753 ha tại Đồng Nai.
> Tại TP HCM, danh sách dự án được đưa ra chào bán cũng khá đa dạng. Công ty cổ phần Him Lam chào bán Khu dân cư Invesco tại xã Bình Hưng; Công ty cổ phần Tập đoàn Gia Định rao bán dự á

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0091 -->
## 091. edge-0091

**Triple:** First Round Capital (ORG) —INVESTED_IN→ Ellis AI (ORG)
**Assertion status:** reported
**Evidence:**
> Ellis AI announced Thursday its emergence from stealth with $10 million in seed funding from investors including First Round Capital, 645 Ventures, Harlem Capital, Khosla Ventures, Thrive Capital, Slow Capital, Kearny Jackson, and Ariel Alternatives CEO Mellody Hobson.

**Article:** [Repeat founder Ryan Williams raises $10M seed for an AI startup for private credit managers](https://techcrunch.com/2026/07/31/repeat-founder-ryan-williams-raises-10m-seed-for-an-ai-startup-for-private-credit-managers/) | en | techcrunch.com
**Ngữ cảnh:**
> Ellis AI announced Thursday its emergence from stealth with $10 million in seed funding from investors including First Round Capital, 645 Ventures, Harlem Capital, Khosla Ventures, Thrive Capital, Slow Capital, Kearny Jackson, and Ariel Alternatives CEO Mellody Hobson.
> Ellis uses AI agents to tackle the fragmented workflow private credit managers deal with, including managing documents, spreadsheets, and correspondence. The company was founded by Ryan Williams, best known for co-creating the real estate investment platform Cadre alongside Josh and Jared Kushner back in 2014. That company raised more than $160 mi

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0092 -->
## 092. edge-0092

**Triple:** Randy Allen (PERSON) —FOUNDED→ Still Bright (ORG)
**Assertion status:** reported
**Evidence:**
> “The fact that we’ve already mined the easily mineable stuff, and the fact that we need many more mines to come into production every year — we’re talking like 60-plus mines — is it seems like an impossibility, like there’s no path to get there,” Randy Allen, co-founder and CEO of Still Bright, told TechCrunch.

**Article:** [How a New Jersey startup found an electrifying way to slash copper costs](https://techcrunch.com/2025/07/30/how-a-new-jersey-startup-found-an-electrifying-way-to-slash-copper-costs/) | en | techcrunch.com
**Ngữ cảnh:**
>  copper promises to push prices to new heights. As the global economy transitions away from fossil fuels, it is going to need twice as much copper in the coming years than humanity has mined throughout all of its existence.
> Still Bright, a New Jersey-based startup founded in 2022, thinks it has found a novel (and cleaner way) to slash those costs.
> “The fact that we’ve already mined the easily mineable stuff, and the fact that we need many more mines to come into production every year — we’re talking like 60-plus mines — is it seems like an impossibility, like there’s no path to get there,” Randy Allen, co-founder and CEO of Still Bright, told TechCrunch.
> But a large fraction of that demand could be met if companies can extract more copper from the ore they already mine.
> Still Bright has developed a new way to extract copper, one that it says can recover nearly all the copper from typical ores without pre-processing steps that lose up to 20% of the metal. It’s effective enough that it could even be

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0093 -->
## 093. edge-0093

**Triple:** Valor Equity Partners (ORG) —CO_INVESTED_WITH→ Human Capital (ORG)
**Assertion status:** reported
**Evidence:**
> The round was led by the United Arab Emirates. The Boring Company said Thursday that it now plans to dig more than 150 kilometers of tunnels in the Middle Eastern country. Andreessen Horowitz, Sequoia Capital, Human Capital, Vy Capital, and Valor Equity Partners also participated.

**Article:** [The Boring Company raises $3B in round led by UAE](https://techcrunch.com/2026/09/10/the-boring-company-raises-3b-in-round-led-by-uae/) | en | techcrunch.com
**Ngữ cảnh:**
> Elon Musk’s tunneling company, The Boring Company, has raised a $3 billion Series D funding round that pushes its valuation to $23 billion.
> 
> The round was led by the United Arab Emirates. The Boring Company said Thursday that it now plans to dig more than 150 kilometers of tunnels in the Middle Eastern country. Andreessen Horowitz, Sequoia Capital, Human Capital, Vy Capital, and Valor Equity Partners also participated.
> 
> The Wall Street Journal reported in July that The Boring Company was looking to raise as much as $4 billion.
> 
> The Boring Company has done most of its digging to date in Las Vegas, Nevada, where it operates a handful of tunnels that connect hotel casinos and the convention center. It recently started work on a project in Nashville, Tennessee, that

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0094 -->
## 094. edge-0094

**Triple:** Jeff Lawson (PERSON) —FOUNDED→ Inertia Enterprises (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Only one fusion experiment, the National Ignition Facility (NIF), has surpassed scientific breakeven, and the chief scientist of that endeavor, Annie Kritcher, is part of Inertia Enterprises‘ founding team. She’s joined by Mike Dunne, a Stanford professor, and Jeff Lawson, who co-founded Twilio and currently owns The Onion. In April, the startup signed three agreements to commercialize the technology developed at the NIF.

**Article:** [Every fusion startup that has raised over $100M](https://techcrunch.com/2026/08/15/every-fusion-startup-that-has-raised-over-100m/) | en | techcrunch.com
**Ngữ cảnh:**
> ucleation Capital, and the Wisconsin Alumni Research Foundation. The company most recently raised a $240 million round in February led by NantWorks with participation from investors, including Deerfield Management, Fidelity Management & Research Company, Oaktree Capital Management, Pelican Energy Partners, and the Sumitomo Corporation of Americas.
> Only one fusion experiment, the National Ignition Facility (NIF), has surpassed scientific breakeven, and the chief scientist of that endeavor, Annie Kritcher, is part of Inertia Enterprises‘ founding team. She’s joined by Mike Dunne, a Stanford professor, and Jeff Lawson, who co-founded Twilio and currently owns The Onion. In April, the startup signed three agreements to commercialize the technology developed at the NIF.
> Inertia plans to use lasers to bombard fusion fuel pellets, an inertial confinement design that echoes the one Kritcher successfully used at the NIF. Inertia Enterprises emerged from stealth in February with $450 million in Series A funding in a round led by Bessemer Venture Partners with participation from GV, Modern Capital, Threshold Ventures, 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0095 -->
## 095. edge-0095

**Triple:** Ted Parkhill (PERSON) —FOUNDED→ Incline Investment Management (ORG)
**Assertion status:** reported
**Evidence:**
> Ông Ted Parkhill, nhà sáng lập Incline Investment Management, nhận định thị trường đang chuyển từ giai đoạn đặt cược vào tiềm năng AI sang đánh giá thực tế chi phí đầu tư cho công nghệ này.

**Article:** [2.500 tỉ USD vốn hoá “bốc hơi“, cổ phiếu AI bị bán tháo dữ dội: Chuyên gia dự báo biến động tiếp theo](https://www.24h.com.vn/kinh-doanh/2500-ti-usd-von-hoa-boc-hoi-co-phieu-ai-bi-ban-thao-du-doi-chuyen-gia-du-bao-bien-dong-tiep-theo-c161a1809114.html) | vi | www.24h.com.vn
**Ngữ cảnh:**
> i Granite Wealth Management, cho rằng các dự án trung tâm dữ liệu sẽ đối mặt với sự phản đối ngày càng lớn từ cộng đồng địa phương do nguy cơ gây quá tải lưới điện và hệ thống cấp nước.
> Theo ước tính của UBS, khoảng 30% công suất trung tâm dữ liệu dự kiến được bổ sung tại Mỹ vào năm 2028 có nguy cơ bị ảnh hưởng nếu các dự án xây dựng bị đình hoãn.
> Ông Ted Parkhill, nhà sáng lập Incline Investment Management, nhận định thị trường đang chuyển từ giai đoạn đặt cược vào tiềm năng AI sang đánh giá thực tế chi phí đầu tư cho công nghệ này.
> Dù AI được kỳ vọng sẽ thay đổi thế giới trong dài hạn, không phải cổ phiếu nào gắn với lĩnh vực này cũng đang được định giá hợp lý. Giới đầu tư vì thế có thể còn chứng kiến những biến động mạnh trong thời gian tới.
> Mất 80 tỷ USD trong 1 ngày, Elon Musk vẫn giàu nhất thế giới
> Tỷ phú Elon Musk đang trải qua một trong những tuần tồi tệ nhất về tài sả

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0096 -->
## 096. edge-0096

**Triple:** Sands Capital (ORG) —CO_INVESTED_WITH→ General Catalyst (ORG)
**Assertion status:** reported
**Evidence:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.

**Article:** [Legora reaches $5.55 billion valuation as AI legal tech boom endures](https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/) | en | techcrunch.com
**Ngữ cảnh:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.
> There are other signs that investors are bullish about AI legal tech. Legora’s Series D and valuation jump come just a few months after its October 2025 $150 million Series C round led at a $1.8 billion valuation. Its competitor, Harvey, which is backed by a16z, is already valued at $8 billion, and is now reportedly seeking to raise at an $11 bill

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0097 -->
## 097. edge-0097

**Triple:** UnternehmerTUM (ORG) —CO_INVESTED_WITH→ First Momentum (ORG)
**Assertion status:** reported
**Evidence:**
> A spinout from the Technical University of Munich (TUM), QuantumDiamonds has also raised a €15 million equity round led by VC firm World Fund, TechCrunch learned exclusively. The company declined to disclose its valuation, but said its round was also backed by Bayern Kapital and existing investors including Creator Fund, Earlybird, First Momentum, IQ Capital, Onsight Ventures, and UnternehmerTUM.

**Article:** [With EU backing, QuantumDiamonds aims to speed up chip manufacturing](https://techcrunch.com/2026/07/08/with-eu-backing-quantumdiamonds-aims-to-speed-up-chip-manufacturing/) | en | techcrunch.com
**Ngữ cảnh:**
> he approval of the European Commission, it has been granted €76 million in non-dilutive funding provided by Germany’s federal economy ministry and the state of Bavaria. The startup will use it to set up a new facility for the production of semiconductor testing equipment in Munich as part of a $178 million investment plan it had already announced.
> A spinout from the Technical University of Munich (TUM), QuantumDiamonds has also raised a €15 million equity round led by VC firm World Fund, TechCrunch learned exclusively. The company declined to disclose its valuation, but said its round was also backed by Bayern Kapital and existing investors including Creator Fund, Earlybird, First Momentum, IQ Capital, Onsight Ventures, and UnternehmerTUM.
> CEO Kevin Berghoff told TechCrunch that raising the round was a fairly quick process, as QuantumDiamonds was able to demonstrate customer pull. “We work with almost everyone in the chip ecosystem,” he said. With huge demand for all kinds of chips, there’s just as much demand for solutions to speed up the manufacturing process and improve the outpu

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0098 -->
## 098. edge-0098

**Triple:** Vista Equity Partners (ORG) —CO_INVESTED_WITH→ General Atlantic (ORG)
**Assertion status:** reported
**Evidence:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Article:** [AI chip maker SambaNova raises $1B at $11B valuation, 5 months after last mega round](https://techcrunch.com/2026/07/08/sambanova-draws-1b-at-11b-valuation-in-series-f-first-close/) | en | techcrunch.com
**Ngữ cảnh:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0099 -->
## 099. edge-0099

**Triple:** Gia Lai Provincial People's Committee (GOV) —APPROVED→ Nam Pleiku Dry Port (PROJECT)
**Assertion status:** reported
**Evidence:**
> HÀ NỘI — The Gia Lai Provincial People’s Committee has recently approved the investment policy and the investor for the VNĐ250 billion (US$9.6 million) Nam Pleiku Dry Port project.

**Article:** [$10 million dry port project approved in Gia Lai Province](https://vietnamnews.vn/economy/1803385/10-million-dry-port-project-approved-in-gia-lai-province.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> HÀ NỘI — The Gia Lai Provincial People’s Committee has recently approved the investment policy and the investor for the VNĐ250 billion (US$9.6 million) Nam Pleiku Dry Port project.
> 
> The project spans 10 hectares and has a designed capacity of 50,000 TEU per year. Key components include a warehouse complex, a container yard and an area for cargo handling and consolidation.
> 
> The project also includes an internal transport network, parking areas, an administrative office, a wastewater treatment system, green spaces and other au

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0100 -->
## 100. edge-0100

**Triple:** Index Ventures (ORG) —CO_INVESTED_WITH→ Bain Capital Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> - Simile, which builds AI to mimic human decisions, raised a $100 million Series A round led by Index Ventures. The round was announced on February 12 and included Hanabi Capital, Bain Capital Ventures, and multiple angel investors.

**Article:** [Here are the 17 US-based AI companies that have raised $100M or more in 2026](https://techcrunch.com/2026/02/17/here-are-the-17-us-based-ai-companies-that-have-raised-100m-or-more-in-2026/) | en | techcrunch.com
**Ngữ cảnh:**
> I startup market is in for another year of monster funding rounds at eye-watering valuations. U.S. AI startups raised more than $76 billion through mega-rounds in 2025, per TechCrunch’s count.
> Will startups see the same success in 2026? Time will tell.
> Here are all the U.S.-based AI startups that have raised $100 million or more thus far:
> February
> - Simile, which builds AI to mimic human decisions, raised a $100 million Series A round led by Index Ventures. The round was announced on February 12 and included Hanabi Capital, Bain Capital Ventures, and multiple angel investors.
> - Anthropic announced a $30 billion Series G funding round on February 12 that valued the AI research lab at $380 billion. More than 30 investors participated in the round, including Founders Fund, Coatue, and Nvidia, among many others.
> - Media-generation platform Runway raised a $315 million Series E round that valued the company at $5.3 billion.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0101 -->
## 101. edge-0101

**Triple:** Korea Development Bank (ORG) —INVESTED_IN→ Config (ORG)
**Assertion status:** reported
**Evidence:**
> Samsung Venture Investment led its oversubscribed $27 million seed round at a valuation of more than $200 million, bringing Config’s total raised to $35 million. Hyundai Motor’s venture arm ZER01NE Ventures; LG Technology Ventures; and SKT America, a South Korean telco giant’s VC unit, also joined as strategic investors. Other investors include angel investor Pieter Abbeel (co-founder of Covariant and a UC Berkeley professor) and financial backers Mirae Asset Ventures, Korea Development Bank, GS Futures, Kakao Ventures, and Z Ventures.

**Article:** [Korea&#8217;s biggest manufacturers back Config, the TSMC of robot data](https://techcrunch.com/2026/05/11/koreas-biggest-manufacturers-back-config-the-tsmc-of-robot-data/) | en | techcrunch.com
**Ngữ cảnh:**
> hains. That structural foundation is now shaping how artificial intelligence is adopted and where investment flows.
> Which makes it particularly significant that Config, a Seoul- and San Jose-based startup building the data layer for robotics foundation models (RFMs), has secured backing from the venture arms of South Korea’s biggest manufacturers.
> Samsung Venture Investment led its oversubscribed $27 million seed round at a valuation of more than $200 million, bringing Config’s total raised to $35 million. Hyundai Motor’s venture arm ZER01NE Ventures; LG Technology Ventures; and SKT America, a South Korean telco giant’s VC unit, also joined as strategic investors. Other investors include angel investor Pieter Abbeel (co-founder of Covariant and a UC Berkeley professor) and financial backers Mirae Asset Ventures, Korea Development Bank, GS Futures, Kakao Ventures, and Z Ventures.
> Config was founded in January 2025 by CEO Minjoon Seo, a former researcher at Meta and chief scientist at TwelveLabs, along with three co-founders with backgrounds at Waymo, Google, and Naver. Instead of building robots themselves, the team is focused on a simpler goal — providing data that robots need to learn and operate. They believe that bette

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0102 -->
## 102. edge-0102

**Triple:** Bill Ackman (PERSON) —CO_INVESTED_WITH→ Guillermo Rauch (PERSON)
**Assertion status:** reported
**Evidence:**
> The round was led by Iconiq’s Murali Joshi, who helped lead the firm’s investments in companies like Anthropic, Datadog, Drata, 1Password, among others.
> Angels who invested include Microsoft CEO Satya Nadella; Palo Alto Networks CEO Nikesh Arora; Pershing Square Holdings CEO Bill Ackman; Palantir CTO Shyam Sankar; Anduril co-founder Trae Stephens; Former OpenAI VP Bob McGrew; Vercel CEO Guillermo Rauch, and Former AT&T CEO John Donovan. Whew!

**Article:** [AI security startup Outtake raises $40M from Iconiq, Satya Nadella, Bill Ackman, and other big names](https://techcrunch.com/2026/01/28/ai-security-startup-outtake-raises-40m-from-iconiq-satya-nadella-bill-ackman-and-other-big-names/) | en | techcrunch.com
**Ngữ cảnh:**
> Outtake, which makes an agentic cybersecurity platform to help enterprises detect, investigate, and take down identity fraud, has raised a $40 million Series B round of funding.
> While that might not sound like a lot given the huge sums some AI companies are raising, the names involved in this financing reads like a tech industry who’s who.
> The round was led by Iconiq’s Murali Joshi, who helped lead the firm’s investments in companies like Anthropic, Datadog, Drata, 1Password, among others.
> Angels who invested include Microsoft CEO Satya Nadella; Palo Alto Networks CEO Nikesh Arora; Pershing Square Holdings CEO Bill Ackman; Palantir CTO Shyam Sankar; Anduril co-founder Trae Stephens; Former OpenAI VP Bob McGrew; Vercel CEO Guillermo Rauch, and Former AT&T CEO John Donovan. Whew!
> The reason for the excitement? Outtake, founded in 2023 by a former Palantir engineer, Alex Dhillon, has found a way to automate what has largely been the manual problem of spotting and taking down digital identity posers: impersonation accounts, malicious domains posing as the company’s, rogue apps, fraudulent ads, and more. This problem has grow

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0103 -->
## 103. edge-0103

**Triple:** Lightspeed (ORG) —CO_INVESTED_WITH→ SignalFire (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Three-year-old Clutch was last valued at $85 million when it raised a $20 million Series A round in January 2025, led by Lightspeed and SignalFire, according to our source. The startup is currently approaching $10 million in annual recurring revenue (ARR). That means the acquisition, if completed, would value Clutch at about 50 times its ARR, a standard way of pricing software companies.

**Article:** [Palo Alto Networks in talks to buy AI agent security startup Clutch for $500M](https://techcrunch.com/2026/11/05/palo-alto-networks-in-talks-to-buy-ai-agent-security-startup-clutch-for-500m/) | en | techcrunch.com
**Ngữ cảnh:**
> Palo Alto Networks is in talks to acquire Clutch Security , a startup that secures AI agents’ access to company systems, for $500 million in cash plus additional milestone-based payouts, according to a person familiar with the discussions.
> 
> Three-year-old Clutch was last valued at $85 million when it raised a $20 million Series A round in January 2025, led by Lightspeed and SignalFire, according to our source. The startup is currently approaching $10 million in annual recurring revenue (ARR). That means the acquisition, if completed, would value Clutch at about 50 times its ARR, a standard way of pricing software companies.
> 
> Palo Alto Networks and Clutch Security did not respond to a request for comment. The Information was the first to report the acquisition discussions.
> 
> The high valuation is not an anomaly in a market increasingly focused on securing software against bad actors using AI to breach systems more easily. Upwind, a startup using AI to secure cloud infr

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0104 -->
## 104. edge-0104

**Triple:** Bain Capital Ventures (ORG) —INVESTED_IN→ Armadin (ORG)
**Assertion status:** reported
**Evidence:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.

**Article:** [Kevin Mandia&#8217;s new &#8216;agent swarm&#8217; security startup Armadin raises $255.5M at $2.5B valuation](https://techcrunch.com/2026/10/01/kevin-mandias-new-agent-swarm-security-startup-armadin-raises-255-5m-at-2-5b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.
> The new round comes just six months after Armadin raised a $190 million Series A in March. It has now raised more than $445 million.
> Armadin is offering enterprises a new kind of always-on security by reimagining defense testing for the AI era. Instead of traditional penetration tests, where hired guns attempt to break in and report on the weaknes

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0105 -->
## 105. edge-0105

**Triple:** Alkeon Capital (ORG) —CO_INVESTED_WITH→ Y Combinator (ORG)
**Assertion status:** reported
**Evidence:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.

**Article:** [Legora reaches $5.55 billion valuation as AI legal tech boom endures](https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/) | en | techcrunch.com
**Ngữ cảnh:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.
> There are other signs that investors are bullish about AI legal tech. Legora’s Series D and valuation jump come just a few months after its October 2025 $150 million Series C round led at a $1.8 billion valuation. Its competitor, Harvey, which is backed by a16z, is already valued at $8 billion, and is now reportedly seeking to raise at an $11 bill

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0106 -->
## 106. edge-0106

**Triple:** Bessemer Venture Partners (ORG) —INVESTED_IN→ Inertia Enterprises (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Inertia plans to use lasers to bombard fusion fuel pellets, an inertial confinement design that echoes the one Kritcher successfully used at the NIF. Inertia Enterprises emerged from stealth in February with $450 million in Series A funding in a round led by Bessemer Venture Partners with participation from GV, Modern Capital, Threshold Ventures, and others.

**Article:** [Every fusion startup that has raised over $100M](https://techcrunch.com/2026/08/15/every-fusion-startup-that-has-raised-over-100m/) | en | techcrunch.com
**Ngữ cảnh:**
> sed scientific breakeven, and the chief scientist of that endeavor, Annie Kritcher, is part of Inertia Enterprises‘ founding team. She’s joined by Mike Dunne, a Stanford professor, and Jeff Lawson, who co-founded Twilio and currently owns The Onion. In April, the startup signed three agreements to commercialize the technology developed at the NIF.
> Inertia plans to use lasers to bombard fusion fuel pellets, an inertial confinement design that echoes the one Kritcher successfully used at the NIF. Inertia Enterprises emerged from stealth in February with $450 million in Series A funding in a round led by Bessemer Venture Partners with participation from GV, Modern Capital, Threshold Ventures, and others.
> Now in its third decade, General Fusion has raised over $442 million, according to FusionX data. The Richmond, British Columbia-based company was founded in 2002 by physicist Michel Laberge, who wanted to prove a different approach to fusion known as magnetized target fusion (MTF). Investors include Jeff Bezos, Temasek, BDC Capital, and Chrysalix 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0107 -->
## 107. edge-0107

**Triple:** Lightspeed (ORG) —INVESTED_IN→ Cyera (ORG)
**Assertion status:** reported
**Evidence:**
> The new round is expected to come just five months after Cyera announced that it had raised a $400 million Series F at a $9 billion valuation led by Blackstone with participation from existing investors, including Accel, Coatue, Lightspeed, Redpoint, Sapphire, Sequoia, Cyberstarts, and others.

**Article:** [Cyera eyes $12B valuation at 80x ARR multiple despite operating losses](https://techcrunch.com/2026/06/02/cyera-eyes-12b-valuation-at-80x-arr-multiple-despite-operating-losses/) | en | techcrunch.com
**Ngữ cảnh:**
> TechCrunch the company is spending money faster than it makes it. Some of those costs are directed at hiring sales staff. According to PitchBook, Cyera has added 500 jobs so far this year.
> Cyera’s spokeperson said that “the numbers cited are factually and significantly inaccurate.” Evolution Equity Partners didn’t respond to a request for comment.
> The new round is expected to come just five months after Cyera announced that it had raised a $400 million Series F at a $9 billion valuation led by Blackstone with participation from existing investors, including Accel, Coatue, Lightspeed, Redpoint, Sapphire, Sequoia, Cyberstarts, and others. The upcoming round will bring Cyera’s total capital haul to at least $2 billion.
> Cyera, which was founded in 2021, has benefited as enterprises turn to its platform to safeguard their data from attackers weaponizing AI. When it announced its Series F, the company claimed its customers comprised one-fifth of the Fortune 500, and its revenue had mor

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0108 -->
## 108. edge-0108

**Triple:** Felicis (ORG) —INVESTED_IN→ Supabase (ORG)
**Assertion status:** historical_reported
**Evidence:**
> But on Tuesday, the fruits of that became evident when it announced a $200 million Series D at a $2 billion post-money valuation led by Accel, with Coatue, Y Combinator, Craft Ventures, and longtime investor Felicis participating in the round, Fortune reported.

**Article:** [Vibe coding helps Supabase nab $200M at $2B valuation just seven months after its last raise](https://techcrunch.com/2025/04/22/vibe-coding-helps-supabase-nab-200m-at-2b-valuation-just-seven-months-after-its-last-raise/) | en | techcrunch.com
**Ngữ cảnh:**
> In 2020, when open source database Supabase was founded, its New Zealand-based CEO, Paul Copplestone, couldn’t have imagined it would be sitting in the sweet spot for 2025’s biggest trend: vibe coding.
> But on Tuesday, the fruits of that became evident when it announced a $200 million Series D at a $2 billion post-money valuation led by Accel, with Coatue, Y Combinator, Craft Ventures, and longtime investor Felicis participating in the round, Fortune reported.
> This fresh $200 million comes just seven months after Supabase announced it raised $80 million led by Peak XV (a Sequoia spinoff) and David Sacks’ Craft Ventures. Supabase wouldn’t comment on the valuation at that time, but PitchBook put it at about $900 million. All told, the startup has now raised about $398 million.
> Supabase is another example 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0109 -->
## 109. edge-0109

**Triple:** Warburg Pincus (ORG) —PARTNERED_WITH→ BW Industrial Development (ORG)
**Assertion status:** reported
**Evidence:**
> Mới đây, BW Industrial Development, liên doanh giữa công ty Warburg Pincus (có trụ sở tại Mỹ) và Becamex IDC thành lập với cam kết đầu tư ban đầu hơn 200 triệu USD.

**Article:** [Nhà đầu tư ngoại tăng 'bắt tay' doanh nghiệp Việt làm dự án](https://vnexpress.net/nha-dau-tu-ngoai-tang-bat-tay-doanh-nghiep-viet-lam-du-an-5139617.html) | vi | vnexpress.net
**Ngữ cảnh:**
> n
> Thay vì mua lại dự án, nhà đầu tư ngoại ngày càng chuộng cách góp vốn, hợp tác với doanh nghiệp Việt để tiếp cận quỹ đất, mở rộng hoạt động phát triển bất động sản.
> Mô hình góp vốn, lập liên doanh với đối tác trong nước giúp các nhà đầu tư nước ngoài tiếp cận quỹ đất, tận dụng kinh nghiệm địa phương, đồng thời chia sẻ nguồn lực và rủi ro đầu tư.
> Mới đây, BW Industrial Development, liên doanh giữa công ty Warburg Pincus (có trụ sở tại Mỹ) và Becamex IDC thành lập với cam kết đầu tư ban đầu hơn 200 triệu USD. Từ quỹ đất hơn 2 triệu m2 khi ra mắt, doanh nghiệp hiện kiểm soát trên 3,8 triệu m2 tại các khu kinh tế và công nghiệp trọng điểm, theo Warburg Pincus.
> Tại phân khúc nhà ở, Frasers Property (tập đoàn bất động sản đa quốc gia có trụ sở chính tại Singapore) và GELEX Infrastructure cũng mở rộng hợp tác từ công nghiệp, logistics sang phát triển đô thị

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0110 -->
## 110. edge-0110

**Triple:** Thrive Capital (ORG) —CO_INVESTED_WITH→ Anti Fund (ORG)
**Assertion status:** reported
**Evidence:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.

**Article:** [Helion, the Sam Altman-backed fusion startup, raises $465M to build a power plant for Microsoft](https://techcrunch.com/2026/06/04/helion-the-sam-altman-backed-fusion-startup-raises-465m-to-build-a-power-plant-for-microsoft/) | en | techcrunch.com
**Ngữ cảnh:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.
> Helion’s approach to fusion power differs from many of its peers. Some use magnets to contain the superheated plasma required for fusion conditions, while others use lasers to compress fusion fuel until it reacts. In both cases, the majority of startups plan to use steam turbines to transform the intense heat into electricity.
> But Helion, which us

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0111 -->
## 111. edge-0111

**Triple:** Bessemer Venture Partners (ORG) —CO_INVESTED_WITH→ Bain Capital (ORG)
**Assertion status:** reported
**Evidence:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.

**Article:** [Legora reaches $5.55 billion valuation as AI legal tech boom endures](https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/) | en | techcrunch.com
**Ngữ cảnh:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.
> There are other signs that investors are bullish about AI legal tech. Legora’s Series D and valuation jump come just a few months after its October 2025 $150 million Series C round led at a $1.8 billion valuation. Its competitor, Harvey, which is backed by a16z, is already valued at $8 billion, and is now reportedly seeking to raise at an $11 bill

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0112 -->
## 112. edge-0112

**Triple:** 1789 Capital (ORG) —CO_INVESTED_WITH→ Apollo Global Management (ORG)
**Assertion status:** reported
**Evidence:**
> Defense tech Hadrian announced on Thursday that it had raised a fresh $1.37 billion round at a valuation of $7.87 billion from a mile-long list of well-known investors.
> The lead investors in the round include WCM Investment Management, Washington Harbour Partners, Valor Equity Partners, 137 Ventures, and Baillie Gifford. Participating investors include 1789 Capital, Morgan Stanley Wealth Management, funds managed by Apollo and T. Rowe Price, as well as firms like CapitalG, Andreessen Horowitz, Founders Fund, Lux Capital, Altimeter, and others.

**Article:** [Defense tech Hadrian raises $1.37B at $8B valuation](https://techcrunch.com/2026/08/06/defense-tech-hadrian-raises-1-37b-at-8b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Defense tech Hadrian announced on Thursday that it had raised a fresh $1.37 billion round at a valuation of $7.87 billion from a mile-long list of well-known investors.
> The lead investors in the round include WCM Investment Management, Washington Harbour Partners, Valor Equity Partners, 137 Ventures, and Baillie Gifford. Participating investors include 1789 Capital, Morgan Stanley Wealth Management, funds managed by Apollo and T. Rowe Price, as well as firms like CapitalG, Andreessen Horowitz, Founders Fund, Lux Capital, Altimeter, and others.
> Founders Fund and Lux led the company’s $260 million Series C financing about a year ago, bringing the total raised to date to around $2 billion, according to PitchBook estimates.
> Hadrian is an interesting defense tech in that it’s not trying to build new AI-powered weapons. The company is building automated manufacturing facilities that will mass

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0113 -->
## 113. edge-0113

**Triple:** Bunat Ventures (ORG) —INVESTED_IN→ Journify (ORG)
**Assertion status:** reported
**Evidence:**
> Journify, the ad signal infrastructure company, today announced a $12 million Series A at four times its previous valuation. Al Mada Ventures led the round, co-led by returning investor Silicon Badia, with Shorooq and Bunat Ventures increasing their investment and Du Ventures and Oraseya Capital joining as new investors. The funding will take Journify into the US and Europe and expand the AI behind its platform.

**Article:** [Journify raises $12M Series A amid 5x growth](https://techcrunch.com/press-release/journify-raises-12m-series-a-amid-5x-growth/) | en | techcrunch.com
**Ngữ cảnh:**
> San Francisco, California, USA, November 3rd, 2026, TechnologyWire
> Investors back Journify’s push into the US and Europe
> Journify, the ad signal infrastructure company, today announced a $12 million Series A at four times its previous valuation. Al Mada Ventures led the round, co-led by returning investor Silicon Badia, with Shorooq and Bunat Ventures increasing their investment and Du Ventures and Oraseya Capital joining as new investors. The funding will take Journify into the US and Europe and expand the AI behind its platform.
> Global ad spend will exceed $1 trillion in 2026, with algorithms expected to place three quarters by 2028, according to dentsu. These systems learn from the customer outcomes brands send back. Browser restrictions, broken tracking, and disconnected offline sales leave them with an incomplete picture of who buys.
> Journify makes sure ad platforms su

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0114 -->
## 114. edge-0114

**Triple:** SoftBank Vision Fund 2 (ORG) —CO_INVESTED_WITH→ Peak XV Partners (ORG)
**Assertion status:** reported
**Evidence:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.

**Article:** [Helion, the Sam Altman-backed fusion startup, raises $465M to build a power plant for Microsoft](https://techcrunch.com/2026/06/04/helion-the-sam-altman-backed-fusion-startup-raises-465m-to-build-a-power-plant-for-microsoft/) | en | techcrunch.com
**Ngữ cảnh:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.
> Helion’s approach to fusion power differs from many of its peers. Some use magnets to contain the superheated plasma required for fusion conditions, while others use lasers to compress fusion fuel until it reacts. In both cases, the majority of startups plan to use steam turbines to transform the intense heat into electricity.
> But Helion, which us

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0115 -->
## 115. edge-0115

**Triple:** Sapphire Ventures (ORG) —INVESTED_IN→ Cyera (ORG)
**Assertion status:** reported
**Evidence:**
> The new round is expected to come just five months after Cyera announced that it had raised a $400 million Series F at a $9 billion valuation led by Blackstone with participation from existing investors, including Accel, Coatue, Lightspeed, Redpoint, Sapphire, Sequoia, Cyberstarts, and others. The upcoming round will bring Cyera’s total capital haul to at least $2 billion.

**Article:** [Cyera eyes $12B valuation at 80x ARR multiple despite operating losses](https://techcrunch.com/2026/06/02/cyera-eyes-12b-valuation-at-80x-arr-multiple-despite-operating-losses/) | en | techcrunch.com
**Ngữ cảnh:**
> TechCrunch the company is spending money faster than it makes it. Some of those costs are directed at hiring sales staff. According to PitchBook, Cyera has added 500 jobs so far this year.
> Cyera’s spokeperson said that “the numbers cited are factually and significantly inaccurate.” Evolution Equity Partners didn’t respond to a request for comment.
> The new round is expected to come just five months after Cyera announced that it had raised a $400 million Series F at a $9 billion valuation led by Blackstone with participation from existing investors, including Accel, Coatue, Lightspeed, Redpoint, Sapphire, Sequoia, Cyberstarts, and others. The upcoming round will bring Cyera’s total capital haul to at least $2 billion.
> Cyera, which was founded in 2021, has benefited as enterprises turn to its platform to safeguard their data from attackers weaponizing AI. When it announced its Series F, the company claimed its customers comprised one-fifth of the Fortune 500, and its revenue had more than tripled in 2025.
> In recent months, the company has used its capital to fin

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0116 -->
## 116. edge-0116

**Triple:** CRV (ORG) —INVESTED_IN→ Vega (ORG)
**Assertion status:** reported
**Evidence:**
> Led by Accel with participation from Cyberstarts, Redpoint, and CRV, the new round nearly doubles Vega’s valuation to $700 million, and brings its total funding to $185 million, money the startup will use to further develop its AI-native security operations suite, beef up its go-to-market team, and expand globally.

**Article:** [Vega raises $120M Series B to rethink how enterprises detect cyber threats](https://techcrunch.com/2026/02/10/vega-raises-120m-series-b-to-rethink-how-enterprises-detect-cyber-threats/) | en | techcrunch.com
**Ngữ cảnh:**
> oding and data lives everywhere.
> AI cybersecurity startup Vega Security wants to flip that approach by running security where the data already lives, implementing in cloud services, data lakes, and existing storage systems. And the two-year-old firm just raised a $120 million Series B round to scale that vision, TechCrunch has exclusively learned.
> Led by Accel with participation from Cyberstarts, Redpoint, and CRV, the new round nearly doubles Vega’s valuation to $700 million, and brings its total funding to $185 million, money the startup will use to further develop its AI-native security operations suite, beef up its go-to-market team, and expand globally.
> Shay Sandler, co-founder and CEO of Vega, told TechCrunch that the current operating model of the SIEM (security information and event management) — the dominant technology in this domain for the last two decades — is not only “crazy expensive,” but is also increasingly causing AI-native security operations to fail. In complex cloud environments, 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0117 -->
## 117. edge-0117

**Triple:** Vietnam-Oman Investment Fund (VOI) (ORG) —JOINT_VENTURE_OF→ Oman Investment Authority (OIA) (ORG)
**Assertion status:** reported
**Evidence:**
> VOI là liên doanh giữa Ủy ban Đầu tư Vương quốc Oman và Tổng công ty Đầu tư và Kinh doanh vốn nhà nước (SCIC), được thành lập vào năm 2008.

**Article:** [Quỹ đầu tư của Oman lần đầu rót vốn vào lĩnh vực du lịch tại Việt Nam](https://vneconomy.vn/quy-dau-tu-cua-oman-lan-dau-rot-von-vao-linh-vuc-du-lich-tai-viet-nam.htm) | vi | vneconomy.vn
**Ngữ cảnh:**
> h vực mới và doanh nghiệp có dư địa tăng trưởng cao, mà Vinpearl chính là minh chứng tiêu biểu.
> “Vinpearl là một trong những nền tảng du lịch và nghỉ dưỡng hàng đầu Việt Nam, có vị thế thuận lợi để hưởng lợi từ sự gia tăng của tiêu dùng nội địa, lượng khách quốc tế ngày càng tăng và đà phát triển mạnh mẽ của ngành du lịch”, đại diện VOI nhận định.
> VOI là liên doanh giữa Ủy ban Đầu tư Vương quốc Oman và Tổng công ty Đầu tư và Kinh doanh vốn nhà nước (SCIC), được thành lập vào năm 2008. Quỹ đóng vai trò cầu nối cho dòng vốn giữa Oman, khu vực Vùng Vịnh và Việt Nam.
> Trong suốt 18 năm hoạt động, VOI đã đồng hành cùng các cơ quan chức năng Việt Nam triển khai hiệu quả nhiều sáng kiến hợp tác, đồng thời đầu tư vào các lĩnh vực then chốt như giáo dục, y tế, năng lượng tái tạo cùng các khoản đầu tư hướng tới phát triển bền vững và an s

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0118 -->
## 118. edge-0118

**Triple:** Deutsche Telekom (ORG) —CO_INVESTED_WITH→ Eva Longoria (PERSON)
**Assertion status:** reported
**Evidence:**
> Voice AI company ElevenLabs revealed new investors that are part of its $500 million Series D fundraise, which was first announced in February. The additions include institutions such as BlackRock, Wellington, D.E. Shaw, and Schroders; enterprises like Nvidia, Salesforce Ventures, Santander, KPN, and Deutsche Telekom; and individual investors such as Jamie Foxx, Eva Longoria, and Squid Game creator Hwang Dong-hyuk.

**Article:** [ElevenLabs lists BlackRock, Jamie Foxx, and Eva Longoria as new investors](https://techcrunch.com/2026/05/05/elevenlabs-lists-blackrock-jamie-foxx-and-eva-longoria-as-new-investors/) | en | techcrunch.com
**Ngữ cảnh:**
> Voice AI company ElevenLabs revealed new investors that are part of its $500 million Series D fundraise, which was first announced in February. The additions include institutions such as BlackRock, Wellington, D.E. Shaw, and Schroders; enterprises like Nvidia, Salesforce Ventures, Santander, KPN, and Deutsche Telekom; and individual investors such as Jamie Foxx, Eva Longoria, and Squid Game creator Hwang Dong-hyuk.
> The startup also noted that it surpassed $500 million in ARR (annual recurring revenue), after ending last year with nearly $350 million in ARR. The company’s co-founder and CEO, Mati Staniszewski, said last month that ElevenLabs added $100 million in net new ARR in Q1 2026, ending the quarter at roughly $450 million in ARR.
> The company has also a

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0119 -->
## 119. edge-0119

**Triple:** B Capital (ORG) —CO_INVESTED_WITH→ 2.2 Capital (ORG)
**Assertion status:** reported
**Evidence:**
> The two-year-old startup said Thursday it had raised $9 million in a seed round led by Susquehanna International Group (SIG) and Lightspeed, with participation from B Capital, Seaborne Capital, Beenext, Sparrow Capital, and 2.2 Capital. The round values Gushwork at $33 million post-money, up from about $7.5 million following its Lightspeed-led $2.1 million pre-seed in July 2023, a person familiar with the matter told TechCrunch. The latest financing brings Gushwork’s total funding to $11 million, the startup said.

**Article:** [Gushwork bets on AI search for customer leads — and early results are emerging](https://techcrunch.com/2026/02/25/gushwork-bets-on-ai-search-for-customer-leads-and-early-results-are-emerging/) | en | techcrunch.com
**Ngữ cảnh:**
> As AI-powered search tools reshape how businesses are discovered online, India-founded startup Gushwork is helping companies capture customers from platforms such as ChatGPT, Gemini, and Perplexity — with early traction that is beginning to draw investor support.
> The two-year-old startup said Thursday it had raised $9 million in a seed round led by Susquehanna International Group (SIG) and Lightspeed, with participation from B Capital, Seaborne Capital, Beenext, Sparrow Capital, and 2.2 Capital. The round values Gushwork at $33 million post-money, up from about $7.5 million following its Lightspeed-led $2.1 million pre-seed in July 2023, a person familiar with the matter told TechCrunch. The latest financing brings Gushwork’s total funding to $11 million, the startup said.
> The funding comes as AI companies, including OpenAI and Perplexity, begin to chip away at traditional web search, prompting incumbents like Google to roll out AI-generated overviews and other conversational features across their search products. Gushwork is betting this shift will create a new opportunity to help businesses surface in AI-driven di

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0120 -->
## 120. edge-0120

**Triple:** Khosla Ventures (ORG) —CO_INVESTED_WITH→ Lightspeed Venture Partners (ORG)
**Assertion status:** reported
**Evidence:**
> Arena, which originated in 2023 as a research project at UC Berkeley that crowdsourced rankings of AI models, has raised a $200 million Series B round at a $3.1 billion valuation, it said on Thursday.
> This comes after the company said it reached $100 million in annualized run-rate revenue in June.
> The round was led by Lightspeed Venture Partners and Khosla Ventures, with Salesforce Ventures, 01 Advisors, Dell Technologies Capital, Endeavor Catalyst, a16z, Felicis, and others joining in. Arena previously announced a $150 million Series A in January at a $1.7 billion post-money valuation. At the time, its annualized revenue was $30 million, it said. So that means its valuation has nearly doubled in about 10 months.

**Article:** [Popular AI leaderboard Arena nearly doubles valuation to $3.1B valuation in 10 months](https://techcrunch.com/2026/10/08/popular-ai-leaderboard-arena-nearly-doubles-valuation-to-3-1b-valuation-in-10-months/) | en | techcrunch.com
**Ngữ cảnh:**
> Arena, which originated in 2023 as a research project at UC Berkeley that crowdsourced rankings of AI models, has raised a $200 million Series B round at a $3.1 billion valuation, it said on Thursday.
> This comes after the company said it reached $100 million in annualized run-rate revenue in June.
> The round was led by Lightspeed Venture Partners and Khosla Ventures, with Salesforce Ventures, 01 Advisors, Dell Technologies Capital, Endeavor Catalyst, a16z, Felicis, and others joining in. Arena previously announced a $150 million Series A in January at a $1.7 billion post-money valuation. At the time, its annualized revenue was $30 million, it said. So that means its valuation has nearly doubled in about 10 months.
> Arena provides a crowdsourced platform that is free for consumers to use. People enter prompts or request vibe-coded projects and then rate which model does it better. Arena claims it has tens of millions of monthly visitors.
> In September of last year, it introduced its commercial product, AI Evaluations, a service that provides model labs and ent

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0121 -->
## 121. edge-0121

**Triple:** Craft Ventures (ORG) —CO_INVESTED_WITH→ Salesforce Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> The company, 8090 Labs, closed a $135 million round led by Salesforce Ventures with participation from Jeffrey Katzenberg’s WndrCo; David Sacks’ Craft Ventures; fellow All-In hosts and “besties” David Friedberg (The Production Board) and Jason Calacanis (Launch); and angel investors like Palo Alto Networks CEO Nikesh Arora and Quora CEO Adam D’Angelo.

**Article:** [Chamath Palihapitiya raises $135M Series A for his AI coding startup, takes CEO role](https://techcrunch.com/2026/06/29/chamath-palihapitiya-raises-135m-series-a-for-his-ai-coding-startup-takes-ceo-role/) | en | techcrunch.com
**Ngữ cảnh:**
> Chamath Palihapitiya, best known for his venture capital firm Social Capital and the All-In podcast, announced Monday that the AI coding startup he founded raised a sizable Series A.
> The company, 8090 Labs, closed a $135 million round led by Salesforce Ventures with participation from Jeffrey Katzenberg’s WndrCo; David Sacks’ Craft Ventures; fellow All-In hosts and “besties” David Friedberg (The Production Board) and Jason Calacanis (Launch); and angel investors like Palo Alto Networks CEO Nikesh Arora and Quora CEO Adam D’Angelo.
> Palihapitiya founded 8090 Labs in January 2024 to offer an AI coding agent specifically for corporate programming teams. Its product, Software Factory, helps corporate coders use AI to build production-quality software, not just vibe-coded prototypes, with all the controls enterprises need, such as audit trails, the company promises.
> With the rais

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0122 -->
## 122. edge-0122

**Triple:** Launch (ORG) —CO_INVESTED_WITH→ Nikesh Arora (PERSON)
**Assertion status:** reported
**Evidence:**
> The company, 8090 Labs, closed a $135 million round led by Salesforce Ventures with participation from Jeffrey Katzenberg’s WndrCo; David Sacks’ Craft Ventures; fellow All-In hosts and “besties” David Friedberg (The Production Board) and Jason Calacanis (Launch); and angel investors like Palo Alto Networks CEO Nikesh Arora and Quora CEO Adam D’Angelo.

**Article:** [Chamath Palihapitiya raises $135M Series A for his AI coding startup, takes CEO role](https://techcrunch.com/2026/06/29/chamath-palihapitiya-raises-135m-series-a-for-his-ai-coding-startup-takes-ceo-role/) | en | techcrunch.com
**Ngữ cảnh:**
> Chamath Palihapitiya, best known for his venture capital firm Social Capital and the All-In podcast, announced Monday that the AI coding startup he founded raised a sizable Series A.
> The company, 8090 Labs, closed a $135 million round led by Salesforce Ventures with participation from Jeffrey Katzenberg’s WndrCo; David Sacks’ Craft Ventures; fellow All-In hosts and “besties” David Friedberg (The Production Board) and Jason Calacanis (Launch); and angel investors like Palo Alto Networks CEO Nikesh Arora and Quora CEO Adam D’Angelo.
> Palihapitiya founded 8090 Labs in January 2024 to offer an AI coding agent specifically for corporate programming teams. Its product, Software Factory, helps corporate coders use AI to build production-quality software, not just vibe-coded prototypes, with all the controls enterprises need, such as audit trails, the company promises.
> With the rais

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0123 -->
## 123. edge-0123

**Triple:** Rule 30 (ORG) —CO_INVESTED_WITH→ Chicago Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> The company raised $6.2 million in funding in a round led by Chicago Ventures, with participation from BAM Ventures, Aglaé Ventures, Corazon Capital, Press On Ventures, Tusk Ventures, Yonder Ventures, Rule 30, and Brown Angel Group.

**Article:** [Siri co-founder backs Helix for its voice ID tech](https://techcrunch.com/2026/11/11/siri-co-founder-backs-helix-for-its-voice-id-tech/) | en | techcrunch.com
**Ngữ cảnh:**
> otos or videos to verify users’ identities. Now, a startup called Helix is betting that voice technology can do the same job, without requiring users to hand over sensitive personal information.
> The voice technology, which can run directly on a user’s device, has attracted backing from Siri co-founder Dag Kittlaus, who will also act as an adviser.
> The company raised $6.2 million in funding in a round led by Chicago Ventures, with participation from BAM Ventures, Aglaé Ventures, Corazon Capital, Press On Ventures, Tusk Ventures, Yonder Ventures, Rule 30, and Brown Angel Group.
> The startup was founded by Alex Oberg, Anna Dorofiyenko, and Mike Hall in 2025. Oberg previously worked at Ticketmaster, which acquired his startup; Dorofiyenko led data science teams at Live Nation and Zillow; and Hall has worked at Nike and Tinder, where he helped develop the initial matching algorithm.
> At Ticketmaster, Oberg played a role in cr

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0124 -->
## 124. edge-0124

**Triple:** Nan Li (PERSON) —INVESTED_IN→ Proximal Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Proximal’s backers include VC firms SignalFire and Kleiner Perkins, Bertelsmann Healthcare Investments, and individual investors such as Dimension Capital co-founders Nan Li and Zavain Dar.

**Article:** [Proximal Ventures raises debut fund to back startups bringing AI to drug development](https://techcrunch.com/2026/11/10/proximal-ventures-raises-debut-fund-to-back-startups-bringing-ai-to-drug-development/) | en | techcrunch.com
**Ngữ cảnh:**
> ng into the life sciences, one of the hardest things to do is starting that initial commercial flywheel,” Raoof said.
> His sales chops, deep understanding of the healthcare ecosystem, and extensive industry relationships gave limited partners, the investors in VC funds, the confidence that he could spot strong startups and help them land customers. Proximal’s backers include VC firms SignalFire and Kleiner Perkins, Bertelsmann Healthcare Investments, and individual investors such as Dimension Capital co-founders Nan Li and Zavain Dar.
> Amy Abernethy, co-founder of Highlander Health and former principal deputy commissioner of the FDA, is also an investor. She first met Raoof when they worked together at Flatiron Health, where she served as chief medical officer. She told TechCrunch that his ability to build relationships and spot industry bottlenecks made a lasting impression. Ab

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0125 -->
## 125. edge-0125

**Triple:** Permanent Capital Ventures (ORG) —INVESTED_IN→ Outmarket (ORG)
**Assertion status:** reported
**Evidence:**
> Outmarket is set to announce that it raised a $34.5 million Series B led by SignalFire, with participation from Fika Ventures, Permanent Capital Ventures, TTV Capital, and Dash Fund. The new round, which comes four months after the startup’s $17 million Series A, valued the company at $335 million, according to a person familiar with the investment.

**Article:** [Insurtech Outmarket raises $34.5M just months after prior round](https://techcrunch.com/2026/09/28/insuretech-outmarket-raises-34-5m-just-months-after-prior-round/) | en | techcrunch.com
**Ngữ cảnh:**
> ding to customers during emergencies.
> That value has attracted over 300 insurance agencies, including 25% among the top 100, as Outmarket’s customers since launching a new product 14 months ago. “For insurance, which is typically not a fast-moving industry, it’s quite fast growth,” Sankhla said.
> Investors have been impressed with the company, too.
> Outmarket is set to announce that it raised a $34.5 million Series B led by SignalFire, with participation from Fika Ventures, Permanent Capital Ventures, TTV Capital, and Dash Fund. The new round, which comes four months after the startup’s $17 million Series A, valued the company at $335 million, according to a person familiar with the investment.
> The startup is not alone in building an AI operating layer for insurance brokerages. Other startups trying to help insurance brokers include Fulcrum AI and FurtherAI.
> But with the U.S. property and casualty insurance market alone over a trillion dollars in annual premiums, Sankhla believes that Outmarket has plenty of room to grow by helping agenc

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0126 -->
## 126. edge-0126

**Triple:** LocalGlobe (ORG) —INVESTED_IN→ Mistral AI (ORG)
**Assertion status:** reported
**Evidence:**
> In June 2023, just one month after being founded, Mistral AI raised a record $113 million seed round led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
> rmy and job agency, Luxembourg, shipping giant CMA, German defense tech startup Helsing, IBM, Orange, and Stellantis.
> How much funding has Mistral AI raised to date?
> Most of Mistral AI’s funding to date was debt financing, but the company has also raised several venture funding rounds, with a grand total around $4 billion, according to Crunchbase.
> In June 2023, just one month after being founded, Mistral AI raised a record $113 million seed round led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.
> Microsoft’s $16.3 million convertible investment 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0127 -->
## 127. edge-0127

**Triple:** Doerr Capital (ORG) —CO_INVESTED_WITH→ Khosla Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Geothermal startup Mazama Energy raised $135 million in an oversubscribed Series B, the startup said Thursday.
> The fresh funding will help the company develop horizontal wells in superhot rocks capable of generating 15 megawatts of electricity per well.
> Mazama plans to start generating electricity sometime next year and said its first site in Oregon is capable of producing 10 gigawatts of electricity. That’s a sharp upward revision from the company’s estimate last year, when investor Vinod Khosla said the site had the potential to produce 5 gigawatts.
> Enhanced geothermal startups are shaping up to be the dark horse in the battle to power AI data centers and other large loads on the grid. While tech companies and data center developers have been throwing their weight behind natural gas, geothermal startups have been quickly advancing their technology.
> Unlike previous geothermal projects, enhanced geothermal startups are targeting deeper and hotter rock. Mazama, for example, has drilled past 10,000 feet in 15 days on its way to about 15,000 feet deep. At those depths, the company can access 750˚ F (400˚ C) heat, which at high pressures turns water into a “supercritical” fluid that’s neither fully liquid nor fully gas — a state that lets it absorb far more energy than ordinary steam. Mazama said that will allow each well to produce up to 10 times more power than traditional geothermal technologies.
> Given the depths Mazama is targeting, the potential payoff is significant. Tapping just 1% of superhot rock worldwide could generate more than 63 terawatts of electricity, according to the University of Twente and the Clean Air Task Force.
> While work at its Oregon site is still in the early stages, the startup has already secured land for a second development. Mazama aims to complete development of the first site by 2030, at which point it says it should generate 200 megawatts of electricity.
> The new round was led by Centaurus Capital and Doerr Capital, with participation from ConocoPhillips and Shell Ventures. Existing investors including Khosla Ventures and Gates Frontier returned, and new investors SiteGround Capital, H. Barton Asset Management, and the Jeffrey and Marieke Rothschild Foundation also joined the round.

**Article:** [Khosla-backed Mazama Energy just raised $135M to drill deeper into superhot-rock geothermal](https://techcrunch.com/2026/09/17/khosla-backed-mazama-energy-just-raised-135m-to-drill-deeper-into-super-hot-rock-geothermal/) | en | techcrunch.com
**Ngữ cảnh:**
> Geothermal startup Mazama Energy raised $135 million in an oversubscribed Series B, the startup said Thursday.
> The fresh funding will help the company develop horizontal wells in superhot rocks capable of generating 15 megawatts of electricity per well.
> Mazama plans to start generating electricity sometime next year and said its first site in Oregon is capable of producing 10 gigawatts of electricity. That’s a sharp upward revision from the company’s estimate last year, when investor Vinod Khosla said the site had the potential to produce 5 gigawatts.
> Enhanced geothermal startups are shaping up to be the dark horse in the battle to power AI data centers and other large loads on the grid. While tech companies and data center developers have been throwing their weight behind natural gas, geothermal startups have been quickly advancing their technology.
> Unlike previous geothermal projects, enhanced geothermal startups are targeting deeper and hotter rock. Mazama, for example, has drilled past 10,000 feet in 15 days on its way to about 15,000 feet deep. At those depths, the company can access 750˚ F (400˚ C) heat, which at high pressures turns water into a “supercritical” fluid that’s neither fully liquid nor fully gas — a state that lets it absorb far more energy than ordinary steam. Mazama said that will allow each well to produce up to 10 times more power than traditional geothermal technologies.
> Given the depths Mazama is targeting, the potential payoff is significant. Tapping just 1% of superhot rock worldwide could generate more than 63 terawatts of electricity, according to the University of Twente and the Clean Air Task Force.
> While work at its Oregon site is still in the early stages, the startup has already secured land for a second development. Mazama aims to complete development of the first site by 2030, at which point it says it should generate 200 megawatts of electricity.
> The new round was led by Centaurus Capital and Doerr Capital, with participation from ConocoPhillips and Shell Ventures. Existing investors including Khosla Ventures and Gates Frontier returned, and new investors SiteGround Capital, H. Barton Asset Management, and the Jeffrey and Marieke Rothschild Foundation also joined the round.
> Mazama was incubated at Khosla Ventures.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0128 -->
## 128. edge-0128

**Triple:** Sequoia (ORG) —INVESTED_IN→ Odessia (ORG)
**Assertion status:** reported
**Evidence:**
> The year-old Odessia raised a $6 million pre-seed round led by Sequoia and launched its AI travel agent around five months ago.

**Article:** [OpenAI acquires Odessia, travel startup created by Sonder founder](https://techcrunch.com/2026/11/10/openai-acquires-odessia-travel-startup-created-by-sonder-founder/) | en | techcrunch.com
**Ngữ cảnh:**
> dessia’s founder, Francis Davidson. Davidson says in a post announcing the deal that he’s now working for OpenAI, helping the AI lab with the future of travel.
> Terms of the deal were not disclosed, but this looks like an acqui-hire. Davidson’s announcement focused largely on how he built his AI travel agent Odessia by directing teams of AI agents. The year-old Odessia raised a $6 million pre-seed round led by Sequoia and launched its AI travel agent around five months ago. Davidson says that it had helped early adopters plan millions of dollars’ worth of travel, but the tool has already been shut down.
> OpenAI did not announce this acquisition, nor confirm it to TechCrunch, when asked. Nor has it announced new travel-specific products or plans. It does, however, count such companies as Bookings.com, Expedia, and KAYA

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0129 -->
## 129. edge-0129

**Triple:** Nvidia (ORG) —CO_INVESTED_WITH→ Sutter Hill Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> SiFive, a company founded in 2015 by the UC Berkeley engineers who created an open source chip design, has landed a $400 million oversubscribed round that values the company at $3.65 billion.
> This deal is interesting for a bunch of reasons. For one, SiFive’s RISC-V open chip design is based on the RISC processor, not Intel’s x86 or ARM, the two major types of CPUs that currently feed Nvidia’s GPU computer system AI empire.
> Also, Nvidia was investor in this round, alongside a long list of VCs, private equity, and hedge funds. The round was led by Atreides Management, founded by former Fidelity investor bigwig Gavin Baker. (Atreides was also an investor in Cerebras Systems $1 billion round). Other investors in the round include Apollo Global Management, D1 Capital Partners, Point72 Turion, T. Rowe Price, Sutter Hill Ventures, and others.

**Article:** [Nvidia-backed SiFive hits $3.65B valuation for open AI chips](https://techcrunch.com/2026/04/11/nvidia-backed-sifive-hits-3-65-billion-valuation-for-open-ai-chips/) | en | techcrunch.com
**Ngữ cảnh:**
> SiFive, a company founded in 2015 by the UC Berkeley engineers who created an open source chip design, has landed a $400 million oversubscribed round that values the company at $3.65 billion.
> This deal is interesting for a bunch of reasons. For one, SiFive’s RISC-V open chip design is based on the RISC processor, not Intel’s x86 or ARM, the two major types of CPUs that currently feed Nvidia’s GPU computer system AI empire.
> Also, Nvidia was investor in this round, alongside a long list of VCs, private equity, and hedge funds. The round was led by Atreides Management, founded by former Fidelity investor bigwig Gavin Baker. (Atreides was also an investor in Cerebras Systems $1 billion round). Other investors in the round include Apollo Global Management, D1 Capital Partners, Point72 Turion, T. Rowe Price, Sutter Hill Ventures, and others.
> SiFive’s business model is like Arm’s was in years past — it licenses its chip designs to those who modify them for their own needs and does not sell the chips themselves. (In March, Arm changed its model when it launched the first-ever chip it manufactured, an AI chip, developed with Meta with customers including OpenAI, Cerebras, and Cloudflare.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0130 -->
## 130. edge-0130

**Triple:** Carpenter Capital (ORG) —INVESTED_IN→ Clipbook (ORG)
**Assertion status:** reported
**Evidence:**
> On Monday, Clipbook, an AI-powered platform that helps companies monitor their media coverage, announced a $3 million seed round co-led by Mark Cuban, Commonweal Ventures, and Carpenter Capital.

**Article:** [How AI PR startup Clipbook won Mark Cuban&#8217;s investment from a cold email](https://techcrunch.com/2025/12/01/how-ai-pr-startup-clipbook-won-mark-cubans-investment-from-a-cold-email/) | en | techcrunch.com
**Ngữ cảnh:**
> On Monday, Clipbook, an AI-powered platform that helps companies monitor their media coverage, announced a $3 million seed round co-led by Mark Cuban, Commonweal Ventures, and Carpenter Capital.
> The deal happened because Clipbook’s founder, Adam Joseph, took a long shot with a cold email that he never thought anyone would read, he told TechCrunch.
> Joseph launched Clipbook in 2023 and bootstrapped it to a million dollars in annual recurring revenue, he said. At that point, about a year ago, he felt he was ready to find investors.
> “I litera

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0131 -->
## 131. edge-0131

**Triple:** Konrad Zieliński (PERSON) —FOUNDED→ Uhura Bionics (ORG)
**Assertion status:** reported
**Evidence:**
> Experience a live demonstration of voice-restoration technology as Uhura Bionics co-founder Konrad Zieliński showcases the Whitney Electrolarynx for a U.S. audience.

**Article:** [More Ways to Disrupt: New 2026 Side Events from KOTRA, WayFounder, Enterprise Ireland, SafetyWing + Descope](https://techcrunch.com/2026/09/29/more-ways-to-disrupt-new-2026-side-events-from-kotra-wayfounder-enterprise-ireland-safetywing-descope/) | en | techcrunch.com
**Ngữ cảnh:**
> onomous, the event brings together leaders working on the challenges of keeping sensitive data and identity secure, with plenty of time to connect away from the conference floor.
> Hosted by: Descope
> RSVP
> More Side Events
> Pursuit of Happiness: Revolutionary Demonstration of Whitney Electrolarynx by Uhura Bionics
> October 7 \| 6:00 p.m. – 10:00 p.m. PT
> Experience a live demonstration of voice-restoration technology as Uhura Bionics co-founder Konrad Zieliński showcases the Whitney Electrolarynx for a U.S. audience. The event explores how technology can help people reclaim their voices and agency following cancer treatment.
> Hosted by: Uhura Bionics
> RSVP
> Find the 10x Opportunity Hiding in Your Product
> October 10 \| 9:00 a.m. – 11:00 a.m. PT
> Learn how first-principles thinking can uncover overlooked customer needs, strengthen product-market fit, and reveal oppor

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0132 -->
## 132. edge-0132

**Triple:** Starwood Capital (ORG) —CO_INVESTED_WITH→ Redpoint Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.

**Article:** [Legora reaches $5.55 billion valuation as AI legal tech boom endures](https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/) | en | techcrunch.com
**Ngữ cảnh:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.
> There are other signs that investors are bullish about AI legal tech. Legora’s Series D and valuation jump come just a few months after its October 2025 $150 million Series C round led at a $1.8 billion valuation. Its competitor, Harvey, which is backed by a16z, is already valued at $8 billion, and is now reportedly seeking to raise at an $11 bill

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0133 -->
## 133. edge-0133

**Triple:** Arab Bank for Investment and Foreign Trade (ORG) —CO_FINANCED_WITH→ Mashreq Bank (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).
> With the partnership of 15 international financial institutions, this facility represents VPBank’s largest-ever transaction in terms of the number of MLAUBs involved. The scale of the transaction and the breadth of participation underscore the strong confidence of the international financial community in VPBank’s financial strength, growth prospects and sustainable development orientation.
> In addition to the MLAUBs, the transaction also received strong market support, with participation from 19 international financial institutions following a series of investor roadshows in two major regional financial markets, Singapore and Taiwan (China).
> Speaking at the signing ceremony, Nguyễn Đức Vinh, CEO of VPBank, said: “The $1.44 billion syndicated loan, supported by 15 leading global financial institutions, is a clear testament to the strong confidence that the international financial community places in VPBank.
> "It also marks an important step forward in the bank’s implementation of sustainability-linked financing instruments, serving both as an affirmation of our commitment and as a catalyst for VPBank to further contribute to sustainable growth objectives, institutionalise Environmental, Social and Governance (ESG) goals, create long-term value for shareholders and customers and make positive contributions to society.”
> Notably, despite ongoing geopolitical uncertainties, escalating tensions in the Middle East and tighter liquidity conditions in global financial markets, the transaction secured commitments from several leading financial institutions in the Middle East, including FAB, Mashreq, NBK, Arab Bank for Investment and Foreign Trade and Doha Bank. Their participation is a strong testament to VPBank’s growing reputation and standing in international capital markets.

**Article:** [VPBank and 15 international financial institutions sign maiden US$1.44 billion sustainability-linked syndicated loan facility](https://vietnamnews.vn/economy/1784501/vpbank-and-15-international-financial-institutions-sign-maiden-us-1-44-billion-sustainability-linked-syndicated-loan-facility.html) | en | vietnamnews.vn
**Ngữ cảnh:**
>  strategic partnership between VPBank and SMBC, while enhancing VPBank’s standing in regional and international financial markets.
> The transaction attracted several financial institutions taking on lead roles for the first time or expanding their existing participation, with these banks accounting for nearly half of all participating institutions.
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).
> With the partnership of 15 international financial institutions, this facility represents VPBank’s largest-ever transaction in terms of the number of MLAUBs involved. The scale of the transaction and the breadth of participation underscore the strong confidence of the international financial community in VPBank’s financial strength, growth prospects and sustainable development orientation.
> In addition to the MLAUBs, the transaction also received strong market support, with participation from 19 international financial institutions following a series of investor roadshows in two major regional financial markets, Singapore and Taiwan (China).
> Speaking at the signing ceremony, Nguyễn Đức Vinh, CEO of VPBank, said: “The $1.44 billion syndicated loan, supported by 15 leading global financial institutions, is a clear testament to the strong confidence that the international financial community places in VPBank.
> "It also marks an important step forward in the bank’s implementation of sustainability-linked financing instruments, serving both as an affirmation of our commitment and as a catalyst for VPBank to further contribute to sustainable growth objectives, institutionalise Environmental, Social and Governance (ESG) goals, create long-term value for shareholders and customers and make positive contributions to society.”
> Notably, despite ongoing geopolitical uncertainties, escalating tensions in the Middle East and tighter liquidity conditions in global financial markets, the transaction secured commitments from several leading financial institutions in the Middle East, including FAB, Mashreq, NBK, Arab Bank for Investment and Foreign Trade and Doha Bank. Their participation is a strong testament to VPBank’s growing reputation and standing in international capital markets.
> The successful completion of the transaction marks an important milestone in VPBank’s strategy to diversify its medium- and long-term funding sources, providing momentum for the bank to pursue its ambitious growth objectives in 2026.
> It also significantly expands VPBank’s network of financial partners, laying a strong foundation for the bank to ac

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0134 -->
## 134. edge-0134

**Triple:** Mithril Capital Management (ORG) —CO_INVESTED_WITH→ SoftBank Vision Fund 2 (ORG)
**Assertion status:** reported
**Evidence:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.

**Article:** [Helion, the Sam Altman-backed fusion startup, raises $465M to build a power plant for Microsoft](https://techcrunch.com/2026/06/04/helion-the-sam-altman-backed-fusion-startup-raises-465m-to-build-a-power-plant-for-microsoft/) | en | techcrunch.com
**Ngữ cảnh:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.
> Helion’s approach to fusion power differs from many of its peers. Some use magnets to contain the superheated plasma required for fusion conditions, while others use lasers to compress fusion fuel until it reacts. In both cases, the majority of startups plan to use steam turbines to transform the intense heat into electricity.
> But Helion, which us

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0135 -->
## 135. edge-0135

**Triple:** FH One Investments (ORG) —CO_INVESTED_WITH→ AP Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Rubi recently raised $7.5 million to build a demonstration scale of its cellulosic production system, which is designed to produce tens of tons of material using CO2 as its main ingredient. The round was led by AP Ventures and FH One Investments, with participation from CMPC Ventures, H&M Group, Talis Capital, and Understorey Ventures, Rubi exclusively told TechCrunch.

**Article:** [H&amp;M wants to make clothing from CO2 using this startup&#8217;s tech](https://techcrunch.com/2026/03/17/hm-wants-to-make-clothing-from-co2-using-this-startups-tech/) | en | techcrunch.com
**Ngữ cảnh:**
> w materials that won’t require fossil fuels. One startup, Rubi, is “basically taking the machinery of biology outside of the cell” to make the building blocks of lyocell and viscose, co-founder and CEO Neeka Mashouf told TechCrunch. The startup’s technology would allow any company that uses cellulose to build products from captured carbon dioxide.
> Rubi recently raised $7.5 million to build a demonstration scale of its cellulosic production system, which is designed to produce tens of tons of material using CO2 as its main ingredient. The round was led by AP Ventures and FH One Investments, with participation from CMPC Ventures, H&M Group, Talis Capital, and Understorey Ventures, Rubi exclusively told TechCrunch.
> The startup has booked more than $60 million in non-binding off-take agreements with a couple of partners, Mashouf told TechCrunch. The company has tested the material with 15 pilot partners, including H&M, Patagonia, and Walmart.
> To make cellulose for lyocell or viscose, Rubi uses enzymes. That differs from other startups, which might use enginee

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0136 -->
## 136. edge-0136

**Triple:** Strava (ORG) —ACQUIRED→ Cal AI (ORG)
**Assertion status:** reported
**Evidence:**
> Recent moves include MyFitnessPal acquiring Cal AI, an AI calorie counting app, and Strava buying two apps: cycling app The Breakaway and running app Runna.

**Article:** [The company behind ClassPass and Mindbody just got a lot bigger with a $7.5B merger](https://techcrunch.com/2026/03/31/the-company-behind-classpass-and-mindbody-just-got-a-lot-bigger-with-a-7-5b-merger/) | en | techcrunch.com
**Ngữ cảnh:**
> s particularly notable. The company says it will reach millions of users across more than 30 countries, bringing together over 40,000 businesses on Mindbody, more than 88,000 venues on ClassPass, upwards of 20,000 employer partners through EGYM Wellpass, and over 33,000 fitness locations with EGYM equipment.
> It’s hardly alone in making such moves. Recent moves include MyFitnessPal acquiring Cal AI, an AI calorie counting app, and Strava buying two apps: cycling app The Breakaway and running app Runna.
> EGYM itself acquired U.S.-based FitReserve in 2024.
> The merger is also a shift away from Playlist’s earlier plans to go public. Back in 2024, the company was operating as Mindbody-ClassPass and was exploring a potential IPO. By 2025, it instead rebranded as Playlist, bringing its three core businesses under a single identity.
> As previously announc

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0137 -->
## 137. edge-0137

**Triple:** Jeffrey and Marieke Rothschild Foundation (ORG) —CO_INVESTED_WITH→ Gates Frontier (ORG)
**Assertion status:** reported
**Evidence:**
> Geothermal startup Mazama Energy raised $135 million in an oversubscribed Series B, the startup said Thursday.
> The fresh funding will help the company develop horizontal wells in superhot rocks capable of generating 15 megawatts of electricity per well.
> Mazama plans to start generating electricity sometime next year and said its first site in Oregon is capable of producing 10 gigawatts of electricity. That’s a sharp upward revision from the company’s estimate last year, when investor Vinod Khosla said the site had the potential to produce 5 gigawatts.
> Enhanced geothermal startups are shaping up to be the dark horse in the battle to power AI data centers and other large loads on the grid. While tech companies and data center developers have been throwing their weight behind natural gas, geothermal startups have been quickly advancing their technology.
> Unlike previous geothermal projects, enhanced geothermal startups are targeting deeper and hotter rock. Mazama, for example, has drilled past 10,000 feet in 15 days on its way to about 15,000 feet deep. At those depths, the company can access 750˚ F (400˚ C) heat, which at high pressures turns water into a “supercritical” fluid that’s neither fully liquid nor fully gas — a state that lets it absorb far more energy than ordinary steam. Mazama said that will allow each well to produce up to 10 times more power than traditional geothermal technologies.
> Given the depths Mazama is targeting, the potential payoff is significant. Tapping just 1% of superhot rock worldwide could generate more than 63 terawatts of electricity, according to the University of Twente and the Clean Air Task Force.
> While work at its Oregon site is still in the early stages, the startup has already secured land for a second development. Mazama aims to complete development of the first site by 2030, at which point it says it should generate 200 megawatts of electricity.
> The new round was led by Centaurus Capital and Doerr Capital, with participation from ConocoPhillips and Shell Ventures. Existing investors including Khosla Ventures and Gates Frontier returned, and new investors SiteGround Capital, H. Barton Asset Management, and the Jeffrey and Marieke Rothschild Foundation also joined the round.

**Article:** [Khosla-backed Mazama Energy just raised $135M to drill deeper into superhot-rock geothermal](https://techcrunch.com/2026/09/17/khosla-backed-mazama-energy-just-raised-135m-to-drill-deeper-into-super-hot-rock-geothermal/) | en | techcrunch.com
**Ngữ cảnh:**
> Geothermal startup Mazama Energy raised $135 million in an oversubscribed Series B, the startup said Thursday.
> The fresh funding will help the company develop horizontal wells in superhot rocks capable of generating 15 megawatts of electricity per well.
> Mazama plans to start generating electricity sometime next year and said its first site in Oregon is capable of producing 10 gigawatts of electricity. That’s a sharp upward revision from the company’s estimate last year, when investor Vinod Khosla said the site had the potential to produce 5 gigawatts.
> Enhanced geothermal startups are shaping up to be the dark horse in the battle to power AI data centers and other large loads on the grid. While tech companies and data center developers have been throwing their weight behind natural gas, geothermal startups have been quickly advancing their technology.
> Unlike previous geothermal projects, enhanced geothermal startups are targeting deeper and hotter rock. Mazama, for example, has drilled past 10,000 feet in 15 days on its way to about 15,000 feet deep. At those depths, the company can access 750˚ F (400˚ C) heat, which at high pressures turns water into a “supercritical” fluid that’s neither fully liquid nor fully gas — a state that lets it absorb far more energy than ordinary steam. Mazama said that will allow each well to produce up to 10 times more power than traditional geothermal technologies.
> Given the depths Mazama is targeting, the potential payoff is significant. Tapping just 1% of superhot rock worldwide could generate more than 63 terawatts of electricity, according to the University of Twente and the Clean Air Task Force.
> While work at its Oregon site is still in the early stages, the startup has already secured land for a second development. Mazama aims to complete development of the first site by 2030, at which point it says it should generate 200 megawatts of electricity.
> The new round was led by Centaurus Capital and Doerr Capital, with participation from ConocoPhillips and Shell Ventures. Existing investors including Khosla Ventures and Gates Frontier returned, and new investors SiteGround Capital, H. Barton Asset Management, and the Jeffrey and Marieke Rothschild Foundation also joined the round.
> Mazama was incubated at Khosla Ventures.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0138 -->
## 138. edge-0138

**Triple:** Aglaé Ventures (ORG) —CO_INVESTED_WITH→ Tusk Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> The company raised $6.2 million in funding in a round led by Chicago Ventures, with participation from BAM Ventures, Aglaé Ventures, Corazon Capital, Press On Ventures, Tusk Ventures, Yonder Ventures, Rule 30, and Brown Angel Group.

**Article:** [Siri co-founder backs Helix for its voice ID tech](https://techcrunch.com/2026/11/11/siri-co-founder-backs-helix-for-its-voice-id-tech/) | en | techcrunch.com
**Ngữ cảnh:**
> otos or videos to verify users’ identities. Now, a startup called Helix is betting that voice technology can do the same job, without requiring users to hand over sensitive personal information.
> The voice technology, which can run directly on a user’s device, has attracted backing from Siri co-founder Dag Kittlaus, who will also act as an adviser.
> The company raised $6.2 million in funding in a round led by Chicago Ventures, with participation from BAM Ventures, Aglaé Ventures, Corazon Capital, Press On Ventures, Tusk Ventures, Yonder Ventures, Rule 30, and Brown Angel Group.
> The startup was founded by Alex Oberg, Anna Dorofiyenko, and Mike Hall in 2025. Oberg previously worked at Ticketmaster, which acquired his startup; Dorofiyenko led data science teams at Live Nation and Zillow; and Hall has worked at Nike and Tinder, where he helped develop the initial matching algorithm.
> At Ticketmaster, Oberg played a role in cr

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0139 -->
## 139. edge-0139

**Triple:** Andreessen Horowitz (ORG) —INVESTED_IN→ Mistral AI (ORG)
**Assertion status:** reported
**Evidence:**
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
> nd led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.
> Microsoft’s $16.3 million convertible investment in Mistral as part of a partnership announced in February 2024 was presented as a Series A extension, implying an unchanged valuation.
> In June 2024, Mistral raised €600 million (about $640 million) in a mix of equity and debt. The long-rumored round was led by General Catalyst at a $6 billion valuat

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0140 -->
## 140. edge-0140

**Triple:** Thrive Capital (ORG) —CO_INVESTED_WITH→ Peak XV Partners (ORG)
**Assertion status:** reported
**Evidence:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.

**Article:** [Helion, the Sam Altman-backed fusion startup, raises $465M to build a power plant for Microsoft](https://techcrunch.com/2026/06/04/helion-the-sam-altman-backed-fusion-startup-raises-465m-to-build-a-power-plant-for-microsoft/) | en | techcrunch.com
**Ngữ cảnh:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.
> Helion’s approach to fusion power differs from many of its peers. Some use magnets to contain the superheated plasma required for fusion conditions, while others use lasers to compress fusion fuel until it reacts. In both cases, the majority of startups plan to use steam turbines to transform the intense heat into electricity.
> But Helion, which us

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0141 -->
## 141. edge-0141

**Triple:** Gradient Ventures (ORG) —INVESTED_IN→ Feather (ORG)
**Assertion status:** reported
**Evidence:**
> That vision was attractive to Gradient Ventures, which backed Feather at its inception, leading the startup’s previously announced $7.6 million pre-seed round.

**Article:** [Meet Feather, the startup building the &#8216;Android of robotics&#8217; for developers](https://techcrunch.com/2026/09/24/meet-feather-the-startup-building-the-android-of-robotics-for-developers/) | en | techcrunch.com
**Ngữ cảnh:**
>  was deployable, and then they added complexity over time.”
> In 2025, after his previous humanoid startup was sold to 1X, Mai (pictured above, left) teamed up with Parsa Bakhtiari (pictured above, right), a former Tesla Model 3 engineer who at one point reported directly to Elon Musk, to build what the duo hopes will become the Android of robotics.
> That vision was attractive to Gradient Ventures, which backed Feather at its inception, leading the startup’s previously announced $7.6 million pre-seed round.
> Since then, Feather has rolled out a modular robotic system that allows developers to customize the hardware for different use cases, such as adjusting arm lengths. The startup has already begun selling to customers, surpassing $1 million in revenue.
> Although Feather is not disclosing its customers, it said that its robots are working as cooks in 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0142 -->
## 142. edge-0142

**Triple:** Dropbox (ORG) —INTEGRATES_WITH→ Muse (ASSET)
**Assertion status:** planned
**Evidence:**
> Beyond its infrastructure ambitions, Dropbox is also bringing more AI capabilities to its core product. Users will be able to ask AI to perform supported tasks using their files, choose between different AI models, and connect their Dropbox content to third-party tools, including ChatGPT, Claude, and Muse.

**Article:** [Dropbox acquires Tigris Data for $350M to bolster its AI infrastructure](https://techcrunch.com/2026/11/05/dropbox-acquires-tigris-data-for-350m-to-bolster-its-ai-iinfrastructure/) | en | techcrunch.com
**Ngữ cảnh:**
> onth, WSJ reported.
> 
> DBX Agent Cloud will initially offer object storage as a stand-alone product, allowing businesses to purchase storage independently and use it with existing tools and applications built for Amazon S3 (Simple Storage Service), which is a cloud storage service that enables businesses to store and retrieve large volumes of data.
> 
> Beyond its infrastructure ambitions, Dropbox is also bringing more AI capabilities to its core product. Users will be able to ask AI to perform supported tasks using their files, choose between different AI models, and connect their Dropbox content to third-party tools, including ChatGPT, Claude, and Muse.
> 
> The company also plans to expand DBX Agent Cloud with additional capabilities designed to help AI systems work with different types of content, including documents, images, audio, and video. Other planned additions include filesystem features that will allow AI agents to manage files and maintain continuity across tasks and sessions.
> 
> Dropbox say

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0143 -->
## 143. edge-0143

**Triple:** Nikola Todorovic (PERSON) —FOUNDED→ Wonder Dynamics (ORG)
**Assertion status:** reported
**Evidence:**
> Nikola Todorovic, co-founder of Wonder Dynamics, an Autodesk company, built industry-changing AI software that makes it easier for creators to animate and bring 3D characters to life.

**Article:** [Creative machines and where AI meets imagination at TechCrunch Disrupt 2025](https://techcrunch.com/2025/10/01/creative-machines-and-where-ai-meets-imagination-at-techcrunch-disrupt-2025/) | en | techcrunch.com
**Ngữ cảnh:**
> d 20% off group passes before October 3, or save up to $444 on your ticket before doors open.
> Meet the founders shaping the future of storytelling, animation, and video with AI
> Prateek Dixit, co-founder of Pocket Entertainment, is pioneering audio-first storytelling, blending AI-driven tools with human creativity to scale stories across the globe.
> Nikola Todorovic, co-founder of Wonder Dynamics, an Autodesk company, built industry-changing AI software that makes it easier for creators to animate and bring 3D characters to life.
> Soyoung Lee, co-founder and head of GTM at TwelveLabs, is redefining how video is searched, understood, and used at scale through advanced video foundation models.
> See how human imagination and AI are redefining the creative industries
> The creative industries are on the edge of a transformation. AI is no longer just behind the scenes — it’s becomi

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0144 -->
## 144. edge-0144

**Triple:** AIRO (ORG) —INVESTED_IN→ Án mạng Karaoke (PROJECT)
**Assertion status:** reported
**Evidence:**
> Trong điện ảnh, doanh nghiệp tham gia khoảng 30-40% vốn đầu tư tùy dự án. Một số phim có sự tham gia của công ty như "Chị chị em em 3", "Án mạng Karaoke" dự kiến khởi chiếu tháng 10 và "Chiến bào" của đạo diễn Victor Vũ.

**Article:** [Liên doanh AI của Kido lấn sân làm phim](https://vnexpress.net/lien-doanh-ai-cua-kido-lan-san-lam-phim-5126383.html) | vi | vnexpress.net
**Ngữ cảnh:**
> phim ngắn và đưa sản phẩm lên FPT Play, TV360. Một hướng khác là khai thác kho nội dung sẵn có của HTV bằng AI để phát triển thành các sản phẩm mới.
> Phim ngắn cũng là bước đệm để mở rộng sang chương trình giải trí và concert. Công ty hợp tác với Mango TV để sản xuất show, chương trình thực tế và concert có nghệ sĩ Việt Nam, Trung Quốc và Hàn Quốc.
> Trong điện ảnh, doanh nghiệp tham gia khoảng 30-40% vốn đầu tư tùy dự án. Một số phim có sự tham gia của công ty như "Chị chị em em 3", "Án mạng Karaoke" dự kiến khởi chiếu tháng 10 và "Chiến bào" của đạo diễn Victor Vũ.
> Ông Nguyên cho biết, AIRO sẽ là một trụ cột mới của Kido nhưng trước mắt hoạt động độc lập. Những năm đầu có thể cần đầu tư lớn cho sản xuất và xây dựng thị trường trước khi doanh thu đủ để tự vận hành. Kido đặt mục tiêu đưa AIRO IPO vào năm 2030, song chưa công bố tổng vốn đầu tư, mục tiêu lợi nhuận và cơ sở định giá cho kế hoạch này.
> Thi Hà

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0145 -->
## 145. edge-0145

**Triple:** Cyberstarts (ORG) —CO_INVESTED_WITH→ Greenoaks (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.

**Article:** [Glow emerges from stealth at $1.2B valuation to challenge endpoint security in the AI era](https://techcrunch.com/2026/07/22/glow-emerges-from-stealth-at-1-2b-valuation-to-challenge-endpoint-security-in-the-ai-era/) | en | techcrunch.com
**Ngữ cảnh:**
> Glow, a cybersecurity startup founded by former Meta and Snowflake executives, emerged from stealth as a unicorn, betting that artificial intelligence is reshaping how enterprises secure employee devices.
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.
> As more enterprises deploy AI tools and attackers increasingly use generative AI to automate phishing, develop malware, and launch more sophisticated cyberattacks, companies are rethinking how they secure endpoints — from employee laptops to servers and other connected devices. Concerns have intensified since Anthropic unveiled its Mythos AI model

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0146 -->
## 146. edge-0146

**Triple:** Strong Ventures (ORG) —INVESTED_IN→ Unastella (ORG)
**Assertion status:** reported
**Evidence:**
> One of them is Unastella, a four-year-old South Korean startup that just closed a $24 million Series B, bringing its total funding to $44 million. The company launched its own rocket, the UNA EXPRESS-I, from South Korean soil in May 2025.
> The Seoul-based rocket startup is developing its own launch vehicles and engines, with an initial focus on small satellite launch services. Unastella’s near-term focus is validating its technology and business model through orbital launches, with crewed suborbital spaceflight as a longer-term goal, founder and CEO Jae Park told TechCrunch.
> Unastella uses a kerosene and liquid oxygen propulsion system, one of the most proven combinations in rocket history, and one that is also used by SpaceX’s Falcon series. On top of that, the company swapped out the traditional turbo pump for an electric motor pump, a simpler and cheaper alternative that Rocket Lab has already validated in flight.
> The tradeoff is payload. Electric motor pumps are heavier, which means less room for satellites. But Park said that’s a deliberate decision.
> “We’re not an R&D group trying to build the most impressive rocket,” Park said. “We’re a commercial launch company trying to get to market fast.”
> Park also notes that Unastella handles everything in-house, such as design, manufacturing, ground operations, and flight data. The UNA EXPRESS-I launch last year was the first real-world test of the entire system end-to-end, Park said.
> The CEO has spent his entire career working on rocket engines. Before founding Unastella, Park worked on combustion systems for Korea’s Nuri rocket — the country’s first indigenously developed orbital launch vehicle, built by the Korea Aerospace Research Institute (KARI). He then moved to the German Aerospace Center in Berlin to work on European launch vehicle engines, and returned to Korea to join another rocket startup before deciding to build his own.
> Unastella isn’t generating revenue yet, but investors appear to be backing the startup’s roadmap. Altos Ventures led the Series B, joined by Korea Development Bank, Strong Ventures, and Hana Ventures, among others.

**Article:** [Unastella, a South Korean rocket startup that launched from home, raises $24M](https://techcrunch.com/2026/06/01/unastella-a-south-korean-rocket-startup-that-launched-from-home-raises-24m/) | en | techcrunch.com
**Ngữ cảnh:**
> As SpaceX counts down to what could be the largest IPO in history, the race to build the next generation of launch vehicles is heating up. Asia wants in. Startups across Australia, India, Japan, and South Korea are racing to establish themselves in a market long dominated by the U.S. and China.
> One of them is Unastella, a four-year-old South Korean startup that just closed a $24 million Series B, bringing its total funding to $44 million. The company launched its own rocket, the UNA EXPRESS-I, from South Korean soil in May 2025.
> The Seoul-based rocket startup is developing its own launch vehicles and engines, with an initial focus on small satellite launch services. Unastella’s near-term focus is validating its technology and business model through orbital launches, with crewed suborbital spaceflight as a longer-term goal, founder and CEO Jae Park told TechCrunch.
> Unastella uses a kerosene and liquid oxygen propulsion system, one of the most proven combinations in rocket history, and one that is also used by SpaceX’s Falcon series. On top of that, the company swapped out the traditional turbo pump for an electric motor pump, a simpler and cheaper alternative that Rocket Lab has already validated in flight.
> The tradeoff is payload. Electric motor pumps are heavier, which means less room for satellites. But Park said that’s a deliberate decision.
> “We’re not an R&D group trying to build the most impressive rocket,” Park said. “We’re a commercial launch company trying to get to market fast.”
> Park also notes that Unastella handles everything in-house, such as design, manufacturing, ground operations, and flight data. The UNA EXPRESS-I launch last year was the first real-world test of the entire system end-to-end, Park said.
> The CEO has spent his entire career working on rocket engines. Before founding Unastella, Park worked on combustion systems for Korea’s Nuri rocket — the country’s first indigenously developed orbital launch vehicle, built by the Korea Aerospace Research Institute (KARI). He then moved to the German Aerospace Center in Berlin to work on European launch vehicle engines, and returned to Korea to join another rocket startup before deciding to build his own.
> Unastella isn’t generating revenue yet, but investors appear to be backing the startup’s roadmap. Altos Ventures led the Series B, joined by Korea Development Bank, Strong Ventures, and Hana Ventures, among others.
> UNA EXPRESS-II, targeted for next year, is the launch Park is really building toward. Reaching 100 kilometers would mark a significant milestone, one he believes will open the door to partnerships with South Korea’s major aerospace and defense firms.
> The 22-person startup has already laid the foundation and developed institutional relationships. K

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0147 -->
## 147. edge-0147

**Triple:** World Fund (ORG) —INVESTED_IN→ Hyperscale (ORG)
**Assertion status:** reported
**Evidence:**
> To build a prototype of the transformer, Hyperscale recently raised a €5 million seed round led by World Fund and Vsquared Ventures, the company exclusively told TechCrunch.

**Article:** [Hyperscale Power is the latest startup to challenge 140-year-old transformer tech](https://techcrunch.com/2026/03/10/hyperscale-power-is-the-latest-startup-to-challenge-140-year-old-transformer-tech/) | en | techcrunch.com
**Ngữ cảnh:**
> o slash the number of components needed by data centers, improve the stability of the grid, and shrink the footprint of power-conversion equipment.
> Now, Hyperscale Power says it can slim things down further. “We haven’t seen something that is as small as our system will be,” Daniel Rothmund, co-founder and CEO at Hyperscale Power, told TechCrunch.
> To build a prototype of the transformer, Hyperscale recently raised a €5 million seed round led by World Fund and Vsquared Ventures, the company exclusively told TechCrunch.
> In the past couple of years, the solid-state transformer market went from nearly nonexistent to almost crowded. Among the competitors are Amperesand, which was incubated by Temasek’s early-stage fund; DG Matrix, which counts industrial giant ABB as an investor; and Heron Power, which was founded by former Tesla executive Drew Baglino and is backed

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0148 -->
## 148. edge-0148

**Triple:** Ministry of Science and Technology of Vietnam (GOV) —COOPERATES_WITH→ Ministry of Industry and Information Technology of China (GOV)
**Assertion status:** reported
**Evidence:**
> The Ministry of Science and Technology of Việt Nam and the Ministry of Science and Technology of China inked an MoU on implementing a Việt Nam-China joint research programme; and the Ministry of Science and Technology of Việt Nam signed another MoU on cooperation in digital technology with the Ministry of Industry and Information Technology of China.

**Article:** [Việt Nam, China sign 32 cooperation documents](https://vietnamnews.vn/politics-laws/1779705/viet-nam-china-sign-32-cooperation-documents.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> n the Ministry of Construction of Việt Nam and the National Development and Reform Commission (NDRC) of China on implementing railway training cooperation to enhance capacity of Vietnamese railway personnel; an MoU on vocational education cooperation between the Ministry of Education and Training of Việt Nam and the Ministry of Education of China.
> The Ministry of Science and Technology of Việt Nam and the Ministry of Science and Technology of China inked an MoU on implementing a Việt Nam-China joint research programme; and the Ministry of Science and Technology of Việt Nam signed another MoU on cooperation in digital technology with the Ministry of Industry and Information Technology of China.
> Meanwhile, the Ministries of Public Security of the two countries signed a protocol on the establishment, management, and operation of a ministerial-level hotline; an MoU on cooperation and exchange in culture, arts, and sports; and another MoU on cooperation in ensuring security and order in tourism activities.
> The Ministries of Justice of Việt N

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0149 -->
## 149. edge-0149

**Triple:** CRV (ORG) —INVESTED_IN→ Outtake (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The firm’s latest investments include CodeRabbit, a startup for AI code review, and Outtake, a company that uses AI for cybersecurity.

**Article:** [Venture firm CRV raises $750M, downsizing after returning capital to investors](https://techcrunch.com/2025/08/01/venture-firm-crv-raises-750m-downsizing-after-returning-capital-to-investors/) | en | techcrunch.com
**Ngữ cảnh:**
> ups and it will focus on backing consumer and devtools companies.
> CRV is known for leading DoorDash’s seed financing and the Series A rounds for both Mercury and Vercel, a cloud platform for web developers, which was last valued at $3.25 billion.
> Since its founding in 1970, CRV has backed over 750 startups, with 80 of them eventually going public.
> The firm’s latest investments include CodeRabbit, a startup for AI code review, and Outtake, a company that uses AI for cybersecurity.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0150 -->
## 150. edge-0150

**Triple:** Bunat Ventures (ORG) —CO_INVESTED_WITH→ Al Mada Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Journify, the ad signal infrastructure company, today announced a $12 million Series A at four times its previous valuation. Al Mada Ventures led the round, co-led by returning investor Silicon Badia, with Shorooq and Bunat Ventures increasing their investment and Du Ventures and Oraseya Capital joining as new investors. The funding will take Journify into the US and Europe and expand the AI behind its platform.

**Article:** [Journify raises $12M Series A amid 5x growth](https://techcrunch.com/press-release/journify-raises-12m-series-a-amid-5x-growth/) | en | techcrunch.com
**Ngữ cảnh:**
> San Francisco, California, USA, November 3rd, 2026, TechnologyWire
> Investors back Journify’s push into the US and Europe
> Journify, the ad signal infrastructure company, today announced a $12 million Series A at four times its previous valuation. Al Mada Ventures led the round, co-led by returning investor Silicon Badia, with Shorooq and Bunat Ventures increasing their investment and Du Ventures and Oraseya Capital joining as new investors. The funding will take Journify into the US and Europe and expand the AI behind its platform.
> Global ad spend will exceed $1 trillion in 2026, with algorithms expected to place three quarters by 2028, according to dentsu. These systems learn from the customer outcomes brands send back. Browser restrictions, broken tracking, and disconnected offline sales leave them with an incomplete picture of who buys.
> Journify makes sure ad platforms su

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0151 -->
## 151. edge-0151

**Triple:** Cohen Circle (ORG) —CO_INVESTED_WITH→ Plug and Play (ORG)
**Assertion status:** reported
**Evidence:**
> Last year, the duo launched Reload, an AI workforce management platform. On Thursday, the company announced its first AI product, Epic, alongside a $2.275 million round led by Anthemis, with participation from Zeal Capital Partners, Plug and Play, Cohen Circle, Blueprint, and Axiom.

**Article:** [Reload wants to give your AI agents a shared memory](https://techcrunch.com/2026/02/19/reload-an-ai-employee-agent-management-platform-raises-2-275m-and-launches-an-ai-employee/) | en | techcrunch.com
**Ngữ cảnh:**
> h serial founders, noticed they were using AI agents to perform tasks they usually would have done themselves. Asare said he came to believe that the future lay in people managing AI employees.
> “And if that’s true, we’ll need a real system to manage them, with structure around onboarding, coordination, and oversight for digital workers,” he added.
> Last year, the duo launched Reload, an AI workforce management platform. On Thursday, the company announced its first AI product, Epic, alongside a $2.275 million round led by Anthemis, with participation from Zeal Capital Partners, Plug and Play, Cohen Circle, Blueprint, and Axiom.
> Reload is a platform that lets organizations manage their AI agents across teams and departments. Companies can connect agents, regardless of who built them (whether by a third party or internally), assign them roles and permissions, and track the work they perform. “Reload acts like the system of record for AI employees, providing visibility, coo

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0152 -->
## 152. edge-0152

**Triple:** American VC (ORG) —INVESTED_IN→ European defense tech (ORG)
**Assertion status:** reported
**Evidence:**
> His path from developing gadgets and software for CIA agents to becoming perhaps the only American VC exclusively investing in European defense tech also appears to be a prescient one.

**Article:** [This American VC is betting on European defense tech; that&#8217;s still very unusual](https://techcrunch.com/2025/05/12/this-american-vc-is-betting-on-european-defense-tech-thats-still-very-unusual/) | en | techcrunch.com
**Ngữ cảnh:**
> o move in herds, which is why Eric Slesinger stands out a bit. While most American investors chase AI startups or U.S.-based defense tech startups, the former CIA officer is hunting for defense tech deals in Europe. In fact, Slesinger, founder of 201 Ventures, recently closed a $22 million fund focused on seed-stage European defense tech startups. His path from developing gadgets and software for CIA agents to becoming perhaps the only American VC exclusively investing in European defense tech also appears to be a prescient one.
> What would compel someone to leave “the best first job ever” at the CIA to pursue this specific ambition? As Slesinger told TechCrunch in a recent StrictlyVC Download podcast interview, the answer came from identifying a critical shift that many missed. “I left because I noticed that the private sector was increasingly playing a role in this compe

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0153 -->
## 153. edge-0153

**Triple:** Detroit Venture Partners (ORG) —INVESTED_IN→ Bloom (ORG)
**Assertion status:** reported
**Evidence:**
> Bloom has raised $3.6 million to become the “Alibaba” of American manufacturing. The seed round was led by SNAK Venture Partners and included Flyover Capital, deep tech firm Mana Ventures, Detroit Venture Partners, Invest Detroit Ventures, and the Michigan Outdoor Innovation Fund.

**Article:** [TechCrunch Mobility: A roadblock clears for self-driving trucks](https://techcrunch.com/2026/10/11/techcrunch-mobility-a-roadblock-clears-for-self-driving-trucks/) | en | techcrunch.com
**Ngữ cảnh:**
> e Owl, Diameter Capital Partners, Franklin Templeton, Fidelity Management & Research Company, HPS Investment Partners, and Oaktree.
> The debt financing comes as the company accelerates its commercial expansion within existing cities while pushing into new markets in the United States, Europe, and Japan.
> Other deals that got my attention this week …
> Bloom has raised $3.6 million to become the “Alibaba” of American manufacturing. The seed round was led by SNAK Venture Partners and included Flyover Capital, deep tech firm Mana Ventures, Detroit Venture Partners, Invest Detroit Ventures, and the Michigan Outdoor Innovation Fund.
> Flai, a startup that developed AI software for dealerships, raised $27 million in a Series A funding round led by automation-focused firm Base10 Partners. The round included funding from dealers (Friedkin Group and Findlay Automotive), Toyota’s venture arm, Y Combinator, and First Round Capital.
> Parallel Systems, a startup developing a rail vehicl

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0154 -->
## 154. edge-0154

**Triple:** Jeffrey and Marieke Rothschild Foundation (ORG) —CO_INVESTED_WITH→ ConocoPhillips (ORG)
**Assertion status:** reported
**Evidence:**
> Geothermal startup Mazama Energy raised $135 million in an oversubscribed Series B, the startup said Thursday.
> The fresh funding will help the company develop horizontal wells in superhot rocks capable of generating 15 megawatts of electricity per well.
> Mazama plans to start generating electricity sometime next year and said its first site in Oregon is capable of producing 10 gigawatts of electricity. That’s a sharp upward revision from the company’s estimate last year, when investor Vinod Khosla said the site had the potential to produce 5 gigawatts.
> Enhanced geothermal startups are shaping up to be the dark horse in the battle to power AI data centers and other large loads on the grid. While tech companies and data center developers have been throwing their weight behind natural gas, geothermal startups have been quickly advancing their technology.
> Unlike previous geothermal projects, enhanced geothermal startups are targeting deeper and hotter rock. Mazama, for example, has drilled past 10,000 feet in 15 days on its way to about 15,000 feet deep. At those depths, the company can access 750˚ F (400˚ C) heat, which at high pressures turns water into a “supercritical” fluid that’s neither fully liquid nor fully gas — a state that lets it absorb far more energy than ordinary steam. Mazama said that will allow each well to produce up to 10 times more power than traditional geothermal technologies.
> Given the depths Mazama is targeting, the potential payoff is significant. Tapping just 1% of superhot rock worldwide could generate more than 63 terawatts of electricity, according to the University of Twente and the Clean Air Task Force.
> While work at its Oregon site is still in the early stages, the startup has already secured land for a second development. Mazama aims to complete development of the first site by 2030, at which point it says it should generate 200 megawatts of electricity.
> The new round was led by Centaurus Capital and Doerr Capital, with participation from ConocoPhillips and Shell Ventures. Existing investors including Khosla Ventures and Gates Frontier returned, and new investors SiteGround Capital, H. Barton Asset Management, and the Jeffrey and Marieke Rothschild Foundation also joined the round.

**Article:** [Khosla-backed Mazama Energy just raised $135M to drill deeper into superhot-rock geothermal](https://techcrunch.com/2026/09/17/khosla-backed-mazama-energy-just-raised-135m-to-drill-deeper-into-super-hot-rock-geothermal/) | en | techcrunch.com
**Ngữ cảnh:**
> Geothermal startup Mazama Energy raised $135 million in an oversubscribed Series B, the startup said Thursday.
> The fresh funding will help the company develop horizontal wells in superhot rocks capable of generating 15 megawatts of electricity per well.
> Mazama plans to start generating electricity sometime next year and said its first site in Oregon is capable of producing 10 gigawatts of electricity. That’s a sharp upward revision from the company’s estimate last year, when investor Vinod Khosla said the site had the potential to produce 5 gigawatts.
> Enhanced geothermal startups are shaping up to be the dark horse in the battle to power AI data centers and other large loads on the grid. While tech companies and data center developers have been throwing their weight behind natural gas, geothermal startups have been quickly advancing their technology.
> Unlike previous geothermal projects, enhanced geothermal startups are targeting deeper and hotter rock. Mazama, for example, has drilled past 10,000 feet in 15 days on its way to about 15,000 feet deep. At those depths, the company can access 750˚ F (400˚ C) heat, which at high pressures turns water into a “supercritical” fluid that’s neither fully liquid nor fully gas — a state that lets it absorb far more energy than ordinary steam. Mazama said that will allow each well to produce up to 10 times more power than traditional geothermal technologies.
> Given the depths Mazama is targeting, the potential payoff is significant. Tapping just 1% of superhot rock worldwide could generate more than 63 terawatts of electricity, according to the University of Twente and the Clean Air Task Force.
> While work at its Oregon site is still in the early stages, the startup has already secured land for a second development. Mazama aims to complete development of the first site by 2030, at which point it says it should generate 200 megawatts of electricity.
> The new round was led by Centaurus Capital and Doerr Capital, with participation from ConocoPhillips and Shell Ventures. Existing investors including Khosla Ventures and Gates Frontier returned, and new investors SiteGround Capital, H. Barton Asset Management, and the Jeffrey and Marieke Rothschild Foundation also joined the round.
> Mazama was incubated at Khosla Ventures.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0155 -->
## 155. edge-0155

**Triple:** Smith Point Capital (ORG) —INVESTED_IN→ Gather AI (ORG)
**Assertion status:** reported
**Evidence:**
> Gather AI, a startup that offers an AI platform for warehouse cameras and drones, has raised a $40 million Series B funding round led by Smith Point Capital.

**Article:** [Gather AI, maker of ‘curious’ warehouse drones, lands $40M led by Keith Block’s firm](https://techcrunch.com/2026/02/09/gather-ai-maker-of-curious-warehouse-drones-lands-40m-led-by-keith-blocks-firm/) | en | techcrunch.com
**Ngữ cảnh:**
> Gather AI, a startup that offers an AI platform for warehouse cameras and drones, has raised a $40 million Series B funding round led by Smith Point Capital. That’s the VC firm founded by former Salesforce co-CEO Keith Block.
> The Gather team first met Smith Point a year ago at a logistics conference, and “it took Keith and his team five minutes to get what we’re doing,” co-founder and CEO Sankalp Arora told TechCrunch.
> What Gather AI is doing is unusual. The three founders met as PhD students at Carneg

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0156 -->
## 156. edge-0156

**Triple:** Bệnh viện Đại học Aalborg (ORG) —PARTNERED_WITH→ Bệnh viện 19-8 (ORG)
**Assertion status:** reported
**Evidence:**
> Các thỏa thuận khác liên quan đến nghiên cứu công nghệ lượng tử giữa FPT và Viện Niels Bohr thuộc Đại học Copenhagen; giáo dục STEAM giữa Hà Nội và LEGO; hợp tác y sinh giữa Bệnh viện 19-8 và Bệnh viện Đại học Aalborg; phát triển du lịch giữa Vietravel và Nordic Travel Associates.

**Article:** [Loạt thỏa thuận hợp tác năng lượng, logistics, công nghệ của Việt Nam - Đan Mạch - Báo VnExpress Kinh doanh](https://vnexpress.net/loat-thoa-thuan-hop-tac-nang-luong-logistics-cong-nghe-cua-viet-nam-dan-mach-5134816.html) | vi | vnexpress.net
**Ngữ cảnh:**
> t, Danish Industry và Scandinavian Airlines (SAS), hướng tới mở rộng hợp tác vận hành sân bay, vận tải hành khách, hàng hóa và liên danh chuyến bay.
> 
> Trong lĩnh vực công nghiệp, Carlsberg trao ý định thư với chính quyền thành phố Huế về mở rộng nhà máy bia tại Khu công nghiệp Phú Bài và với thành phố Đà Nẵng về cam kết đầu tư giai đoạn 2026-2030.
> 
> Các thỏa thuận khác liên quan đến nghiên cứu công nghệ lượng tử giữa FPT và Viện Niels Bohr thuộc Đại học Copenhagen; giáo dục STEAM giữa Hà Nội và LEGO; hợp tác y sinh giữa Bệnh viện 19-8 và Bệnh viện Đại học Aalborg; phát triển du lịch giữa Vietravel và Nordic Travel Associates.
> 
> Phát biểu tại diễn đàn, Tổng Bí thư, Chủ tịch nước Tô Lâm đề nghị các doanh nghiệp Đan Mạch chuyển từ "đầu tư tại Việt Nam" sang "đầu tư cùng Việt Nam", tăng liên kết với doanh nghiệp trong nước, hỗ trợ doanh nghiệp Việt Nam tham gia sâu hơn vào chuỗi giá trị toàn cầu.
> 
> Ông cũng đề nghị chuyển từ "sản xuất tại Việt Nam" sang "nghiên cứu, sáng tạo

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0157 -->
## 157. edge-0157

**Triple:** Terrain Capital (ORG) —CO_INVESTED_WITH→ Kleiner Perkins (ORG)
**Assertion status:** reported
**Evidence:**
> Parallel Web Systems, the AI agent-tool startup founded by former Twitter CEO Parag Agrawal, has raised a $100 million Series B at a $2 billion valuation led by Sequoia. Existing investors Kleiner Perkins, Index Ventures, Khosla Ventures, First Round Capital, Spark Capital, and Terrain Capital also participated, the company said.

**Article:** [Parallel Web Systems hits $2B valuation five months after its last big raise](https://techcrunch.com/2026/04/29/parallel-web-systems-hits-2b-valuation-five-months-after-its-last-big-raise/) | en | techcrunch.com
**Ngữ cảnh:**
> Parallel Web Systems, the AI agent-tool startup founded by former Twitter CEO Parag Agrawal, has raised a $100 million Series B at a $2 billion valuation led by Sequoia. Existing investors Kleiner Perkins, Index Ventures, Khosla Ventures, First Round Capital, Spark Capital, and Terrain Capital also participated, the company said.
> This raise comes just five months after the startup announced its $100 million Series A at a $740 million valuation led by Kleiner and Index, and brings the total capital it raised to $230 million.
> Parallel offers a suite of web search and research APIs specifically for AI agents and names customers such as Clay, Harvey, Notion, and Opendoor. It s

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0158 -->
## 158. edge-0158

**Triple:** Axiom (ORG) —CO_INVESTED_WITH→ Blueprint (ORG)
**Assertion status:** reported
**Evidence:**
> Last year, the duo launched Reload, an AI workforce management platform. On Thursday, the company announced its first AI product, Epic, alongside a $2.275 million round led by Anthemis, with participation from Zeal Capital Partners, Plug and Play, Cohen Circle, Blueprint, and Axiom.

**Article:** [Reload wants to give your AI agents a shared memory](https://techcrunch.com/2026/02/19/reload-an-ai-employee-agent-management-platform-raises-2-275m-and-launches-an-ai-employee/) | en | techcrunch.com
**Ngữ cảnh:**
> h serial founders, noticed they were using AI agents to perform tasks they usually would have done themselves. Asare said he came to believe that the future lay in people managing AI employees.
> “And if that’s true, we’ll need a real system to manage them, with structure around onboarding, coordination, and oversight for digital workers,” he added.
> Last year, the duo launched Reload, an AI workforce management platform. On Thursday, the company announced its first AI product, Epic, alongside a $2.275 million round led by Anthemis, with participation from Zeal Capital Partners, Plug and Play, Cohen Circle, Blueprint, and Axiom.
> Reload is a platform that lets organizations manage their AI agents across teams and departments. Companies can connect agents, regardless of who built them (whether by a third party or internally), assign them roles and permissions, and track the work they perform. “Reload acts like the system of record for AI employees, providing visibility, coo

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0159 -->
## 159. edge-0159

**Triple:** AVP (ORG) —CO_INVESTED_WITH→ Madrona (ORG)
**Assertion status:** reported
**Evidence:**
> - Voice AI platform Deepgram raised a $130 million Series C round led by AVP, with participation from Tiger Global, ServiceNow Ventures, and Madrona, among others. The round was announced on January 13 and valued the company at $1.3 billion.

**Article:** [Here are the 17 US-based AI companies that have raised $100M or more in 2026](https://techcrunch.com/2026/02/17/here-are-the-17-us-based-ai-companies-that-have-raised-100m-or-more-in-2026/) | en | techcrunch.com
**Ngữ cảnh:**
> unced on January 20. Investors in the round include Nvidia, Jeff Bezos, and GV, among others. This round valued the young startup at $4.48 billion.
> - SkildAI, which builds AI models to power robots, raised a $1.4 billion Series C round that valued the startup at $14 billion. The round was announced on January 14 and was led by SoftBank and Nvidia.
> - Voice AI platform Deepgram raised a $130 million Series C round led by AVP, with participation from Tiger Global, ServiceNow Ventures, and Madrona, among others. The round was announced on January 13 and valued the company at $1.3 billion.
> - Arena, a large language model evaluation platform, raised a $150 million Series A round that was co-led by Felicis and UC Investments. This round valued the one-year-old startup at $1.7 billion and was announced on January 6.
> - Elon Musk’s xAI started the new year with a bang. The AI research lab announced a $20 billion Series E round on January

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0160 -->
## 160. edge-0160

**Triple:** Temasek (ORG) —INVESTED_IN→ AMI Labs (ORG)
**Assertion status:** reported
**Evidence:**
> In addition to its lead investors and angels, AMI Labs is backed by Nvidia, Samsung, Sea, Temasek, and Toyota Ventures, as well as French players Association Familiale Mulliez, Groupe Industriel Marcel Dassault, and Publicis Groupe.

**Article:** [Yann LeCun&#8217;s AMI Labs raises $1.03B to build world models](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/) | en | techcrunch.com
**Ngữ cảnh:**
> ions,” LeBrun said.
> When the time comes, AMI Labs will turn to partners to explore deployments — and Nabla is the first disclosed partner expecting to access these early models, but definitely not the last. “This may explain the presence and strong interest of certain industrial players and potential partners in the investment round,” LeBrun said.
> In addition to its lead investors and angels, AMI Labs is backed by Nvidia, Samsung, Sea, Temasek, and Toyota Ventures, as well as French players Association Familiale Mulliez, Groupe Industriel Marcel Dassault, and Publicis Groupe. Aglaé Lab, Alpha Intelligence Capital, Artémis, Bpifrance Digital Venture, New Legacy Ventures, SBVA, and ZEBOX Ventures also participated.
> These investments may take a while to turn into commercial applications. But staying true to LeCun’s beliefs, AMI Labs will publish papers as it goes.
> “We will also make a lot of code open source,” said LeBrun

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0161 -->
## 161. edge-0161

**Triple:** Lightspeed (ORG) —CO_INVESTED_WITH→ General Catalyst (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The Series A round was led by General Catalyst, with participation from existing investors Square Peg, Stripe, Lightspeed, and Moore Capital, while PayPal Ventures joined as a new backer. The all-equity round values the Bengaluru-based startup at $85 million post-investment and brings its total funding to more than $32 million to date.

**Article:** [Stripe, PayPal Ventures bet on India&#8217;s Xflow to fix cross-border B2B payments](https://techcrunch.com/2026/02/23/stripe-paypal-ventures-bet-on-indias-xflow-to-fix-cross-border-b2b-payments/) | en | techcrunch.com
**Ngữ cảnh:**
> Xflow, an Indian fintech startup, has secured backing from both Stripe and PayPal Ventures in a $16.6 million funding round. The investment comes as the company works to carve out a position in cross-border B2B payments, a market still dominated by banks and manual processes.
> The Series A round was led by General Catalyst, with participation from existing investors Square Peg, Stripe, Lightspeed, and Moore Capital, while PayPal Ventures joined as a new backer. The all-equity round values the Bengaluru-based startup at $85 million post-investment and brings its total funding to more than $32 million to date.
> Despite rapid digitization in domestic payments, cross-border B2B transfers for Indian exporters remain heavily reliant on banks, often with limited visibility into fees, settlement timelines, and the final amount received in rupees. The friction is particularly acute for larger exporters moving millions of dollars into India to fund salaries and 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0162 -->
## 162. edge-0162

**Triple:** Justin Banusing (PERSON) —FOUNDED→ Clouted (ORG)
**Assertion status:** reported
**Evidence:**
> Clouted co-founder and CEO Justin Banusing first applied the company’s technology to his personal passion: electronic music and festival production.

**Article:** [Clouted wants to take the guesswork out of making short videos go viral](https://techcrunch.com/2026/05/20/clouted-wants-to-take-the-guesswork-out-of-making-short-videos-go-viral/) | en | techcrunch.com
**Ngữ cảnh:**
> t through a16z’s Speedrun accelerator in 2024, is building the infrastructure to automatically handle both the distribution strategy and the logistics of the clipping process. The platform taps into a network of over 100,000 gig creators to edit clips, then uses AI to determine the best social media platform and target audience for promoting them.
> Clouted co-founder and CEO Justin Banusing first applied the company’s technology to his personal passion: electronic music and festival production. As a longtime DJ, he used Clouted to promote and grow &Friends, a Manila-based electronic dance music and pop-culture festival that now draws over 20,000 people.
> Clouted’s approach has caught investor interest. The startup just announced a $7 million seed round led by Slow Ventures, with participation from Gold House Ventures, Weekend Fund, Peak X

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0163 -->
## 163. edge-0163

**Triple:** Swish Ventures (ORG) —CO_INVESTED_WITH→ Holly Ventures (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.

**Article:** [Glow emerges from stealth at $1.2B valuation to challenge endpoint security in the AI era](https://techcrunch.com/2026/07/22/glow-emerges-from-stealth-at-1-2b-valuation-to-challenge-endpoint-security-in-the-ai-era/) | en | techcrunch.com
**Ngữ cảnh:**
> Glow, a cybersecurity startup founded by former Meta and Snowflake executives, emerged from stealth as a unicorn, betting that artificial intelligence is reshaping how enterprises secure employee devices.
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.
> As more enterprises deploy AI tools and attackers increasingly use generative AI to automate phishing, develop malware, and launch more sophisticated cyberattacks, companies are rethinking how they secure endpoints — from employee laptops to servers and other connected devices. Concerns have intensified since Anthropic unveiled its Mythos AI model

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0164 -->
## 164. edge-0164

**Triple:** Headline (ORG) —CO_INVESTED_WITH→ Firstminute Capital (ORG)
**Assertion status:** reported
**Evidence:**
> In June 2023, just one month after being founded, Mistral AI raised a record $113 million seed round led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
> rmy and job agency, Luxembourg, shipping giant CMA, German defense tech startup Helsing, IBM, Orange, and Stellantis.
> How much funding has Mistral AI raised to date?
> Most of Mistral AI’s funding to date was debt financing, but the company has also raised several venture funding rounds, with a grand total around $4 billion, according to Crunchbase.
> In June 2023, just one month after being founded, Mistral AI raised a record $113 million seed round led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.
> Microsoft’s $16.3 million convertible investment 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0165 -->
## 165. edge-0165

**Triple:** Deutsche Telekom (ORG) —CO_INVESTED_WITH→ Nvidia (ORG)
**Assertion status:** reported
**Evidence:**
> Voice AI company ElevenLabs revealed new investors that are part of its $500 million Series D fundraise, which was first announced in February. The additions include institutions such as BlackRock, Wellington, D.E. Shaw, and Schroders; enterprises like Nvidia, Salesforce Ventures, Santander, KPN, and Deutsche Telekom; and individual investors such as Jamie Foxx, Eva Longoria, and Squid Game creator Hwang Dong-hyuk.

**Article:** [ElevenLabs lists BlackRock, Jamie Foxx, and Eva Longoria as new investors](https://techcrunch.com/2026/05/05/elevenlabs-lists-blackrock-jamie-foxx-and-eva-longoria-as-new-investors/) | en | techcrunch.com
**Ngữ cảnh:**
> Voice AI company ElevenLabs revealed new investors that are part of its $500 million Series D fundraise, which was first announced in February. The additions include institutions such as BlackRock, Wellington, D.E. Shaw, and Schroders; enterprises like Nvidia, Salesforce Ventures, Santander, KPN, and Deutsche Telekom; and individual investors such as Jamie Foxx, Eva Longoria, and Squid Game creator Hwang Dong-hyuk.
> The startup also noted that it surpassed $500 million in ARR (annual recurring revenue), after ending last year with nearly $350 million in ARR. The company’s co-founder and CEO, Mati Staniszewski, said last month that ElevenLabs added $100 million in net new ARR in Q1 2026, ending the quarter at roughly $450 million in ARR.
> The company has also a

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0166 -->
## 166. edge-0166

**Triple:** Velocity (ORG) —INVESTED_IN→ Plurai (ORG)
**Assertion status:** reported
**Evidence:**
> On Wednesday, the startup said it had raised $13 million in seed funding to make that happen. The round was led by Team8, with participation from U&I, Velocity, and Mercer.

**Article:** [Plurai wants to help AI agents work better using the same approach that helped get self-driving cars to roads](https://techcrunch.com/2026/11/11/plurai-wants-to-help-ai-agents-work-better-using-the-same-approach-that-helped-get-self-driving-cars-to-roads/) | en | techcrunch.com
**Ngữ cảnh:**
> e its end-to-end deep learning driving software.
> “The moment that we saw the wave of AI agents, we saw the same pattern: That it is very easy to build a demo, but [hard] to get something that will be reliable and cost effective,” Kadar told TechCrunch. “Since we saw the same pattern, the same pitch was that we want to build this simulation layer.”
> On Wednesday, the startup said it had raised $13 million in seed funding to make that happen. The round was led by Team8, with participation from U&I, Velocity, and Mercer.
> Like the end-to-end models trained to drive cars, AI agents are probabilistic systems operating in unpredictable environments. When pressed by customers, agents tasked with booking travel can ignore spending policies. Or, when tasked with querying one database, agents can reliably provide an answer, but combining information from multiple datasets

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0167 -->
## 167. edge-0167

**Triple:** Notable Capital (ORG) —INVESTED_IN→ Patronus (ORG)
**Assertion status:** reported
**Evidence:**
> Patronus’ revenue has grown 15-fold over the past year, fueling significant investor interest. On Thursday, the company announced a $50 million Series B round led by Greenfield Partners, with participation from Notable Capital, Lightspeed, Datadog, and Samsung. The round brings the company’s total funding to $70 million.

**Article:** [Patronus AI lands $50M to build ‘digital worlds’ that stress-test AI agents](https://techcrunch.com/2026/06/25/patronus-ai-lands-50m-to-build-digital-worlds-that-stress-test-ai-agents/) | en | techcrunch.com
**Ngữ cảnh:**
> nts in which to evaluate the agents’ performance.
> The San Francisco-based startup must be solving an important problem. Virtually every frontier AI lab and many emerging startups are now customers, according to Glenn Solomon, a managing director at Notable Capital, who describes demand for the company’s simulated environments as nearly insatiable.
> Patronus’ revenue has grown 15-fold over the past year, fueling significant investor interest. On Thursday, the company announced a $50 million Series B round led by Greenfield Partners, with participation from Notable Capital, Lightspeed, Datadog, and Samsung. The round brings the company’s total funding to $70 million.
> Patronus uses what it calls “digital world models” to create replicas of websites and internal systems. In these environments, agents are stress-tested after training using reinforcement learning, which iteratively rewards successful task completion and penalizes errors.
> AI labs see great value in these digital simulations because they give agents

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0168 -->
## 168. edge-0168

**Triple:** AVP (ORG) —CO_INVESTED_WITH→ Hillspire (ORG)
**Assertion status:** reported
**Evidence:**
> Parallel Systems, a startup developing a rail vehicle capable of moving over several tons of freight as far as 500 miles without an operator, raised $100 million in a Series C round led by AVP, with participation from Hillspire, Agility Global, Cobalt Capital, Anthos Capital, Congruent Ventures, Riot Ventures, and Collaborative Fund.

**Article:** [TechCrunch Mobility: A roadblock clears for self-driving trucks](https://techcrunch.com/2026/10/11/techcrunch-mobility-a-roadblock-clears-for-self-driving-trucks/) | en | techcrunch.com
**Ngữ cảnh:**
>  Ventures, and the Michigan Outdoor Innovation Fund.
> Flai, a startup that developed AI software for dealerships, raised $27 million in a Series A funding round led by automation-focused firm Base10 Partners. The round included funding from dealers (Friedkin Group and Findlay Automotive), Toyota’s venture arm, Y Combinator, and First Round Capital.
> Parallel Systems, a startup developing a rail vehicle capable of moving over several tons of freight as far as 500 miles without an operator, raised $100 million in a Series C round led by AVP, with participation from Hillspire, Agility Global, Cobalt Capital, Anthos Capital, Congruent Ventures, Riot Ventures, and Collaborative Fund.
> Uber has agreed to buy catering company ezCater in an all-cash transaction valued at $2.3 billion.
> Notable reads and other tidbits
> Surveillance camera maker Flock cut its workforce by 18%, or around 270 employees, as the company faces ongoing and growing backlash to its license plate readers and people-tracking technology. FYI: Flock founder and C

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0169 -->
## 169. edge-0169

**Triple:** CRV (ORG) —INVESTED_IN→ DoorDash (ORG)
**Assertion status:** historical_reported
**Evidence:**
> CRV is known for leading DoorDash’s seed financing and the Series A rounds for both Mercury and Vercel, a cloud platform for web developers, which was last valued at $3.25 billion.

**Article:** [Venture firm CRV raises $750M, downsizing after returning capital to investors](https://techcrunch.com/2025/08/01/venture-firm-crv-raises-750m-downsizing-after-returning-capital-to-investors/) | en | techcrunch.com
**Ngữ cảnh:**
> uld lower its overall returns.
> CRV’s limited partners were eager to back the firm’s smaller fund, the firm said. It raised its entire $750 million fund in just four weeks, with demand for double that amount, CRV wrote.
> The latest fund will be used to invest in seed and Series A startups and it will focus on backing consumer and devtools companies.
> CRV is known for leading DoorDash’s seed financing and the Series A rounds for both Mercury and Vercel, a cloud platform for web developers, which was last valued at $3.25 billion.
> Since its founding in 1970, CRV has backed over 750 startups, with 80 of them eventually going public.
> The firm’s latest investments include CodeRabbit, a startup for AI code review, and Outtake, a company that uses AI for cybersecurity.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0170 -->
## 170. edge-0170

**Triple:** The Export-Import Bank of China (ORG) —CO_FINANCED_WITH→ KEXIM Asia Limited (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> Tham gia giao dịch còn có các định chế tài chính phát triển gồm IFC, DEG (Đức), Proparco (Pháp) và Norfund (Na Uy); các ngân hàng xuất nhập khẩu China Eximbank, Korea Eximbank cùng nhóm ngân hàng thương mại và tổ chức tài chính như SMBC, Punjab National Bank, Commercial Bank of Ceylon, ICBC, Shinhan Bank, Woori Bank và KEXIM Asia Limited.

**Article:** [VPBank huy động 730 triệu USD vốn quốc tế](https://vnexpress.net/vpbank-huy-dong-730-trieu-usd-von-quoc-te-5143246.html) | vi | vnexpress.net
**Ngữ cảnh:**
> y động thành công khoản vay hợp vốn quốc tế 730 triệu USD, tương đương gần 19.000 tỷ đồng, do IFC và SMBC thu xếp, ngày 10/11.
> Giao dịch do Tổ chức Tài chính Quốc tế (IFC) và Ngân hàng Sumitomo Mitsui Banking Corporation (SMBC) đồng điều phối, thu xếp, gồm các khoản vay có kỳ hạn 3 năm, 5 năm và 7 năm, được giải ngân theo nhiều đợt trong năm 2026.
> Tham gia giao dịch còn có các định chế tài chính phát triển gồm IFC, DEG (Đức), Proparco (Pháp) và Norfund (Na Uy); các ngân hàng xuất nhập khẩu China Eximbank, Korea Eximbank cùng nhóm ngân hàng thương mại và tổ chức tài chính như SMBC, Punjab National Bank, Commercial Bank of Ceylon, ICBC, Shinhan Bank, Woori Bank và KEXIM Asia Limited. Sự tham gia của các tổ chức đến từ nhiều quốc gia giúp VPBank đa dạng hóa đối tác và mở rộng khả năng tiếp cận thị trường vốn quốc tế.
> Theo VPBank, nguồn vốn này sẽ được sử dụng để mở rộng tín dụng cho doanh nghiệp vừa và nhỏ (SME), đặc biệt là doanh nghiệp do phụ nữ làm chủ hoặc lãnh đạo (WSME) và doanh nghiệp hoạt động trong lĩnh vực nông nghiệp

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0171 -->
## 171. edge-0171

**Triple:** 1517 (ORG) —CO_INVESTED_WITH→ Breakthrough Energy Discovery (ORG)
**Assertion status:** reported
**Evidence:**
> “We’re hitting this inflection point of AI and the electrification of nearly every industry, and it’s creating this point where we have overburdened and overstressed the energy grid,” Amir Mashal, founder and CEO of Arcturus, told TechCrunch.
> One option is to throw more metal at the problem, but Mashal said his startup, which has been operating in stealth, offers an alternative. Arcturus can reduce the amount of energy that electrical conductors lose to heat by infusing carbon nanomaterials into copper and aluminum using lasers. Replacing traditional metal with Arcturus’s material would allow the same size power lines to carry more electricity.
> In practical terms, that could cut losses on the electrical grid in half, which would immediately unlock around 3% more electricity on average and up to 10% more during the most congested times, when the grid arguably needs it most. At the low end, that’s about a year’s worth of demand growth in the U.S.
> “Copper loses conductivity as it heats up, so the hotter it gets, the more energy it wastes as heat,” Mashal said. “As I kept peeling back the layers of that onion, everything kind of started clicking to me because I noticed the same limit shows up everywhere. The modern world really runs on metals.”
> While the grid is the ultimate destination for a materials startup like Arcturus, the company is starting smaller with drones, robotics, and, yes, data centers, where a few percentage points more electricity can have an outsized impact.
> The company exclusively told TechCrunch that it raised $8 million in a seed round led by Initialized Capital with participation from Toyota Ventures, Breakthrough Energy Discovery, 1517, and Wireframe Ventures.

**Article:** [Arcturus could halve the grid’s electrical losses using its nano-infused metals](https://techcrunch.com/2026/06/30/arcturus-could-halve-the-grids-electrical-losses-using-its-nano-infused-copper/) | en | techcrunch.com
**Ngữ cảnh:**
> ses a lot of copper, but thanks to the energy transition and data centers, it’ll need a lot more. Between now and 2050, we’ll have to produce more copper than has been mined throughout all of human history, according to one study.
> Plenty of that copper — and even more aluminum — ends up in the electrical grid, which in the U.S. is showing its age.
> “We’re hitting this inflection point of AI and the electrification of nearly every industry, and it’s creating this point where we have overburdened and overstressed the energy grid,” Amir Mashal, founder and CEO of Arcturus, told TechCrunch.
> One option is to throw more metal at the problem, but Mashal said his startup, which has been operating in stealth, offers an alternative. Arcturus can reduce the amount of energy that electrical conductors lose to heat by infusing carbon nanomaterials into copper and aluminum using lasers. Replacing traditional metal with Arcturus’s material would allow the same size power lines to carry more electricity.
> In practical terms, that could cut losses on the electrical grid in half, which would immediately unlock around 3% more electricity on average and up to 10% more during the most congested times, when the grid arguably needs it most. At the low end, that’s about a year’s worth of demand growth in the U.S.
> “Copper loses conductivity as it heats up, so the hotter it gets, the more energy it wastes as heat,” Mashal said. “As I kept peeling back the layers of that onion, everything kind of started clicking to me because I noticed the same limit shows up everywhere. The modern world really runs on metals.”
> While the grid is the ultimate destination for a materials startup like Arcturus, the company is starting smaller with drones, robotics, and, yes, data centers, where a few percentage points more electricity can have an outsized impact.
> The company exclusively told TechCrunch that it raised $8 million in a seed round led by Initialized Capital with participation from Toyota Ventures, Breakthrough Energy Discovery, 1517, and Wireframe Ventures.
> Mashal has been quietly refining his materials in a garage in Malibu, California, where he’s currently able to produce several centimeters of wire as a proof of concept. With the new funding, he plans to ramp up to tens of meters so that the nano-infused materials can be tested in various applications, including windings in electric motors and bus

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0172 -->
## 172. edge-0172

**Triple:** Ernij Next (ORG) —CO_INVESTED_WITH→ European Innovation Council Fund (ORG)
**Assertion status:** reported
**Evidence:**
> Morphotonics has spent 12 years developing that technology, largely under the radar. Now, as demand for smart glasses and other optics surges, the company said Tuesday it has raised €40 million to scale up production and push into a new market: optical components for data centers.The round was backed by 3M Ventures, Innovation Industries, BOM, and Invest-NL. The European Innovation Council (EIC) Fund, Ernij Next (a Dutch family office), and the European Investment Bank (EIB) also participated.

**Article:** [Morphotonics raises €40M to expand its display tech into data centers](https://techcrunch.com/2026/09/21/morphotonics-raises-e40m-to-expand-its-display-tech-into-data-centers/) | en | techcrunch.com
**Ngữ cảnh:**
> ilicon wafers inside a computer chip factory known as a fab. Fellow Dutch company Morphotonics is smaller and works in a different corner of the same field: nanoimprint lithography, or NIL, a process used to manufacture the displays in AR glasses and other optics. It said it has benefited from ASML’s supply chain and uses many of the same vendors.
> Morphotonics has spent 12 years developing that technology, largely under the radar. Now, as demand for smart glasses and other optics surges, the company said Tuesday it has raised €40 million to scale up production and push into a new market: optical components for data centers.The round was backed by 3M Ventures, Innovation Industries, BOM, and Invest-NL. The European Innovation Council (EIC) Fund, Ernij Next (a Dutch family office), and the European Investment Bank (EIB) also participated.
> Morphotonics’ NIL work means the startup creates a “stamp” and applies it to photosensitive materials to create various kinds of displays, from augmented reality glasses to privacy screens for cars.
> This is useful in creating the waveguide technology used in smart glasses, including the Meta Ray-Ban Display, Even Reality, and Magic Leap. Waveguide

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0173 -->
## 173. edge-0173

**Triple:** Aspex (ORG) —OWNS_STAKE_IN→ Delivery Hero (ORG)
**Assertion status:** reported
**Evidence:**
> Aspex, cổ đông sở hữu 15% cổ phần tại Delivery Hero, kêu gọi nền tảng giao hàng này thu hẹp thị trường hoạt động, và nhanh chóng tìm người thay thế CEO Oestberg.

**Article:** [Uber tính chi 11,6 tỷ USD mua lại đối thủ giao đồ ăn Delivery Hero](https://vnexpress.net/uber-tinh-chi-11-6-ty-usd-mua-lai-doi-thu-giao-do-an-delivery-hero-5077521.html) | vi | vnexpress.net
**Ngữ cảnh:**
> ớc, Uber tăng tỷ lệ sở hữu đối thủ từ 7% lên 19,5%, trở thành cổ đông lớn nhất. Theo tính toán, lượng cổ phần này trị giá khoảng 1,7 tỷ euro.
> Ông Niklas Oestberg, CEO Delivery Hero, cho biết sẽ từ chức sau nhiều năm chịu áp lực từ các cổ đông lớn, buộc họ thay đổi chiến lược. Ông dự kiến hoàn tất chuyển giao quyền lực chậm nhất vào ngày 31/3/2027.
> Aspex, cổ đông sở hữu 15% cổ phần tại Delivery Hero, kêu gọi nền tảng giao hàng này thu hẹp thị trường hoạt động, và nhanh chóng tìm người thay thế CEO Oestberg.
> Delivery Hero là công ty mẹ của Baemin, thương hiệu đã rời Việt Nam ba năm trước do tính cạnh tranh khốc liệt của thị trường này.
> Thị trường giao đồ ăn toàn cầu đang chứng kiến nhiều thương vụ sáp nhập. Năm ngoái, DoorDash mua lại Deliveroo với giá 2,9 tỷ bảng Anh.
> Tập đoàn đầu tư Hà Lan Prosus thâu tóm Just Eat Takeaway với 4,1 tỷ euro. Tuy nhiên

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0174 -->
## 174. edge-0174

**Triple:** Mitsubishi (ORG) —INVESTED_IN→ Kyoto Fusioneering (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Venture capitalists appear to agree, having invested $121 million in Kyoto Fusioneering, per FusionX. Investors include 31Ventures, In-Q-Tel, JIC Venture Growth Investments, Mitsubishi, and Sumitomo Mitsui Trust Investment, according to PitchBook.

**Article:** [Every fusion startup that has raised over $100M](https://techcrunch.com/2026/08/15/every-fusion-startup-that-has-raised-over-100m/) | en | techcrunch.com
**Ngữ cảnh:**
> n systems to harvest power from fusion reactions to turn it into electricity.
> Kyoto Fusioneering has made an early bet that if even one fusion startup succeeds in generating enough power to sell to the grid, then the industry will need a supplier for the balance of plant and the expertise to integrate it into whichever fusion technologies win out.
> Venture capitalists appear to agree, having invested $121 million in Kyoto Fusioneering, per FusionX. Investors include 31Ventures, In-Q-Tel, JIC Venture Growth Investments, Mitsubishi, and Sumitomo Mitsui Trust Investment, according to PitchBook.
> Unlike many other fusion startups, First Light Fusion doesn’t use magnets to generate the conditions necessary for fusion. Instead, it follows an approach known as inertial confinement, in which fusion fuel pellets are compressed until they ignite.
> But even then, First Light doesn’t hew to orthodoxy. Most attempts at inertial confinement use laser

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0175 -->
## 175. edge-0175

**Triple:** Valor Equity Partners (ORG) —CO_INVESTED_WITH→ Founders Fund (ORG)
**Assertion status:** reported
**Evidence:**
> Defense tech Hadrian announced on Thursday that it had raised a fresh $1.37 billion round at a valuation of $7.87 billion from a mile-long list of well-known investors.
> The lead investors in the round include WCM Investment Management, Washington Harbour Partners, Valor Equity Partners, 137 Ventures, and Baillie Gifford. Participating investors include 1789 Capital, Morgan Stanley Wealth Management, funds managed by Apollo and T. Rowe Price, as well as firms like CapitalG, Andreessen Horowitz, Founders Fund, Lux Capital, Altimeter, and others.

**Article:** [Defense tech Hadrian raises $1.37B at $8B valuation](https://techcrunch.com/2026/08/06/defense-tech-hadrian-raises-1-37b-at-8b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Defense tech Hadrian announced on Thursday that it had raised a fresh $1.37 billion round at a valuation of $7.87 billion from a mile-long list of well-known investors.
> The lead investors in the round include WCM Investment Management, Washington Harbour Partners, Valor Equity Partners, 137 Ventures, and Baillie Gifford. Participating investors include 1789 Capital, Morgan Stanley Wealth Management, funds managed by Apollo and T. Rowe Price, as well as firms like CapitalG, Andreessen Horowitz, Founders Fund, Lux Capital, Altimeter, and others.
> Founders Fund and Lux led the company’s $260 million Series C financing about a year ago, bringing the total raised to date to around $2 billion, according to PitchBook estimates.
> Hadrian is an interesting defense tech in that it’s not trying to build new AI-powered weapons. The company is building automated manufacturing facilities that will mass

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0176 -->
## 176. edge-0176

**Triple:** Reah Miyara (PERSON) —INVESTED_IN→ Plurai (ORG)
**Assertion status:** reported
**Evidence:**
> Reah Miyara, a Google DeepMind researcher who backed Plurai as an angel investor, said the company’s edge comes from understanding failure modes in production, and generating synthetic data to tune models. As businesses try to optimize their AI expense, Plurai’s approach could prove a real advantage, since IT leaders are seeing that “frontier-capable models are out of distribution with my specific data, and the cost of these things isn’t sustainable in the long term,” Miyara said.

**Article:** [Plurai wants to help AI agents work better using the same approach that helped get self-driving cars to roads](https://techcrunch.com/2026/11/11/plurai-wants-to-help-ai-agents-work-better-using-the-same-approach-that-helped-get-self-driving-cars-to-roads/) | en | techcrunch.com
**Ngữ cảnh:**
> ng midtier frontier models at lower costs.
> “We can take a large language model, we can take the task, decompose it into a smaller task using the simulation, train [an open-weight] model, and using the simulation, verify that the quality is higher or comparable to the frontier model, and an order or two orders of magnitude cost reduction,” he said.
> Reah Miyara, a Google DeepMind researcher who backed Plurai as an angel investor, said the company’s edge comes from understanding failure modes in production, and generating synthetic data to tune models. As businesses try to optimize their AI expense, Plurai’s approach could prove a real advantage, since IT leaders are seeing that “frontier-capable models are out of distribution with my specific data, and the cost of these things isn’t sustainable in the long term,” Miyara said.
> Plurai hopes analogies between AI agents in physical and digital environments can prove predictive: While powerful general AI models are imbuing robots with fascinating capabilities, they aren’t yet reliable enough to be deployed widely. Meanwhile, robots powered by AI models built for specific tasks are in the field right now, working for custome

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0177 -->
## 177. edge-0177

**Triple:** TPBank (ORG) —FINANCED→ HCM City–Trung Lương–Mỹ Thuận Expressway Expansion (PROJECT)
**Assertion status:** reported
**Evidence:**
> HÀ NỘI — Vietcombank has arranged a syndicated loan worth nearly VNĐ27.1 trillion (over US$1 billion) to finance the expansion of the HCM City–Trung Lương–Mỹ Thuận Expressway under a public-private partnership (PPP) model.
> 
> The syndicated credit agreement was signed on Thursday in Hà Nội between project company BOT Sài Gòn–Mỹ Thuận Co and a consortium of six lenders comprising Vietcombank, the lead arranger, and VietinBank, BIDV, Agribank, VPBank and TPBank.
> 
> The HCM City–Trung Lương–Mỹ Thuận Expressway expansion project spans more than 96 kilometres and has a total investment of VNĐ36.1 trillion. Developed under the PPP model, the project has secured nearly VNĐ27.1 trillion in syndicated financing from the six participating banks.

**Article:** [Vietcombank arranges over VNĐ27 trillion loan for expressway project](https://vietnamnews.vn/economy/1785633/vietcombank-arranges-over-vnd27-trillion-loan-for-expressway-project.html) | vi | vietnamnews.vn
**Ngữ cảnh:**
> HÀ NỘI — Vietcombank has arranged a syndicated loan worth nearly VNĐ27.1 trillion (over US$1 billion) to finance the expansion of the HCM City–Trung Lương–Mỹ Thuận Expressway under a public-private partnership (PPP) model.
> 
> The syndicated credit agreement was signed on Thursday in Hà Nội between project company BOT Sài Gòn–Mỹ Thuận Co and a consortium of six lenders comprising Vietcombank, the lead arranger, and VietinBank, BIDV, Agribank, VPBank and TPBank.
> 
> The HCM City–Trung Lương–Mỹ Thuận Expressway expansion project spans more than 96 kilometres and has a total investment of VNĐ36.1 trillion. Developed under the PPP model, the project has secured nearly VNĐ27.1 trillion in syndicated financing from the six participating banks.
> 
> According to the organisers, this is the largest syndicated credit package ever arranged for a build-operate-transfer (BOT) transport project in Việt Nam, providing a strong financial foundation for one of the country's key transport infrastructure developments.
> 
> Speaking at the signing ceremony, Vietcombank CEO Lê Quang Vinh said the expressway 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0178 -->
## 178. edge-0178

**Triple:** Kakao Ventures (ORG) —CO_INVESTED_WITH→ SKT America (ORG)
**Assertion status:** reported
**Evidence:**
> Samsung Venture Investment led its oversubscribed $27 million seed round at a valuation of more than $200 million, bringing Config’s total raised to $35 million. Hyundai Motor’s venture arm ZER01NE Ventures; LG Technology Ventures; and SKT America, a South Korean telco giant’s VC unit, also joined as strategic investors. Other investors include angel investor Pieter Abbeel (co-founder of Covariant and a UC Berkeley professor) and financial backers Mirae Asset Ventures, Korea Development Bank, GS Futures, Kakao Ventures, and Z Ventures.

**Article:** [Korea&#8217;s biggest manufacturers back Config, the TSMC of robot data](https://techcrunch.com/2026/05/11/koreas-biggest-manufacturers-back-config-the-tsmc-of-robot-data/) | en | techcrunch.com
**Ngữ cảnh:**
> hains. That structural foundation is now shaping how artificial intelligence is adopted and where investment flows.
> Which makes it particularly significant that Config, a Seoul- and San Jose-based startup building the data layer for robotics foundation models (RFMs), has secured backing from the venture arms of South Korea’s biggest manufacturers.
> Samsung Venture Investment led its oversubscribed $27 million seed round at a valuation of more than $200 million, bringing Config’s total raised to $35 million. Hyundai Motor’s venture arm ZER01NE Ventures; LG Technology Ventures; and SKT America, a South Korean telco giant’s VC unit, also joined as strategic investors. Other investors include angel investor Pieter Abbeel (co-founder of Covariant and a UC Berkeley professor) and financial backers Mirae Asset Ventures, Korea Development Bank, GS Futures, Kakao Ventures, and Z Ventures.
> Config was founded in January 2025 by CEO Minjoon Seo, a former researcher at Meta and chief scientist at TwelveLabs, along with three co-founders with backgrounds at Waymo, Google, and Naver. Instead of building robots themselves, the team is focused on a simpler goal — providing data that robots need to learn and operate. They believe that bette

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0179 -->
## 179. edge-0179

**Triple:** Thomas Boser (PERSON) —FOUNDED→ Hiloop (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Hiloop — founded by Jad Ghalayini, Karan Brar, and Thomas Boser — helps AI companies adapt general-purpose open-weight models for specific applications using its post-training platform. Its founding team includes former Reducto engineers and a Cambridge computer science PhD who completed his doctorate at 24.

**Article:** [Peak XV ups Surge seed investment ceiling to $5M, unveils 18-startup cohort](https://techcrunch.com/2026/09/28/peak-xv-goes-bigger-at-seed-with-new-surge-cohort-as-series-a-bar-rises/) | en | techcrunch.com
**Ngữ cảnh:**
> $9.2 million in a Peak XV-led seed round announced earlier this year.
> GameStock — founded by Antoine Mistico, Easton Dana, and Vivek Indlebele Narasimha Prasad — brings competition mechanics to financial markets, turning investing and trading into a more competitive experience. Mistico is a two-time founder and former professional baseball player.
> Hiloop — founded by Jad Ghalayini, Karan Brar, and Thomas Boser — helps AI companies adapt general-purpose open-weight models for specific applications using its post-training platform. Its founding team includes former Reducto engineers and a Cambridge computer science PhD who completed his doctorate at 24.
> Hoola Health — founded by Deeksha Senguttuvan — focuses on care for children and their families, providing consultations, vaccinations, medicines, diagnostics, developmental therapy, and dental services on a single platform. Senguttuvan grew up around healthcare, as her family built and operated a hospital group.
> Kello — founded by Mona Gandhi and

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0180 -->
## 180. edge-0180

**Triple:** Lightspeed Venture Partners (ORG) —CO_INVESTED_WITH→ Sparrow Capital (ORG)
**Assertion status:** reported
**Evidence:**
> The two-year-old startup said Thursday it had raised $9 million in a seed round led by Susquehanna International Group (SIG) and Lightspeed, with participation from B Capital, Seaborne Capital, Beenext, Sparrow Capital, and 2.2 Capital. The round values Gushwork at $33 million post-money, up from about $7.5 million following its Lightspeed-led $2.1 million pre-seed in July 2023, a person familiar with the matter told TechCrunch. The latest financing brings Gushwork’s total funding to $11 million, the startup said.

**Article:** [Gushwork bets on AI search for customer leads — and early results are emerging](https://techcrunch.com/2026/02/25/gushwork-bets-on-ai-search-for-customer-leads-and-early-results-are-emerging/) | en | techcrunch.com
**Ngữ cảnh:**
> As AI-powered search tools reshape how businesses are discovered online, India-founded startup Gushwork is helping companies capture customers from platforms such as ChatGPT, Gemini, and Perplexity — with early traction that is beginning to draw investor support.
> The two-year-old startup said Thursday it had raised $9 million in a seed round led by Susquehanna International Group (SIG) and Lightspeed, with participation from B Capital, Seaborne Capital, Beenext, Sparrow Capital, and 2.2 Capital. The round values Gushwork at $33 million post-money, up from about $7.5 million following its Lightspeed-led $2.1 million pre-seed in July 2023, a person familiar with the matter told TechCrunch. The latest financing brings Gushwork’s total funding to $11 million, the startup said.
> The funding comes as AI companies, including OpenAI and Perplexity, begin to chip away at traditional web search, prompting incumbents like Google to roll out AI-generated overviews and other conversational features across their search products. Gushwork is betting this shift will create a new opportunity to help businesses surface in AI-driven di

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0181 -->
## 181. edge-0181

**Triple:** Atomico (ORG) —CO_INVESTED_WITH→ O.G. Venture Partners (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The round was led by Lightspeed Venture Partners and O.G. Venture Partners. This follows the company’s $260 million Series B raised in January 2025.
> Neko Health has developed proprietary body-scanning technology, which it couples with bloodwork, to assess a person’s health. For gym lovers, the scan also now includes body composition information. It can couple the assessment with Apple Health data, which Nilsonne says gives its medical clinicians real-world data to use in its assessments.
> Neko Health, which has locations in the U.K. and Sweden, is preparing for its first U.S. location in New York. The company says more than 100,000 people have already had scans and more than 350,000 people have either registered for the waitlist or set an appointment.
> One of the people who had a Neko Health scan is Calm founder Alex Tew. He posted on X that it found a malignant mole on his back, which he promptly had removed. “I’m grateful to Neko for helping me discover this – I’m not sure how I would have otherwise.”
> Neko Health isn’t the only health scanning company founded by tech folks. Midjourney, the AI Lab best known for its AI image and video creation model and website, is also creating a body scanner, which it plans to integrate into a spa experience with hot tubs and saunas, opening in San Francisco sometime in 2027.
> Other investors in Neko Health’s latest round include Atomico, General Catalyst, Lakestar, Liberty City Ventures, Positive Sum, and BDT & MSD.

**Article:** [Daniel Ek&#8217;s body-scanning startup Neko Health raises another $700M](https://techcrunch.com/2026/07/15/daniel-eks-body-scanning-startup-neko-health-raises-another-700m/) | en | techcrunch.com
**Ngữ cảnh:**
> Neko Health, the body-scanning and health assessment startup founded by Spotify’s Daniel Ek (pictured above, right) and his co-founder Hjalmar Nilsonne (above, left), has raised a $700 million Series C.
> The round was led by Lightspeed Venture Partners and O.G. Venture Partners. This follows the company’s $260 million Series B raised in January 2025.
> Neko Health has developed proprietary body-scanning technology, which it couples with bloodwork, to assess a person’s health. For gym lovers, the scan also now includes body composition information. It can couple the assessment with Apple Health data, which Nilsonne says gives its medical clinicians real-world data to use in its assessments.
> Neko Health, which has locations in the U.K. and Sweden, is preparing for its first U.S. location in New York. The company says more than 100,000 people have already had scans and more than 350,000 people have either registered for the waitlist or set an appointment.
> One of the people who had a Neko Health scan is Calm founder Alex Tew. He posted on X that it found a malignant mole on his back, which he promptly had removed. “I’m grateful to Neko for helping me discover this – I’m not sure how I would have otherwise.”
> Neko Health isn’t the only health scanning company founded by tech folks. Midjourney, the AI Lab best known for its AI image and video creation model and website, is also creating a body scanner, which it plans to integrate into a spa experience with hot tubs and saunas, opening in San Francisco sometime in 2027.
> Other investors in Neko Health’s latest round include Atomico, General Catalyst, Lakestar, Liberty City Ventures, Positive Sum, and BDT & MSD.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0182 -->
## 182. edge-0182

**Triple:** PowerCo (ORG) —CO_INVESTED_WITH→ Gotion High-Tech (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> Ngày 28/9/2026, Tập đoàn Volkswagen, công ty con PowerCo và Gotion High-Tech của Trung Quốc công bố thỏa thuận đầu tư khoảng 1,1 tỷ euro (1,29 tỷ USD). Theo đó, Gotion sẽ nắm giữ 49% cổ phần nhà máy pin của PowerCo tại Sagunto, miền Đông Tây Ban Nha, còn PowerCo giữ 51%. Liên doanh dự kiến bắt đầu hoạt động vào năm 2027. Thỏa thuận phản ánh nỗ lực của Tây Ban Nha nhằm thu hút công nghệ và đầu tư, mở rộng năng lực sản xuất pin và giữ lại nhiều giá trị hơn trong chuỗi cung ứng xe điện

**Article:** [Tây Ban Nha hợp tác với Trung Quốc, tìm cách giữ vị thế trong chuỗi giá trị xe điện](https://vneconomy.vn/tay-ban-nha-hop-tac-voi-trung-quoc-tim-cach-giu-vi-the-trong-chuoi-gia-tri-xe-dien.htm) | vi | vneconomy.vn
**Ngữ cảnh:**
> Ngày 28/9/2026, Tập đoàn Volkswagen, công ty con PowerCo và Gotion High-Tech của Trung Quốc công bố thỏa thuận đầu tư khoảng 1,1 tỷ euro (1,29 tỷ USD). Theo đó, Gotion sẽ nắm giữ 49% cổ phần nhà máy pin của PowerCo tại Sagunto, miền Đông Tây Ban Nha, còn PowerCo giữ 51%. Liên doanh dự kiến bắt đầu hoạt động vào năm 2027. Thỏa thuận phản ánh nỗ lực của Tây Ban Nha nhằm thu hút công nghệ và đầu tư, mở rộng năng lực sản xuất pin và giữ lại nhiều giá trị hơn trong chuỗi cung ứng xe điện
> 
> TỪ CƯỜNG QUỐC SẢN XUẤT Ô TÔ ĐẾN BÀI TOÁN KIỂM SOÁT CHUỖI GIÁ TRỊ
> 
> Tây Ban Nha có hệ sinh thái công nghiệp ô tô phát triển, với mạng lưới nhà máy lắp ráp, doanh nghiệp sản xuất linh kiện và các nhà cung ứng quy mô lớn. Theo ICEX, cơ quan nhà nước phụ trách xúc tiến xuất khẩu và đầu tư của Tây Ban Nha, có 9 tập đoàn đa quốc gia vận hành 18 nhà máy 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0183 -->
## 183. edge-0183

**Triple:** Mithril Capital Management (ORG) —CO_INVESTED_WITH→ Capricorn Technology Impact Funds (ORG)
**Assertion status:** reported
**Evidence:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.

**Article:** [Helion, the Sam Altman-backed fusion startup, raises $465M to build a power plant for Microsoft](https://techcrunch.com/2026/06/04/helion-the-sam-altman-backed-fusion-startup-raises-465m-to-build-a-power-plant-for-microsoft/) | en | techcrunch.com
**Ngữ cảnh:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.
> Helion’s approach to fusion power differs from many of its peers. Some use magnets to contain the superheated plasma required for fusion conditions, while others use lasers to compress fusion fuel until it reacts. In both cases, the majority of startups plan to use steam turbines to transform the intense heat into electricity.
> But Helion, which us

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0184 -->
## 184. edge-0184

**Triple:** Outlander VC (ORG) —INVESTED_IN→ Superpanel (ORG)
**Assertion status:** reported
**Evidence:**
> He’s the CEO and co-founder of Superpanel, a platform that helps law firms seamlessly onboard new clients.
> He listed emotional encounters with the law: As a Canadian, he found access to legal help hard and expensive; he also recalls his mother in a car accident, and how the legal payout helped keep his family afloat for years. He found the legal intake — the process of a firm evaluating a new client or request — tedious.
> “For consumers, it’s a maze of forms, phone calls, and dropped leads that cause most people to give up before getting help,” he told TechCrunch. “For firms, it’s a costly, error-prone bottleneck.”
> Before the recent advancements in artificial intelligence, he said that the intake process was regarded as too complex for automation. But that’s changed. Emery worked at Hootsuite, then founded the health insurance underwriting platform Allay (which exited to Novo Benefits), before teaming up with his friend Dingyu Zhang, who had a background in AI, to launch Superpanel in 2024.
> Superpanel automates half the work of legal intake, Emery said, managing collection and feedback. It provides plaintiff law firms with a “digital teammate” that helps with escalation and compliance. “It engages clients across phone, texting, email, and forums, guiding them through their story and sharing documents,” he continued. For firms, it helps sort case type, jurisdiction, and documentation.
> “When there’s risk of ambiguity, the system escalates to a human team member,” he said. “The result is a unified, multi-channel workflow that delivers measurable results and gives firms a system they can trust like a real employee.”
> The company announced Tuesday a seed $5.3 million raise in a round co-led by Outlander VC and Field Ventures. Emery said he met some investors in this round through his last startup, and those early investors introduced him to the ones who led the round for this new one. Others in this round include LOI Venture (co-founded by the founder of Hootsuite), Zenda Capital, 8-Bit Capital, and Behind Genius Ventures.

**Article:** [AI company Superpanel raises $5.3M seed to automate legal intake](https://techcrunch.com/2025/09/23/superpanel-raises-5-3m-seed-to-automate-legal-intake/) | en | techcrunch.com
**Ngữ cảnh:**
> For Julien Emery, the problem has always been personal.
> He’s the CEO and co-founder of Superpanel, a platform that helps law firms seamlessly onboard new clients.
> He listed emotional encounters with the law: As a Canadian, he found access to legal help hard and expensive; he also recalls his mother in a car accident, and how the legal payout helped keep his family afloat for years. He found the legal intake — the process of a firm evaluating a new client or request — tedious.
> “For consumers, it’s a maze of forms, phone calls, and dropped leads that cause most people to give up before getting help,” he told TechCrunch. “For firms, it’s a costly, error-prone bottleneck.”
> Before the recent advancements in artificial intelligence, he said that the intake process was regarded as too complex for automation. But that’s changed. Emery worked at Hootsuite, then founded the health insurance underwriting platform Allay (which exited to Novo Benefits), before teaming up with his friend Dingyu Zhang, who had a background in AI, to launch Superpanel in 2024.
> Superpanel automates half the work of legal intake, Emery said, managing collection and feedback. It provides plaintiff law firms with a “digital teammate” that helps with escalation and compliance. “It engages clients across phone, texting, email, and forums, guiding them through their story and sharing documents,” he continued. For firms, it helps sort case type, jurisdiction, and documentation.
> “When there’s risk of ambiguity, the system escalates to a human team member,” he said. “The result is a unified, multi-channel workflow that delivers measurable results and gives firms a system they can trust like a real employee.”
> The company announced Tuesday a seed $5.3 million raise in a round co-led by Outlander VC and Field Ventures. Emery said he met some investors in this round through his last startup, and those early investors introduced him to the ones who led the round for this new one. Others in this round include LOI Venture (co-founded by the founder of Hootsuite), Zenda Capital, 8-Bit Capital, and Behind Genius Ventures.
> “We’ll use the funding to accelerate hiring and expand Superpanel’s capabilities for plaintiff law firms,” he said.
> Legal is one of the top industries seeing transformation as artificial intelligence continues to innovate. So Superpanel certainly isn’t alone in this space, and its competitors include Clio Grow, LegalClerk.ai, MyCase, and Whippy.ai

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0185 -->
## 185. edge-0185

**Triple:** The Family Fund (ORG) —CO_INVESTED_WITH→ Flex Capital (ORG)
**Assertion status:** reported
**Evidence:**
> The funding round also saw participation from Town Hall Ventures, Eniac Ventures, Flex Capital, Foundry Square Capital, Pear VC, and The Family Fund.

**Article:** [Kin Health raises $9M to build an AI notetaker for patients](https://techcrunch.com/2026/05/18/kin-health-raises-9m-to-build-an-ai-notetaker-for-patients/) | en | techcrunch.com
**Ngữ cảnh:**
> to coordinate their own treatment actions. “Kin is built to solve an entirely different consumer need: it can travel with them between specialists, systems, and providers. It’s not beholden to any single health network or EHR relationship. It’s built to serve the patient, not the institution, and that’s a massive distribution advantage,” she said.
> The funding round also saw participation from Town Hall Ventures, Eniac Ventures, Flex Capital, Foundry Square Capital, Pear VC, and The Family Fund. GoodRx’s Hirsch and Bezdek; angel investors Jay Desai, Nabeel Quryshi, Alex Cohen, and Saharsh Patel; and more than 30 physicians also invested.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0186 -->
## 186. edge-0186

**Triple:** DST Global (ORG) —INVESTED_IN→ Mistral (ORG)
**Assertion status:** reported
**Evidence:**
> In September 2025, Mistral closed a €1.7 billion Series C round (about $2 billion) led by ASML at a €11.7 billion valuation (approximately $13.8 billion), with participation from existing backers DST Global, a16z, Bpifrance, General Catalyst, Index Ventures, Lightspeed, and Nvidia.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
>  presented as a Series A extension, implying an unchanged valuation.
> In June 2024, Mistral raised €600 million (about $640 million) in a mix of equity and debt. The long-rumored round was led by General Catalyst at a $6 billion valuation, with notable investors including Cisco, IBM, Nvidia, and Samsung Venture Investment Corporation participating.
> In September 2025, Mistral closed a €1.7 billion Series C round (about $2 billion) led by ASML at a €11.7 billion valuation (approximately $13.8 billion), with participation from existing backers DST Global, a16z, Bpifrance, General Catalyst, Index Ventures, Lightspeed, and Nvidia.
> What companies has Mistral AI acquired?
> In addition to infrastructure startup Koyeb, Mistral has also bought Emmi, an Austrian startup focusing on physics AI, with the ambition to better support industrial enterprises in their AI transformation.
> Will Mistral AI make its own chips?
> While Mistral has yet to design its own chips, Mensch isn’t ruling 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0187 -->
## 187. edge-0187

**Triple:** Redpoint Ventures (ORG) —CO_INVESTED_WITH→ Andreessen Horowitz (ORG)
**Assertion status:** reported
**Evidence:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.

**Article:** [Kevin Mandia&#8217;s new &#8216;agent swarm&#8217; security startup Armadin raises $255.5M at $2.5B valuation](https://techcrunch.com/2026/10/01/kevin-mandias-new-agent-swarm-security-startup-armadin-raises-255-5m-at-2-5b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.
> The new round comes just six months after Armadin raised a $190 million Series A in March. It has now raised more than $445 million.
> Armadin is offering enterprises a new kind of always-on security by reimagining defense testing for the AI era. Instead of traditional penetration tests, where hired guns attempt to break in and report on the weaknes

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0188 -->
## 188. edge-0188

**Triple:** Felicis (ORG) —CO_INVESTED_WITH→ Coatue (ORG)
**Assertion status:** historical_reported
**Evidence:**
> But on Tuesday, the fruits of that became evident when it announced a $200 million Series D at a $2 billion post-money valuation led by Accel, with Coatue, Y Combinator, Craft Ventures, and longtime investor Felicis participating in the round, Fortune reported.

**Article:** [Vibe coding helps Supabase nab $200M at $2B valuation just seven months after its last raise](https://techcrunch.com/2025/04/22/vibe-coding-helps-supabase-nab-200m-at-2b-valuation-just-seven-months-after-its-last-raise/) | en | techcrunch.com
**Ngữ cảnh:**
> In 2020, when open source database Supabase was founded, its New Zealand-based CEO, Paul Copplestone, couldn’t have imagined it would be sitting in the sweet spot for 2025’s biggest trend: vibe coding.
> But on Tuesday, the fruits of that became evident when it announced a $200 million Series D at a $2 billion post-money valuation led by Accel, with Coatue, Y Combinator, Craft Ventures, and longtime investor Felicis participating in the round, Fortune reported.
> This fresh $200 million comes just seven months after Supabase announced it raised $80 million led by Peak XV (a Sequoia spinoff) and David Sacks’ Craft Ventures. Supabase wouldn’t comment on the valuation at that time, but PitchBook put it at about $900 million. All told, the startup has now raised about $398 million.
> Supabase is another example 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0189 -->
## 189. edge-0189

**Triple:** SignalFire (ORG) —INVESTED_IN→ Clutch Security (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Three-year-old Clutch was last valued at $85 million when it raised a $20 million Series A round in January 2025, led by Lightspeed and SignalFire, according to our source. The startup is currently approaching $10 million in annual recurring revenue (ARR). That means the acquisition, if completed, would value Clutch at about 50 times its ARR, a standard way of pricing software companies.

**Article:** [Palo Alto Networks in talks to buy AI agent security startup Clutch for $500M](https://techcrunch.com/2026/11/05/palo-alto-networks-in-talks-to-buy-ai-agent-security-startup-clutch-for-500m/) | en | techcrunch.com
**Ngữ cảnh:**
> Palo Alto Networks is in talks to acquire Clutch Security , a startup that secures AI agents’ access to company systems, for $500 million in cash plus additional milestone-based payouts, according to a person familiar with the discussions.
> 
> Three-year-old Clutch was last valued at $85 million when it raised a $20 million Series A round in January 2025, led by Lightspeed and SignalFire, according to our source. The startup is currently approaching $10 million in annual recurring revenue (ARR). That means the acquisition, if completed, would value Clutch at about 50 times its ARR, a standard way of pricing software companies.
> 
> Palo Alto Networks and Clutch Security did not respond to a request for comment. The Information was the first to report the acquisition discussions.
> 
> The high valuation is not an anomaly in a market increasingly focused on securing software against bad actors using AI to breach systems more easily. Upwind, a startup using AI to secure cloud infr

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0190 -->
## 190. edge-0190

**Triple:** Commerce Ventures (ORG) —INVESTED_IN→ Fuse (ORG)
**Assertion status:** reported
**Evidence:**
> On Monday, Fuse announced that it has raised a $25 million Series A led by Footwork, Primary Venture Partners, NextView Ventures, and Commerce Ventures.

**Article:** [Fuse raises $25M to disrupt aging loan origination systems used by US credit unions](https://techcrunch.com/2026/03/16/fuse-raises-25m-to-disrupt-aging-loan-origination-systems-used-by-u-s-credit-unions/) | en | techcrunch.com
**Ngữ cảnh:**
> a realized that LLMs could modernize something even more significant: the loan origination system (LOS), which is the backbone of the lending industry.
> Frustrated by the limitations of legacy software, Klaric (pictured left), a Bolivian native, and Escapa (pictured righ), a Spanish immigrant, pivoted their business to build Fuse, an AI-native LOS.
> On Monday, Fuse announced that it has raised a $25 million Series A led by Footwork, Primary Venture Partners, NextView Ventures, and Commerce Ventures.
> An LOS serves as the primary system of record for most lenders, managing the entire loan life cycle: from initial application and underwriting to final approval and credit disbursement. However, traditional systems can take as long as a year to integrate and typically have multi-year, expensive contracts, Klaric said.
> By leveraging AI, Fuse claims

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0191 -->
## 191. edge-0191

**Triple:** U.S. Innovative Technology Fund (ORG) —INVESTED_IN→ Thea Energy (ORG)
**Assertion status:** historical_reported
**Evidence:**
> In May 2026, Thea raised $100 million in a Series B led by the U.S. Innovative Technology Fund, just over two years after a $20 million Series A. Across all rounds, the startup has raised $120 million in private capital. Other investors include Prelude Ventures, Lowercarbon Capital, Hitachi Ventures, and Emerald Technology Ventures.

**Article:** [Every fusion startup that has raised over $100M](https://techcrunch.com/2026/08/15/every-fusion-startup-that-has-raised-over-100m/) | en | techcrunch.com
**Ngữ cảnh:**
>  periods of time — a boon when it comes to running a commercial power plant — but to do so, they require twisty magnetic fields. Most stellarators build magnets that mimic that complex shape, but Thea Energy thinks that by wreathing its doughnut-shaped reactor in dozens of smaller magnets, it can use control software to create the necessary kinks.
> In May 2026, Thea raised $100 million in a Series B led by the U.S. Innovative Technology Fund, just over two years after a $20 million Series A. Across all rounds, the startup has raised $120 million in private capital. Other investors include Prelude Ventures, Lowercarbon Capital, Hitachi Ventures, and Emerald Technology Ventures.
> Though nothing about fusion can be described as simple, Xcimer takes a relatively straightforward approach: Follow the basic science that’s behind the National Ignition Facility’s breakthrough net-positive experiment and redesign the technology that underpins it from the ground up. The Colorado-based startup is planning to build a 10-megajoule las

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0192 -->
## 192. edge-0192

**Triple:** Whitney Wolfe Herd (PERSON) —FOUNDED→ Bumble (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Founded in 2014 by Whitney Wolfe Herd, Bumble made a name for itself for its unique approach where only women made the first move. That helped it stand out in a crowded dating market, and the company eventually went public in 2021 at a valuation of roughly $14 billion.

**Article:** [Bumble agrees to a $1.3B acquisition deal as online dating faces a reset](https://techcrunch.com/2026/10/13/bumble-agrees-to-a-1-3b-acquisition-deal-as-online-dating-faces-a-reset/) | en | techcrunch.com
**Ngữ cảnh:**
> any that once looked like one of the biggest success stories in online dating.
> 
> The deal would take the company private after years of declining subscriber numbers, falling revenue, and mounting pressure to rethink the online dating experience. The move may give Bumble a chance to work on its next chapter away from the pressure of public markets.
> 
> Founded in 2014 by Whitney Wolfe Herd, Bumble made a name for itself for its unique approach where only women made the first move. That helped it stand out in a crowded dating market, and the company eventually went public in 2021 at a valuation of roughly $14 billion.
> 
> Since then, however, the dating app landscape has changed considerably. Bumble has faced declining paying users, weaker revenue, and growing dissatisfaction with the familiar swipe-based model. The company recently reported second-quarter 2026 revenue of $211 million, down 15.2% year over year, while its paying user base fell 16.4% to approximate

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0193 -->
## 193. edge-0193

**Triple:** UnternehmerTUM (ORG) —INVESTED_IN→ QuantumDiamonds (ORG)
**Assertion status:** reported
**Evidence:**
> A spinout from the Technical University of Munich (TUM), QuantumDiamonds has also raised a €15 million equity round led by VC firm World Fund, TechCrunch learned exclusively. The company declined to disclose its valuation, but said its round was also backed by Bayern Kapital and existing investors including Creator Fund, Earlybird, First Momentum, IQ Capital, Onsight Ventures, and UnternehmerTUM.

**Article:** [With EU backing, QuantumDiamonds aims to speed up chip manufacturing](https://techcrunch.com/2026/07/08/with-eu-backing-quantumdiamonds-aims-to-speed-up-chip-manufacturing/) | en | techcrunch.com
**Ngữ cảnh:**
> he approval of the European Commission, it has been granted €76 million in non-dilutive funding provided by Germany’s federal economy ministry and the state of Bavaria. The startup will use it to set up a new facility for the production of semiconductor testing equipment in Munich as part of a $178 million investment plan it had already announced.
> A spinout from the Technical University of Munich (TUM), QuantumDiamonds has also raised a €15 million equity round led by VC firm World Fund, TechCrunch learned exclusively. The company declined to disclose its valuation, but said its round was also backed by Bayern Kapital and existing investors including Creator Fund, Earlybird, First Momentum, IQ Capital, Onsight Ventures, and UnternehmerTUM.
> CEO Kevin Berghoff told TechCrunch that raising the round was a fairly quick process, as QuantumDiamonds was able to demonstrate customer pull. “We work with almost everyone in the chip ecosystem,” he said. With huge demand for all kinds of chips, there’s just as much demand for solutions to speed up the manufacturing process and improve the outpu

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0194 -->
## 194. edge-0194

**Triple:** Iconiq (ORG) —INVESTED_IN→ Rillet (ORG)
**Assertion status:** reported
**Evidence:**
> AI accounting startup Rillet announced a $100 million Series C at a $1 billion valuation on Tuesday, led by Iconiq.

**Article:** [Rillet raises $100M Series C at $1B valuation — 2 years after emerging from stealth](https://techcrunch.com/2026/08/19/rillet-raises-100m-series-c-at-1b-valuation-2-years-after-emerging-from-stealth/) | en | techcrunch.com
**Ngữ cảnh:**
> AI accounting startup Rillet announced a $100 million Series C at a $1 billion valuation on Tuesday, led by Iconiq. Returning investors include Andreessen Horowitz and Sequoia. Rillet, which emerged from stealth in 2024, is quickly becoming one of the hottest AI startups in the enterprise resource planning (ERP) industry.
> The company’s platform deploys AI to help finance professionals manage a company’s books. It says it can, for instance, automatically and con

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0195 -->
## 195. edge-0195

**Triple:** Doha Bank (ORG) —CO_FINANCED_WITH→ National Bank of Kuwait (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).
> With the partnership of 15 international financial institutions, this facility represents VPBank’s largest-ever transaction in terms of the number of MLAUBs involved. The scale of the transaction and the breadth of participation underscore the strong confidence of the international financial community in VPBank’s financial strength, growth prospects and sustainable development orientation.
> In addition to the MLAUBs, the transaction also received strong market support, with participation from 19 international financial institutions following a series of investor roadshows in two major regional financial markets, Singapore and Taiwan (China).
> Speaking at the signing ceremony, Nguyễn Đức Vinh, CEO of VPBank, said: “The $1.44 billion syndicated loan, supported by 15 leading global financial institutions, is a clear testament to the strong confidence that the international financial community places in VPBank.
> "It also marks an important step forward in the bank’s implementation of sustainability-linked financing instruments, serving both as an affirmation of our commitment and as a catalyst for VPBank to further contribute to sustainable growth objectives, institutionalise Environmental, Social and Governance (ESG) goals, create long-term value for shareholders and customers and make positive contributions to society.”
> Notably, despite ongoing geopolitical uncertainties, escalating tensions in the Middle East and tighter liquidity conditions in global financial markets, the transaction secured commitments from several leading financial institutions in the Middle East, including FAB, Mashreq, NBK, Arab Bank for Investment and Foreign Trade and Doha Bank. Their participation is a strong testament to VPBank’s growing reputation and standing in international capital markets.

**Article:** [VPBank and 15 international financial institutions sign maiden US$1.44 billion sustainability-linked syndicated loan facility](https://vietnamnews.vn/economy/1784501/vpbank-and-15-international-financial-institutions-sign-maiden-us-1-44-billion-sustainability-linked-syndicated-loan-facility.html) | en | vietnamnews.vn
**Ngữ cảnh:**
>  strategic partnership between VPBank and SMBC, while enhancing VPBank’s standing in regional and international financial markets.
> The transaction attracted several financial institutions taking on lead roles for the first time or expanding their existing participation, with these banks accounting for nearly half of all participating institutions.
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).
> With the partnership of 15 international financial institutions, this facility represents VPBank’s largest-ever transaction in terms of the number of MLAUBs involved. The scale of the transaction and the breadth of participation underscore the strong confidence of the international financial community in VPBank’s financial strength, growth prospects and sustainable development orientation.
> In addition to the MLAUBs, the transaction also received strong market support, with participation from 19 international financial institutions following a series of investor roadshows in two major regional financial markets, Singapore and Taiwan (China).
> Speaking at the signing ceremony, Nguyễn Đức Vinh, CEO of VPBank, said: “The $1.44 billion syndicated loan, supported by 15 leading global financial institutions, is a clear testament to the strong confidence that the international financial community places in VPBank.
> "It also marks an important step forward in the bank’s implementation of sustainability-linked financing instruments, serving both as an affirmation of our commitment and as a catalyst for VPBank to further contribute to sustainable growth objectives, institutionalise Environmental, Social and Governance (ESG) goals, create long-term value for shareholders and customers and make positive contributions to society.”
> Notably, despite ongoing geopolitical uncertainties, escalating tensions in the Middle East and tighter liquidity conditions in global financial markets, the transaction secured commitments from several leading financial institutions in the Middle East, including FAB, Mashreq, NBK, Arab Bank for Investment and Foreign Trade and Doha Bank. Their participation is a strong testament to VPBank’s growing reputation and standing in international capital markets.
> The successful completion of the transaction marks an important milestone in VPBank’s strategy to diversify its medium- and long-term funding sources, providing momentum for the bank to pursue its ambitious growth objectives in 2026.
> It also significantly expands VPBank’s network of financial partners, laying a strong foundation for the bank to ac

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0196 -->
## 196. edge-0196

**Triple:** Phu Ninh International Investment Co Ltd (ORG) —DEVELOPS→ Doi 30 Industrial Cluster (PROJECT)
**Assertion status:** reported
**Evidence:**
> Tại cuộc họp, ông Mai Thành Vinh, Giám đốc Công ty TNHH Đầu tư quốc tế Phú Ninh (chủ đầu tư hạ tầng cụm công nghiệp), cho rằng việc chậm hoàn thiện hệ thống xử lý nước thải tập trung xuất phát từ khó khăn trong bàn giao mặt bằng. Diện tích thực tế được bàn giao mới khoảng 15 ha đất công nghiệp trên tổng diện tích 30,47 ha theo quyết định thành lập, gây khó khăn về mặt bằng và nguồn vốn triển khai các công trình hạ tầng.

**Article:** [Doanh nghiệp FDI mắc kẹt ở cụm công nghiệp, Đà Nẵng ra 'tối hậu thư' tháo gỡ](https://thanhnien.vn/doanh-nghiep-fdi-mac-ket-o-cum-cong-nghiep-da-nang-ra-toi-hau-thu-thao-go-185261111165833795.htm) | vi | thanhnien.vn
**Ngữ cảnh:**
>  vẫn chưa thể đưa nhà máy vào vận hành.
> Một trong những nguyên nhân là do hệ thống xử lý nước thải tập trung chưa được chủ đầu tư hoàn thiện theo quy định, khiến doanh nghiệp thứ cấp gặp khó trong việc hoàn tất thủ tục vận hành.
> Phó chủ tịch UBND thành phố Đà Nẵng Phan Thái Bình chủ trì họp tháo gỡ vướng mắc tại Cụm công nghiệp Đồi 30
> ẢNH: HUY ĐẠT
> Tại cuộc họp, ông Mai Thành Vinh, Giám đốc Công ty TNHH Đầu tư quốc tế Phú Ninh (chủ đầu tư hạ tầng cụm công nghiệp), cho rằng việc chậm hoàn thiện hệ thống xử lý nước thải tập trung xuất phát từ khó khăn trong bàn giao mặt bằng. Diện tích thực tế được bàn giao mới khoảng 15 ha đất công nghiệp trên tổng diện tích 30,47 ha theo quyết định thành lập, gây khó khăn về mặt bằng và nguồn vốn triển khai các công trình hạ tầng.
> Bên cạnh đó, việc các khoản hỗ trợ đầu tư hạ tầng vướng mắc qua thanh tra cũng ảnh hưởng đến khả năng cân đối tài chính.
> Ông Mai Thành Vinh, Giám đốc Công ty TNHH Đầu tư quốc tế Phú Ninh, nêu ý kiến tại buổi làm việc
> ẢNH: HUY ĐẠT
> Trong khi đó, đại diện Sở Nông nghiệp và Môi trường thành phố Đà Nẵng nhấn mạnh hệ thống xử lý nước thải tập trung là h

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0197 -->
## 197. edge-0197

**Triple:** Tim Cook (PERSON) —CEO_OF→ Apple (ORG)
**Assertion status:** reported
**Evidence:**
> OpenAI CEO Sam Altman, Apple CEO Tim Cook, and Anthropic CEO Dario Amodei have also expressed concern over the Border Patrol incidents, with some doing so in leaked internal memos.

**Article:** [Reid Hoffman urges Silicon Valley leaders to stop bending the knee to President Trump](https://techcrunch.com/2026/01/30/reid-hoffman-urges-silicon-valley-leaders-to-stop-bending-the-knee-to-president-trump/) | en | techcrunch.com
**Ngữ cảnh:**
> mp to trample whatever he can see, including our own business and security interests.”
> There’s been some pushback among the most powerful in the Valley against these deaths. Besides Hoffman, a longtime critic of Trump, billionaire VC Vinod Khosla has been the most vocal, characterizing the White House and crew as “a conscious-less administration.”
> OpenAI CEO Sam Altman, Apple CEO Tim Cook, and Anthropic CEO Dario Amodei have also expressed concern over the Border Patrol incidents, with some doing so in leaked internal memos. But most of them were quick to distance their concerns over this issue from the president himself.
> That’s the distinction that Hoffman wants to end. He’s making the case that tech leaders have power “and sitting on that power is not good for business. It’s also not neutrality. It’s a choice.”
> Still, many of the largest tech companies depend on the

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0198 -->
## 198. edge-0198

**Triple:** Stability AI (ORG) —PARTNERED_WITH→ Universal Music Group (ORG)
**Assertion status:** reported
**Evidence:**
> Stability, founded in 2019, has spent the past year signing deals to weave generative AI into entertainment companies’ creative workflows. It struck partnerships with Universal Music and EA last October and with Warner Music last November, each giving those companies a hand in co-developing Stability’s AI tools rather than just licensing the output..

**Article:** [Stability AI, maker of image generator Stable Diffusion, raises $76 million in fresh funding](https://techcrunch.com/2026/08/25/stability-ai-maker-of-image-generator-stable-diffusion-raises-76-million-in-fresh-funding/) | en | techcrunch.com
**Ngữ cảnh:**
> er, musician, and storyteller.”
> The company says it plans to use the money from its latest funding round to continue building out its “creative production” product suite while also expanding its professional services arm. Currently, Stability offers a variety of AI models that are designed for the purposes of AI music, video, and image generation.
> Stability, founded in 2019, has spent the past year signing deals to weave generative AI into entertainment companies’ creative workflows. It struck partnerships with Universal Music and EA last October and with Warner Music last November, each giving those companies a hand in co-developing Stability’s AI tools rather than just licensing the output..
> Stability has also had a mostly winning stretch in court. The company largely prevailed in a copyright lawsuit brought by Getty Images in the United Kingdom, which had accused the company of infringing upon IP rights by using the company’s images in the training of its image generation model. A judge ruled largely in Stability’s favor in that case

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0199 -->
## 199. edge-0199

**Triple:** Proparco (ORG) —CO_FINANCED_WITH→ Sumitomo Mitsui Banking Corporation (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> Tham gia giao dịch còn có các định chế tài chính phát triển gồm IFC, DEG (Đức), Proparco (Pháp) và Norfund (Na Uy); các ngân hàng xuất nhập khẩu China Eximbank, Korea Eximbank cùng nhóm ngân hàng thương mại và tổ chức tài chính như SMBC, Punjab National Bank, Commercial Bank of Ceylon, ICBC, Shinhan Bank, Woori Bank và KEXIM Asia Limited.

**Article:** [VPBank huy động 730 triệu USD vốn quốc tế](https://vnexpress.net/vpbank-huy-dong-730-trieu-usd-von-quoc-te-5143246.html) | vi | vnexpress.net
**Ngữ cảnh:**
> y động thành công khoản vay hợp vốn quốc tế 730 triệu USD, tương đương gần 19.000 tỷ đồng, do IFC và SMBC thu xếp, ngày 10/11.
> Giao dịch do Tổ chức Tài chính Quốc tế (IFC) và Ngân hàng Sumitomo Mitsui Banking Corporation (SMBC) đồng điều phối, thu xếp, gồm các khoản vay có kỳ hạn 3 năm, 5 năm và 7 năm, được giải ngân theo nhiều đợt trong năm 2026.
> Tham gia giao dịch còn có các định chế tài chính phát triển gồm IFC, DEG (Đức), Proparco (Pháp) và Norfund (Na Uy); các ngân hàng xuất nhập khẩu China Eximbank, Korea Eximbank cùng nhóm ngân hàng thương mại và tổ chức tài chính như SMBC, Punjab National Bank, Commercial Bank of Ceylon, ICBC, Shinhan Bank, Woori Bank và KEXIM Asia Limited. Sự tham gia của các tổ chức đến từ nhiều quốc gia giúp VPBank đa dạng hóa đối tác và mở rộng khả năng tiếp cận thị trường vốn quốc tế.
> Theo VPBank, nguồn vốn này sẽ được sử dụng để mở rộng tín dụng cho doanh nghiệp vừa và nhỏ (SME), đặc biệt là doanh nghiệp do phụ nữ làm chủ hoặc lãnh đạo (WSME) và doanh nghiệp hoạt động trong lĩnh vực nông nghiệp

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0200 -->
## 200. edge-0200

**Triple:** BNP Paribas (ORG) —CO_INVESTED_WITH→ Andreessen Horowitz (ORG)
**Assertion status:** reported
**Evidence:**
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
> nd led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.
> Microsoft’s $16.3 million convertible investment in Mistral as part of a partnership announced in February 2024 was presented as a Series A extension, implying an unchanged valuation.
> In June 2024, Mistral raised €600 million (about $640 million) in a mix of equity and debt. The long-rumored round was led by General Catalyst at a $6 billion valuat

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0201 -->
## 201. edge-0201

**Triple:** Fusion Hotel Group (ORG) —PARTNERED_WITH→ HMJ (ORG)
**Assertion status:** reported
**Evidence:**
> Sau thương vụ, Fusion sẽ cùng HMJ (Nhật Bản) và Topotels (Indonesia) quản lý khoảng 16.000 phòng khách sạn tại bốn thị trường châu Á.

**Article:** [M&A bất động sản 6 tháng đầu năm: Nhà đầu tư ngoại ưu tiên tài sản tạo dòng tiền hơn "lướt sóng"](https://vneconomy.vn/ma-bat-dong-san-6-thang-dau-nam-nha-dau-tu-ngoai-uu-tien-tai-san-tao-dong-tien-hon-luot-song.htm) | vi | vneconomy.vn
**Ngữ cảnh:**
> 
> Đối với bất động sản công nghiệp, hoạt động M&A thận trọng hơn với thương vụ Viconship mua 65% cổ phần Harbour City - doanh nghiệp đang phát triển dự án bất động sản công nghiệp tại Hải Phòng.
> Một điểm sáng khác đến từ phân khúc khách sạn và nghỉ dưỡng khi nhà sáng lập SC Capital Partners (Singapore) hoàn tất thương vụ mua lại Fusion Hotel Group. Sau thương vụ, Fusion sẽ cùng HMJ (Nhật Bản) và Topotels (Indonesia) quản lý khoảng 16.000 phòng khách sạn tại bốn thị trường châu Á.
> Theo JLL, trung tâm dữ liệu (data center) nhiều khả năng sẽ trở thành điểm nóng mới của thị trường M&A trong nửa cuối năm. Hiện tại nhiều nhà đầu tư khu vực đang tích cực tìm kiếm quỹ đất, đánh giá hạ tầng kỹ thuật và chuẩn bị gia nhập thị trường Việt Nam.
> Tuy nhiên, ông Tạ Mỹ Bách cho biết trở ngại lớn nhất của thị trường hiện nay không nằm ở tha

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0202 -->
## 202. edge-0202

**Triple:** Fuse (ORG) —CO_INVESTED_WITH→ Booz Allen Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Portal, founded in 2021, announced a $50 million Series A funding round Thursday that values the company at $250 million. The round was led by Geodesic Capital and Mach33, alongside Booz Allen Ventures, ARK Invest, AlleyCorp, and FUSE.

**Article:** [This founder helped build SpaceX&#8217;s most powerful rocket engine. Now he&#8217;s building a &#8216;fighter jet for orbit.&#8217;](https://techcrunch.com/2026/04/09/portal-raises-50-million-to-build-a-new-kind-of-high-power-rocket-engine/) | en | techcrunch.com
**Ngữ cảnh:**
> Jeff Thornburg helped turn a government research project into SpaceX’s most powerful rocket engine. Now, he’s trying to do the same thing at his startup Portal Space Systems, which is taking an idea set aside by NASA and turning it into high-powered propulsion for the next generation of spacecraft.
> Portal, founded in 2021, announced a $50 million Series A funding round Thursday that values the company at $250 million. The round was led by Geodesic Capital and Mach33, alongside Booz Allen Ventures, ARK Invest, AlleyCorp, and FUSE.
> The company is developing a technology called solar thermal propulsion. Today’s standard satellite engines either burn chemical fuel or convert the sun’s energy to electricity, using that to power efficient but low-powered thrusters. Portal’s engines would instead concentrate the heat of the sun, using that to heat propellant and move the spacecra

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0203 -->
## 203. edge-0203

**Triple:** Bill Ackman (PERSON) —CO_INVESTED_WITH→ Shyam Sankar (PERSON)
**Assertion status:** reported
**Evidence:**
> The round was led by Iconiq’s Murali Joshi, who helped lead the firm’s investments in companies like Anthropic, Datadog, Drata, 1Password, among others.
> Angels who invested include Microsoft CEO Satya Nadella; Palo Alto Networks CEO Nikesh Arora; Pershing Square Holdings CEO Bill Ackman; Palantir CTO Shyam Sankar; Anduril co-founder Trae Stephens; Former OpenAI VP Bob McGrew; Vercel CEO Guillermo Rauch, and Former AT&T CEO John Donovan. Whew!

**Article:** [AI security startup Outtake raises $40M from Iconiq, Satya Nadella, Bill Ackman, and other big names](https://techcrunch.com/2026/01/28/ai-security-startup-outtake-raises-40m-from-iconiq-satya-nadella-bill-ackman-and-other-big-names/) | en | techcrunch.com
**Ngữ cảnh:**
> Outtake, which makes an agentic cybersecurity platform to help enterprises detect, investigate, and take down identity fraud, has raised a $40 million Series B round of funding.
> While that might not sound like a lot given the huge sums some AI companies are raising, the names involved in this financing reads like a tech industry who’s who.
> The round was led by Iconiq’s Murali Joshi, who helped lead the firm’s investments in companies like Anthropic, Datadog, Drata, 1Password, among others.
> Angels who invested include Microsoft CEO Satya Nadella; Palo Alto Networks CEO Nikesh Arora; Pershing Square Holdings CEO Bill Ackman; Palantir CTO Shyam Sankar; Anduril co-founder Trae Stephens; Former OpenAI VP Bob McGrew; Vercel CEO Guillermo Rauch, and Former AT&T CEO John Donovan. Whew!
> The reason for the excitement? Outtake, founded in 2023 by a former Palantir engineer, Alex Dhillon, has found a way to automate what has largely been the manual problem of spotting and taking down digital identity posers: impersonation accounts, malicious domains posing as the company’s, rogue apps, fraudulent ads, and more. This problem has grow

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0204 -->
## 204. edge-0204

**Triple:** TQ Ventures (ORG) —INVESTED_IN→ Poseidon Aerospace (ORG)
**Assertion status:** reported
**Evidence:**
> Poseidon Aerospace secured $11 million in seed funding last year in pursuit of this goal. Now, the company has closed a $60 million Series A ahead of the first test flight of its uncrewed cargo plane, Egret, expected by the end of this year.
> The funding round was led by early-stage VC firm TQ Ventures, and saw new investments from Hanwha Asset Management, G Squared, and JAWS. Existing backers Starship Ventures, Draper Associates, and Drover Ventures also invested.

**Article:** [Poseidon Aerospace lands $60M ahead of first pilotless test flight](https://techcrunch.com/2026/09/08/poseidon-aerospace-lands-60m-ahead-of-first-pilotless-test-flight/) | en | techcrunch.com
**Ngữ cảnh:**
>  that the focus was almost always on introducing flashy new technologies.
> “Philosophically, we want to build the future of aerologistics,” Zagaynov said. “Not to be a hater, but I think a lot of people who start aerospace companies get nerd-sniped by very cool technology and then want to implement it into market. For us, we want to improve cargo.”
> Poseidon Aerospace secured $11 million in seed funding last year in pursuit of this goal. Now, the company has closed a $60 million Series A ahead of the first test flight of its uncrewed cargo plane, Egret, expected by the end of this year.
> The funding round was led by early-stage VC firm TQ Ventures, and saw new investments from Hanwha Asset Management, G Squared, and JAWS. Existing backers Starship Ventures, Draper Associates, and Drover Ventures also invested.
> True to Zagaynov’s allergy to getting “nerd-sniped” by promising-yet-currently-unworkable technologies, Poseidon is being built with a ruthless approach to lowering the cost of transporting cargo.
> The startup is embracing autonomy and remote piloting, but it’s not bothering with the vertical takeoff and landing tech that is de rigueur among so man

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0205 -->
## 205. edge-0205

**Triple:** Shorooq (ORG) —CO_INVESTED_WITH→ Silicon Badia (ORG)
**Assertion status:** reported
**Evidence:**
> Journify, the ad signal infrastructure company, today announced a $12 million Series A at four times its previous valuation. Al Mada Ventures led the round, co-led by returning investor Silicon Badia, with Shorooq and Bunat Ventures increasing their investment and Du Ventures and Oraseya Capital joining as new investors. The funding will take Journify into the US and Europe and expand the AI behind its platform.

**Article:** [Journify raises $12M Series A amid 5x growth](https://techcrunch.com/press-release/journify-raises-12m-series-a-amid-5x-growth/) | en | techcrunch.com
**Ngữ cảnh:**
> San Francisco, California, USA, November 3rd, 2026, TechnologyWire
> Investors back Journify’s push into the US and Europe
> Journify, the ad signal infrastructure company, today announced a $12 million Series A at four times its previous valuation. Al Mada Ventures led the round, co-led by returning investor Silicon Badia, with Shorooq and Bunat Ventures increasing their investment and Du Ventures and Oraseya Capital joining as new investors. The funding will take Journify into the US and Europe and expand the AI behind its platform.
> Global ad spend will exceed $1 trillion in 2026, with algorithms expected to place three quarters by 2028, according to dentsu. These systems learn from the customer outcomes brands send back. Browser restrictions, broken tracking, and disconnected offline sales leave them with an incomplete picture of who buys.
> Journify makes sure ad platforms su

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0206 -->
## 206. edge-0206

**Triple:** General Catalyst (ORG) —CO_INVESTED_WITH→ Theory Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> On Tuesday, Doss announced that it raised a $55 million Series B co-led by Madrona and Premji Invest, with participation from Intuit Ventures. Other new and existing inventors in the round include Theory Ventures, General Catalyst, Contrary Capital, and Greyhound Capital.

**Article:** [Doss raises $55M for AI inventory management that plugs into ERP](https://techcrunch.com/2026/03/24/doss-raises-55m-for-ai-inventory-management-that-plugs-into-erp/) | en | techcrunch.com
**Ngữ cảnh:**
> ey Jones, many new AI ERPs lack robust inventory management, the process of ensuring that the data on physical goods remains synced with the accounting ledger.
> Doss claims to solve this by providing an AI-native inventory management layer that integrates with existing accounting systems, whether traditional ERPs or ones built by AI-based startups.
> On Tuesday, Doss announced that it raised a $55 million Series B co-led by Madrona and Premji Invest, with participation from Intuit Ventures. Other new and existing inventors in the round include Theory Ventures, General Catalyst, Contrary Capital, and Greyhound Capital.
> Doss, founded in 2022, originally focused on a core accounting product similar to those offered by AI-native startups like Rillet and Campfire. But last year, the startup decided instead of competing with these companies, “we would rather partner with them, and play a different game,” Jones told TechCrunch.
> Jones explained that AI-native ERP compa

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0207 -->
## 207. edge-0207

**Triple:** Picture Capital (ORG) —INVESTED_IN→ ScaleOps (ORG)
**Assertion status:** reported
**Evidence:**
> The startup, which builds software that automatically manages and reallocates computing resources in real time, has raised $130 million at an $800 million valuation, ScaleOps said Monday. The Series C funding round was led by Insight Partners, with participation from existing investors, including Lightspeed Venture Partners, NFX, Glilot Capital Partners, and Picture Capital. The company says its software reduces cloud and AI infrastructure costs by as much as 80%.

**Article:** [ScaleOps raises $130M to improve computing efficiency amid AI demand](https://techcrunch.com/2026/03/30/scaleops-130m-series-c-kubernetes-efficiency-ai-demand-funding/) | en | techcrunch.com
**Ngữ cảnh:**
> AI may be booming, but behind the scenes, companies are wasting vast amounts of expensive compute. GPUs sit idle, workloads are over-provisioned, and cloud costs continue to climb. ScaleOps believes the problem isn’t a shortage — it’s mismanagement.
> The startup, which builds software that automatically manages and reallocates computing resources in real time, has raised $130 million at an $800 million valuation, ScaleOps said Monday. The Series C funding round was led by Insight Partners, with participation from existing investors, including Lightspeed Venture Partners, NFX, Glilot Capital Partners, and Picture Capital. The company says its software reduces cloud and AI infrastructure costs by as much as 80%.
> ScaleOps was co-founded in 2022 by Yodar Shafrir, a former engineer at Run:ai, a GPU orchestration startup acquired by Nvidia, after seeing firsthand how difficult it was for companies to manage increasingly complex AI workloads. While tools like Kubernetes help run applications across large clusters of machines, they often rely on static configur

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0208 -->
## 208. edge-0208

**Triple:** Amazon Alexa Fund (ORG) —CO_INVESTED_WITH→ Dick Costolo (PERSON)
**Assertion status:** reported
**Evidence:**
> “Eugenia has a unique sense for where AI is headed and a track record of great taste in building it,” said Alex Lim, general partner at IVP, which led the new round, in a statement. “She has a clear vision for how people will interact with AI, one that goes far beyond the text box or command line. Wabi is the expression of that vision, and we’re thrilled to support her.”
> Other participants in the round included Andreessen Horowitz (a16z), Forerunner, Amazon Alexa Fund, and angel investors like Shopify CEO Tobi Lütke, Salesforce CEO Marc Benioff, former Yahoo! head Marissa Mayer, former Twitter CEO Dick Costolo, and one half of The Chainsmokers, Alex Pall.

**Article:** [Wabi, the AI agent that builds mini apps, now valued at $1.25B after latest round](https://techcrunch.com/2026/10/29/wabi-the-ai-agent-that-builds-mini-apps-now-valued-at-1-25b-after-latest-round/) | en | techcrunch.com
**Ngữ cảnh:**
> es that Wabi’s investors agree that its new agentic angle has some potential, especially given the market around AI agents is hot right now, with viral AI agent Instinct pulling in another billion at a $10 billion valuation in September.
> Even Tolan, which makes a cute, Muppet-like AI companion to help people navigate life, just raised $30 million.
> “Eugenia has a unique sense for where AI is headed and a track record of great taste in building it,” said Alex Lim, general partner at IVP, which led the new round, in a statement. “She has a clear vision for how people will interact with AI, one that goes far beyond the text box or command line. Wabi is the expression of that vision, and we’re thrilled to support her.”
> Other participants in the round included Andreessen Horowitz (a16z), Forerunner, Amazon Alexa Fund, and angel investors like Shopify CEO Tobi Lütke, Salesforce CEO Marc Benioff, former Yahoo! head Marissa Mayer, former Twitter CEO Dick Costolo, and one half of The Chainsmokers, Alex Pall.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0209 -->
## 209. edge-0209

**Triple:** Neo (ORG) —INVESTED_IN→ Altara (ORG)
**Assertion status:** reported
**Evidence:**
> San Francisco-based startup Altara, which just secured $7 million in seed funding, says it has built an AI layer designed to bridge these data gaps and bring fragmented technical information into a single platform. The round was led by Greylock, with participation from Neo, BoxGroup, Liquid 2 Ventures, and Jeff Dean.

**Article:** [Altara secures $7M to bridge the data gap that&#8217;s slowing down physical sciences](https://techcrunch.com/2026/05/05/altara-secures-7m-to-bridge-the-data-gap-thats-slowing-down-physical-sciences/) | en | techcrunch.com
**Ngữ cảnh:**
> Companies working on batteries, semiconductors, and medical devices generate vast amounts of data — and much of it ends up scattered across spreadsheets and legacy systems, making it hard to use to improve products or understand failures.
> San Francisco-based startup Altara, which just secured $7 million in seed funding, says it has built an AI layer designed to bridge these data gaps and bring fragmented technical information into a single platform. The round was led by Greylock, with participation from Neo, BoxGroup, Liquid 2 Ventures, and Jeff Dean.
> Altara was founded in 2025 by Eva Tuecke (pictured right), who previously conducted particle physics research at Fermilab and worked at SpaceX; and Catherine Yeo (pictured left), a former AI engineer at Warp. The two met while studying computer science at Harvard University.
> “Imagine if you’re a company building next-generation batteries, and a ba

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0210 -->
## 210. edge-0210

**Triple:** Pear VC (ORG) —INVESTED_IN→ Listen Labs (ORG)
**Assertion status:** reported
**Evidence:**
> Listen Labs was previously valued at $500 million when it announced a $69 million Series B round in late January led by Ribbit Capital, with participation from returning backers Sequoia, Conviction, and Pear VC.

**Article:** [AI research startup Listen Labs scrubbed a $1.5B funding round for Salesforce talks](https://techcrunch.com/2026/09/09/ai-research-startup-listen-labs-scrubbed-a-1-5b-funding-round-for-salesforce-talks/) | en | techcrunch.com
**Ngữ cảnh:**
> ups using AI to disrupt the customer research market.
> Besides Simile, competitors in the space include Outset, Keplar, and Aaru. While some platforms automate interviews with real humans, others startups — like Aaru and Simile — take a synthetic approach, using AI to simulate human behavior and predict responses without interviewing anyone at all.
> Listen Labs was previously valued at $500 million when it announced a $69 million Series B round in late January led by Ribbit Capital, with participation from returning backers Sequoia, Conviction, and Pear VC.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0211 -->
## 211. edge-0211

**Triple:** Eugenia Kuyda (PERSON) —FOUNDED→ Replika (ORG)
**Assertion status:** reported
**Evidence:**
> Founded by Eugenia Kuyda, who previously founded the AI companion startup Replika, Wabi originally focused on allowing anyone to build apps using prompts. Last month, however, the startup announced a pivot of sorts to become an AI messenger.

**Article:** [Wabi, the AI agent that builds mini apps, now valued at $1.25B after latest round](https://techcrunch.com/2026/10/29/wabi-the-ai-agent-that-builds-mini-apps-now-valued-at-1-25b-after-latest-round/) | en | techcrunch.com
**Ngữ cảnh:**
> The race to build the winning AI assistant is on, and investors are spreading out their bets. On Thursday, another AI app, Wabi, now describing itself as a “personal agent,” said it has raised $55 million at a $1.25 billion valuation.
> Founded by Eugenia Kuyda, who previously founded the AI companion startup Replika, Wabi originally focused on allowing anyone to build apps using prompts. Last month, however, the startup announced a pivot of sorts to become an AI messenger.
> The idea now is that the new Wabi — or Wabi 2.0, as it was called — could build the interfaces you need to get things done as part of its role as your personal AI agent.
> The company suggests Wabi could be used to build mini apps for things like meal planning, tracking local restaurants, planning date nights, creating fitness plans, designing speci

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0212 -->
## 212. edge-0212

**Triple:** Jane Street (ORG) —CO_INVESTED_WITH→ Salesforce Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> If finalized, the deal would nearly triple Anthropic’s valuation, which was $61.5 billion after a $3.5 billion funding round led by Lightspeed Venture Partners announced in March. Other participants in the startup’s last round included Bessemer Venture Partners, Cisco Investments, D1 Capital Partners, Fidelity Management & Research Company, General Catalyst, Jane Street, Menlo Ventures, and Salesforce Ventures.

**Article:** [Anthropic reportedly nears $170B valuation with potential $5B round](https://techcrunch.com/2025/07/29/anthropic-reportedly-nears-170b-valuation-with-potential-5b-round/) | en | techcrunch.com
**Ngữ cảnh:**
> llion in funding, valuing the large language model developer at $170 billion, Bloomberg reported.
> Iconiq Capital is leading this funding round, but there’s a possibility of a second lead investor joining the deal. The company has also been in talks with Qatar Investment Authority and GIC, Singapore’s sovereign wealth fund, according to the report.
> If finalized, the deal would nearly triple Anthropic’s valuation, which was $61.5 billion after a $3.5 billion funding round led by Lightspeed Venture Partners announced in March. Other participants in the startup’s last round included Bessemer Venture Partners, Cisco Investments, D1 Capital Partners, Fidelity Management & Research Company, General Catalyst, Jane Street, Menlo Ventures, and Salesforce Ventures.
> Despite Anthropic’s mission as a safety-conscious AI model developer, the company’s CEO, Dario Amodei, recently confessed in a memo to employees, reported by Wired, that he’s “not thrilled” about taking money from sovereign wealth funds of dictatorial governments.
> To keep pace with the massive capital requirements of developing AI models, the comp

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0213 -->
## 213. edge-0213

**Triple:** Z Ventures (ORG) —INVESTED_IN→ Config (ORG)
**Assertion status:** reported
**Evidence:**
> Samsung Venture Investment led its oversubscribed $27 million seed round at a valuation of more than $200 million, bringing Config’s total raised to $35 million. Hyundai Motor’s venture arm ZER01NE Ventures; LG Technology Ventures; and SKT America, a South Korean telco giant’s VC unit, also joined as strategic investors. Other investors include angel investor Pieter Abbeel (co-founder of Covariant and a UC Berkeley professor) and financial backers Mirae Asset Ventures, Korea Development Bank, GS Futures, Kakao Ventures, and Z Ventures.

**Article:** [Korea&#8217;s biggest manufacturers back Config, the TSMC of robot data](https://techcrunch.com/2026/05/11/koreas-biggest-manufacturers-back-config-the-tsmc-of-robot-data/) | en | techcrunch.com
**Ngữ cảnh:**
> hains. That structural foundation is now shaping how artificial intelligence is adopted and where investment flows.
> Which makes it particularly significant that Config, a Seoul- and San Jose-based startup building the data layer for robotics foundation models (RFMs), has secured backing from the venture arms of South Korea’s biggest manufacturers.
> Samsung Venture Investment led its oversubscribed $27 million seed round at a valuation of more than $200 million, bringing Config’s total raised to $35 million. Hyundai Motor’s venture arm ZER01NE Ventures; LG Technology Ventures; and SKT America, a South Korean telco giant’s VC unit, also joined as strategic investors. Other investors include angel investor Pieter Abbeel (co-founder of Covariant and a UC Berkeley professor) and financial backers Mirae Asset Ventures, Korea Development Bank, GS Futures, Kakao Ventures, and Z Ventures.
> Config was founded in January 2025 by CEO Minjoon Seo, a former researcher at Meta and chief scientist at TwelveLabs, along with three co-founders with backgrounds at Waymo, Google, and Naver. Instead of building robots themselves, the team is focused on a simpler goal — providing data that robots need to learn and operate. They believe that bette

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0214 -->
## 214. edge-0214

**Triple:** Linse Capital (ORG) —CO_INVESTED_WITH→ Threshold Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Executives at Freeform, a startup developing a novel 3D-printing system for metal components, told TechCrunch that the company raised a $67 million Series B to expand its manufacturing platform.
> Investors include Apandion, AE Ventures, Founders Fund, Linse Capital, Nvidia’s NVentures, Threshold Ventures, and Two Sigma Ventures. FreeForm declined to disclose the company’s post-financing valuation, which PitchBook cites as $179 million.

**Article:** [Freeform raises $67M Series B to scale up laser AI manufacturing](https://techcrunch.com/2026/02/19/freeform-raises-67m-series-b-to-scale-up-laser-ai-manufacturing/) | en | techcrunch.com
**Ngữ cảnh:**
> Tech investors haven’t given up on the dream of making physical products with the same speed and ease as coding software.
> Executives at Freeform, a startup developing a novel 3D-printing system for metal components, told TechCrunch that the company raised a $67 million Series B to expand its manufacturing platform.
> Investors include Apandion, AE Ventures, Founders Fund, Linse Capital, Nvidia’s NVentures, Threshold Ventures, and Two Sigma Ventures. FreeForm declined to disclose the company’s post-financing valuation, which PitchBook cites as $179 million.
> CEO and co-founder Erik Palitsch said the funding would allow the company to upgrade its current GoldenEye printing system, which uses 18 lasers to fuse metal powders into precision components, to a new version. Dubbed Skyfall, the next iteration of the platform would use hundreds of lasers to produce thousands of kilograms of metal parts each day

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0215 -->
## 215. edge-0215

**Triple:** Wonder (ORG) —ACQUIRED→ Blue Apron (ORG)
**Assertion status:** reported
**Evidence:**
> Additionally, Wonder has acquired meal-kit company Blue Apron, restaurant delivery platform Grubhub, media company Tastemade, and kitchen robotics company Spyce.

**Article:** [Food delivery startup Wonder files for IPO as it explores its next big bite](https://techcrunch.com/2026/11/05/food-delivery-startup-wonder-files-for-ipo-as-it-explores-its-next-big-bite/) | en | techcrunch.com
**Ngữ cảnh:**
> d it at around $9 billion. Investors include Accel, GV, AllianceBernstein, and ARK Invest.
> Meanwhile, Wonder has been busy expanding its footprint and strengthening its business through acquisitions. The company has outlined ambitious growth plans, including a major push into Texas, where it aims to open more than 100 locations by the end of 2027.
> Additionally, Wonder has acquired meal-kit company Blue Apron, restaurant delivery platform Grubhub, media company Tastemade, and kitchen robotics company Spyce. The latter acquisition gives Wonder access to automation technology that could help streamline food preparation and improve how food is served.
> Wonder is also branching out with Wonder Create, its platform focused on letting food entrepreneurs and social media influencers develop new food concepts, restaurant brands, and menu items. The platform l

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0216 -->
## 216. edge-0216

**Triple:** Contrary Capital (ORG) —CO_INVESTED_WITH→ Theory Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> On Tuesday, Doss announced that it raised a $55 million Series B co-led by Madrona and Premji Invest, with participation from Intuit Ventures. Other new and existing inventors in the round include Theory Ventures, General Catalyst, Contrary Capital, and Greyhound Capital.

**Article:** [Doss raises $55M for AI inventory management that plugs into ERP](https://techcrunch.com/2026/03/24/doss-raises-55m-for-ai-inventory-management-that-plugs-into-erp/) | en | techcrunch.com
**Ngữ cảnh:**
> ey Jones, many new AI ERPs lack robust inventory management, the process of ensuring that the data on physical goods remains synced with the accounting ledger.
> Doss claims to solve this by providing an AI-native inventory management layer that integrates with existing accounting systems, whether traditional ERPs or ones built by AI-based startups.
> On Tuesday, Doss announced that it raised a $55 million Series B co-led by Madrona and Premji Invest, with participation from Intuit Ventures. Other new and existing inventors in the round include Theory Ventures, General Catalyst, Contrary Capital, and Greyhound Capital.
> Doss, founded in 2022, originally focused on a core accounting product similar to those offered by AI-native startups like Rillet and Campfire. But last year, the startup decided instead of competing with these companies, “we would rather partner with them, and play a different game,” Jones told TechCrunch.
> Jones explained that AI-native ERP compa

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0217 -->
## 217. edge-0217

**Triple:** Benchmark (ORG) —CO_INVESTED_WITH→ Salesforce Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.

**Article:** [Legora reaches $5.55 billion valuation as AI legal tech boom endures](https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/) | en | techcrunch.com
**Ngữ cảnh:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.
> There are other signs that investors are bullish about AI legal tech. Legora’s Series D and valuation jump come just a few months after its October 2025 $150 million Series C round led at a $1.8 billion valuation. Its competitor, Harvey, which is backed by a16z, is already valued at $8 billion, and is now reportedly seeking to raise at an $11 bill

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0218 -->
## 218. edge-0218

**Triple:** O.G. Venture Partners (ORG) —CO_INVESTED_WITH→ Lightspeed Venture Partners (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The round was led by Lightspeed Venture Partners and O.G. Venture Partners. This follows the company’s $260 million Series B raised in January 2025.
> Neko Health has developed proprietary body-scanning technology, which it couples with bloodwork, to assess a person’s health. For gym lovers, the scan also now includes body composition information. It can couple the assessment with Apple Health data, which Nilsonne says gives its medical clinicians real-world data to use in its assessments.
> Neko Health, which has locations in the U.K. and Sweden, is preparing for its first U.S. location in New York. The company says more than 100,000 people have already had scans and more than 350,000 people have either registered for the waitlist or set an appointment.
> One of the people who had a Neko Health scan is Calm founder Alex Tew. He posted on X that it found a malignant mole on his back, which he promptly had removed. “I’m grateful to Neko for helping me discover this – I’m not sure how I would have otherwise.”
> Neko Health isn’t the only health scanning company founded by tech folks. Midjourney, the AI Lab best known for its AI image and video creation model and website, is also creating a body scanner, which it plans to integrate into a spa experience with hot tubs and saunas, opening in San Francisco sometime in 2027.
> Other investors in Neko Health’s latest round include Atomico, General Catalyst, Lakestar, Liberty City Ventures, Positive Sum, and BDT & MSD.

**Article:** [Daniel Ek&#8217;s body-scanning startup Neko Health raises another $700M](https://techcrunch.com/2026/07/15/daniel-eks-body-scanning-startup-neko-health-raises-another-700m/) | en | techcrunch.com
**Ngữ cảnh:**
> Neko Health, the body-scanning and health assessment startup founded by Spotify’s Daniel Ek (pictured above, right) and his co-founder Hjalmar Nilsonne (above, left), has raised a $700 million Series C.
> The round was led by Lightspeed Venture Partners and O.G. Venture Partners. This follows the company’s $260 million Series B raised in January 2025.
> Neko Health has developed proprietary body-scanning technology, which it couples with bloodwork, to assess a person’s health. For gym lovers, the scan also now includes body composition information. It can couple the assessment with Apple Health data, which Nilsonne says gives its medical clinicians real-world data to use in its assessments.
> Neko Health, which has locations in the U.K. and Sweden, is preparing for its first U.S. location in New York. The company says more than 100,000 people have already had scans and more than 350,000 people have either registered for the waitlist or set an appointment.
> One of the people who had a Neko Health scan is Calm founder Alex Tew. He posted on X that it found a malignant mole on his back, which he promptly had removed. “I’m grateful to Neko for helping me discover this – I’m not sure how I would have otherwise.”
> Neko Health isn’t the only health scanning company founded by tech folks. Midjourney, the AI Lab best known for its AI image and video creation model and website, is also creating a body scanner, which it plans to integrate into a spa experience with hot tubs and saunas, opening in San Francisco sometime in 2027.
> Other investors in Neko Health’s latest round include Atomico, General Catalyst, Lakestar, Liberty City Ventures, Positive Sum, and BDT & MSD.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0219 -->
## 219. edge-0219

**Triple:** Sean Jacobsohn (PERSON) —INVESTED_IN→ InScope (ORG)
**Assertion status:** reported
**Evidence:**
> Norwest partner Sean Jacobsohn told TechCrunch that he invested in InScope after he heard from multiple clients that the startup’s product saves them a lot of time.

**Article:** [InScope nabs $14.5M to solve the pain of financial reporting](https://techcrunch.com/2026/02/20/inscope-nabs-14-5m-to-solve-the-pain-of-financial-reporting/) | en | techcrunch.com
**Ngữ cảnh:**
>  customer base by 5x, attracting significant accounting firms such as CohnReznick, currently ranked in the top 15 nationally.
> Of course, it may be a while before accountants — a profession Antony describes as risk-averse — feel comfortable letting AI fully automate financial statement preparation. Nonetheless, that remains InScope’s ultimate goal.
> Norwest partner Sean Jacobsohn told TechCrunch that he invested in InScope after he heard from multiple clients that the startup’s product saves them a lot of time.
> Jacobsohn is convinced that InScope stands out because few founders possess the specific expertise required to reinvent financial reporting technology.
> “It’s a very complex space, and you need to be able to have been in the shoes of the buyer before,” he said.
> Antony agrees that accountants are not typically the type to launch startups. Fortunatel

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0220 -->
## 220. edge-0220

**Triple:** Sacombank Laos (ORG) —PARTNERED_WITH→ Green SM (ORG)
**Assertion status:** reported
**Evidence:**
> Green SM also signed comprehensive cooperation agreements with major banks, including VietinBank Laos, JDB, MB Bank Laos and Sacombank Laos; Lao telecom operator ETL; e-wallet providers U-Money and M-Money; and leading hotel and tourism groups such as Bawanli, Mường Thanh Vientiane Hotel and Latsavong Wanda Vista Hotel.

**Article:** [Việt Nam, Laos step up cooperation on green transition, digital economy](https://vietnamnews.vn/economy/1803930/viet-nam-laos-step-up-cooperation-on-green-transition-digital-economy.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> referential rates to roaming customers travelling from Việt Nam to Laos; integrating ride-hailing services directly into the Lao Travel national tourism app; providing green-transition vouchers to customers purchasing Unitel tourist SIM cards; and deploying Green SM’s Green Business corporate mobility solution across Unitel’s internal operations.
> 
> Green SM also signed comprehensive cooperation agreements with major banks, including VietinBank Laos, JDB, MB Bank Laos and Sacombank Laos; Lao telecom operator ETL; e-wallet providers U-Money and M-Money; and leading hotel and tourism groups such as Bawanli, Mường Thanh Vientiane Hotel and Latsavong Wanda Vista Hotel.
> 
> The agreements focus on integrating payment technology infrastructure, introducing joint promotional programmes and promoting environmentally friendly mobility solutions to a wider audience of tourists and local residents.
> 
> Speaking at the event, Tâm lauded Green SM Laos for its efforts and impressive achievements. He said the company’s investmen

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0221 -->
## 221. edge-0221

**Triple:** SoftBank (ORG) —INVESTED_IN→ OpenAI (ORG)
**Assertion status:** reported
**Evidence:**
> SoftBank has taken on a new $40 billion loan to help it cover its $30 billion commitment to invest in OpenAI as part of the AI model maker’s record-breaking $110 billion raise last month, the Japanese conglomerate said on Friday.

**Article:** [Why SoftBank’s new $40B loan points to a 2026 OpenAI IPO](https://techcrunch.com/2026/03/27/why-softbanks-new-40b-loan-points-to-a-2026-openai-ipo/) | en | techcrunch.com
**Ngữ cảnh:**
> SoftBank has taken on a new $40 billion loan to help it cover its $30 billion commitment to invest in OpenAI as part of the AI model maker’s record-breaking $110 billion raise last month, the Japanese conglomerate said on Friday.
> Most striking is that the loan is unsecured and has a 12-month term, meaning it must be repaid or refinanced by next year. This could be a signal that the lenders believe OpenAI’s highly anticipated public listing will indeed come later this year, as some outlets, like CNBC, have reported. The loan is provided by JPMorgan Chase, Goldman Sachs, and

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0222 -->
## 222. edge-0222

**Triple:** FinDev Canada (ORG) —CO_FINANCED_WITH→ Export Finance Australia (ORG)
**Assertion status:** reported
**Evidence:**
> HÀ NỘI — VPBank has secured a VNĐ9.1 trillion (US$350 million) term loan facility, backed by Sumitomo Mitsui Banking Corporation (SMBC) and a group of development finance institutions and bilateral agencies, including British International Investment (BII), Export Finance Australia (EFA), Development Finance Institute Canada (FinDev Canada) and the Japan International Cooperation Agency (JICA).

**Article:** [VPBank, global partners launch $350m deal for Việt Nam’s sustainable development](https://vietnamnews.vn/economy/1722286/vpbank-global-partners-launch-350m-deal-for-viet-nam-s-sustainable-development.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> HÀ NỘI — VPBank has secured a VNĐ9.1 trillion (US$350 million) term loan facility, backed by Sumitomo Mitsui Banking Corporation (SMBC) and a group of development finance institutions and bilateral agencies, including British International Investment (BII), Export Finance Australia (EFA), Development Finance Institute Canada (FinDev Canada) and the Japan International Cooperation Agency (JICA).
> SMBC acted as co-ordinator and mandated lead arranger for this financing.
> The signing ceremony took place at VPBank’s Hà Nội headquarters, attended by the Ambassadors of the United Kingdom, Australia, and Japan, as well as senior diplomatic representatives from the Canadian Embassy and other participating embassies. High-level delegates from the p

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0223 -->
## 223. edge-0223

**Triple:** Storm Ventures (ORG) —CO_INVESTED_WITH→ Norwest (ORG)
**Assertion status:** reported
**Evidence:**
> So, in 2023, the pair decided to launch InScope, an AI-powered financial reporting platform that helps companies and accounting firms automate many aspects of the financial statement preparation process. The startup just raised $14.5 million in Series A funding led by Norwest, with participation from Storm Ventures and existing backers Better Tomorrow Ventures and Lightspeed Venture Partners.

**Article:** [InScope nabs $14.5M to solve the pain of financial reporting](https://techcrunch.com/2026/02/20/inscope-nabs-14-5m-to-solve-the-pain-of-financial-reporting/) | en | techcrunch.com
**Ngữ cảnh:**
> to Miro and Gootnick to Hopin and later Thrive Global.
> No matter where they worked, Antony and Gootnick kept running into the same manual challenges.
> “The way financial statements come together, it’s just patched together in a lot of spreadsheets, moved into a bunch of Word documents, emailed back and forth between people,” Antony told TechCrunch.
> So, in 2023, the pair decided to launch InScope, an AI-powered financial reporting platform that helps companies and accounting firms automate many aspects of the financial statement preparation process. The startup just raised $14.5 million in Series A funding led by Norwest, with participation from Storm Ventures and existing backers Better Tomorrow Ventures and Lightspeed Venture Partners.
> While InScope isn’t fully automating the generation of income statements and balance sheets yet, it automates a vast amount of the manual busy work, from verifying math to formatting. Simply ensuring that dollar signs and commas are uniform and correctly placed can save accountants up to 20% of their time, according to Antony, InScope’s CEO.
> Over 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0224 -->
## 224. edge-0224

**Triple:** Tobi Lütke (PERSON) —CO_INVESTED_WITH→ Andreessen Horowitz (ORG)
**Assertion status:** reported
**Evidence:**
> “Eugenia has a unique sense for where AI is headed and a track record of great taste in building it,” said Alex Lim, general partner at IVP, which led the new round, in a statement. “She has a clear vision for how people will interact with AI, one that goes far beyond the text box or command line. Wabi is the expression of that vision, and we’re thrilled to support her.”
> Other participants in the round included Andreessen Horowitz (a16z), Forerunner, Amazon Alexa Fund, and angel investors like Shopify CEO Tobi Lütke, Salesforce CEO Marc Benioff, former Yahoo! head Marissa Mayer, former Twitter CEO Dick Costolo, and one half of The Chainsmokers, Alex Pall.

**Article:** [Wabi, the AI agent that builds mini apps, now valued at $1.25B after latest round](https://techcrunch.com/2026/10/29/wabi-the-ai-agent-that-builds-mini-apps-now-valued-at-1-25b-after-latest-round/) | en | techcrunch.com
**Ngữ cảnh:**
> es that Wabi’s investors agree that its new agentic angle has some potential, especially given the market around AI agents is hot right now, with viral AI agent Instinct pulling in another billion at a $10 billion valuation in September.
> Even Tolan, which makes a cute, Muppet-like AI companion to help people navigate life, just raised $30 million.
> “Eugenia has a unique sense for where AI is headed and a track record of great taste in building it,” said Alex Lim, general partner at IVP, which led the new round, in a statement. “She has a clear vision for how people will interact with AI, one that goes far beyond the text box or command line. Wabi is the expression of that vision, and we’re thrilled to support her.”
> Other participants in the round included Andreessen Horowitz (a16z), Forerunner, Amazon Alexa Fund, and angel investors like Shopify CEO Tobi Lütke, Salesforce CEO Marc Benioff, former Yahoo! head Marissa Mayer, former Twitter CEO Dick Costolo, and one half of The Chainsmokers, Alex Pall.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0225 -->
## 225. edge-0225

**Triple:** Even Rogers (PERSON) —CEO_OF→ True Anomaly (ORG)
**Assertion status:** reported
**Evidence:**
> Even Rogers, co-founder and CEO of True Anomaly, is a former Air Force officer and space systems strategist.

**Article:** [Space defense, gravity, and connectivity with Bridgit Mendler, Even Rogers, and Max Haot at TechCrunch Disrupt 2025](https://techcrunch.com/2025/10/03/space-is-open-for-business-with-even-rogers-and-max-haot-at-techcrunch-disrupt-2025/) | en | techcrunch.com
**Ngữ cảnh:**
> -only debut at Disrupt 2024. Mendler is back to share how Northwood Space is scaling ground station networks to power the next generation of satellite connectivity. Known globally as a former Disney star, she’s now making headlines for her pivot to space tech entrepreneurship, focusing on building resilient, scalable communications infrastructure.
> Even Rogers, co-founder and CEO of True Anomaly, is a former Air Force officer and space systems strategist. Rogers helped shape the foundational doctrine of the U.S. Space Force as a DARPA Service Chiefs Fellow. Now he’s deploying cutting-edge space defense technologies to protect orbital assets and reimagine how the U.S. ensures freedom of action in space.
> Max Haot, multi-exit entrepreneur across aerospace, livestreaming, and connected devices; founder

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0226 -->
## 226. edge-0226

**Triple:** Terrain Capital (ORG) —INVESTED_IN→ Parallel Web Systems (ORG)
**Assertion status:** reported
**Evidence:**
> Parallel Web Systems, the AI agent-tool startup founded by former Twitter CEO Parag Agrawal, has raised a $100 million Series B at a $2 billion valuation led by Sequoia. Existing investors Kleiner Perkins, Index Ventures, Khosla Ventures, First Round Capital, Spark Capital, and Terrain Capital also participated, the company said.

**Article:** [Parallel Web Systems hits $2B valuation five months after its last big raise](https://techcrunch.com/2026/04/29/parallel-web-systems-hits-2b-valuation-five-months-after-its-last-big-raise/) | en | techcrunch.com
**Ngữ cảnh:**
> Parallel Web Systems, the AI agent-tool startup founded by former Twitter CEO Parag Agrawal, has raised a $100 million Series B at a $2 billion valuation led by Sequoia. Existing investors Kleiner Perkins, Index Ventures, Khosla Ventures, First Round Capital, Spark Capital, and Terrain Capital also participated, the company said.
> This raise comes just five months after the startup announced its $100 million Series A at a $740 million valuation led by Kleiner and Index, and brings the total capital it raised to $230 million.
> Parallel offers a suite of web search and research APIs specifically for AI agents and names customers such as Clay, Harvey, Notion, and Opendoor. It s

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0227 -->
## 227. edge-0227

**Triple:** Point72 Ventures (ORG) —INVESTED_IN→ Antares (ORG)
**Assertion status:** reported
**Evidence:**
> Nuclear power startup Antares Nuclear said Monday that it has raised $470 million to build small reactors for U.S. military bases.
> The Series C round, which was led by Paradigm and Caffeinated Capital with participation from Industrious Ventures, Point72 Ventures, and Shine Capital, underscores investors’ growing interest in advanced nuclear startups — a trend fueled by an AI data center building boom and demand for new sources of power. The Series C round included $370 million in equity and $100 million in debt.

**Article:** [Antares raises $470M to build nuclear reactors for the US military](https://techcrunch.com/2026/07/27/antares-raises-470m-to-build-nuclear-reactors-for-the-u-s-military/) | en | techcrunch.com
**Ngữ cảnh:**
> Nuclear power startup Antares Nuclear said Monday that it has raised $470 million to build small reactors for U.S. military bases.
> The Series C round, which was led by Paradigm and Caffeinated Capital with participation from Industrious Ventures, Point72 Ventures, and Shine Capital, underscores investors’ growing interest in advanced nuclear startups — a trend fueled by an AI data center building boom and demand for new sources of power. The Series C round included $370 million in equity and $100 million in debt.
> Antares has been developing a small modular reactor (SMR) capable of producing between 100 kilowatts and 1 megawatt of electricity, enough to power up to 750 homes.
> Like many other advanced nuclear startups, Antares’ reactor uses TRISO fuel, which encapsulates uranium in carbon and ceramic shells. TRISO has been touted for years as a safer alterna

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0228 -->
## 228. edge-0228

**Triple:** Vietnam Trade Promotion Agency (Vietrade) (GOV) —PART_OF→ Bộ Công Thương Việt Nam (GOV)
**Assertion status:** reported
**Evidence:**
> Việt Nam's Trade Promotion Agency (Vietrade) under the Ministry of Industry and Trade has signed a memorandum of understanding (MoU) with Meta Platforms to help Vietnamese businesses strengthen their use of digital tools for trade promotion and market expansion.

**Article:** [Trade promotion agency, Meta sign MoU to support Vietnamese SMEs’ digital capabilities](https://vietnamnews.vn/economy/1796686/trade-promotion-agency-meta-sign-mou-to-support-vietnamese-smes-digital-capabilities.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> HÀ NỘI — Việt Nam's Trade Promotion Agency (Vietrade) under the Ministry of Industry and Trade has signed a memorandum of understanding (MoU) with Meta Platforms to help Vietnamese businesses strengthen their use of digital tools for trade promotion and market expansion.
> The agreement was signed on Friday in Singapore by Vietrade Director General Vũ Bá Phú and Meta's Public Policy Director Sarim Aziz on the sidelines of the 10th ASEAN Conference themed "ASEAN's Future in a Fractured World" hosted by the Singapore Business Federation.
> Under the MoU, the two sides will cooperate on digital trade promotion, knowledge

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0229 -->
## 229. edge-0229

**Triple:** CMA CGM (ORG) —CO_INVESTED_WITH→ Conviction (ORG)
**Assertion status:** reported
**Evidence:**
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
> nd led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.
> Microsoft’s $16.3 million convertible investment in Mistral as part of a partnership announced in February 2024 was presented as a Series A extension, implying an unchanged valuation.
> In June 2024, Mistral raised €600 million (about $640 million) in a mix of equity and debt. The long-rumored round was led by General Catalyst at a $6 billion valuat

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0230 -->
## 230. edge-0230

**Triple:** BDC Capital (ORG) —INVESTED_IN→ General Fusion (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Now in its third decade, General Fusion has raised over $442 million, according to FusionX data. The Richmond, British Columbia-based company was founded in 2002 by physicist Michel Laberge, who wanted to prove a different approach to fusion known as magnetized target fusion (MTF). Investors include Jeff Bezos, Temasek, BDC Capital, and Chrysalix Venture Capital.

**Article:** [Every fusion startup that has raised over $100M](https://techcrunch.com/2026/08/15/every-fusion-startup-that-has-raised-over-100m/) | en | techcrunch.com
**Ngữ cảnh:**
> ns to use lasers to bombard fusion fuel pellets, an inertial confinement design that echoes the one Kritcher successfully used at the NIF. Inertia Enterprises emerged from stealth in February with $450 million in Series A funding in a round led by Bessemer Venture Partners with participation from GV, Modern Capital, Threshold Ventures, and others.
> Now in its third decade, General Fusion has raised over $442 million, according to FusionX data. The Richmond, British Columbia-based company was founded in 2002 by physicist Michel Laberge, who wanted to prove a different approach to fusion known as magnetized target fusion (MTF). Investors include Jeff Bezos, Temasek, BDC Capital, and Chrysalix Venture Capital.
> In General Fusion’s reactor, a liquid metal wall surrounds a chamber in which plasma is injected. Pistons surrounding the wall push it inward, compressing the plasma inside and sparking a fusion reaction. The resulting neutrons heat the liquid metal, which can be circulated through a heat exchanger to generate steam to spin a turbine.
> General Fusi

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0231 -->
## 231. edge-0231

**Triple:** Jabil Technology Vietnam (ORG) —INVESTED_IN→ Jabil Technology Vietnam factory in Dong Nai (PROJECT)
**Assertion status:** reported
**Evidence:**
> Dự án cũ tăng quy mô, những dự án mới cũng liên tục được khởi động. Có thể kể đến như Công ty TNHH Winner Medical (Việt Nam) đã khởi công Nhà máy sản xuất vật tư y tế Winner Medical Việt Nam tại Khu công nghiệp Texhong - Hải Hà (Quảng Ninh), có tổng vốn đầu tư tương đương hơn 60,5 triệu USD. Dự án do Công ty TNHH Nature Health Development International (trụ sở tại Hồng Kông, Trung Quốc) làm chủ đầu tư. Đây là doanh nghiệp thuộc Tập đoàn Winner Medical, là một trong những tập đoàn lớn trên thế giới chuyên nghiên cứu, phát triển, sản xuất và kinh doanh thiết bị, vật tư y tế. Hay dự án Nhà máy Công ty TNHH Jabil Technology Việt Nam (Singapore) tại TP.Đồng Nai, với vốn đầu tư 80 triệu USD… Kết quả của các dự án mới và mở rộng đã đưa tổng vốn đầu tư nước ngoài trực tiếp (FDI) đăng ký vào VN sau 8 tháng năm 2026 đạt 40,63 tỉ USD, tăng 55,4% so với cùng kỳ. Đáng chú ý, vốn giải ngân FDI thực hiện (17,25 tỉ USD) đạt mức cao nhất trong 5 năm. Trong khi đó, số dự án mới chỉ tăng 9,4% nhưng số vốn tăng gần gấp đôi, nghĩa là quy mô dự án đang lớn lên rõ rệt. Điều này cho thấy đằng sau con số kỷ lục không chỉ là những dự án mới, mà còn là xu hướng các nhà đầu tư quốc tế tái cấu trúc chuỗi cung ứng, đa dạng hóa địa điểm sản xuất và dịch chuyển một phần nguồn lực sang VN.

**Article:** [Vốn ngoại tìm đến Việt Nam 'làm tổ'](https://thanhnien.vn/von-ngoai-tim-den-viet-nam-lam-to-185260909213408303.htm) | vi | thanhnien.vn
**Ngữ cảnh:**
> ng tại nhiều tỉnh thành trên toàn quốc với đa dạng mô hình.
> "Ngay từ những ngày đầu bước chân vào VN, Aeon đã luôn tin tưởng vào tiềm năng to lớn của thị trường này và định vị đây là một khu vực cực kỳ quan trọng. Chúng tôi dự kiến sẽ ưu tiên phân bổ khoảng 60% ngân sách đầu tư của toàn khu vực ASEAN cho thị trường VN", ông Tezuka Daisuke chia sẻ.
> Dự án cũ tăng quy mô, những dự án mới cũng liên tục được khởi động. Có thể kể đến như Công ty TNHH Winner Medical (Việt Nam) đã khởi công Nhà máy sản xuất vật tư y tế Winner Medical Việt Nam tại Khu công nghiệp Texhong - Hải Hà (Quảng Ninh), có tổng vốn đầu tư tương đương hơn 60,5 triệu USD. Dự án do Công ty TNHH Nature Health Development International (trụ sở tại Hồng Kông, Trung Quốc) làm chủ đầu tư. Đây là doanh nghiệp thuộc Tập đoàn Winner Medical, là một trong những tập đoàn lớn trên thế giới chuyên nghiên cứu, phát triển, sản xuất và kinh doanh thiết bị, vật tư y tế. Hay dự án Nhà máy Công ty TNHH Jabil Technology Việt Nam (Singapore) tại TP.Đồng Nai, với vốn đầu tư 80 triệu USD… Kết quả của các dự án mới và mở rộng đã đưa tổng vốn đầu tư nước ngoài trực tiếp (FDI) đăng ký vào VN sau 8 tháng năm 2026 đạt 40,63 tỉ USD, tăng 55,4% so với cùng kỳ. Đáng chú ý, vốn giải ngân FDI thực hiện (17,25 tỉ USD) đạt mức cao nhất trong 5 năm. Trong khi đó, số dự án mới chỉ tăng 9,4% nhưng số vốn tăng gần gấp đôi, nghĩa là quy mô dự án đang lớn lên rõ rệt. Điều này cho thấy đằng sau con số kỷ lục không chỉ là những dự án mới, mà còn là xu hướng các nhà đầu tư quốc tế tái cấu trúc chuỗi cung ứng, đa dạng hóa địa điểm sản xuất và dịch chuyển một phần nguồn lực sang VN.
> Chúng ta vẫn còn nhiều việc phải làm và quan trọng nhất là cần thúc đẩy triển khai các chính sách cụ thể cho từng lĩnh vực ưu tiên. Từ đó các nhà đầu tư ngoại sẽ yên tâm và tiếp tục rót vốn vào VN.
> Nhìn vào những con số thu hút và giải ngân vốn FDI, chuyên gia kinh tế, PGS-TS Nguyễn Thường Lạng (Viện Nghiên cứu kinh tế và thương mại quốc tế) nhấn 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0232 -->
## 232. edge-0232

**Triple:** UnternehmerTUM (ORG) —CO_INVESTED_WITH→ IQ Capital (ORG)
**Assertion status:** reported
**Evidence:**
> A spinout from the Technical University of Munich (TUM), QuantumDiamonds has also raised a €15 million equity round led by VC firm World Fund, TechCrunch learned exclusively. The company declined to disclose its valuation, but said its round was also backed by Bayern Kapital and existing investors including Creator Fund, Earlybird, First Momentum, IQ Capital, Onsight Ventures, and UnternehmerTUM.

**Article:** [With EU backing, QuantumDiamonds aims to speed up chip manufacturing](https://techcrunch.com/2026/07/08/with-eu-backing-quantumdiamonds-aims-to-speed-up-chip-manufacturing/) | en | techcrunch.com
**Ngữ cảnh:**
> he approval of the European Commission, it has been granted €76 million in non-dilutive funding provided by Germany’s federal economy ministry and the state of Bavaria. The startup will use it to set up a new facility for the production of semiconductor testing equipment in Munich as part of a $178 million investment plan it had already announced.
> A spinout from the Technical University of Munich (TUM), QuantumDiamonds has also raised a €15 million equity round led by VC firm World Fund, TechCrunch learned exclusively. The company declined to disclose its valuation, but said its round was also backed by Bayern Kapital and existing investors including Creator Fund, Earlybird, First Momentum, IQ Capital, Onsight Ventures, and UnternehmerTUM.
> CEO Kevin Berghoff told TechCrunch that raising the round was a fairly quick process, as QuantumDiamonds was able to demonstrate customer pull. “We work with almost everyone in the chip ecosystem,” he said. With huge demand for all kinds of chips, there’s just as much demand for solutions to speed up the manufacturing process and improve the outpu

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0233 -->
## 233. edge-0233

**Triple:** JCDecaux Holding (ORG) —CO_INVESTED_WITH→ Exor Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> In June 2023, just one month after being founded, Mistral AI raised a record $113 million seed round led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
> rmy and job agency, Luxembourg, shipping giant CMA, German defense tech startup Helsing, IBM, Orange, and Stellantis.
> How much funding has Mistral AI raised to date?
> Most of Mistral AI’s funding to date was debt financing, but the company has also raised several venture funding rounds, with a grand total around $4 billion, according to Crunchbase.
> In June 2023, just one month after being founded, Mistral AI raised a record $113 million seed round led by Lightspeed Venture Partners. Sources at the time said the seed round, Europe’s largest ever, valued the startup at $260 million.
> Other investors in that round included Bpifrance, Eric Schmidt, Exor Ventures, Firstminute Capital, Headline, JCDecaux Holding, La Famiglia, LocalGlobe, Motier Ventures, Rodolphe Saadé, Sofina, and Xavier Niel.
> Six months later, Mistral closed a €385 million Series A ($415 million at the time), at a reported valuation of $2 billion. The round was led by Andreessen Horowitz (a16z) and saw participation from Lightspeed, as well as BNP Paribas, CMA CGM, Conviction, Elad Gil, General Catalyst, and Salesforce.
> Microsoft’s $16.3 million convertible investment 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0234 -->
## 234. edge-0234

**Triple:** Baruch Future Ventures (ORG) —INVESTED_IN→ Giraffe Bio (ORG)
**Assertion status:** reported
**Evidence:**
> To bring the technology out of the lab, Giraffe Bio recently raised a $6.4 million seed round led by Orion Industrial Ventures, with participation from BHP Ventures, Twynam, Air Capital, and Baruch Future Ventures, TechCrunch has exclusively learned.

**Article:** [Giraffe Bio aims its bespoke biomolecules at the looming copper shortage](https://techcrunch.com/2026/10/13/giraffe-bio-aims-its-bespoke-biomolecules-at-the-looming-copper-shortage/) | en | techcrunch.com
**Ngữ cảnh:**
> micals to help mines recover up to 5% more copper. In mining, that amount “is really very material,” Alejandro Buffo Sempé, co-founder and CEO of Giraffe Bio, told TechCrunch. Most would be happy with an additional 1% to 2%.
> The startup says it can extract more copper because it’s able to engineer compounds specific to each mine’s mineral content.
> To bring the technology out of the lab, Giraffe Bio recently raised a $6.4 million seed round led by Orion Industrial Ventures, with participation from BHP Ventures, Twynam, Air Capital, and Baruch Future Ventures, TechCrunch has exclusively learned.
> Rather than douse ores with bacteria thought to facilitate copper extraction, the company grows engineered microbes in a bioreactor to produce the bespoke compounds. Those chemicals are then inserted into a mine’s existing process.
> “We can leverage all of the biological machinery without having to deal with keeping alive a microbe, which is very c

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0235 -->
## 235. edge-0235

**Triple:** Ribbit Capital (ORG) —CO_INVESTED_WITH→ General Catalyst (ORG)
**Assertion status:** reported
**Evidence:**
> Cognition, the makers of the autonomous AI software engineer named Devin, has raised more than $1 billion at a $25 billion pre-money valuation ($26 billion post money), the company announced on Wednesday.
> That’s a major leap from its $10.2 billion post-money valuation when it closed a $400 million funding round just eight months ago in September.
> The round was led by Lux Capital, General Catalyst and 8VC, with a host of existing investors pouring in, including Elad Gil, Soma Capital, Omri Casspi, Founders Fund, and a long list of others. The round also included new investors like Ribbit Capital, Atreides, and Layer Global.

**Article:** [AI coding startup Cognition raises $1B at $25B pre-money valuation](https://techcrunch.com/2026/05/27/ai-coding-startup-cognition-raises-1b-at-25b-pre-money-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Cognition, the makers of the autonomous AI software engineer named Devin, has raised more than $1 billion at a $25 billion pre-money valuation ($26 billion post money), the company announced on Wednesday.
> That’s a major leap from its $10.2 billion post-money valuation when it closed a $400 million funding round just eight months ago in September.
> The round was led by Lux Capital, General Catalyst and 8VC, with a host of existing investors pouring in, including Elad Gil, Soma Capital, Omri Casspi, Founders Fund, and a long list of others. The round also included new investors like Ribbit Capital, Atreides, and Layer Global.
> This is a giant vote of confidence from top-tier VCs that there will be room for independent AI software coding startups. Last year, all signs pointed to model makers swallowing this hot market themselves. Certainly Anthropic’s Claude Code, OpenAI’s Codex, and maybe even Google’s coding agent Jules (after Google’s acqui-hire deal of Windsurf last 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0236 -->
## 236. edge-0236

**Triple:** United States Department of Justice (GOV) —ANTITRUST_ACTION_AGAINST→ Roku (ORG)
**Assertion status:** reported
**Evidence:**
> Fox has completed its $22 billion acquisition of Roku, wrapping up one of the biggest media deals in recent years and giving the company a major boost in the streaming and connected TV space.
> Announced Friday, the deal brings the streaming company founded in 2002 formally under Fox’s ownership. Fox says the combined company now ranks as the third-largest television business in the U.S. by viewership.
> “We started Roku more than two decades ago to give people a better way to watch TV, and that mission doesn’t change today. What does change is our reach and resources,” Roku founder Anthony Wood said in a statement. “Our teams will keep building and innovating as they always have, now with the support and capabilities of Fox behind us.”
> For Fox, the move provides direct access to Roku’s reach of more than 100 million households. The company expects that audience to help it improve advertising targeting, strengthen its position in the fast-growing connected TV market, and reduce its reliance on traditional TV distribution.
> Today’s announcement comes two months after the Justice Department issued a second request for information, asking both companies to provide additional data and documents as part of its antitrust review. Earlier this month, reports suggested the deal was nearing U.S. regulatory approval.

**Article:** [Fox completes its $22B acquisition of Roku](https://techcrunch.com/2026/11/06/fox-completes-its-22b-acquisition-of-roku/) | en | techcrunch.com
**Ngữ cảnh:**
> Fox has completed its $22 billion acquisition of Roku, wrapping up one of the biggest media deals in recent years and giving the company a major boost in the streaming and connected TV space.
> Announced Friday, the deal brings the streaming company founded in 2002 formally under Fox’s ownership. Fox says the combined company now ranks as the third-largest television business in the U.S. by viewership.
> “We started Roku more than two decades ago to give people a better way to watch TV, and that mission doesn’t change today. What does change is our reach and resources,” Roku founder Anthony Wood said in a statement. “Our teams will keep building and innovating as they always have, now with the support and capabilities of Fox behind us.”
> For Fox, the move provides direct access to Roku’s reach of more than 100 million households. The company expects that audience to help it improve advertising targeting, strengthen its position in the fast-growing connected TV market, and reduce its reliance on traditional TV distribution.
> Today’s announcement comes two months after the Justice Department issued a second request for information, asking both companies to provide additional data and documents as part of its antitrust review. Earlier this month, reports suggested the deal was nearing U.S. regulatory approval.
> The acquisition also closed much earlier than expected. When the deal was first announced in June, the companies projected it would be completed in the first half of 2027.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0237 -->
## 237. edge-0237

**Triple:** Max Hodak (PERSON) —FOUNDED→ Neuralink (ORG)
**Assertion status:** reported
**Evidence:**
> Then we closed out the year in early December in Palo Alto, where former Intel CEO Pat Gelsinger discussed government and religion, we got an inside look at one of the buzziest new companies in the AI manufacturing landscape, and Neuralink co-founder Max Hodak gave us a glimpse into the breathtaking ambition driving his current company, Science Corp.

**Article:** [No keynotes, no BS — why this year&#8217;s best tech talks happened over cocktails at StrictlyVC](https://techcrunch.com/2025/12/18/no-keynotes-no-bs-why-this-years-best-tech-talks-happened-over-cocktails-at-strictlyvc/) | en | techcrunch.com
**Ngữ cảnh:**
> itization of real-world assets is inevitable.
> StrictlyVC meets TechCrunch Disrupt
> At our TechCrunch Disrupt conference in San Francisco — where we hosted a mini StrictlyVC event inside the event — serial entrepreneur-turned-VC Kevin Hartz reflected on the rise of teen founders, and a killer panel of LPs dissected aging portfolios.
> Palo Alto finale
> Then we closed out the year in early December in Palo Alto, where former Intel CEO Pat Gelsinger discussed government and religion, we got an inside look at one of the buzziest new companies in the AI manufacturing landscape, and Neuralink co-founder Max Hodak gave us a glimpse into the breathtaking ambition driving his current company, Science Corp.
> From first conversations to future insights
> Yet these are just some of the highlights from 2025. The StrictlyVC series has been home to so many incredible voices over the years — former FTC chair Lina Khan, Waymo co-CEO Tekedra Mawakana, Meredith Whittaker of Signal, Sam Altman of OpenAI, Alfred Lin of Sequoia Capital, famed founder Marc Lore, and

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0238 -->
## 238. edge-0238

**Triple:** Baillie Gifford (ORG) —CO_INVESTED_WITH→ Lux Capital (ORG)
**Assertion status:** reported
**Evidence:**
> Defense tech Hadrian announced on Thursday that it had raised a fresh $1.37 billion round at a valuation of $7.87 billion from a mile-long list of well-known investors.
> The lead investors in the round include WCM Investment Management, Washington Harbour Partners, Valor Equity Partners, 137 Ventures, and Baillie Gifford. Participating investors include 1789 Capital, Morgan Stanley Wealth Management, funds managed by Apollo and T. Rowe Price, as well as firms like CapitalG, Andreessen Horowitz, Founders Fund, Lux Capital, Altimeter, and others.

**Article:** [Defense tech Hadrian raises $1.37B at $8B valuation](https://techcrunch.com/2026/08/06/defense-tech-hadrian-raises-1-37b-at-8b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Defense tech Hadrian announced on Thursday that it had raised a fresh $1.37 billion round at a valuation of $7.87 billion from a mile-long list of well-known investors.
> The lead investors in the round include WCM Investment Management, Washington Harbour Partners, Valor Equity Partners, 137 Ventures, and Baillie Gifford. Participating investors include 1789 Capital, Morgan Stanley Wealth Management, funds managed by Apollo and T. Rowe Price, as well as firms like CapitalG, Andreessen Horowitz, Founders Fund, Lux Capital, Altimeter, and others.
> Founders Fund and Lux led the company’s $260 million Series C financing about a year ago, bringing the total raised to date to around $2 billion, according to PitchBook estimates.
> Hadrian is an interesting defense tech in that it’s not trying to build new AI-powered weapons. The company is building automated manufacturing facilities that will mass

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0239 -->
## 239. edge-0239

**Triple:** Pegasus Capital (ORG) —CO_INVESTED_WITH→ TTGG Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> To get there, Evotrex has closed a $30 million Series A funding round, bringing its total raised to $46 million. Much of that came from a consortium of Chinese and Hong Kong-based investment firms, like GSR United Capital, Forebright Concerto Capital, TTGG Ventures, and Pegasus Capital, among others. Anker, the consumer electronics company, is among its seed investors.

**Article:** [Evotrex raises $30M to build the RV that doesn&#8217;t need a charging station](https://techcrunch.com/2026/06/09/anker-backed-evotrex-raises-30m-to-build-its-off-grid-rv/) | en | techcrunch.com
**Ngữ cảnh:**
> Evotrex has been around for just two years, but the startup is already planning to build and sell its first hybrid RV travel trailers next year, targeting around 1,000 units annually.
> To get there, Evotrex has closed a $30 million Series A funding round, bringing its total raised to $46 million. Much of that came from a consortium of Chinese and Hong Kong-based investment firms, like GSR United Capital, Forebright Concerto Capital, TTGG Ventures, and Pegasus Capital, among others. Anker, the consumer electronics company, is among its seed investors.
> The LA-based startup will need that capital to finish building and testing its RV, which it revealed at this year’s Consumer Electronics Show after emerging from stealth mode last year.
> It will also need it to hold its ground in a crowded field of startups. Legacy manufacturers have been slow to get going. Thor’s first electric vehicle is going to

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0240 -->
## 240. edge-0240

**Triple:** Andrew Dumont (PERSON) —FOUNDED→ Curious (ORG)
**Assertion status:** reported
**Evidence:**
> Andrew Dumont, the founder and CEO of Curious, a firm that also acquires and revitalizes what he calls “venture zombies,” is convinced this “hold forever” strategy will become increasingly prominent in the coming years as AI-native startups make older VC-backed software businesses less relevant.

**Article:** [Why &#8216;hold forever&#8217; investors are snapping up venture capital &#8216;zombies&#8217;](https://techcrunch.com/2025/11/25/why-hold-forever-investors-are-snapping-up-venture-capital-zombies/) | en | techcrunch.com
**Ngữ cảnh:**
> ion set in early 2024.
> Bending Spoons has grown rapidly by acquiring stagnating tech brands like Evernote, Meetup, and Vimeo, then turning them profitable through aggressive cost-cutting and price increases. While the company’s approach is similar to private equity, there is one key difference: Bending Spoons has no plans to sell these businesses.
> Andrew Dumont, the founder and CEO of Curious, a firm that also acquires and revitalizes what he calls “venture zombies,” is convinced this “hold forever” strategy will become increasingly prominent in the coming years as AI-native startups make older VC-backed software businesses less relevant.
> “Our belief is that the venture power law, in which 80% of companies ‘fail,’ produces many great businesses, even if they’re not unicorns,” Dumont told TechCrunch.
> Dumont defines a “great business” as one that can be purchased at a low price and quickly revived to generate substantial cash flows. This “buy, fix, and hold” strategy is the playbook 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0241 -->
## 241. edge-0241

**Triple:** Ardor Green (ORG) —PART_OF→ TT Genesis residential project (PROJECT)
**Assertion status:** reported
**Evidence:**
> Ardor Green tham gia thiết kế bền vững và tư vấn công trình xanh.

**Article:** [Liên doanh Nhật cùng loạt đối tác phát triển dự án 6.000 tỷ đồng](https://vnexpress.net/lien-doanh-nhat-cung-loat-doi-tac-phat-trien-du-an-6-000-ty-dong-5108727.html) | vi | vnexpress.net
**Ngữ cảnh:**
> t triển dự án tiếp tục công bố các đối tác tham gia gồm Ricons, TWOG, Vertical Studio, VPBank, CBRE và Ardor Green. Trong đó, Ricons đảm nhận vai trò tổng thầu xây dựng. TWOG thiết kế kiến trúc, cảnh quan và nội thất, trong khi Vertical Studio tư vấn thiết kế.
> Ở nhóm tài chính và vận hành, VPBank là ngân hàng tài trợ, CBRE tư vấn quản lý vận hành. Ardor Green tham gia thiết kế bền vững và tư vấn công trình xanh.
> Theo ông Kihara Takashi, đại diện Hinokiya Group, việc hợp tác với các đối tác nhằm xây dựng hệ thống triển khai dự án, đồng thời đáp ứng các yêu cầu về chất lượng, tiến độ và định hướng phát triển bền vững.
> Bên cạnh các đơn vị xây dựng, thiết kế và vận hành, liên doanh cũng thiết lập mạng lưới phân phối gồm 10 đối tác chiến lược: T&A, IQI Việt Na

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0242 -->
## 242. edge-0242

**Triple:** 8VC (ORG) —CO_INVESTED_WITH→ Andreessen Horowitz (ORG)
**Assertion status:** reported
**Evidence:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.

**Article:** [Kevin Mandia&#8217;s new &#8216;agent swarm&#8217; security startup Armadin raises $255.5M at $2.5B valuation](https://techcrunch.com/2026/10/01/kevin-mandias-new-agent-swarm-security-startup-armadin-raises-255-5m-at-2-5b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Kevin Mandia, best known as the founder of cybersecurity startup Mandiant, which sold to Google for $5.4 billion in 2022, has raised $255.5 million for his latest startup, Armadin, at a valuation of more than $2.5 billion, the company announced on Thursday.
> The Series B round was led by Andreessen Horowitz and Accel, with Bain Capital Ventures, Redpoint, 8VC, Ballistic Ventures, Google Ventures, In-Q-Tel, Kleiner Perkins, and Menlo Ventures joining in.
> The new round comes just six months after Armadin raised a $190 million Series A in March. It has now raised more than $445 million.
> Armadin is offering enterprises a new kind of always-on security by reimagining defense testing for the AI era. Instead of traditional penetration tests, where hired guns attempt to break in and report on the weaknes

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0243 -->
## 243. edge-0243

**Triple:** Deutsche Telekom (ORG) —CO_INVESTED_WITH→ Hwang Dong-hyuk (PERSON)
**Assertion status:** reported
**Evidence:**
> Voice AI company ElevenLabs revealed new investors that are part of its $500 million Series D fundraise, which was first announced in February. The additions include institutions such as BlackRock, Wellington, D.E. Shaw, and Schroders; enterprises like Nvidia, Salesforce Ventures, Santander, KPN, and Deutsche Telekom; and individual investors such as Jamie Foxx, Eva Longoria, and Squid Game creator Hwang Dong-hyuk.

**Article:** [ElevenLabs lists BlackRock, Jamie Foxx, and Eva Longoria as new investors](https://techcrunch.com/2026/05/05/elevenlabs-lists-blackrock-jamie-foxx-and-eva-longoria-as-new-investors/) | en | techcrunch.com
**Ngữ cảnh:**
> Voice AI company ElevenLabs revealed new investors that are part of its $500 million Series D fundraise, which was first announced in February. The additions include institutions such as BlackRock, Wellington, D.E. Shaw, and Schroders; enterprises like Nvidia, Salesforce Ventures, Santander, KPN, and Deutsche Telekom; and individual investors such as Jamie Foxx, Eva Longoria, and Squid Game creator Hwang Dong-hyuk.
> The startup also noted that it surpassed $500 million in ARR (annual recurring revenue), after ending last year with nearly $350 million in ARR. The company’s co-founder and CEO, Mati Staniszewski, said last month that ElevenLabs added $100 million in net new ARR in Q1 2026, ending the quarter at roughly $450 million in ARR.
> The company has also a

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0244 -->
## 244. edge-0244

**Triple:** Lachy Groom (PERSON) —CO_INVESTED_WITH→ Greenoaks (ORG)
**Assertion status:** reported
**Evidence:**
> Airbound, an Indian startup building autonomous drones, has raised $37 million in fresh capital as it pushes to make moving goods through the air as cheap as trucking them by road.
> The Series A round, led by Greenoaks with participation from DoorDash, Lachy Groom, Lightspeed, and Humba Ventures, comes less than a year after Airbound raised an $8.65 million seed round. With this funding, the three-year-old startup has raised nearly $50 million.

**Article:** [India&#8217;s Airbound bags $37M to take on trucks with rocket-like drones](https://techcrunch.com/2026/08/24/indias-airbound-bags-37m-to-take-on-trucks-with-rocket-like-drones/) | en | techcrunch.com
**Ngữ cảnh:**
> Airbound, an Indian startup building autonomous drones, has raised $37 million in fresh capital as it pushes to make moving goods through the air as cheap as trucking them by road.
> The Series A round, led by Greenoaks with participation from DoorDash, Lachy Groom, Lightspeed, and Humba Ventures, comes less than a year after Airbound raised an $8.65 million seed round. With this funding, the three-year-old startup has raised nearly $50 million.
> Airbound and other startups in this nascent sector argue that drones can move certain goods faster and cheaper than vehicles on the road. And while there have been successful deployments, drone delivery is still far from matching the scale and versatility of trucking.
> Airbound is trying to close that gap by redesigning the aircraft to make it more

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0245 -->
## 245. edge-0245

**Triple:** Proparco (ORG) —CO_FINANCED_WITH→ Woori Bank (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> Tham gia giao dịch còn có các định chế tài chính phát triển gồm IFC, DEG (Đức), Proparco (Pháp) và Norfund (Na Uy); các ngân hàng xuất nhập khẩu China Eximbank, Korea Eximbank cùng nhóm ngân hàng thương mại và tổ chức tài chính như SMBC, Punjab National Bank, Commercial Bank of Ceylon, ICBC, Shinhan Bank, Woori Bank và KEXIM Asia Limited.

**Article:** [VPBank huy động 730 triệu USD vốn quốc tế](https://vnexpress.net/vpbank-huy-dong-730-trieu-usd-von-quoc-te-5143246.html) | vi | vnexpress.net
**Ngữ cảnh:**
> y động thành công khoản vay hợp vốn quốc tế 730 triệu USD, tương đương gần 19.000 tỷ đồng, do IFC và SMBC thu xếp, ngày 10/11.
> Giao dịch do Tổ chức Tài chính Quốc tế (IFC) và Ngân hàng Sumitomo Mitsui Banking Corporation (SMBC) đồng điều phối, thu xếp, gồm các khoản vay có kỳ hạn 3 năm, 5 năm và 7 năm, được giải ngân theo nhiều đợt trong năm 2026.
> Tham gia giao dịch còn có các định chế tài chính phát triển gồm IFC, DEG (Đức), Proparco (Pháp) và Norfund (Na Uy); các ngân hàng xuất nhập khẩu China Eximbank, Korea Eximbank cùng nhóm ngân hàng thương mại và tổ chức tài chính như SMBC, Punjab National Bank, Commercial Bank of Ceylon, ICBC, Shinhan Bank, Woori Bank và KEXIM Asia Limited. Sự tham gia của các tổ chức đến từ nhiều quốc gia giúp VPBank đa dạng hóa đối tác và mở rộng khả năng tiếp cận thị trường vốn quốc tế.
> Theo VPBank, nguồn vốn này sẽ được sử dụng để mở rộng tín dụng cho doanh nghiệp vừa và nhỏ (SME), đặc biệt là doanh nghiệp do phụ nữ làm chủ hoặc lãnh đạo (WSME) và doanh nghiệp hoạt động trong lĩnh vực nông nghiệp

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0246 -->
## 246. edge-0246

**Triple:** Emergence Capital (ORG) —CO_INVESTED_WITH→ S Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> The round was led by Aramco Ventures, with participation from Vista Equity Partners, General Catalyst, Emergence Capital, Nvidia, March Capital, Pegatron, SentinelOne’s S Ventures, and others.

**Article:** [Neocloud Together AI raises $800M, leaps to $8.3B valuation](https://techcrunch.com/2026/07/01/neocloud-together-ai-raises-800m-leaps-to-8-3b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Together AI — an AI neocloud that rents out Nvidia GPU clusters and other AI-specific infrastructure — has raised an $800 million Series C at an $8.3 billion valuation, the company announced on Wednesday. The company was founded in 2022.
> The round was led by Aramco Ventures, with participation from Vista Equity Partners, General Catalyst, Emergence Capital, Nvidia, March Capital, Pegatron, SentinelOne’s S Ventures, and others.
> Together AI last raised a $305 million Series B at a $3.3 billion valuation about 16 months ago. It actually came out of the gate well-funded, with a $102.5 million Series A funding round led by Kleiner Perkins with participation from Nvidia and Emergence Capital back in 2023.
> There were whispers of this round back in March, when The Information r

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0247 -->
## 247. edge-0247

**Triple:** Eva Longoria (PERSON) —INVESTED_IN→ ElevenLabs (ORG)
**Assertion status:** reported
**Evidence:**
> Voice AI company ElevenLabs revealed new investors that are part of its $500 million Series D fundraise, which was first announced in February. The additions include institutions such as BlackRock, Wellington, D.E. Shaw, and Schroders; enterprises like Nvidia, Salesforce Ventures, Santander, KPN, and Deutsche Telekom; and individual investors such as Jamie Foxx, Eva Longoria, and Squid Game creator Hwang Dong-hyuk.

**Article:** [ElevenLabs lists BlackRock, Jamie Foxx, and Eva Longoria as new investors](https://techcrunch.com/2026/05/05/elevenlabs-lists-blackrock-jamie-foxx-and-eva-longoria-as-new-investors/) | en | techcrunch.com
**Ngữ cảnh:**
> Voice AI company ElevenLabs revealed new investors that are part of its $500 million Series D fundraise, which was first announced in February. The additions include institutions such as BlackRock, Wellington, D.E. Shaw, and Schroders; enterprises like Nvidia, Salesforce Ventures, Santander, KPN, and Deutsche Telekom; and individual investors such as Jamie Foxx, Eva Longoria, and Squid Game creator Hwang Dong-hyuk.
> The startup also noted that it surpassed $500 million in ARR (annual recurring revenue), after ending last year with nearly $350 million in ARR. The company’s co-founder and CEO, Mati Staniszewski, said last month that ElevenLabs added $100 million in net new ARR in Q1 2026, ending the quarter at roughly $450 million in ARR.
> The company has also a

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0248 -->
## 248. edge-0248

**Triple:** Starwood Capital (ORG) —CO_INVESTED_WITH→ Bain Capital (ORG)
**Assertion status:** reported
**Evidence:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.

**Article:** [Legora reaches $5.55 billion valuation as AI legal tech boom endures](https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/) | en | techcrunch.com
**Ngữ cảnh:**
> Legora, an AI platform for lawyers, is now valued at $5.55 billion following a $550 million Series D set to fuel its growth in the U.S. That’s despite growing competition with rival Harvey, but also with Microsoft Copilot and generalist large language models (LLMs). Publicly listed legal software companies saw their stocks drop when Anthropic unveiled a legal plug-in for Claude.
> Legora is built on top of LLMs, and mostly on Claude, but its positioning as a platform that supports lawyers with complex cases gives CEO Max Junestrand some peace of mind. “It’s amazing that everybody can have their own pocket lawyer in Claude, but we’re not solving for the same use case,” he said via livestream at the TechArena conference in Stockholm.
> With a focus on embedding itself into its clients’ workflows, Legora’s platform is now used by 800 law firms and legal teams — and investors took note. Its Series D was led by Accel, with participation from existing investors Benchmark, Bessemer, General Catalyst, ICONIQ, Redpoint Ventures, and Y Combinator; and new backers including Alkeon Capital, Bain Capital, Firstmark Capital, Menlo Ventures, Salesforce Ventures, Sands Capital, and Starwood Capital.
> There are other signs that investors are bullish about AI legal tech. Legora’s Series D and valuation jump come just a few months after its October 2025 $150 million Series C round led at a $1.8 billion valuation. Its competitor, Harvey, which is backed by a16z, is already valued at $8 billion, and is now reportedly seeking to raise at an $11 bill

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0249 -->
## 249. edge-0249

**Triple:** D1 Capital Partners (ORG) —INVESTED_IN→ Groq (ORG)
**Assertion status:** reported
**Evidence:**
> AI chip startup Groq confirmed Wednesday that it raised a fresh $750 million in funding at a post-money valuation of $6.9 billion.
> This topped the rumored numbers when word leaked in July that Groq was raising. At that time, reports suggested that the raise would be about $600 million, at near a $6 billion valuation.
> Groq, which also sells data center computing power, previously raised $640 million at a $2.8 billion valuation in August 2024, making this more than double the valuation in about a year. Groq has now raised over $3 billion to date, PitchBook estimates.
> Groq has been a hot commodity because it is working on breaking the chokehold that AI chip maker Nvidia has over the tech industry. Groq’s chips are not GPUs, the graphics processing units that typically power AI systems. Instead, Groq calls them LPUs (language processing units) and calls its hardware an inference engine — specialized computers optimized for running AI models quickly and efficiently.
> Its products are geared toward developers and enterprises, available as either a cloud service or an on-premises hardware cluster. The on-prem hardware is a server rack outfitted with a stack of its integrated hardware/software nodes. Both the cloud and on-prem hardware run open versions of popular models, like those from Meta, DeepSeek, Qwen, Mistral, Google, and OpenAI. Groq says its offerings maintain, or in some cases improve, AI performance at significantly less cost than alternatives.
> Groq’s founder, Jonathan Ross, has a particularly relevant pedigree for this work. Ross previously worked at Google developing its Tensor Processing Unit chip, which are specialized processors designed for machine learning tasks. The TPU was announced in 2016, the same year Groq emerged from stealth. TPUs still power Google Cloud’s AI services.
> Groq says it now powers the AI apps of more than 2 million developers, up from 356,000 developers when the company talked to TechCrunch a year ago.
> The new round was led by investment firm Disruptive, with additional funding from BlackRock, Neuberger Berman, Deutsche Telekom Capital Partners, and others. Existing investors, including Samsung, Cisco, D1, and Altimeter, also joined the round.

**Article:** [Nvidia AI chip challenger Groq raises even more than expected, hits $6.9B valuation](https://techcrunch.com/2025/09/17/nvidia-ai-chip-challenger-groq-raises-even-more-than-expected-hits-6-9b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> AI chip startup Groq confirmed Wednesday that it raised a fresh $750 million in funding at a post-money valuation of $6.9 billion.
> This topped the rumored numbers when word leaked in July that Groq was raising. At that time, reports suggested that the raise would be about $600 million, at near a $6 billion valuation.
> Groq, which also sells data center computing power, previously raised $640 million at a $2.8 billion valuation in August 2024, making this more than double the valuation in about a year. Groq has now raised over $3 billion to date, PitchBook estimates.
> Groq has been a hot commodity because it is working on breaking the chokehold that AI chip maker Nvidia has over the tech industry. Groq’s chips are not GPUs, the graphics processing units that typically power AI systems. Instead, Groq calls them LPUs (language processing units) and calls its hardware an inference engine — specialized computers optimized for running AI models quickly and efficiently.
> Its products are geared toward developers and enterprises, available as either a cloud service or an on-premises hardware cluster. The on-prem hardware is a server rack outfitted with a stack of its integrated hardware/software nodes. Both the cloud and on-prem hardware run open versions of popular models, like those from Meta, DeepSeek, Qwen, Mistral, Google, and OpenAI. Groq says its offerings maintain, or in some cases improve, AI performance at significantly less cost than alternatives.
> Groq’s founder, Jonathan Ross, has a particularly relevant pedigree for this work. Ross previously worked at Google developing its Tensor Processing Unit chip, which are specialized processors designed for machine learning tasks. The TPU was announced in 2016, the same year Groq emerged from stealth. TPUs still power Google Cloud’s AI services.
> Groq says it now powers the AI apps of more than 2 million developers, up from 356,000 developers when the company talked to TechCrunch a year ago.
> The new round was led by investment firm Disruptive, with additional funding from BlackRock, Neuberger Berman, Deutsche Telekom Capital Partners, and others. Existing investors, including Samsung, Cisco, D1, and Altimeter, also joined the round.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0250 -->
## 250. edge-0250

**Triple:** Pegatron (ORG) —INVESTED_IN→ Together AI (ORG)
**Assertion status:** reported
**Evidence:**
> The round was led by Aramco Ventures, with participation from Vista Equity Partners, General Catalyst, Emergence Capital, Nvidia, March Capital, Pegatron, SentinelOne’s S Ventures, and others.

**Article:** [Neocloud Together AI raises $800M, leaps to $8.3B valuation](https://techcrunch.com/2026/07/01/neocloud-together-ai-raises-800m-leaps-to-8-3b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Together AI — an AI neocloud that rents out Nvidia GPU clusters and other AI-specific infrastructure — has raised an $800 million Series C at an $8.3 billion valuation, the company announced on Wednesday. The company was founded in 2022.
> The round was led by Aramco Ventures, with participation from Vista Equity Partners, General Catalyst, Emergence Capital, Nvidia, March Capital, Pegatron, SentinelOne’s S Ventures, and others.
> Together AI last raised a $305 million Series B at a $3.3 billion valuation about 16 months ago. It actually came out of the gate well-funded, with a $102.5 million Series A funding round led by Kleiner Perkins with participation from Nvidia and Emergence Capital back in 2023.
> There were whispers of this round back in March, when The Information r

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0251 -->
## 251. edge-0251

**Triple:** 137 Ventures (ORG) —CO_INVESTED_WITH→ CapitalG (ORG)
**Assertion status:** reported
**Evidence:**
> Defense tech Hadrian announced on Thursday that it had raised a fresh $1.37 billion round at a valuation of $7.87 billion from a mile-long list of well-known investors.
> The lead investors in the round include WCM Investment Management, Washington Harbour Partners, Valor Equity Partners, 137 Ventures, and Baillie Gifford. Participating investors include 1789 Capital, Morgan Stanley Wealth Management, funds managed by Apollo and T. Rowe Price, as well as firms like CapitalG, Andreessen Horowitz, Founders Fund, Lux Capital, Altimeter, and others.

**Article:** [Defense tech Hadrian raises $1.37B at $8B valuation](https://techcrunch.com/2026/08/06/defense-tech-hadrian-raises-1-37b-at-8b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Defense tech Hadrian announced on Thursday that it had raised a fresh $1.37 billion round at a valuation of $7.87 billion from a mile-long list of well-known investors.
> The lead investors in the round include WCM Investment Management, Washington Harbour Partners, Valor Equity Partners, 137 Ventures, and Baillie Gifford. Participating investors include 1789 Capital, Morgan Stanley Wealth Management, funds managed by Apollo and T. Rowe Price, as well as firms like CapitalG, Andreessen Horowitz, Founders Fund, Lux Capital, Altimeter, and others.
> Founders Fund and Lux led the company’s $260 million Series C financing about a year ago, bringing the total raised to date to around $2 billion, according to PitchBook estimates.
> Hadrian is an interesting defense tech in that it’s not trying to build new AI-powered weapons. The company is building automated manufacturing facilities that will mass

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0252 -->
## 252. edge-0252

**Triple:** Fidelity Management & Research Company (ORG) —INVESTED_IN→ Anthropic (ORG)
**Assertion status:** reported
**Evidence:**
> If finalized, the deal would nearly triple Anthropic’s valuation, which was $61.5 billion after a $3.5 billion funding round led by Lightspeed Venture Partners announced in March. Other participants in the startup’s last round included Bessemer Venture Partners, Cisco Investments, D1 Capital Partners, Fidelity Management & Research Company, General Catalyst, Jane Street, Menlo Ventures, and Salesforce Ventures.

**Article:** [Anthropic reportedly nears $170B valuation with potential $5B round](https://techcrunch.com/2025/07/29/anthropic-reportedly-nears-170b-valuation-with-potential-5b-round/) | en | techcrunch.com
**Ngữ cảnh:**
> llion in funding, valuing the large language model developer at $170 billion, Bloomberg reported.
> Iconiq Capital is leading this funding round, but there’s a possibility of a second lead investor joining the deal. The company has also been in talks with Qatar Investment Authority and GIC, Singapore’s sovereign wealth fund, according to the report.
> If finalized, the deal would nearly triple Anthropic’s valuation, which was $61.5 billion after a $3.5 billion funding round led by Lightspeed Venture Partners announced in March. Other participants in the startup’s last round included Bessemer Venture Partners, Cisco Investments, D1 Capital Partners, Fidelity Management & Research Company, General Catalyst, Jane Street, Menlo Ventures, and Salesforce Ventures.
> Despite Anthropic’s mission as a safety-conscious AI model developer, the company’s CEO, Dario Amodei, recently confessed in a memo to employees, reported by Wired, that he’s “not thrilled” about taking money from sovereign wealth funds of dictatorial governments.
> To keep pace with the massive capital requirements of developing AI models, the comp

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0253 -->
## 253. edge-0253

**Triple:** Index Ventures (ORG) —CO_INVESTED_WITH→ Redpoint Ventures (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.

**Article:** [Glow emerges from stealth at $1.2B valuation to challenge endpoint security in the AI era](https://techcrunch.com/2026/07/22/glow-emerges-from-stealth-at-1-2b-valuation-to-challenge-endpoint-security-in-the-ai-era/) | en | techcrunch.com
**Ngữ cảnh:**
> Glow, a cybersecurity startup founded by former Meta and Snowflake executives, emerged from stealth as a unicorn, betting that artificial intelligence is reshaping how enterprises secure employee devices.
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.
> As more enterprises deploy AI tools and attackers increasingly use generative AI to automate phishing, develop malware, and launch more sophisticated cyberattacks, companies are rethinking how they secure endpoints — from employee laptops to servers and other connected devices. Concerns have intensified since Anthropic unveiled its Mythos AI model

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0254 -->
## 254. edge-0254

**Triple:** Fidelity Management & Research Company (ORG) —CO_INVESTED_WITH→ Lightspeed Venture Partners (ORG)
**Assertion status:** reported
**Evidence:**
> If finalized, the deal would nearly triple Anthropic’s valuation, which was $61.5 billion after a $3.5 billion funding round led by Lightspeed Venture Partners announced in March. Other participants in the startup’s last round included Bessemer Venture Partners, Cisco Investments, D1 Capital Partners, Fidelity Management & Research Company, General Catalyst, Jane Street, Menlo Ventures, and Salesforce Ventures.

**Article:** [Anthropic reportedly nears $170B valuation with potential $5B round](https://techcrunch.com/2025/07/29/anthropic-reportedly-nears-170b-valuation-with-potential-5b-round/) | en | techcrunch.com
**Ngữ cảnh:**
> llion in funding, valuing the large language model developer at $170 billion, Bloomberg reported.
> Iconiq Capital is leading this funding round, but there’s a possibility of a second lead investor joining the deal. The company has also been in talks with Qatar Investment Authority and GIC, Singapore’s sovereign wealth fund, according to the report.
> If finalized, the deal would nearly triple Anthropic’s valuation, which was $61.5 billion after a $3.5 billion funding round led by Lightspeed Venture Partners announced in March. Other participants in the startup’s last round included Bessemer Venture Partners, Cisco Investments, D1 Capital Partners, Fidelity Management & Research Company, General Catalyst, Jane Street, Menlo Ventures, and Salesforce Ventures.
> Despite Anthropic’s mission as a safety-conscious AI model developer, the company’s CEO, Dario Amodei, recently confessed in a memo to employees, reported by Wired, that he’s “not thrilled” about taking money from sovereign wealth funds of dictatorial governments.
> To keep pace with the massive capital requirements of developing AI models, the comp

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0255 -->
## 255. edge-0255

**Triple:** Ashwin Bhatnagar (PERSON) —FOUNDED→ Xflow (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Balaji, who previously helped build out Stripe’s India business, founded Xflow with former Stripe colleagues Ashwin Bhatnagar (pictured above, right) and Abhijit Chandrasekaran (pictured above, left).

**Article:** [Stripe, PayPal Ventures bet on India&#8217;s Xflow to fix cross-border B2B payments](https://techcrunch.com/2026/02/23/stripe-paypal-ventures-bet-on-indias-xflow-to-fix-cross-border-b2b-payments/) | en | techcrunch.com
**Ngữ cảnh:**
> s, enabling them to collect international payments, manage foreign exchange, and settle funds in India.
> “Cross-border B2B payments were stuck in a different age compared to UPI,” co-founder Anand Balaji (pictured above, center) said in an interview, referring to India’s widely used instant domestic payments network, the Unified Payments Interface.
> Balaji, who previously helped build out Stripe’s India business, founded Xflow with former Stripe colleagues Ashwin Bhatnagar (pictured above, right) and Abhijit Chandrasekaran (pictured above, left).
> Last year, Xflow said it enabled Indian businesses to collect payments from more than 100 countries in over 25 currencies. It processed close to $1 billion in annualized cross-border payment volume last year, marking roughly tenfold growth from the same period in 2024, Balaji told TechCrunch.
> According to the company, its customer base has expande

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0256 -->
## 256. edge-0256

**Triple:** Initialized Capital (ORG) —CO_INVESTED_WITH→ Toyota Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> “We’re hitting this inflection point of AI and the electrification of nearly every industry, and it’s creating this point where we have overburdened and overstressed the energy grid,” Amir Mashal, founder and CEO of Arcturus, told TechCrunch.
> One option is to throw more metal at the problem, but Mashal said his startup, which has been operating in stealth, offers an alternative. Arcturus can reduce the amount of energy that electrical conductors lose to heat by infusing carbon nanomaterials into copper and aluminum using lasers. Replacing traditional metal with Arcturus’s material would allow the same size power lines to carry more electricity.
> In practical terms, that could cut losses on the electrical grid in half, which would immediately unlock around 3% more electricity on average and up to 10% more during the most congested times, when the grid arguably needs it most. At the low end, that’s about a year’s worth of demand growth in the U.S.
> “Copper loses conductivity as it heats up, so the hotter it gets, the more energy it wastes as heat,” Mashal said. “As I kept peeling back the layers of that onion, everything kind of started clicking to me because I noticed the same limit shows up everywhere. The modern world really runs on metals.”
> While the grid is the ultimate destination for a materials startup like Arcturus, the company is starting smaller with drones, robotics, and, yes, data centers, where a few percentage points more electricity can have an outsized impact.
> The company exclusively told TechCrunch that it raised $8 million in a seed round led by Initialized Capital with participation from Toyota Ventures, Breakthrough Energy Discovery, 1517, and Wireframe Ventures.

**Article:** [Arcturus could halve the grid’s electrical losses using its nano-infused metals](https://techcrunch.com/2026/06/30/arcturus-could-halve-the-grids-electrical-losses-using-its-nano-infused-copper/) | en | techcrunch.com
**Ngữ cảnh:**
> ses a lot of copper, but thanks to the energy transition and data centers, it’ll need a lot more. Between now and 2050, we’ll have to produce more copper than has been mined throughout all of human history, according to one study.
> Plenty of that copper — and even more aluminum — ends up in the electrical grid, which in the U.S. is showing its age.
> “We’re hitting this inflection point of AI and the electrification of nearly every industry, and it’s creating this point where we have overburdened and overstressed the energy grid,” Amir Mashal, founder and CEO of Arcturus, told TechCrunch.
> One option is to throw more metal at the problem, but Mashal said his startup, which has been operating in stealth, offers an alternative. Arcturus can reduce the amount of energy that electrical conductors lose to heat by infusing carbon nanomaterials into copper and aluminum using lasers. Replacing traditional metal with Arcturus’s material would allow the same size power lines to carry more electricity.
> In practical terms, that could cut losses on the electrical grid in half, which would immediately unlock around 3% more electricity on average and up to 10% more during the most congested times, when the grid arguably needs it most. At the low end, that’s about a year’s worth of demand growth in the U.S.
> “Copper loses conductivity as it heats up, so the hotter it gets, the more energy it wastes as heat,” Mashal said. “As I kept peeling back the layers of that onion, everything kind of started clicking to me because I noticed the same limit shows up everywhere. The modern world really runs on metals.”
> While the grid is the ultimate destination for a materials startup like Arcturus, the company is starting smaller with drones, robotics, and, yes, data centers, where a few percentage points more electricity can have an outsized impact.
> The company exclusively told TechCrunch that it raised $8 million in a seed round led by Initialized Capital with participation from Toyota Ventures, Breakthrough Energy Discovery, 1517, and Wireframe Ventures.
> Mashal has been quietly refining his materials in a garage in Malibu, California, where he’s currently able to produce several centimeters of wire as a proof of concept. With the new funding, he plans to ramp up to tens of meters so that the nano-infused materials can be tested in various applications, including windings in electric motors and bus

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0257 -->
## 257. edge-0257

**Triple:** World Trade Centre Mumbai (WTC Mumbai) (ORG) —PARTNERED_WITH→ HGI Investment (ORG)
**Assertion status:** reported
**Evidence:**
> Participants also spent time on networking and B2B meetings. Việt Nam's HGI Investment and WTC Mumbai signed an MoU, adding a further basis for follow-up on business connectivity. — VNA/VNS

**Article:** [Việt Nam, India move to deepen business, e-commerce connectivity](https://vietnamnews.vn/economy/1800996/viet-nam-india-move-to-deepen-business-e-commerce-connectivity.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> any products win access to the other's market, he said.
> Alongside in-person missions, the initiative will create a regular channel for sharing business opportunities, including importer and distributor demand, supply sources, technology partners and investment projects. The goal is to keep contacts active year-round rather than only around events.
> Participants also spent time on networking and B2B meetings. Việt Nam's HGI Investment and WTC Mumbai signed an MoU, adding a further basis for follow-up on business connectivity. — VNA/VNS

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0258 -->
## 258. edge-0258

**Triple:** Maybank Securities (ORG) —CO_FINANCED_WITH→ HSBC (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).

**Article:** [VPBank and 15 international financial institutions sign maiden US$1.44 billion sustainability-linked syndicated loan facility](https://vietnamnews.vn/economy/1784501/vpbank-and-15-international-financial-institutions-sign-maiden-us-1-44-billion-sustainability-linked-syndicated-loan-facility.html) | en | vietnamnews.vn
**Ngữ cảnh:**
>  strategic partnership between VPBank and SMBC, while enhancing VPBank’s standing in regional and international financial markets.
> The transaction attracted several financial institutions taking on lead roles for the first time or expanding their existing participation, with these banks accounting for nearly half of all participating institutions.
> They included First Abu Dhabi Bank (FAB), Landesbank Baden-Württemberg (LBBW), National Bank of Kuwait (NBK), Oversea-Chinese Banking Corporation Limited (OCBC), Taipei Fubon Commercial Bank, The Hongkong and Shanghai Banking Corporation (HSBC) and The Bank of East Asia (BEA). Existing MLAUB partners also participated, including Australia and New Zealand Banking Group (ANZ), Cathay United Bank (CUB), Commerzbank, CTBC Bank (CTBC), Mashreq Bank, Maybank Securities and Standard Chartered Bank (SCB).
> With the partnership of 15 international financial institutions, this facility represents VPBank’s largest-ever transaction in terms of the number of MLAUBs involved. The scale of the transaction and the breadth of participation underscore the strong confidence of the international financial community in VPBank’s financial strength, growth prospec

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0259 -->
## 259. edge-0259

**Triple:** Y Combinator (ORG) —INVESTED_IN→ Stilta (ORG)
**Assertion status:** reported
**Evidence:**
> Block and Estreen saw an opening and teamed up with two others, Petrus Werner and Oscar Adamsson, to launch Stilta, an AI platform designed to automate the research and analytical work behind intellectual property cases — the kind of labor-intensive work that has historically made patent litigation slow and expensive. The startup announced a $10.5 million seed round on Tuesday, led by Andreessen Horowitz. Other investors include Y Combinator and operators from companies like OpenAI, Legora, and Lovable.

**Article:** [Stilta raises $10.5M from a16z and YC to help companies rediscover the patents they forgot they had](https://techcrunch.com/2026/05/19/legal-tech-announced-stilta-announces-10m-seed-backed-by-yc-and-a16z-months-after-launch/) | en | techcrunch.com
**Ngữ cảnh:**
> any, where he saw firsthand how manual and slow the patent process was. The idea for his next company came one evening at dinner with a friend and colleague, Tobias Estreen, when Estreen’s father, a patent attorney, started recounting what his days looked like: “Reading the same kind of documents, the same way he had for 30 years,” Block recalled.
> Block and Estreen saw an opening and teamed up with two others, Petrus Werner and Oscar Adamsson, to launch Stilta, an AI platform designed to automate the research and analytical work behind intellectual property cases — the kind of labor-intensive work that has historically made patent litigation slow and expensive. The startup announced a $10.5 million seed round on Tuesday, led by Andreessen Horowitz. Other investors include Y Combinator and operators from companies like OpenAI, Legora, and Lovable.
> Block, the company’s CEO, said Stilta works like a team of lawyers. Users put a patent number into the software along with any relevant content, and from there, a network of AI agents gets to work, searching for other patents that might conflict with the claim, flagging similar property that could apply, and pulling the filing and court history of

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0260 -->
## 260. edge-0260

**Triple:** Qatar Investment Authority (ORG) —INVESTED_IN→ Whoop (ORG)
**Assertion status:** reported
**Evidence:**
> Whoop, the fitness and health tracking wearable company, has closed a $575 million Series G funding round at a $10.1 billion valuation — nearly triple its last reported valuation of $3.6 billion — in a deal that brings together sovereign wealth funds, major health institutions, and some of the world’s most recognizable athletes.
> The round was led by Collaborative Fund and includes participation from Mubadala Investment Company, Qatar Investment Authority, 2PointZero Group, Abbott, Mayo Clinic, Macquarie Capital, IVP, Foundry Group, Accomplice, Affinity Partners, Glade Brook, B-Flexion, Promus Ventures, and Bullhound Capital.

**Article:** [Whoop&#8217;s valuation just tripled to $10 billion](https://techcrunch.com/2026/03/31/whoop-valuation-10b-series-g-fundraise/) | en | techcrunch.com
**Ngữ cảnh:**
> Whoop, the fitness and health tracking wearable company, has closed a $575 million Series G funding round at a $10.1 billion valuation — nearly triple its last reported valuation of $3.6 billion — in a deal that brings together sovereign wealth funds, major health institutions, and some of the world’s most recognizable athletes.
> The round was led by Collaborative Fund and includes participation from Mubadala Investment Company, Qatar Investment Authority, 2PointZero Group, Abbott, Mayo Clinic, Macquarie Capital, IVP, Foundry Group, Accomplice, Affinity Partners, Glade Brook, B-Flexion, Promus Ventures, and Bullhound Capital. Individual investors include Cristiano Ronaldo, LeBron James, Rory McIlroy, Reggie Miller, and Niall Horan, among other prominent athletes and celebrities.
> The company has now raised roughly $900 million in total since its founding.
> One notable addition to the cap table is Abbott, the medical device giant. Whoop founder and CEO Will Ahmed told me 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0261 -->
## 261. edge-0261

**Triple:** Thales (ORG) —COOPERATES_WITH→ Vietnam Space Committee (GOV)
**Assertion status:** reported
**Evidence:**
> For Thales, developing local talent is just as important as bringing advanced technologies to Việt Nam. This commitment is reflected in our industrial and academic partnerships. In the space sector, our cooperation with the Vietnam Space Committee and OSB Group aims to promote education, training and innovation in satellite technologies, helping develop Việt Nam's domestic expertise in this strategic field.

**Article:** [Thales seeks deeper technology and industrial ties with Việt Nam](https://vietnamnews.vn/economy/1803912/thales-seeks-deeper-technology-and-industrial-ties-with-viet-nam.html) | en | vietnamnews.vn
**Ngữ cảnh:**
> eau, near Paris, France in September. We were honoured to welcome the Vietnamese delegation and showcase some of our latest innovations in AI, quantum technologies, semiconductors and other advanced technologies.
> 
> This visit highlighted the strong potential for deeper scientific, technological and industrial cooperation between our two countries.
> 
> For Thales, developing local talent is just as important as bringing advanced technologies to Việt Nam. This commitment is reflected in our industrial and academic partnerships. In the space sector, our cooperation with the Vietnam Space Committee and OSB Group aims to promote education, training and innovation in satellite technologies, helping develop Việt Nam's domestic expertise in this strategic field.
> 
> We are also strongly committed to STEM (Science, Technology, Engineering and Mathematics) education to inspire the next generation of engineers and scientists.
> 
> One particularly inspiring example is the achievement of a young Vietnamese student who won a silver medal at the 2025 International Physics Olympiad in Paris and was also selected as one

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0262 -->
## 262. edge-0262

**Triple:** Qatar Investment Authority (ORG) —INVESTED_IN→ SambaNova (ORG)
**Assertion status:** reported
**Evidence:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Article:** [AI chip maker SambaNova raises $1B at $11B valuation, 5 months after last mega round](https://techcrunch.com/2026/07/08/sambanova-draws-1b-at-11b-valuation-in-series-f-first-close/) | en | techcrunch.com
**Ngữ cảnh:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0263 -->
## 263. edge-0263

**Triple:** Omer Singer (PERSON) —FOUNDED→ Glow (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Tiger, a former Meta vice president of engineering, co-founded Glow alongside former Snowflake cybersecurity strategy head Omer Singer (pictured above, left), former Claroty vice president of research and development Ophir Arie (pictured above, right), and former Meta engineering leader Arnon Joseph. The startup’s leadership team also includes chief operating officer Emily Heath, a former chief information security officer at United Airlines and Docusign who served on the board of Wiz through its $32 billion acquisition by Google and was previously a partner at Cyberstarts.

**Article:** [Glow emerges from stealth at $1.2B valuation to challenge endpoint security in the AI era](https://techcrunch.com/2026/07/22/glow-emerges-from-stealth-at-1-2b-valuation-to-challenge-endpoint-security-in-the-ai-era/) | en | techcrunch.com
**Ngữ cảnh:**
> ialized AI agents to continuously map enterprise environments, assess risk in real time, and enforce security policies.
> “If you think of the past decade, everything was moving to the cloud and SaaS. Suddenly, AI lands on the endpoint in a way we’ve never seen,” co-founder and chief executive Roi Tiger (pictured above, center) said in an interview.
> Tiger, a former Meta vice president of engineering, co-founded Glow alongside former Snowflake cybersecurity strategy head Omer Singer (pictured above, left), former Claroty vice president of research and development Ophir Arie (pictured above, right), and former Meta engineering leader Arnon Joseph. The startup’s leadership team also includes chief operating officer Emily Heath, a former chief information security officer at United Airlines and Docusign who served on the board of Wiz through its $32 billion acquisition by Google and was previously a partner at Cyberstarts.
> Even though it has only just emerged from stealth, Glow said it already has paying customers across industries including healthcare, retail, and financial services. However, it declined to disclose customer names and numbers. The startup’s typical deployments, Tiger said, span tens of thousands of employee devices across global organizations.
> To p

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0264 -->
## 264. edge-0264

**Triple:** Swish Ventures (ORG) —INVESTED_IN→ Glow (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.

**Article:** [Glow emerges from stealth at $1.2B valuation to challenge endpoint security in the AI era](https://techcrunch.com/2026/07/22/glow-emerges-from-stealth-at-1-2b-valuation-to-challenge-endpoint-security-in-the-ai-era/) | en | techcrunch.com
**Ngữ cảnh:**
> Glow, a cybersecurity startup founded by former Meta and Snowflake executives, emerged from stealth as a unicorn, betting that artificial intelligence is reshaping how enterprises secure employee devices.
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.
> As more enterprises deploy AI tools and attackers increasingly use generative AI to automate phishing, develop malware, and launch more sophisticated cyberattacks, companies are rethinking how they secure endpoints — from employee laptops to servers and other connected devices. Concerns have intensified since Anthropic unveiled its Mythos AI model

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0265 -->
## 265. edge-0265

**Triple:** Wonder Project (ORG) —PARTNERED_WITH→ Innovative Dreams (ORG)
**Assertion status:** reported
**Evidence:**
> AI video generation startup Luma has launched Innovative Dreams, a production company built in partnership with Wonder Project, a studio that produces religious and family friendly films and TV, as well as a streaming service on Amazon Prime Video.

**Article:** [Luma launches AI-powered production studio with faith-focused Wonder Project](https://techcrunch.com/2026/04/16/luma-launches-ai-powered-production-studio-with-faith-focused-wonder-project/) | en | techcrunch.com
**Ngữ cảnh:**
> AI video generation startup Luma has launched Innovative Dreams, a production company built in partnership with Wonder Project, a studio that produces religious and family friendly films and TV, as well as a streaming service on Amazon Prime Video.
> The tie-up’s first project will be called “The Old Stories: Moses,” starring British actor Ben Kingsley and set to launch this spring on Prime Video.
> “Innovative Dreams is a production services company where seasoned filmmakers from director Jon Erwin’s team and Luma’s creative technologists work with great studios and filmmakers to help them real

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0266 -->
## 266. edge-0266

**Triple:** Mitch Stein (PERSON) —FOUNDED→ ARENA Private Wealth (ORG)
**Assertion status:** reported
**Evidence:**
> “Companies are staying private longer, and there are fewer IPOs now than we’ve seen historically,” Mitch Stein, founder of Arena Private Wealth, an investment advisory firm for high-net-worth individuals, told TechCrunch on a recent episode of Equity.

**Article:** [The AI gold rush is pulling private wealth into riskier, earlier bets](https://techcrunch.com/2026/04/07/the-ai-gold-rush-is-pulling-private-wealth-into-riskier-earlier-bets/) | en | techcrunch.com
**Ngữ cảnh:**
> Loading the player…
> For decades, buying stock in a hot startup meant being allowed to invest in the funds run by the top VCs. But with the AI boom causing an investment frenzy, more family offices and private wealth are skipping the VC middlemen to get directly onto the cap table.
> “Companies are staying private longer, and there are fewer IPOs now than we’ve seen historically,” Mitch Stein, founder of Arena Private Wealth, an investment advisory firm for high-net-worth individuals, told TechCrunch on a recent episode of Equity. “A lot of money is being made well before companies go public, and right now the private markets are dominated by a lot of these AI names. The family offices who are allocating [directly into AI startups] are right on.”
> Arena recently co-led a $230 million round into AI chip startup Positron, an investment that earned the midwestern firm a board s

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0267 -->
## 267. edge-0267

**Triple:** Joseph Sanberg (PERSON) —FOUNDED→ Aspiration Partners (ORG)
**Assertion status:** reported
**Evidence:**
> Sanberg co-founded green fintech startup Aspiration Partners, which offered what it called sustainable banking services like credit cards and investment products that avoided fossil fuels.

**Article:** [Steve Ballmer blasts founder he backed who pleaded guilty to fraud: &#8216;I was duped and feel silly&#8217;](https://techcrunch.com/2026/04/24/steve-ballmer-blasts-founder-he-backed-who-pleaded-guilty-to-fraud-i-was-duped-and-feel-silly/) | en | techcrunch.com
**Ngữ cảnh:**
> ximum sentence of 20 years in prison.
> Ahead of sentencing, which is scheduled for Monday, victims were invited to describe their experience with Sanberg to the judge. Ballmer did so, and publicly. Ballmer’s lawyers said in the letter that he has lost money, been vilified, and that the NBA is investigating allegations stemming from the association.
> Sanberg co-founded green fintech startup Aspiration Partners, which offered what it called sustainable banking services like credit cards and investment products that avoided fossil fuels. The startup promised to “automatically plant trees with every card purchase.” In 2021, it announced plans to go public via a SPAC merger at a value of $2.3 billion, though that transaction never took place.
> The DOJ alleged that Aspiration booked and recognized revenue from entities held by Sanberg, who made the company appear as if it had a steady

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0268 -->
## 268. edge-0268

**Triple:** Sequoia Capital (ORG) —CO_INVESTED_WITH→ First Round Capital (ORG)
**Assertion status:** reported
**Evidence:**
> Parallel Web Systems, the AI agent-tool startup founded by former Twitter CEO Parag Agrawal, has raised a $100 million Series B at a $2 billion valuation led by Sequoia. Existing investors Kleiner Perkins, Index Ventures, Khosla Ventures, First Round Capital, Spark Capital, and Terrain Capital also participated, the company said.

**Article:** [Parallel Web Systems hits $2B valuation five months after its last big raise](https://techcrunch.com/2026/04/29/parallel-web-systems-hits-2b-valuation-five-months-after-its-last-big-raise/) | en | techcrunch.com
**Ngữ cảnh:**
> Parallel Web Systems, the AI agent-tool startup founded by former Twitter CEO Parag Agrawal, has raised a $100 million Series B at a $2 billion valuation led by Sequoia. Existing investors Kleiner Perkins, Index Ventures, Khosla Ventures, First Round Capital, Spark Capital, and Terrain Capital also participated, the company said.
> This raise comes just five months after the startup announced its $100 million Series A at a $740 million valuation led by Kleiner and Index, and brings the total capital it raised to $230 million.
> Parallel offers a suite of web search and research APIs specifically for AI agents and names customers such as Clay, Harvey, Notion, and Opendoor. It s

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0269 -->
## 269. edge-0269

**Triple:** Josiah Meyer (PERSON) —CEO_OF→ Healthleap (ORG)
**Assertion status:** reported
**Evidence:**
> Founded in South Africa in 2022 by siblings Jemima and Josiah Meyer (pictured above), the startup initially offered a clinical nutrition tool Jemima had built for dietitians. But the company later pivoted and built a more general-purpose platform that aims to identify patients admitted to hospitals who may be suffering from conditions like malnutrition or delirium that aren’t often identified early enough, CEO and co-founder Josiah Meyer told TechCrunch.

**Article:** [Healthleap raises $38M for its AI that flags hospital patients who may need a closer look](https://techcrunch.com/2026/10/07/healthleap-raises-38m-for-its-ai-that-flags-hospital-patients-who-may-need-a-closer-look/) | en | techcrunch.com
**Ngữ cảnh:**
> cords to identify patients at risk of undiagnosed illnesses, has raised $38 million in seed and Series A funding, TechCrunch has exclusively learned.
> The financing includes an $8 million seed round co-led by Sequoia Capital and First Round Capital, and a $30 million Series A led by Hummingbird Ventures. The company is not disclosing its valuation.
> Founded in South Africa in 2022 by siblings Jemima and Josiah Meyer (pictured above), the startup initially offered a clinical nutrition tool Jemima had built for dietitians. But the company later pivoted and built a more general-purpose platform that aims to identify patients admitted to hospitals who may be suffering from conditions like malnutrition or delirium that aren’t often identified early enough, CEO and co-founder Josiah Meyer told TechCrunch.
> “A patient’s chart holds two kinds of data. Labs, weights, and vital signs sit in structured fields, but the most telling signs sit in clinicians’ written notes: poor appetite, recent weight loss, muscle loss, trouble swallowing. Our developing approach is extracting affirmative or negated mentions of these clinical concepts in an easily extensibl

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0270 -->
## 270. edge-0270

**Triple:** Atreides Management (ORG) —CO_INVESTED_WITH→ Layer Global (ORG)
**Assertion status:** reported
**Evidence:**
> Cognition, the makers of the autonomous AI software engineer named Devin, has raised more than $1 billion at a $25 billion pre-money valuation ($26 billion post money), the company announced on Wednesday.
> That’s a major leap from its $10.2 billion post-money valuation when it closed a $400 million funding round just eight months ago in September.
> The round was led by Lux Capital, General Catalyst and 8VC, with a host of existing investors pouring in, including Elad Gil, Soma Capital, Omri Casspi, Founders Fund, and a long list of others. The round also included new investors like Ribbit Capital, Atreides, and Layer Global.

**Article:** [AI coding startup Cognition raises $1B at $25B pre-money valuation](https://techcrunch.com/2026/05/27/ai-coding-startup-cognition-raises-1b-at-25b-pre-money-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Cognition, the makers of the autonomous AI software engineer named Devin, has raised more than $1 billion at a $25 billion pre-money valuation ($26 billion post money), the company announced on Wednesday.
> That’s a major leap from its $10.2 billion post-money valuation when it closed a $400 million funding round just eight months ago in September.
> The round was led by Lux Capital, General Catalyst and 8VC, with a host of existing investors pouring in, including Elad Gil, Soma Capital, Omri Casspi, Founders Fund, and a long list of others. The round also included new investors like Ribbit Capital, Atreides, and Layer Global.
> This is a giant vote of confidence from top-tier VCs that there will be room for independent AI software coding startups. Last year, all signs pointed to model makers swallowing this hot market themselves. Certainly Anthropic’s Claude Code, OpenAI’s Codex, and maybe even Google’s coding agent Jules (after Google’s acqui-hire deal of Windsurf last 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0271 -->
## 271. edge-0271

**Triple:** Kokuyo S&T (ORG) —ACQUIRED→ Camlin Limited (ORG)
**Assertion status:** reported
**Evidence:**
> Năm 2011, Kokuyo thông qua công ty con Kokuyo S&T đã dành khoảng 4,56 tỷ Rupee (tương đương 60 triệu USD tại thời điểm đó) để mua lại 50,3% cổ phần chi phối của Camlin Limited, nhà sản xuất văn phòng phẩm thành lập năm 1931 tại Ấn Độ, từ gia đình sáng lập Dandekar.

**Article:** [Doanh nghiệp về tay Tập đoàn Nhật Bản Kokuyo sẽ được phát triển thế nào?](https://vnexpress.net/doanh-nghiep-ve-tay-tap-doan-nhat-ban-kokuyo-se-duoc-phat-trien-the-nao-5142076.html) | vi | vnexpress.net
**Ngữ cảnh:**
>  kiện để TLG học hỏi các mô hình quản trị, đẩy mạnh cải tiến sản phẩm và mở rộng thị trường ra khu vực ASEAN cùng các quốc gia khác, qua đó đưa sản phẩm "Made in Vietnam" đến với nhiều người tiêu dùng trên thế giới.
> Thực tế, Kokuyo từng thực hiện một số thương vụ mua lại tại thị trường nước ngoài với cách tiếp cận đúng như những gì ông Thọ đề cập.
> Năm 2011, Kokuyo thông qua công ty con Kokuyo S&T đã dành khoảng 4,56 tỷ Rupee (tương đương 60 triệu USD tại thời điểm đó) để mua lại 50,3% cổ phần chi phối của Camlin Limited, nhà sản xuất văn phòng phẩm thành lập năm 1931 tại Ấn Độ, từ gia đình sáng lập Dandekar. Sau giao dịch, doanh nghiệp đổi tên thành Kokuyo Camlin Limited, nhưng các thương hiệu sản phẩm lâu đời như Camlin và Camel vẫn được sử dụng.
> Trước khi về tay Kokuyo, Camlin đã có hơn 80 năm hoạt động, với hai thương hiệu chủ lực là Camlin và Camel, gắn với các sản phẩm văn phòng phẩm, màu vẽ và dụng cụ mỹ thuật. Doanh nghiệp sở hữu danh mục hơn 2

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0272 -->
## 272. edge-0272

**Triple:** Active Impact Investments (ORG) —INVESTED_IN→ Fluxnium (ORG)
**Assertion status:** reported
**Evidence:**
> Fluxnium gave TechCrunch an exclusive look at its technology. The startup recently closed a $7 million seed round led by Congruent Ventures with participation from Active Impact Investments and Constellation Energy, which operates the largest nuclear fleet in the U.S.

**Article:** [Clean tech startup Fluxnium found a way to tap 50,000 years&#8217; worth of nuclear fuel](https://techcrunch.com/2026/09/16/clean-tech-startup-fluxnium-found-a-way-to-tap-50000-years-worth-of-nuclear-fuel/) | en | techcrunch.com
**Ngữ cảnh:**
> tech Fluxnium, told TechCrunch.
> Fluxnium thinks it has solved the problem of how to extract uranium from seawater. Using technology developed at U.S. Department of Energy national labs, the company has an approach that could be competitive with existing uranium mines.
> The startup has been working in stealth until now to develop the new technology. Fluxnium gave TechCrunch an exclusive look at its technology. The startup recently closed a $7 million seed round led by Congruent Ventures with participation from Active Impact Investments and Constellation Energy, which operates the largest nuclear fleet in the U.S.
> Fluxnium is emerging as the nuclear industry in the U.S. undergoes a renaissance. Tech companies have backed several nuclear startups as they search for new sources of electricity to power their AI data centers.
> Green’s timing is good, but perhaps not surprising. He’s a repeat founder, having helped launch Stamps.com in 1996, desalination startup 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0273 -->
## 273. edge-0273

**Triple:** Sequoia Capital (ORG) —INVESTED_IN→ Stripe (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The storied firm, which famously backed Airbnb, Google, Nvidia, and Stripe in their infancy, is putting recent challenges behind it and returning to its core purpose: investing in promising founders at the earliest stages of creation.

**Article:** [Sequoia unveils $950M in new early-stage funds as it strives to be &#8216;only as good as our next investment&#8217;](https://techcrunch.com/2025/10/27/sequoia-unveils-950m-in-new-early-stage-funds-as-it-strives-to-be-only-as-good-as-our-next-investment/) | en | techcrunch.com
**Ngữ cảnh:**
> n fund supported by strategy-specific “sub-funds,” primarily to enable the firm to retain stock in portfolio companies long after their IPO. The firm took a significant financial hit in late 2022, losing over $200 million when its investment in cryptocurrency exchange FTX blew up, followed by the 2023 separation from its India and China divisions.
> The storied firm, which famously backed Airbnb, Google, Nvidia, and Stripe in their infancy, is putting recent challenges behind it and returning to its core purpose: investing in promising founders at the earliest stages of creation.
> Balkansky reinforced this mission: “Our ambition has always been and continues to be to identify these founders as early as possible; to roll up our sleeves and be a very active participant in their company-building journey.”
> With AI startup valuations skyrocketing, Sequoia wants to use the new funds to invest in the most promising founders at the

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0274 -->
## 274. edge-0274

**Triple:** Carta (ORG) —PARTNERED_WITH→ NewView Capital (ORG)
**Assertion status:** reported
**Evidence:**
> To simplify the tender process, NewView Capital, which specializes in secondary deals along with typical venture investments, recently partnered with Carta.

**Article:** [Carta and NewView partner, hoping to entice more startups to let employees sell shares early](https://techcrunch.com/2026/10/23/carta-and-newview-partner-hoping-to-entice-more-startups-to-let-employees-sell-shares-early/) | en | techcrunch.com
**Ngữ cảnh:**
> of their compensation as stock they can’t sell, with little hope of early liquidity.
> An increasing number of late-stage startups are recognizing this and offering tender offers to employees. These are transactions that allow employees (and, often, early investors) to sell a portion of their shares for a predetermined price to an approved investor.
> To simplify the tender process, NewView Capital, which specializes in secondary deals along with typical venture investments, recently partnered with Carta. The collaboration combines NewView’s secondhand deal-structuring experience with Carta’s equity platform. Ravi Viswanathan, founder and managing partner of NewView, pitches this as a way to help startups launch and manage liquidity programs more seamlessly.
> “The hope is that this partnership will make it easier for CEOs and companies to think abou

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0275 -->
## 275. edge-0275

**Triple:** DST Global (ORG) —CO_INVESTED_WITH→ General Catalyst (ORG)
**Assertion status:** reported
**Evidence:**
> In September 2025, Mistral closed a €1.7 billion Series C round (about $2 billion) led by ASML at a €11.7 billion valuation (approximately $13.8 billion), with participation from existing backers DST Global, a16z, Bpifrance, General Catalyst, Index Ventures, Lightspeed, and Nvidia.

**Article:** [What is Mistral AI? Everything to know about the OpenAI competitor](https://techcrunch.com/2026/07/04/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/) | en | techcrunch.com
**Ngữ cảnh:**
>  presented as a Series A extension, implying an unchanged valuation.
> In June 2024, Mistral raised €600 million (about $640 million) in a mix of equity and debt. The long-rumored round was led by General Catalyst at a $6 billion valuation, with notable investors including Cisco, IBM, Nvidia, and Samsung Venture Investment Corporation participating.
> In September 2025, Mistral closed a €1.7 billion Series C round (about $2 billion) led by ASML at a €11.7 billion valuation (approximately $13.8 billion), with participation from existing backers DST Global, a16z, Bpifrance, General Catalyst, Index Ventures, Lightspeed, and Nvidia.
> What companies has Mistral AI acquired?
> In addition to infrastructure startup Koyeb, Mistral has also bought Emmi, an Austrian startup focusing on physics AI, with the ambition to better support industrial enterprises in their AI transformation.
> Will Mistral AI make its own chips?
> While Mistral has yet to design its own chips, Mensch isn’t ruling 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0276 -->
## 276. edge-0276

**Triple:** ACS Group (ORG) —CO_INVESTED_WITH→ Khosla Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> The round was co-led by Suzuki Motor Corporation, ACS Group, and Khosla Ventures. Existing investors Mitsui Chemicals and Gates Frontier, and new investor Obayashi Corporation also participated.

**Article:** [This Khosla-backed autonomous pod startup just raised $170M — now it’s aiming for more](https://techcrunch.com/2026/04/15/this-khosla-backed-autonomous-pod-startup-just-raised-170m-now-its-aiming-for-more/) | en | techcrunch.com
**Ngữ cảnh:**
> Glydways, a San Francisco-based startup developing personal autonomous pods designed to operate on dedicated 2-meter-wide lanes in cities, has raised $170 million in a Series C funding round.
> The round was co-led by Suzuki Motor Corporation, ACS Group, and Khosla Ventures. Existing investors Mitsui Chemicals and Gates Frontier, and new investor Obayashi Corporation also participated.
> Now it seems the startup is already in discussions to raise another $250 million in funding that would push its valuation to more than $1 billion, Bloomberg reported.
> Glydways has made progress on its concept, which it claims can move up to 10,000 people per hour, per lane and reduce infrastructure costs by up to 90% compared to rail. The startup,

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0277 -->
## 277. edge-0277

**Triple:** Day Zero Ventures (ORG) —CO_INVESTED_WITH→ DeVC (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Founded by IIT batchmates Georgi Boby and Dhruv Jaglan in 2025, Rilo raised $1 million from investors including Peak XV, DeVC, and Day Zero Ventures at a $10 million valuation. A source told TechCrunch that investors will get an exit from this deal, and Adobe will integrate some of Rilo’s IP along with the six-member team. Jaglan mentioned on LinkedIn that more than 10,000 people had tried out the tool.

**Article:** [Adobe acquires Indian market intelligence startup Rilo](https://techcrunch.com/2026/09/02/adobe-acquires-indian-market-intelligence-startup-rilo/) | en | techcrunch.com
**Ngữ cảnh:**
> n changing as companies use AI to build tools to automate the creation, deployment, and tracking of campaigns, get action items from meetings or calls to complete tasks, and increase brand visibility on platforms like ChatGPT, Gemini, and Claude. Rilo’s technology could bolster Adobe’s existing products as the company targets its larger customers.
> Founded by IIT batchmates Georgi Boby and Dhruv Jaglan in 2025, Rilo raised $1 million from investors including Peak XV, DeVC, and Day Zero Ventures at a $10 million valuation. A source told TechCrunch that investors will get an exit from this deal, and Adobe will integrate some of Rilo’s IP along with the six-member team. Jaglan mentioned on LinkedIn that more than 10,000 people had tried out the tool.
> The company worked on letting go-to-market teams create custom workflows, including competitor intelligence, content repurposing and distribution, and sales call analysis. It also allowed teams to set up custom workflows comparable to tools like Claude Cowork and ChatGPT Work.
> Post-acquisition, Rilo will shut down and won’t be available to its cus

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0278 -->
## 278. edge-0278

**Triple:** March Capital (ORG) —CO_INVESTED_WITH→ Aramco Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> The round was led by Aramco Ventures, with participation from Vista Equity Partners, General Catalyst, Emergence Capital, Nvidia, March Capital, Pegatron, SentinelOne’s S Ventures, and others.

**Article:** [Neocloud Together AI raises $800M, leaps to $8.3B valuation](https://techcrunch.com/2026/07/01/neocloud-together-ai-raises-800m-leaps-to-8-3b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Together AI — an AI neocloud that rents out Nvidia GPU clusters and other AI-specific infrastructure — has raised an $800 million Series C at an $8.3 billion valuation, the company announced on Wednesday. The company was founded in 2022.
> The round was led by Aramco Ventures, with participation from Vista Equity Partners, General Catalyst, Emergence Capital, Nvidia, March Capital, Pegatron, SentinelOne’s S Ventures, and others.
> Together AI last raised a $305 million Series B at a $3.3 billion valuation about 16 months ago. It actually came out of the gate well-funded, with a $102.5 million Series A funding round led by Kleiner Perkins with participation from Nvidia and Emergence Capital back in 2023.
> There were whispers of this round back in March, when The Information r

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0279 -->
## 279. edge-0279

**Triple:** Cyberstarts (ORG) —CO_INVESTED_WITH→ Swish Ventures (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.

**Article:** [Glow emerges from stealth at $1.2B valuation to challenge endpoint security in the AI era](https://techcrunch.com/2026/07/22/glow-emerges-from-stealth-at-1-2b-valuation-to-challenge-endpoint-security-in-the-ai-era/) | en | techcrunch.com
**Ngữ cảnh:**
> Glow, a cybersecurity startup founded by former Meta and Snowflake executives, emerged from stealth as a unicorn, betting that artificial intelligence is reshaping how enterprises secure employee devices.
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.
> As more enterprises deploy AI tools and attackers increasingly use generative AI to automate phishing, develop malware, and launch more sophisticated cyberattacks, companies are rethinking how they secure endpoints — from employee laptops to servers and other connected devices. Concerns have intensified since Anthropic unveiled its Mythos AI model

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0280 -->
## 280. edge-0280

**Triple:** Cyberstarts (ORG) —CO_INVESTED_WITH→ Index Ventures (ORG)
**Assertion status:** historical_reported
**Evidence:**
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.

**Article:** [Glow emerges from stealth at $1.2B valuation to challenge endpoint security in the AI era](https://techcrunch.com/2026/07/22/glow-emerges-from-stealth-at-1-2b-valuation-to-challenge-endpoint-security-in-the-ai-era/) | en | techcrunch.com
**Ngữ cảnh:**
> Glow, a cybersecurity startup founded by former Meta and Snowflake executives, emerged from stealth as a unicorn, betting that artificial intelligence is reshaping how enterprises secure employee devices.
> The Palo Alto-headquartered startup on Wednesday said it raised $180 million in an all-equity Series A funding round that valued it at $1.2 billion, with backing from Sequoia Capital, Cyberstarts, Greenoaks, and Redpoint Ventures, alongside participation from Index Ventures, Swish Ventures, Lux Capital, Operator Collective, and Holly Ventures. The investment made Glow one of the latest cybersecurity startups to achieve unicorn status before publicly disclosing revenue metrics.
> As more enterprises deploy AI tools and attackers increasingly use generative AI to automate phishing, develop malware, and launch more sophisticated cyberattacks, companies are rethinking how they secure endpoints — from employee laptops to servers and other connected devices. Concerns have intensified since Anthropic unveiled its Mythos AI model

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0281 -->
## 281. edge-0281

**Triple:** Peak XV Partners (ORG) —INVESTED_IN→ Helion (ORG)
**Assertion status:** reported
**Evidence:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.

**Article:** [Helion, the Sam Altman-backed fusion startup, raises $465M to build a power plant for Microsoft](https://techcrunch.com/2026/06/04/helion-the-sam-altman-backed-fusion-startup-raises-465m-to-build-a-power-plant-for-microsoft/) | en | techcrunch.com
**Ngữ cảnh:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.
> Helion’s approach to fusion power differs from many of its peers. Some use magnets to contain the superheated plasma required for fusion conditions, while others use lasers to compress fusion fuel until it reacts. In both cases, the majority of startups plan to use steam turbines to transform the intense heat into electricity.
> But Helion, which us

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0282 -->
## 282. edge-0282

**Triple:** Volantis (ORG) —CO_INVESTED_WITH→ Assam Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Article:** [AI chip maker SambaNova raises $1B at $11B valuation, 5 months after last mega round](https://techcrunch.com/2026/07/08/sambanova-draws-1b-at-11b-valuation-in-series-f-first-close/) | en | techcrunch.com
**Ngữ cảnh:**
> AI chip company SambaNova Systems has raised $1 billion at an $11 billion valuation led by General Atlantic, in a first close of its Series F round, with more investors expected to join soon.
> “In the next few weeks, a few more investors will be coming in, and the second close is likely to finish up,” Rodrigo Liang, CEO and co-founder of SambaNova, told TechCrunch.
> The latest round comes roughly five months after the Palo Alto, California-based startup company unveiled its SN50 chip, alongside a $350 million Series E in February. SambaNova had also been in acquisition talks with Intel, a deal valuing it at roughly $1.6 billion, according to a December report from Bloomberg News.
> Asked whether closing its Series E and F rounds meant SambaNova, founded in 2017, had settled on staying independent, Liang was noncommittal. He said the company keeps fielding interest. “We’re always being approached.” The door is open to such an exit in this dynamic AI market, the CEO said, but momentum and growth will most likely drive the company toward “being public at some point.”
> SambaNova’s ties to Intel, a backer since its Series C and a participant in this latest round, have deepened. Five months ago, the nine-year-old startup announced a multi-year partnership with Intel to support AI inference development based on Intel’s Xeon chip. The two now co-develop products and take them to market together. “That gives us a great relationship with them that lets us leverage the scale of Intel with the technology we have,” Liang said.
> Alongside the new funding, SambaNova said it has been selected by JPMorganChase as an “inference-infrastructure partner,” with its SN40L and SN50 systems set to power secure, on-premises AI inference at the bank.
> “Having JPMorgan Chase decide they’re going to use SambaNova for their inference solution is a big deal,” Liang told TechCrunch. “It sends a message to the banking industry that it’s time not to completely depend on cloud services. These banks want heterogeneous [infrastructure].”
> Liang said the JPMorgan win was a signal to the broader market. Banks “of the caliber of JPMorgan” are now building their own private, secure infrastructure to run inference on their most sensitive models, he said, a move he expects to resonate beyond banking. Enterprises and governments are “just starting their AI journey,” Liang continued, with most of the growth so far concentrated among tech’s model makers and frontier labs, leaving what he called “a huge amount of revenue” still on the table.
> SambaNova launched its SN40L in September 2023, available in the cloud, and on-premises from November 2023. Its next-generation SN50, unveiled in February 2026, is due to begin shipping to customers in the second half of 2026, with SoftBank as its first deployment partner, Liang noted.
> Liang said SambaNova’s edge is “premium inference” running the largest models and running them fast. Today’s frontier models span trillions of parameters, and he said SambaNova was built specifically to handle them at that scale. The company fits multi-trillion-parameter models onto a single rack which helps them run quickly.
> SambaNova sees three types of customers. The first is sovereign clouds, where governments fund local partners to build private clouds, a push Liang expects SambaNova to figure centrally in. The second is neoclouds. The third is enterprises building for their own use. In addition to JPMorgan, it also names Saudi Aramco, Intel, and other Japanese firms as customers.
> SambaNova will use the proceeds to scale the business and shore up its supply chain against what Liang called an incredible wave of demand. “We’re using that capital to secure the supply chain,” he said, describing it as essential to fulfilling orders and buying the materials the company needs to deliver over the next 12 months.
> Other investors participating in the round include Seligman Ventures, T. Rowe Price Associates, and Capital Group. New and existing investors also joined, including A&E Investment, Assam Ventures, Battery Ventures, Cambium Capital, BlackRock, Kabila Capital, QFO Capital, Qatar Investment Authority (QIA), Vista Equity Partners, and Volantis.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0283 -->
## 283. edge-0283

**Triple:** Y Combinator (ORG) —INVESTED_IN→ Supabase (ORG)
**Assertion status:** historical_reported
**Evidence:**
> But on Tuesday, the fruits of that became evident when it announced a $200 million Series D at a $2 billion post-money valuation led by Accel, with Coatue, Y Combinator, Craft Ventures, and longtime investor Felicis participating in the round, Fortune reported.

**Article:** [Vibe coding helps Supabase nab $200M at $2B valuation just seven months after its last raise](https://techcrunch.com/2025/04/22/vibe-coding-helps-supabase-nab-200m-at-2b-valuation-just-seven-months-after-its-last-raise/) | en | techcrunch.com
**Ngữ cảnh:**
> In 2020, when open source database Supabase was founded, its New Zealand-based CEO, Paul Copplestone, couldn’t have imagined it would be sitting in the sweet spot for 2025’s biggest trend: vibe coding.
> But on Tuesday, the fruits of that became evident when it announced a $200 million Series D at a $2 billion post-money valuation led by Accel, with Coatue, Y Combinator, Craft Ventures, and longtime investor Felicis participating in the round, Fortune reported.
> This fresh $200 million comes just seven months after Supabase announced it raised $80 million led by Peak XV (a Sequoia spinoff) and David Sacks’ Craft Ventures. Supabase wouldn’t comment on the valuation at that time, but PitchBook put it at about $900 million. All told, the startup has now raised about $398 million.
> Supabase is another example 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0284 -->
## 284. edge-0284

**Triple:** Edward Kim (PERSON) —FOUNDED→ Gusto (ORG)
**Assertion status:** reported
**Evidence:**
> And Gusto co-founder Edward Kim is apparently telling his team that in the future, offices will sound “more like a sales floor.”

**Article:** [Get ready for the whisper-filled office of the future](https://techcrunch.com/2026/05/10/get-ready-for-the-whisper-filled-office-of-the-future/) | en | techcrunch.com
**Ngữ cảnh:**
> nd more time talking to our computers? A recent feature in the Wall Street Journal looks at the rising popularity of dictation apps like Wispr, especially now that they can be connected to vibe-coding tools, and what that might mean for office etiquette.
> One VC said that visiting startup offices now feels like stepping into a high-end call center. And Gusto co-founder Edward Kim is apparently telling his team that in the future, offices will sound “more like a sales floor.” (As someone still scarred from the time his desk was briefly relocated to a sales floor, let me say: Oh no.)
> Kim claimed that he only types now when he absolutely has to. But he admitted that constantly dictating in the office can be “just a little awkward.”
> Similarly, AI entrepreneur Mollie Amkraut Mueller said her husband became annoyed with her

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0285 -->
## 285. edge-0285

**Triple:** Mithril Capital Management (ORG) —CO_INVESTED_WITH→ Thrive Capital (ORG)
**Assertion status:** reported
**Evidence:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.

**Article:** [Helion, the Sam Altman-backed fusion startup, raises $465M to build a power plant for Microsoft](https://techcrunch.com/2026/06/04/helion-the-sam-altman-backed-fusion-startup-raises-465m-to-build-a-power-plant-for-microsoft/) | en | techcrunch.com
**Ngữ cảnh:**
> Helion, the fusion startup backed by Sam Altman, announced on Thursday that it had raised $465 million in a new funding round that values the company at $15.5 billion.
> The cash infusion lands as Helion is racing to complete Orion, its first power plant. The startup has set an aggressive timeline to deploy fusion power to the grid, as early as 2028 if it can deliver on the terms of its deal with Microsoft.
> The startup last raised $425 million in January 2025. Altogether, Helion said it has raised $1.5 billion.
> The new round, a Series G, was led by Thrive Capital with a long list of participants, including new investors Alta Park Capital, Anti Fund, BoxGroup, Lux Capital, Peak XV Partners, and Bill Ford, along with existing investors, which include Capricorn Technology Impact Funds, Lightspeed Venture Partners, Mithril Capital, Dustin Moskovitz through Good Ventures Foundation, SoftBank Vision Fund 2, and a university endowment fund.
> Helion’s approach to fusion power differs from many of its peers. Some use magnets to contain the superheated plasma required for fusion conditions, while others use lasers to compress fusion fuel until it reacts. In both cases, the majority of startups plan to use steam turbines to transform the intense heat into electricity.
> But Helion, which us

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0286 -->
## 286. edge-0286

**Triple:** Daniela Amodei (PERSON) —OWNS_STAKE_IN→ Anthropic (ORG)
**Assertion status:** planned
**Evidence:**
> The seven co-founders are Dario Amodei, CEO; Daniela Amodei, president and chair of the board; Tom Brown, chief compute officer; Jack Clark, head of public benefit; Jared Kaplan, chief science officer (pictured above); Sam McCandlish, chief architect; and Christopher Olah, interpretability research lead.
> After the sale, each of them will own about 3.2% of the total outstanding Class A shares, the S-1 says, or roughly 22% collectively.

**Article:** [All 7 Anthropic founders will each cash out about $250M in IPO](https://techcrunch.com/2026/11/10/all-7-anthropic-founders-will-each-cash-out-about-250m-in-ipo/) | en | techcrunch.com
**Ngữ cảnh:**
> ever, in an IPO as eagerly anticipated as this one, companies can often price shares above the initial range.
> The S-1 is already hinting at high demand. Board member Reed Hastings has indicated he wants to buy $300 million worth of shares through his donor-advised fund. Board member Christopher Liddell also wants to buy $3 million worth of shares.
> The seven co-founders are Dario Amodei, CEO; Daniela Amodei, president and chair of the board; Tom Brown, chief compute officer; Jack Clark, head of public benefit; Jared Kaplan, chief science officer (pictured above); Sam McCandlish, chief architect; and Christopher Olah, interpretability research lead.
> After the sale, each of them will own about 3.2% of the total outstanding Class A shares, the S-1 says, or roughly 22% collectively. That’s not their share of the company overall. Class A is just one of Anthropic’s share classes, and other holders, including Amazon and Google, hold nonvoting Class N shares, so the founders’ stake in the company’s total equity will be considerably smaller. Even still, they, as a group, remain in control of the company. Each will also receive one

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0287 -->
## 287. edge-0287

**Triple:** Andreessen Horowitz (ORG) —CO_INVESTED_WITH→ Salesforce Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> Arena, which originated in 2023 as a research project at UC Berkeley that crowdsourced rankings of AI models, has raised a $200 million Series B round at a $3.1 billion valuation, it said on Thursday.
> This comes after the company said it reached $100 million in annualized run-rate revenue in June.
> The round was led by Lightspeed Venture Partners and Khosla Ventures, with Salesforce Ventures, 01 Advisors, Dell Technologies Capital, Endeavor Catalyst, a16z, Felicis, and others joining in. Arena previously announced a $150 million Series A in January at a $1.7 billion post-money valuation. At the time, its annualized revenue was $30 million, it said. So that means its valuation has nearly doubled in about 10 months.

**Article:** [Popular AI leaderboard Arena nearly doubles valuation to $3.1B valuation in 10 months](https://techcrunch.com/2026/10/08/popular-ai-leaderboard-arena-nearly-doubles-valuation-to-3-1b-valuation-in-10-months/) | en | techcrunch.com
**Ngữ cảnh:**
> Arena, which originated in 2023 as a research project at UC Berkeley that crowdsourced rankings of AI models, has raised a $200 million Series B round at a $3.1 billion valuation, it said on Thursday.
> This comes after the company said it reached $100 million in annualized run-rate revenue in June.
> The round was led by Lightspeed Venture Partners and Khosla Ventures, with Salesforce Ventures, 01 Advisors, Dell Technologies Capital, Endeavor Catalyst, a16z, Felicis, and others joining in. Arena previously announced a $150 million Series A in January at a $1.7 billion post-money valuation. At the time, its annualized revenue was $30 million, it said. So that means its valuation has nearly doubled in about 10 months.
> Arena provides a crowdsourced platform that is free for consumers to use. People enter prompts or request vibe-coded projects and then rate which model does it better. Arena claims it has tens of millions of monthly visitors.
> In September of last year, it introduced its commercial product, AI Evaluations, a service that provides model labs and ent

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0288 -->
## 288. edge-0288

**Triple:** Leapmotor (ORG) —PARTNERED_WITH→ Stellantis (ORG)
**Assertion status:** reported
**Evidence:**
> Trong khi đó, Ford và Geely đã đạt thỏa thuận về việc thành lập liên doanh liên quan đến nhà máy Almussafes tại Valencia, với kế hoạch sản xuất xe năng lượng mới phục vụ thị trường châu Âu. Thỏa thuận vẫn cần được cơ quan quản lý phê duyệt. Stellantis cũng đang tăng cường hợp tác công nghiệp với Leapmotor, trong đó có kế hoạch sản xuất tại Zaragoza.

**Article:** [Tây Ban Nha hợp tác với Trung Quốc, tìm cách giữ vị thế trong chuỗi giá trị xe điện](https://vneconomy.vn/tay-ban-nha-hop-tac-voi-trung-quoc-tim-cach-giu-vi-the-trong-chuoi-gia-tri-xe-dien.htm) | vi | vneconomy.vn
**Ngữ cảnh:**
> ung Quốc đang mở rộng ra ngoài lĩnh vực pin, bao gồm cả sản xuất ô tô và phát triển các cơ sở công nghiệp.
> 
> Chery đã hợp tác với thương hiệu Tây Ban Nha Ebro nhằm khôi phục hoạt động sản xuất tại nhà máy cũ của Nissan ở Barcelona. Tháng 11/2024, hai bên tổ chức lễ khởi động sản xuất xe tại nhà máy liên doanh Ebro ở Khu thương mại tự do Barcelona.
> 
> Trong khi đó, Ford và Geely đã đạt thỏa thuận về việc thành lập liên doanh liên quan đến nhà máy Almussafes tại Valencia, với kế hoạch sản xuất xe năng lượng mới phục vụ thị trường châu Âu. Thỏa thuận vẫn cần được cơ quan quản lý phê duyệt. Stellantis cũng đang tăng cường hợp tác công nghiệp với Leapmotor, trong đó có kế hoạch sản xuất tại Zaragoza.
> 
> Những liên minh này tạo thêm phương án duy trì hoạt động của các nhà máy, bảo vệ mạng lưới nhà cung ứng và thu hút nguồn vốn đầu tư mới trong bối cảnh ngành ô tô châu Âu đối mặt với áp lực chuyển đổi công nghệ và cạnh tranh quốc tế.
> 
> Đáng chú ý, đầu tư của Gotion tại Tây Ban Nha còn mở rộng sang những công đoạn nằm sâu hơn trong chuỗi cung ứng. D

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0289 -->
## 289. edge-0289

**Triple:** Aramco Ventures (ORG) —CO_INVESTED_WITH→ S Ventures (ORG)
**Assertion status:** reported
**Evidence:**
> The round was led by Aramco Ventures, with participation from Vista Equity Partners, General Catalyst, Emergence Capital, Nvidia, March Capital, Pegatron, SentinelOne’s S Ventures, and others.

**Article:** [Neocloud Together AI raises $800M, leaps to $8.3B valuation](https://techcrunch.com/2026/07/01/neocloud-together-ai-raises-800m-leaps-to-8-3b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Together AI — an AI neocloud that rents out Nvidia GPU clusters and other AI-specific infrastructure — has raised an $800 million Series C at an $8.3 billion valuation, the company announced on Wednesday. The company was founded in 2022.
> The round was led by Aramco Ventures, with participation from Vista Equity Partners, General Catalyst, Emergence Capital, Nvidia, March Capital, Pegatron, SentinelOne’s S Ventures, and others.
> Together AI last raised a $305 million Series B at a $3.3 billion valuation about 16 months ago. It actually came out of the gate well-funded, with a $102.5 million Series A funding round led by Kleiner Perkins with participation from Nvidia and Emergence Capital back in 2023.
> There were whispers of this round back in March, when The Information r

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0290 -->
## 290. edge-0290

**Triple:** Gatik (ORG) —CONTRACTED_WITH→ PepsiCo (ORG)
**Assertion status:** reported
**Evidence:**
> Gatik, the autonomous vehicle startup known for its self-driving box trucks, has raised $200 million just two months after striking a multiyear commercial agreement with PepsiCo.

**Article:** [Self-driving truck startup Gatik raises $200M following PepsiCo deal](https://techcrunch.com/2026/08/25/self-driving-truck-startup-gatik-raises-200m-following-pepsico-deal/) | en | techcrunch.com
**Ngữ cảnh:**
> Gatik, the autonomous vehicle startup known for its self-driving box trucks, has raised $200 million just two months after striking a multiyear commercial agreement with PepsiCo.
> The round was led by Qatar Investment Authority and Koch Disruptive Technologies, with participation from Millennium Management, ARK Invest, and Intact Private Capital. The Santa Clara, California-based company has raised about $500 million since it came out of stealth in 2019. The company didn’t disclose its valuation.
> The funding, the company’s 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0291 -->
## 291. edge-0291

**Triple:** Goldman Sachs Alternatives (ORG) —INVESTED_IN→ Higgsfield (ORG)
**Assertion status:** reported
**Evidence:**
> DST Global led the latest round, with many other investors piling in, including Goldman Sachs Alternatives, Valor Capital, and Tribe Capital.

**Article:** [Higgsfield raises $400M Series B, quadrupling its valuation in 8 months to $5.4B](https://techcrunch.com/2026/08/17/higgsfield-raises-400m-series-b-quadrupling-its-valuation-in-8-months-to-5-4b/) | en | techcrunch.com
**Ngữ cảnh:**
> oduct development. But it will also help pay for compute. “Video is one of the most compute-intensive domains in AI,” Mashrabov explained. Just one minute of video is like processing 60,000 words. Securing reliable compute capacity has therefore become a necessary expense to remain competitive with others in the industry like Synthesia and Runway.
> DST Global led the latest round, with many other investors piling in, including Goldman Sachs Alternatives, Valor Capital, and Tribe Capital.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0292 -->
## 292. edge-0292

**Triple:** Xavier Niel (PERSON) —INVESTED_IN→ Cathay Innovation (ORG)
**Assertion status:** reported
**Evidence:**
> The round was co-led by Cathay Innovation, Greycroft, Hiro Capital, HV Capital, and Bezos Expeditions, with participation from several other funds and industry-tied backers, as well as individuals, including Tim and Rosemary Berners-Lee, Jim Breyer, Mark Cuban, Mark Leslie, Xavier Niel, and Eric Schmidt.

**Article:** [Yann LeCun&#8217;s AMI Labs raises $1.03B to build world models](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/) | en | techcrunch.com
**Ngữ cảnh:**
> a’s VP for Europe Laurent Solly as COO and high-profile researchers Saining Xie as chief science officer, Pascale Fung as chief research and innovation officer, and Michael Rabbat as VP of world models.
> According to LeBrun, high interest gave the startup a chance to have its pick of investors, both in terms of expectation alignment and background. The round was co-led by Cathay Innovation, Greycroft, Hiro Capital, HV Capital, and Bezos Expeditions, with participation from several other funds and industry-tied backers, as well as individuals, including Tim and Rosemary Berners-Lee, Jim Breyer, Mark Cuban, Mark Leslie, Xavier Niel, and Eric Schmidt.
> Value-add aside, this funding will give AMI Labs some meaningful runway to bankroll its two main cost centers: compute and talent. LeBrun said he will prioritize quality over quantity to build AMI Labs’ team in four key locations: Paris, where it is headquartered; New York, where LeCun teaches at NYU; in Montreal, where its Rabbat is based; and in

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0293 -->
## 293. edge-0293

**Triple:** Pham Nhat Vuong (PERSON) —FOUNDED→ Green SM (ORG)
**Assertion status:** reported
**Evidence:**
> Vingroup, controlled by Southeast Asia’s richest man Pham Nhat Vuong, is considering building a US$500 million electric vehicle plant in the Philippines, according to that country’s Department of Trade and Industry.
> The department said in a statement Wednesday that it has held a meeting with Vingroup about the plan, and that construction could begin in the first quarter of next year and take 18 months to complete.
> The plant would have an annual production capacity of around 200,000 vehicles, and serve both the domestic and export markets, it said.
> The department has outlined support measures for Vingroup such as tax incentives and shorter application processing times.
> Vingroup has yet to comment on the information, merely saying the Philippines government wants it to build a factory to create jobs.
> Vingroup entered the Philippines through its subsidiary VinFast in May 2024, selling electric cars. Green SM, the ride-hailing company founded by Vuong, has been in the country since June last year.

**Article:** [Southeast Asia's richest man's Vingroup eyes $500M EV factory in Philippines](https://e.vnexpress.net/news/business/companies/southeast-asia-s-richest-man-s-vingroup-eyes-500m-ev-factory-in-philippines-5135642.html) | en | e.vnexpress.net
**Ngữ cảnh:**
> Southeast Asia's richest man's Vingroup eyes $500M EV factory in Philippines
> Vingroup, controlled by Southeast Asia’s richest man Pham Nhat Vuong, is considering building a US$500 million electric vehicle plant in the Philippines, according to that country’s Department of Trade and Industry.
> The department said in a statement Wednesday that it has held a meeting with Vingroup about the plan, and that construction could begin in the first quarter of next year and take 18 months to complete.
> The plant would have an annual production capacity of around 200,000 vehicles, and serve both the domestic and export markets, it said.
> The department has outlined support measures for Vingroup such as tax incentives and shorter application processing times.
> Vingroup has yet to comment on the information, merely saying the Philippines government wants it to build a factory to create jobs.
> Vingroup entered the Philippines through its subsidiary VinFast in May 2024, selling electric cars. Green SM, the ride-hailing company founded by Vuong, has been in the country since June last year.
> Vingroup has an EV factory each in Indonesia and India with a combined annual capacity of 100,000 cars.
> In the first half of this year, VinFast’s revenues were nearly VND53.2 trillion ($2.1 billion), up 61% year-on-year. It delivered 128,685 electric cars globally, an increase of 77%.
> But it reported an after-tax loss of nearly VND28.4 trillion, d

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0294 -->
## 294. edge-0294

**Triple:** General Atlantic (ORG) —INVESTED_IN→ Runway (ORG)
**Assertion status:** reported
**Evidence:**
> - Media-generation platform Runway raised a $315 million Series E round that valued the company at $5.3 billion. This funding was led by General Atlantic and was announced on February 10. Nvidia, Fidelity, and Felicis also invested, among others.

**Article:** [Here are the 17 US-based AI companies that have raised $100M or more in 2026](https://techcrunch.com/2026/02/17/here-are-the-17-us-based-ai-companies-that-have-raised-100m-or-more-in-2026/) | en | techcrunch.com
**Ngữ cảnh:**
> d was announced on February 12 and included Hanabi Capital, Bain Capital Ventures, and multiple angel investors.
> - Anthropic announced a $30 billion Series G funding round on February 12 that valued the AI research lab at $380 billion. More than 30 investors participated in the round, including Founders Fund, Coatue, and Nvidia, among many others.
> - Media-generation platform Runway raised a $315 million Series E round that valued the company at $5.3 billion. This funding was led by General Atlantic and was announced on February 10. Nvidia, Fidelity, and Felicis also invested, among others.
> - Goodfire, an AI research lab, announced a $150 million Series B round on February 5. B Capital led the round with participation from Juniper Ventures, Lightspeed Venture Partners, and Menlo Ventures. The round valued the company at $1.25 billion.
> - AI research company Fundamental announced a $255 million Series A round on February 5. This round 

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0295 -->
## 295. edge-0295

**Triple:** European Investment Bank (GOV) —CO_INVESTED_WITH→ Invest-NL (ORG)
**Assertion status:** reported
**Evidence:**
> Morphotonics has spent 12 years developing that technology, largely under the radar. Now, as demand for smart glasses and other optics surges, the company said Tuesday it has raised €40 million to scale up production and push into a new market: optical components for data centers.The round was backed by 3M Ventures, Innovation Industries, BOM, and Invest-NL. The European Innovation Council (EIC) Fund, Ernij Next (a Dutch family office), and the European Investment Bank (EIB) also participated.

**Article:** [Morphotonics raises €40M to expand its display tech into data centers](https://techcrunch.com/2026/09/21/morphotonics-raises-e40m-to-expand-its-display-tech-into-data-centers/) | en | techcrunch.com
**Ngữ cảnh:**
> ilicon wafers inside a computer chip factory known as a fab. Fellow Dutch company Morphotonics is smaller and works in a different corner of the same field: nanoimprint lithography, or NIL, a process used to manufacture the displays in AR glasses and other optics. It said it has benefited from ASML’s supply chain and uses many of the same vendors.
> Morphotonics has spent 12 years developing that technology, largely under the radar. Now, as demand for smart glasses and other optics surges, the company said Tuesday it has raised €40 million to scale up production and push into a new market: optical components for data centers.The round was backed by 3M Ventures, Innovation Industries, BOM, and Invest-NL. The European Innovation Council (EIC) Fund, Ernij Next (a Dutch family office), and the European Investment Bank (EIB) also participated.
> Morphotonics’ NIL work means the startup creates a “stamp” and applies it to photosensitive materials to create various kinds of displays, from augmented reality glasses to privacy screens for cars.
> This is useful in creating the waveguide technology used in smart glasses, including the Meta Ray-Ban Display, Even Reality, and Magic Leap. Waveguide

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0296 -->
## 296. edge-0296

**Triple:** Sparrow Capital (ORG) —CO_INVESTED_WITH→ Beenext (ORG)
**Assertion status:** reported
**Evidence:**
> The two-year-old startup said Thursday it had raised $9 million in a seed round led by Susquehanna International Group (SIG) and Lightspeed, with participation from B Capital, Seaborne Capital, Beenext, Sparrow Capital, and 2.2 Capital. The round values Gushwork at $33 million post-money, up from about $7.5 million following its Lightspeed-led $2.1 million pre-seed in July 2023, a person familiar with the matter told TechCrunch. The latest financing brings Gushwork’s total funding to $11 million, the startup said.

**Article:** [Gushwork bets on AI search for customer leads — and early results are emerging](https://techcrunch.com/2026/02/25/gushwork-bets-on-ai-search-for-customer-leads-and-early-results-are-emerging/) | en | techcrunch.com
**Ngữ cảnh:**
> As AI-powered search tools reshape how businesses are discovered online, India-founded startup Gushwork is helping companies capture customers from platforms such as ChatGPT, Gemini, and Perplexity — with early traction that is beginning to draw investor support.
> The two-year-old startup said Thursday it had raised $9 million in a seed round led by Susquehanna International Group (SIG) and Lightspeed, with participation from B Capital, Seaborne Capital, Beenext, Sparrow Capital, and 2.2 Capital. The round values Gushwork at $33 million post-money, up from about $7.5 million following its Lightspeed-led $2.1 million pre-seed in July 2023, a person familiar with the matter told TechCrunch. The latest financing brings Gushwork’s total funding to $11 million, the startup said.
> The funding comes as AI companies, including OpenAI and Perplexity, begin to chip away at traditional web search, prompting incumbents like Google to roll out AI-generated overviews and other conversational features across their search products. Gushwork is betting this shift will create a new opportunity to help businesses surface in AI-driven di

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0297 -->
## 297. edge-0297

**Triple:** Industrial and Commercial Bank of China (ORG) —CO_FINANCED_WITH→ The Export-Import Bank of China (ORG)
**Assertion status:** agreement_reported
**Evidence:**
> Tham gia giao dịch còn có các định chế tài chính phát triển gồm IFC, DEG (Đức), Proparco (Pháp) và Norfund (Na Uy); các ngân hàng xuất nhập khẩu China Eximbank, Korea Eximbank cùng nhóm ngân hàng thương mại và tổ chức tài chính như SMBC, Punjab National Bank, Commercial Bank of Ceylon, ICBC, Shinhan Bank, Woori Bank và KEXIM Asia Limited.

**Article:** [VPBank huy động 730 triệu USD vốn quốc tế](https://vnexpress.net/vpbank-huy-dong-730-trieu-usd-von-quoc-te-5143246.html) | vi | vnexpress.net
**Ngữ cảnh:**
> y động thành công khoản vay hợp vốn quốc tế 730 triệu USD, tương đương gần 19.000 tỷ đồng, do IFC và SMBC thu xếp, ngày 10/11.
> Giao dịch do Tổ chức Tài chính Quốc tế (IFC) và Ngân hàng Sumitomo Mitsui Banking Corporation (SMBC) đồng điều phối, thu xếp, gồm các khoản vay có kỳ hạn 3 năm, 5 năm và 7 năm, được giải ngân theo nhiều đợt trong năm 2026.
> Tham gia giao dịch còn có các định chế tài chính phát triển gồm IFC, DEG (Đức), Proparco (Pháp) và Norfund (Na Uy); các ngân hàng xuất nhập khẩu China Eximbank, Korea Eximbank cùng nhóm ngân hàng thương mại và tổ chức tài chính như SMBC, Punjab National Bank, Commercial Bank of Ceylon, ICBC, Shinhan Bank, Woori Bank và KEXIM Asia Limited. Sự tham gia của các tổ chức đến từ nhiều quốc gia giúp VPBank đa dạng hóa đối tác và mở rộng khả năng tiếp cận thị trường vốn quốc tế.
> Theo VPBank, nguồn vốn này sẽ được sử dụng để mở rộng tín dụng cho doanh nghiệp vừa và nhỏ (SME), đặc biệt là doanh nghiệp do phụ nữ làm chủ hoặc lãnh đạo (WSME) và doanh nghiệp hoạt động trong lĩnh vực nông nghiệp

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0298 -->
## 298. edge-0298

**Triple:** Durable Capital Partners (ORG) —INVESTED_IN→ Skyryse (ORG)
**Assertion status:** reported
**Evidence:**
> Skyryse, an El Segundo, California-based aviation automation startup, has raised more than $300 million in a Series C investment, pushing its valuation to $1.15 billion and into unicorn territory.
> The round, which was announced Tuesday and led by Autopilot Ventures, provided a multimillion-dollar accelerant for the startup as it nears the end of a lengthy Federal Aviation Administration certification process for its flight control system. The capital will also be used to integrate its operating system, known as SkyOS, across numerous aircraft, including U.S. military Black Hawk helicopters.
> Other investors in this round include Fidelity Management & Research Company, ArrowMark Partners, Atreides Management LP, BAM Elevate, Baron Capital Group, Durable Capital Partners, Positive Sum, Qatar Investment Authority, RCM Private Markets Fund managed by Rokos Capital Management, and Woodline Partners.

**Article:** [Skyryse lands another $300M to make flying, even helicopters, simple and safe](https://techcrunch.com/2026/02/03/skyryse-lands-another-300m-to-make-flying-even-helicopters-simple-and-safe/) | en | techcrunch.com
**Ngữ cảnh:**
> Skyryse, an El Segundo, California-based aviation automation startup, has raised more than $300 million in a Series C investment, pushing its valuation to $1.15 billion and into unicorn territory.
> The round, which was announced Tuesday and led by Autopilot Ventures, provided a multimillion-dollar accelerant for the startup as it nears the end of a lengthy Federal Aviation Administration certification process for its flight control system. The capital will also be used to integrate its operating system, known as SkyOS, across numerous aircraft, including U.S. military Black Hawk helicopters.
> Other investors in this round include Fidelity Management & Research Company, ArrowMark Partners, Atreides Management LP, BAM Elevate, Baron Capital Group, Durable Capital Partners, Positive Sum, Qatar Investment Authority, RCM Private Markets Fund managed by Rokos Capital Management, and Woodline Partners. The startup, which was founded in 2016, has raised more than $605 million in equity capital.
> Skyryse has made inroads with investors as well as the U.S. military, emergency medical service operators, law enforcement, and private operators for its simplified flight system. The startup has stripped out dozens of mechanical flight controls like gauge

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0299 -->
## 299. edge-0299

**Triple:** Atomico (ORG) —INVESTED_IN→ Neko Health (ORG)
**Assertion status:** historical_reported
**Evidence:**
> Other investors in Neko Health’s latest round include Atomico, General Catalyst, Lakestar, Liberty City Ventures, Positive Sum, and BDT & MSD.

**Article:** [Daniel Ek&#8217;s body-scanning startup Neko Health raises another $700M](https://techcrunch.com/2026/07/15/daniel-eks-body-scanning-startup-neko-health-raises-another-700m/) | en | techcrunch.com
**Ngữ cảnh:**
>  sure how I would have otherwise.”
> Neko Health isn’t the only health scanning company founded by tech folks. Midjourney, the AI Lab best known for its AI image and video creation model and website, is also creating a body scanner, which it plans to integrate into a spa experience with hot tubs and saunas, opening in San Francisco sometime in 2027.
> Other investors in Neko Health’s latest round include Atomico, General Catalyst, Lakestar, Liberty City Ventures, Positive Sum, and BDT & MSD.

**Verdict:** TODO
**Note:**

---

<!-- task_id: edge-0300 -->
## 300. edge-0300

**Triple:** March Capital (ORG) —CO_INVESTED_WITH→ Vista Equity Partners (ORG)
**Assertion status:** reported
**Evidence:**
> The round was led by Aramco Ventures, with participation from Vista Equity Partners, General Catalyst, Emergence Capital, Nvidia, March Capital, Pegatron, SentinelOne’s S Ventures, and others.

**Article:** [Neocloud Together AI raises $800M, leaps to $8.3B valuation](https://techcrunch.com/2026/07/01/neocloud-together-ai-raises-800m-leaps-to-8-3b-valuation/) | en | techcrunch.com
**Ngữ cảnh:**
> Together AI — an AI neocloud that rents out Nvidia GPU clusters and other AI-specific infrastructure — has raised an $800 million Series C at an $8.3 billion valuation, the company announced on Wednesday. The company was founded in 2022.
> The round was led by Aramco Ventures, with participation from Vista Equity Partners, General Catalyst, Emergence Capital, Nvidia, March Capital, Pegatron, SentinelOne’s S Ventures, and others.
> Together AI last raised a $305 million Series B at a $3.3 billion valuation about 16 months ago. It actually came out of the gate well-funded, with a $102.5 million Series A funding round led by Kleiner Perkins with participation from Nvidia and Emergence Capital back in 2023.
> There were whispers of this round back in March, when The Information r

**Verdict:** TODO
**Note:**

---
