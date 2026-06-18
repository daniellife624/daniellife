# Daniellife 個人網站 — 專案全覽

> 最後更新：2026-06-19

---

## 一、專案簡介

「Daniellife 會計丹尼」是周彥廷（NTU 會計碩士）的個人作品集兼履歷網站。
公開頁面面向求職、展示活動與作品；管理員頁面供本人管理論文筆記、財務規劃等私人資料。

---

## 二、技術棧

| 層級 | 技術 |
|------|------|
| 前端框架 | Vue 3 + TypeScript + Vite |
| 狀態管理 | Pinia (`useAuthStore`) |
| 路由 | Vue Router 4（含 Navigation Guard） |
| CSS | Scoped CSS + Design Tokens（`tokens.css`） |
| 字體 | DM Serif Display / Inter / Noto Serif TC / JetBrains Mono |
| 後端（規劃中） | FastAPI + MySQL |
| AI 整合（規劃中） | GitHub Models（GPT-4o）|

---

## 三、設計 Token（`src/assets/styles/tokens.css`）

### 顏色

| 變數 | 值 | 用途 |
|------|-----|------|
| `--color-primary` | `#E8C13A` | Navbar 背景、按鈕、Active 狀態 |
| `--color-primary-bg` | `#FDF8D8` | 淺黃色 Card 背景 |
| `--color-secondary` | `#7A8C6E` | Sage Green，程式 / S-類 / ESG 社會 |
| `--color-tertiary` | `#C17055` | Terracotta，財會 / G-類 / 美洲 |
| `--color-ink-1` | `#303030` | 主要文字 |
| `--color-ink-2` | `#5e5e5e` | 次要文字 |
| `--color-ink-3` | `#919191` | 提示 / 日期 |
| `--color-ink-4` | `#c6c6c6` | 邊框 / 分隔線 |
| `--color-white` | `#ffffff` | 背景 |

### Badge 顏色對照

| 分類 | 背景 | 字色 |
|------|------|------|
| 財會 / finance | `--color-tertiary` (`#C17055`) | `#fff` |
| 程式 / code | `--color-secondary` (`#7A8C6E`) | `#fff` |
| UIUX | `--color-primary` (`#E8C13A`) | ink-1 |
| ESG Environmental | `#E8C13A` | ink-1 |
| ESG Social | `#7A8C6E` | `#fff` |
| ESG Governance | `#C17055` | `#fff` |

### 間距 / 圓角

```
--space-1: 4px  /  --space-2: 8px  /  --space-3: 12px  /  --space-4: 16px
--space-5: 24px /  --space-6: 32px /  --space-7: 48px  /  --space-8: 64px
--space-9: 96px / --space-10: 128px

--radius-sm: 6px / --radius-md: 12px / --radius-lg: 20px / --radius-full: 9999px
--container-max: 1280px / --navbar-height: 60px
```

---

## 四、目錄結構

```
src/
├── assets/
│   └── styles/
│       └── tokens.css          # Design Tokens（全域 CSS 變數）
│
├── api/                        # Mock API 層（TODO: 替換為 apiFetch）
│   ├── client.ts               # apiFetch<T> 通用 fetch 包裝
│   ├── homepage.ts             # 首頁 5 支 API
│   ├── activities.ts           # 活動 / 旅遊 API
│   ├── social.ts               # 社會參與 API
│   ├── literature.ts           # 文學天地 API
│   ├── market.ts               # 市場消息 API（含分頁）
│   ├── finance.ts              # 理財規劃 API
│   └── thesis.ts               # 論文統整 API（CRUD）
│
├── types/                      # TypeScript 介面定義
│   ├── homepage.ts
│   ├── activities.ts
│   ├── social.ts
│   ├── literature.ts
│   ├── market.ts
│   ├── finance.ts
│   └── thesis.ts
│
├── stores/
│   └── auth.ts                 # Pinia：isLoggedIn / user / login() / logout()
│
├── router/
│   └── index.ts                # 路由表 + beforeEach 權限守衛
│
├── components/
│   ├── common/
│   │   ├── AppNavbar.vue       # 固定頂部導覽列
│   │   └── AppFooter.vue       # 頁尾
│   └── homepage/
│       ├── HeroCard.vue        # 個人卡片（Hero Section）
│       ├── InternSection.vue   # 實習經歷橫向滾動卡
│       ├── ProjectSection.vue  # 作品集 2×2 Grid + 3 Filter
│       ├── CertSection.vue     # 專業證照 3 欄 + 進度條動畫
│       ├── AcademicSection.vue # 學業歷程 SVG 曲線 + 車子動畫
│       └── FuturePlanSection.vue # 近 3 年規劃金字塔
│
├── views/
│   ├── HomeView.vue            # 首頁（組裝 6 個 Homepage 元件）
│   ├── ActivitiesView.vue      # 課外活動（領導 + 社團 + 旅遊地圖）
│   ├── SocialView.vue          # 社會參與（ESG / SDGs 篩選）
│   ├── LiteratureView.vue      # 文學天地（LED 火車時間軸 + 跑馬燈 + 作品）
│   ├── MarketView.vue          # 市場消息（新聞列表 + AI 聊天室）
│   ├── NewsView.vue            # 總經新聞（TradingView 預留 + 總經指標）
│   ├── FinanceView.vue         # 理財規劃（指標卡 + 甜甜圈圖 + 持股表）★ 需登入
│   ├── ThesisView.vue          # 論文統整（筆記 + Kanban + 文獻表）★ 需登入
│   ├── AdminView.vue           # 功能管理（殼，待開發）★ 需登入
│   ├── LoginView.vue           # 登入（殼，待開發，路徑 /danieladmin）
│   └── ForbiddenView.vue       # 403 未授權頁面
│
└── App.vue                     # AppNavbar + RouterView + AppFooter
```

---

## 五、路由表

| 路徑 | Name | View | 備註 |
|------|------|------|------|
| `/` | home | HomeView | 公開 |
| `/activities` | activities | ActivitiesView | 公開 |
| `/social` | social | SocialView | 公開 |
| `/literature` | literature | LiteratureView | 公開 |
| `/market` | market | MarketView | 公開 |
| `/news` | news | NewsView | 公開 |
| `/finance` | finance | FinanceView | **需登入** |
| `/thesis` | thesis | ThesisView | **需登入** |
| `/admin` | admin | AdminView | **需登入** |
| `/danieladmin` | login | LoginView | 隱藏登入入口 |
| `/403` | forbidden | ForbiddenView | 未授權導向 |
| `/:pathMatch(.*)` | not-found | — | redirect → `/` |

> Navigation Guard：`router.beforeEach` 偵測 `meta.requiresAuth`，未登入導向 `/403`。

---

## 六、Mock API 架構

### `src/api/client.ts`

```ts
export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T>
// 讀取 VITE_API_URL 環境變數；後端上線後取消 Mock 直接用此函式
```

### 各 API 模組

每支 API 函式都有 `// TODO: return apiFetch(...)` 佔位，後端接好後直接替換一行。

| 模組 | 匯出函式 |
|------|---------|
| `api/homepage.ts` | `getInternships()` · `getProjects()` · `getCertData()` · `getAcademicMilestones()` · `getFuturePlans()` |
| `api/activities.ts` | `getExperiences()` · `getTravelEntries()` · `groupByContinent(entries)` |
| `api/social.ts` | `getSocialActivities()` |
| `api/literature.ts` | `getTimelineEvents()` · `getLiteratureWorks()` |
| `api/market.ts` | `getNews(region, page, keyword)` → `{ items, total }` (5 筆/頁) |
| `api/finance.ts` | `getHoldings()` · `getPortfolioSummary()` |
| `api/thesis.ts` | `getThesisNote()` · `saveThesisNote(content)` · `getThesisIdeas()` · `addThesisIdea(idea)` · `updateIdeaStatus(id, status)` · `deleteThesisIdea(id)` · `getThesisPapers(topic, journal, keyword)` |

---

## 七、TypeScript 介面總表

### `types/homepage.ts`

```ts
Internship       { id, company, dept, role, period, contribution, photoUrl? }
StarItem         { label: 'S'|'T'|'A'|'R', text }
ProjectType      'code' | 'uiux' | 'finance'
Project          { id, name, type, techLabel, tech, members, period, core,
                   githubUrl?, youtubeUrl?, star: StarItem[], createdAt }
LangCert         { name, score, pct }
CertGroup        { category, items: string[] }
CertData         { language: { en: LangCert[], jp: LangCert[] },
                   finance: CertGroup[], it: CertGroup[] }
AcademicMilestone { id, school, major, period, gpa, rank, facts: string[] }
PlanPhase        'short' | 'mid-short' | 'mid'
FuturePlan       { id, phase, title, subtitle, items: string[] }
```

### `types/activities.ts`

```ts
ExperienceType  'leadership' | 'club'
Experience      { id, type, title, organization, period, contribution, photos }
TravelEntry     { id, country, city, continent, visitedAt,
                  journal?, companions?, activities?, purchases? }
Continent       { key, label, entries: TravelEntry[] }
```

### `types/social.ts`

```ts
EsgType         'Environmental' | 'Social' | 'Governance'
SdgNumber       1–17 (number)
SocialActivity  { id, name, esgType, sdgNumbers, organization, contribution,
                  periodFrom, periodTo, photoUrl?, reflection }
```

### `types/literature.ts`

```ts
TimelineEvent   { id, gradeLabel, awardTitle, result, date, workId? }
LiteratureWork  { id, title, ageWritten, period, awards, summary, fullText? }
```

### `types/market.ts`

```ts
NewsRegion      'US' | 'TAIWAN'
NewsItem        { id, title, summary, source, publishedAt, region, url? }
ChatMessage     { role: 'user'|'assistant', content }
```

### `types/finance.ts`

```ts
Currency        'TWD' | 'USD'
Holding         { id, symbol, name, currency, broker, shares, avgPrice,
                  marketPrice, currentValue, pnl, returnRate, dividend }
PortfolioSummary { twdValue, twdCost, twdPnl, twdReturnRate, twdDividend,
                   usdValue, usdCost, usdPnl, usdReturnRate, updatedAt }
```

### `types/thesis.ts`

```ts
IdeaStatus      'pending' | 'rejected' | 'approved'
ThesisNote      { content, updatedAt }
ThesisIdea      { id, title, content, status, createdAt }
ThesisPaper     { id, topic, name, journal, authors, year, purpose, contribution }
```

---

## 八、各頁面規格

### 8.1 首頁 `/` — HomeView

由 6 個 Homepage 元件垂直堆疊：

#### HeroCard
- 個人照片區 + 姓名 / 職稱 / 標語卡片
- `.hero__inner`：`background: var(--color-primary-bg)` + `border: 1px solid var(--color-primary)`
- `.hero__motto-card`：白色背景
- 社群連結 icon：目前以 18×18 黑色方塊佔位（待換成真實 SVG）

#### InternSection
- 橫向滾動 slider（`scroll-snap`）+ 右側箭頭按鈕（`scrollBy 320px`）
- 每張卡：公司 / 部門職位 / 照片佔位（`#f2ebe4`）/ 貢獻 3 行截斷 / 查看更多按鈕

#### ProjectSection
- 3 個自訂 Dropdown 篩選（類型 / 技術 / 人數），樣式：`appearance: none` + 定位 `∨`
- 2×2 CSS Grid
- Card 背景：`code`=白色、`uiux`=`primary-bg`、`finance`=`#eef1ec`
- Badge 顏色：`code`→secondary green、`uiux`→primary yellow、`finance`→tertiary
- STAR 圓圈 badge 顏色與卡片類型一致

#### CertSection
- 3 欄版面，欄間 1px 分隔線
- 語言欄：進度條動畫（IntersectionObserver 觸發，`width: 0 → lang.pct%`，1.2s ease）
- 財會 / 資訊欄：分類列表 + 方形 dot（已有=secondary green 填滿）

#### AcademicSection
- SVG `viewBox="0 0 900 300"`，立方貝塞爾曲線：
  `M 50,270 C 120,260 200,200 290,165 C 380,130 440,110 510,80 C 580,50 680,30 860,18`
- Path 動畫：`stroke-dasharray: 1500; stroke-dashoffset: 1500 → 0`（`.academic__path--drawn` class 觸發）
- 🚗 emoji：`bottom: 8%; left: 3% → bottom: 88%; left: 92%` CSS transition
- 3 個節點圓圈（座標 290,165 / 510,80 / 860,18），staggered delay 出現
- 3 張 Info 卡：`opacity: 0; translateY(16px) → 可見` on IntersectionObserver

#### FuturePlanSection
- Subtitle：「由於 AI 世代更迭迅速，先以近 3 年規劃為主」
- 金字塔三行（由寬到窄）：
  | phase | 寬度 | margin-left | 背景 / 邊框 |
  |-------|------|-------------|------------|
  | `mid` | 340px | 0 | `#fdf8d8` / `#E8C13A` |
  | `mid-short` | 260px | 40px | `#eef1ec` / `#7A8C6E` |
  | `short` | 180px | 80px | `#f8eee9` / `#C17055` |
- 每行右側：水平線 + bullet 條列

---

### 8.2 課外活動 `/activities` — ActivitiesView

**領導 / 社團經驗**
- 卡片：左（標題、服務機構、期間、貢獻 3 行截斷）+ 右（2 張照片 Grid、查看更多按鈕）
- Teleport Modal 顯示完整內容

**造訪過國家**
- 圓形地圖佔位（360×360，`border-radius: 50%`，待整合真實地圖）
- 5 洲別卡片 2×2 Grid：
  | 洲 | 顏色 |
  |----|------|
  | Europe | `#2563eb` |
  | Asia | `var(--color-primary)` |
  | Africa | `var(--color-ink-1)` |
  | Australia | `#0d9488` |
  | Americas | `var(--color-tertiary)` |

---

### 8.3 社會參與 `/social` — SocialView

- Stage 1 Tab：ESG分類 / SDGs分類（pill 樣式，`border-radius: full`）
- Stage 2 Sub-Tab（僅 ESG）：E（yellow）/ S（green）/ G（terracotta）
- 活動卡：ESG badge、組織、貢獻 2 行截斷、照片佔位、期間、查看更多
- 右側 Sidebar：ESG checkbox（Environmental / Social / Governance）+ SDGs 1–5 checkbox + 紅色計數 badge + 篩選按鈕
- 篩選邏輯：`esgSubMap = { E: 'Environmental', S: 'Social', G: 'Governance' }`
- Teleport Modal

---

### 8.4 文學天地 `/literature` — LiteratureView

**火車時間軸（LED 面板）**
- `background: #0a0a0a`，文字 `color: #00FF41`，`font-family: 'Courier New', monospace`
- 🚂 + 橫向滾動卡片（`scroll-snap`），點擊卡片 highlight（`border-color: #00FF41`）
- 每張卡：年級標籤、得獎標題、結果、日期、◄ ► 導覽按鈕、進度條（出生→現在）

**文學跑馬燈**
- `background: #303030`，白色文字，`animation: marquee 18s linear infinite`（3 份重複，translateX -33.33%）

**文學作品 Grid（2 欄）**
- 每張卡：標題列（閱讀全文按鈕）+ 4 個 metadata 行
  | Row | 背景 |
  |-----|------|
  | 幾歲撰寫 | `primary-bg`（黃） |
  | 撰寫期間 | `primary-bg`（黃） |
  | 得獎紀錄 | `#eef1ec`（綠） |
  | 摘要文字 | `#eef1ec`（綠） |

---

### 8.5 市場消息 `/market` — MarketView

**左側新聞面板**
- 搜尋列（Enter 或按鈕觸發 `doSearch()`）
- Region Tab：美股 US / 台灣 TAIWAN（底部 border-bottom 2px yellow active）
- 新聞卡（source badge + 時間 + 標題 + 摘要 2 行截斷）
- 分頁按鈕（‹ 1 2 3 ›）

**右側 AI 聊天室（UI only）**
- 標題：「AI 財經助理 / GPT-4o · GitHub Models」
- 訊息泡泡：user = `ink-1`（深色）/ assistant = `primary-bg`（黃色）
- sticky `top: var(--space-6)`，高度固定 600px
- `// TODO: call GitHub Models API (GPT-4o)` 佔位

---

### 8.6 總經新聞 `/news` — NewsView

- TradingView 股票走勢圖：2 個 260px dashed 佔位框（待整合 TradingView Widget）
- 總體經濟指標 4 欄卡片：
  - 外匯 Forex：4 個匯率對，up=`#16a34a` / down=`#dc2626`
  - 美債殖利率：2Y / 5Y / 10Y / 30Y
  - GDP 成長率：US / TW / JP / CN
  - CPI 通膨率：US / TW / JP / CN（≥2% 為 up 色）
- 底部 Mock 資料免責聲明

---

### 8.7 理財規劃 `/finance` — FinanceView（需登入）

**5 個指標卡（彩色頂部邊框）**
| 卡片 | 邊框色 |
|------|--------|
| TWD 總市值 | `primary` |
| TWD 損益 | `#16a34a` |
| TWD 累積股息 | `secondary` |
| USD 總市值 | `tertiary` |
| USD 報酬率 | `#2563eb` |

**2 個 SVG 甜甜圈圖（r=46，`stroke-width: 16`）**
- 資產配置：TWD（primary yellow）/ USD（tertiary）
- 券商分布：國泰世華（secondary green）/ 富邦（`#2563eb`）
- 比例動態計算自持股資料

**持股明細表（11 欄）**
- 欄位：股票代碼、名稱、幣別（badge）、券商、股數、均價、市價、市值、損益、報酬率、累積股息
- 虧損 = `#dc2626`，獲利 = `#16a34a`
- Mock 真實持股：00713、00881、00922、奈米投 L1/L2/L3

---

### 8.8 論文統整 `/thesis` — ThesisView（需登入）

**碩論筆記（可收合）**
- 黃色 Collapsible Header，展開後顯示筆記內容 + 「編輯」按鈕
- 編輯模式：`<textarea>` + 取消 / 儲存按鈕
- `saveThesisNote()` Mock 本地更新（待接後端 PUT API）

**論文想法 Kanban（3 欄）**
| 欄 | Header 背景 / 邊框 |
|----|-------------------|
| 待審核 pending | `primary-bg` / primary yellow |
| 已拒絕 rejected | `#fef2f2` / `#dc2626` |
| 已核准 approved | `#f0fdf4` / `#16a34a` |

- 每張 Card：標題、內容 3 行截斷、日期、× 刪除、狀態切換按鈕
- ＋ 新增想法：Teleport Modal，含標題 input + 內容 textarea

**文獻清單表格（7 欄）**
- 欄位：主題（topic badge）、論文名稱、期刊、作者、年份、研究目的、主要貢獻
- 關鍵字搜尋篩選（`getThesisPapers(topic, journal, keyword)`）

---

## 九、Auth 與導覽列

### `stores/auth.ts`
- `isLoggedIn: boolean`
- `user: { name, email } | null`
- `login(userData)` / `logout()`

### AppNavbar
- 固定頂部，`background: var(--color-primary)`（黃色）
- Logo：白色方塊 + "D" 字
- 未登入：顯示 5 個公開連結
- 已登入：額外顯示 論文統整 / 理財規劃 / 功能管理
- RWD：< 768px 隱藏桌面 Nav，顯示漢堡選單

---

## 十、已完成 / 待辦事項

### ✅ 已完成

- [x] Design Token 系統（`tokens.css`）
- [x] TypeScript 介面定義（7 個型別檔）
- [x] Mock API 層（7 個模組，含 `client.ts`）
- [x] Pinia Auth Store
- [x] Vue Router（含 Navigation Guard）
- [x] AppNavbar（含 RWD 漢堡選單）
- [x] AppFooter
- [x] HomeView（HeroCard + InternSection + ProjectSection + CertSection + AcademicSection + FuturePlanSection）
- [x] ActivitiesView（領導 + 社團 + 旅遊地圖）
- [x] SocialView（ESG / SDGs 篩選 + Modal）
- [x] LiteratureView（LED 火車時間軸 + 跑馬燈 + 文學作品）
- [x] MarketView（新聞分頁 + AI 聊天室 UI）
- [x] NewsView（TradingView 佔位 + 總經指標 4 欄）
- [x] FinanceView（指標卡 + SVG 甜甜圈 + 持股表）
- [x] ThesisView（筆記 + Kanban + 文獻表）

### ⏳ 待開發（前端）

- [ ] LoginView — 登入表單（連接 `auth.login()`）
- [ ] AdminView — 功能管理頁
- [ ] ForbiddenView — 403 美化頁面
- [ ] HeroCard SVG icons（Instagram / LinkedIn，目前為黑色佔位方塊）
- [ ] ActivitiesView 旅遊地圖（整合真實地圖 API）
- [ ] NewsView TradingView Widget 真實整合
- [ ] MarketView AI 聊天室接通 GitHub Models（GPT-4o）

### ⏳ 待開發（後端 FastAPI + MySQL）

- [ ] 建立 FastAPI 專案結構
- [ ] 設計 MySQL Schema（依各 TypeScript interface 對應）
- [ ] 實作所有 REST API 端點
- [ ] 設定 `VITE_API_URL` 環境變數
- [ ] 將所有 `// TODO: return apiFetch(...)` 換成真實呼叫
- [ ] JWT 認證（取代目前純前端 Pinia Auth）

---

## 十一、環境變數

| 變數 | 說明 |
|------|------|
| `VITE_API_URL` | FastAPI 後端 Base URL（例：`http://localhost:8000`），未設定時 fallback 為 `''` |

---

## 十二、Mock 資料摘要（目前狀態）

| 資料 | 內容 |
|------|------|
| 實習 | 國泰信（2023）、KPMG（2024）、XXXX（2025，待補） |
| 作品集 | Meetro 相遇地圖×3、存貨流程自動化×1 |
| 語言證照 | TOEIC 865、劍橋英檢 B2+、JLPT N4 |
| 財會證照 | 高級會計師、記帳士（其餘待補） |
| 學業歷程 | 專科中科大→大學中央財金→碩士臺大會計 |
| 持股 | 00713（264股）、00881（281股）、00922（352股）、奈米投 L1/L2/L3 |
| 論文想法 | 3 則（pending / approved / rejected 各 1）|
| 文獻 | 1 篇（LLM × JAE 2025，Bertomeu et al.）|
