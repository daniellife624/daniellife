# Daniellife 個人網站 — 專案全覽

> 最後更新：2026-06-19（本 session 同步）

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
| 地圖 | Leaflet + topojson-client（世界地圖 + 訪國高亮） |
| 後端 | FastAPI 0.111 + SQLAlchemy 2.0 + PyMySQL |
| 資料庫 | MySQL（XAMPP MariaDB 相容）|
| 認證 | JWT（python-jose + passlib bcrypt） |
| AI 整合（待串接） | GitHub Models（GPT-4o）|

### npm 套件（非標準 Vite 預設）

| 套件 | 版本 | 用途 |
|------|------|------|
| `leaflet` | latest | ActivitiesView 世界地圖 |
| `@types/leaflet` | latest | TypeScript 型別 |
| `topojson-client` | latest | TopoJSON → GeoJSON 轉換 |
| `@types/topojson-client` | latest | TypeScript 型別 |

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
│       └── tokens.css              # Design Tokens（全域 CSS 變數）
│
├── api/                            # Mock API 層（TODO: 替換為 apiFetch）
│   ├── client.ts                   # apiFetch<T> 通用 fetch 包裝
│   ├── auth.ts                     # mockLogin()（讀取 .env.local 驗證）
│   ├── homepage.ts                 # 首頁 5 支 API
│   ├── activities.ts               # 活動 / 旅遊 API
│   ├── social.ts                   # 社會參與 API
│   ├── literature.ts               # 文學天地 API
│   ├── market.ts                   # 市場消息 API（新聞分頁）
│   ├── finance.ts                  # 理財規劃 API
│   └── thesis.ts                   # 論文統整 API（CRUD）
│
├── types/                          # TypeScript 介面定義
│   ├── homepage.ts
│   ├── activities.ts
│   ├── social.ts
│   ├── literature.ts
│   ├── market.ts
│   ├── finance.ts
│   └── thesis.ts
│
├── stores/
│   └── auth.ts                     # Pinia：isLoggedIn / user / login() / logout()
│
├── router/
│   └── index.ts                    # 路由表 + beforeEach 權限守衛
│
├── components/
│   ├── common/
│   │   ├── AppNavbar.vue           # 固定頂部導覽列（Logo 圓形）
│   │   └── AppFooter.vue           # 頁尾（精簡 padding）
│   ├── admin/
│   │   └── AdminTable.vue          # 通用 CRUD 表格元件（props: title/columns/rows/ids）
│   ├── market/
│   │   └── MarketOverviewPanel.vue # 大盤行情元件（TW/ASIA/EU/US Tab + OHLC + SVG 折線）
│   └── homepage/
│       ├── HeroCard.vue            # 個人卡片 3 欄（左資訊 / 中照片圈 / 右格言）
│       ├── InternSection.vue       # 實習橫向 slider + Teleport 詳情 Modal
│       ├── ProjectSection.vue      # 作品集 2×2 Grid + 3 Filter
│       ├── CertSection.vue         # 專業證照 3 欄 + 進度條動畫
│       ├── AcademicSection.vue     # 學業歷程 SVG 曲線 + 車子動畫
│       └── FuturePlanSection.vue   # 近 5 年規劃金字塔
│
├── views/
│   ├── HomeView.vue                # 首頁（組裝 6 個 Homepage 元件）
│   ├── ActivitiesView.vue          # 課外活動（領導 + 社團 + Leaflet 地圖 + 3 個 Teleport Modal）
│   ├── SocialView.vue              # 社會參與（ESG / SDGs 篩選）
│   ├── LiteratureView.vue          # 文學天地（台鐵風格白底 火車時間軸 + 作品）
│   ├── MarketView.vue              # 市場資訊（大盤 + Forex + FRED + World Bank）
│   ├── NewsView.vue                # 總經新聞（新聞分頁 + AI 聊天室）
│   ├── FinanceView.vue             # 理財規劃（指標卡 + SVG 甜甜圈 + 持股表）★ 需登入
│   ├── ThesisView.vue              # 論文統整（筆記 + Kanban + 文獻表）★ 需登入
│   ├── AdminView.vue               # 功能管理（深色側欄 + AdminTable CRUD）★ 需登入
│   ├── LoginView.vue               # 登入（/danieladmin，讀取 .env.local 驗證）
│   └── ForbiddenView.vue           # 403 未授權頁面
│
├── App.vue                         # AppNavbar + RouterView + AppFooter + 全站回到頂端按鈕
└── index.html                      # Favicon：SVG inline，圓形黃底 D（垂直水平置中）
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

### `src/api/auth.ts`

```ts
const ADMIN_EMAIL = import.meta.env.VITE_ADMIN_EMAIL ?? 'admin@daniellife.com'
const ADMIN_PASSWORD = import.meta.env.VITE_ADMIN_PASSWORD ?? 'changeme'
export async function mockLogin(email, password): Promise<{ ok: boolean; name: string; email: string }>
// TODO: 後端上線後改為 POST /api/auth/login → { token }
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

### `types/activities.ts`

```ts
ExperienceType  'leadership' | 'club'
Experience      { id, type, title, organization, period, contribution, photos }
TravelEntry     { id, country, city, continent, visitedAt,
                  journal?, companions?, activities?, purchases? }
Continent       { key, label, entries: TravelEntry[] }
```

（其餘型別見原始 `src/types/*.ts`，未在此次 session 變動）

---

## 八、各頁面規格

### 8.0 全站共用

#### App.vue — 回到頂端按鈕

- `window.scrollY > 300` 時浮現右下角圓形按鈕（44×44px，黃邊框白底）
- `fade-up` Transition 動畫（opacity + translateY）
- hover 變黃底
- 點擊 `window.scrollTo({ top: 0, behavior: 'smooth' })`

#### Favicon（`index.html`）

```html
<link rel="icon" href="data:image/svg+xml,<svg ...>
  <rect fill='%23E8C13A' rx='50'/>
  <text x='50' y='50' dominant-baseline='central' text-anchor='middle' ...>D</text>
</svg>">
```
- 圓形黃底，「D」水平 + 垂直置中（`dominant-baseline='central'`）

---

### 8.1 首頁 `/` — HomeView

#### HeroCard（3 欄版面）

```
左欄                中欄                         右欄
──────              ──────────────────           ──────────────────
姓名（26px）        96px 圓形照片×2              白色格言卡片
台北/臺中/男/特質   （background: ink-2）         「你不需要很厲害才能開始
職務標籤列          社群連結 icon 列              但至少要勇於嘗試」
```

**社群連結（已更正）：**

| 平台 | URL |
|------|-----|
| Instagram | `https://www.instagram.com/_daniellife_` |
| LinkedIn | `https://www.linkedin.com/in/yenting2003` |

#### InternSection
- 橫向滾動 slider（`scroll-snap`）+ 右側 `›` 箭頭（`scrollBy 320px`）
- 每張卡：公司 / 部門職位 / 照片佔位 / 貢獻 3 行截斷 / 查看更多按鈕
- **查看更多**：Teleport Modal，顯示完整資訊

#### ProjectSection
- 3 個自訂 Dropdown 篩選（類型 / 技術 / 人數）
- 2×2 CSS Grid，Badge 顏色依 type

#### CertSection
- 3 欄，語言欄進度條動畫（IntersectionObserver）

#### AcademicSection
- SVG `viewBox="0 0 900 300"` 曲線 + 🚗 動畫 + 節點圓圈

#### FuturePlanSection
- 近 5 年金字塔三行（short / mid-short / mid）

---

### 8.2 課外活動 `/activities` — ActivitiesView

**領導 / 社團經驗**
- 卡片：左（標題、服務機構、期間、貢獻 3 行截斷）+ 右（2 張照片 Grid、查看更多）
- Teleport Modal：顯示完整內容

**造訪過國家 — Leaflet 世界地圖**

- **地圖容器**：440×380px 矩形（≤1024px 響應為 100% × 320px）
- **資料來源**：`https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json`（TopoJSON，~100KB）
- **轉換**：`topojson.feature()` → GeoJSON Layer 交給 Leaflet
- **互動**：zoom（+/−鍵）+ drag 啟用，scroll wheel 禁用（不攔截頁面滾動）
- **訪過的國家**：填黃色 `#E8C13A`，hover 深黃 `#c9a500`，cursor pointer
- **未訪國家**：填灰色 `#d1d5db`
- **Country Code 對照表**（ISO 3166-1 numeric）：

| 中文 | ISO numeric |
|------|------------|
| 臺灣 / 台灣 | 158 |
| 日本 | 392 |
| 澳大利亞 | 36 |
| 美國 | 840 |
| 英國 | 826 |
| 法國 | 250 |
| 德國 | 276 |
| 韓國 | 410 |
| 中國 | 156 |
| 泰國 | 764 |
| 新加坡 | 702 |
| 義大利 | 380 |
| 西班牙 | 724 |
| 加拿大 | 124 |

- **點擊國家** → 開啟 TravelEntry Teleport Modal（人事時地物）
- fetch 失敗時靜默 fallback（空白地圖，不 crash）

**5 洲別卡片**

| 洲 | key | 顏色 |
|----|-----|------|
| 歐洲 | Europe | `#2563eb` |
| 亞洲 | Asia | `#E8C13A` |
| 非洲 | Africa | `#303030` |
| 澳洲 | Australia | `#0d9488` |
| 美洲 | Americas | `#C17055` |

- 點擊國家條目 → Travel Modal（viewEntry）
- 點擊「新增國家、見聞」→ **新增旅行日記 Modal**

**新增旅行日記 Modal（人事時地物）**

- 標題：「地區（自動帶入）：{洲名}」（以 `CONT_ZH` 對應中文）
- 顏色繼承洲別（`--accent` + `--accent-text` CSS 自訂屬性傳入 modal）
- 5 個輸入列（底線樣式）：

  | icon | 欄位 | placeholder |
  |------|------|-------------|
  | 人 | companions | 和誰一起去？ |
  | 事 | activities | 做了什麼有趣的事情？ |
  | 時 | visitedAt | 詳細的時間點？ |
  | 地 | city | 去 {洲} 的哪個國家？哪座城市？ |
  | 物 | purchases | 有沒有買什麼東西？ |

- 4 格照片上傳（dashed 虛線框 → file input → ObjectURL 預覽）
- 「新增旅行日記」送出按鈕（TODO: POST 後端）
- icon 圓圈、送出按鈕、focus 底線、洲名文字顏色全部繼承 `--accent`

---

### 8.3 社會參與 `/social` — SocialView

- Stage 1 Tab：ESG分類 / SDGs分類（pill 樣式）
- Stage 2 Sub-Tab（僅 ESG）：E（yellow）/ S（green）/ G（terracotta）
- 活動卡 + ESG badge + Teleport Modal
- 右側 Sidebar：checkbox 篩選

---

### 8.4 文學天地 `/literature` — LiteratureView

**整體色調：白底台鐵懷舊風**

- 主背景：`#faf9f7`（暖白）
- 鐵道區塊背景：`#f5f2ee`（羊皮紙色）

**火車時間軸**

- 枕木（crossties）：`rgba(120, 90, 58, 0.45)` repeating-linear-gradient
- 雙軌（上下）：`2.5px solid #8a8a8a`（鐵灰色）
- 已走過路段（rail-fill）：黃色雙軌 + 淡黃填色
- 🚂 火車 emoji + `easeInOut` 動畫（DURATION 3800ms）+ IntersectionObserver（進入 viewport 觸發）
- 導覽按鈕 ◄ ►：點擊滾動至前/後站

**站牌卡片（light 版）**

| 元素 | 顏色 |
|------|------|
| card 邊框 | `#d8cfc4` |
| card-top 背景 | `#fffbf4`（奶油色） |
| 年級標籤 | `var(--color-ink-3)` |
| 得獎標題 | `var(--color-ink-1)` |
| 得獎結果 | `#8b6200`（深琥珀） |
| card-bottom 背景 | `#f0ebe2` |
| 連接柱 | `#c4b8a8` → 已到達 `#a89880` |
| 軌道圓點 | `#e0d8cc` / `#b8a88a` → 已到達黃色 |

**文學作品（台鐵時刻板風格 · 白底）**

| 元素 | 顏色 |
|------|------|
| card 背景 | `#ffffff` |
| card 邊框 | `#e0d8cc` |
| header 背景 | `var(--color-primary)` 黃色 |
| header 標題文字 | `#1a1000`（深色，高對比） |
| 閱讀全文按鈕 | `#15803d` 邊框 + 文字 |
| 欄位標籤背景 | `#f5f0e8` |
| 年份值（--yellow） | `#7a5800`（深琥珀） |
| 得獎值（--green） | `#166534`（深綠） |

---

### 8.5 市場資訊 `/market` — MarketView

**Section 1：股票市場**

- 使用 `MarketOverviewPanel.vue` 元件（`src/components/market/MarketOverviewPanel.vue`）
- 兩個 Panel：`defaultTab="TW"` 和 `defaultTab="US"`
- Props：`defaultTab?: 'TW' | 'ASIA' | 'EU' | 'US'`
- 內部：Tab 切換 + 指數列表（left 42%）+ OHLC 詳情 + SVG sparkline（right 58%）
- 資料：嘗試 Yahoo Finance `query2.finance.yahoo.com`（CORS 實驗性）；失敗時靜默 fallback mock data
- mock data 用 `genIntraday(price, chg, n=48)` 生成 sin/cos noise 折線
- SVG gradient ID 含 `uid` 避免多 Panel 衝突

**Section 2：外匯市場**

- TradingView `embed-widget-mini-symbol-overview.js`（免費 tier）
- 3 個 widget：`FX_IDC:USDTWD` / `FX_IDC:JPYTWD` / `FX_IDC:EURTWD`
- colorTheme: 'light'，height: 300px

**Section 3：利率與殖利率**

- FRED St. Louis Fed iframes（height: 520px，無 scrolling=no）
- `DGS10`：美國 10 年期公債殖利率
- `FEDFUNDS`：Fed 聯邦基金目標利率
- URL 格式：`https://fred.stlouisfed.org/graph/?id=FEDFUNDS&cosd=2010-01-01`
- **注意**：不要在 FRED URL 加多餘 params（`fq=`, `fam=` 等），否則月頻指標顯示 sad face 錯誤

**Section 4：其他總經重要指標**

- World Bank Open Data API（CORS 友好，免 key）
- **國家切換按鈕**：🇺🇸 美國 / 🇹🇼 台灣（`wbCountry` ref，切換後重新 fetch）
- GDP 年增率：`NY.GDP.MKTP.KD.ZG`
- CPI 通膨率：`FP.CPI.TOTL.ZG`
- 自製 CSS 垂直長條圖：正值藍色、負值紅色、CPI 黃色
- `fetchWB(indicator, country)` → `country` 預設 `'US'`，可傳 `'TW'`

---

### 8.6 總經新聞 `/news` — NewsView

**左側新聞面板**
- 搜尋列（Enter / 按鈕觸發 `doSearch()`）
- Region Tab：US / TAIWAN
- **TAIWAN tab 警告 banner**：黃色 ⚠ 通知，說明目前為 Guardian API 暫時替代，正式版需後端串接 ITIS
- 新聞卡：title → summary（stripHtml） → footer（時間、來源 badge）
- 分頁（PAGE_SIZE = 5）

**資料來源（Guardian Open Platform API）**

```
GUARDIAN_KEY = 'test'（開發用）
US tab:     section=business&q=economy finance
TAIWAN tab: q=taiwan economy finance（暫時，最終換 ITIS）
```

**ITIS 整合（待後端）**

- URL：`https://itisweb2.itis.org.tw/ITIS_Publish/ITISNews_New_One.asp?td=YYYY/M/D`
- CORS 限制 + HTML-only，需後端 proxy
- 後端路由：`GET /api/news/taiwan?date=YYYY-M-D` → 爬 ITIS → 回 JSON

**右側 AI 聊天室（UI only）**

- 標題：「Daniellife 會計丹尼」，D 圓圈 icon
- 氣泡：user=深色 / assistant=黃色半透明
- `position: sticky; top: var(--space-6)`
- `// TODO: call GitHub Models API (GPT-4o)` 佔位

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
- 券商分布：國泰世華（secondary）/ 富邦（`#2563eb`）

**持股明細表（11 欄）**
- 欄位：股票代碼、名稱、幣別（badge）、券商、股數、均價、市價、市值、損益、報酬率、累積股息
- 虧損 = `#dc2626`，獲利 = `#16a34a`

---

### 8.8 論文統整 `/thesis` — ThesisView（需登入）

**碩論注意事項（可收合）**
- 黃色 Collapsible Header（「碩論注意事項、教授建議」）
- 展開後顯示筆記 + 「編輯」按鈕
- 編輯模式：`<textarea>` + 取消 / 儲存

**碩論靈感 Kanban（3 欄，便利貼拖曳）**

| 欄 | status | label |
|----|--------|-------|
| 左 | pending | 待確認（重量提） |
| 中 | rejected | 被拒絕 / 不可執行 |
| 右 | approved | 可以執行 |

- 便利貼樣式：`background: #fffde7`，cursor grab，`box-shadow`
- HTML5 Drag & Drop（`draggable`, `@dragstart`, `@dragover.prevent`, `@drop`）
- `＋ 新增便利貼` 開 modal

**參考文獻統整（篩選 + Notion 連結）**
- Topic / Journal Dropdown 篩選（client-side computed）
- Notion 連結按鈕（黑底白 N，placeholder alert）
- 表格欄位：作者+年份（合欄）、論文名稱、期刊、研究目的、研究貢獻

---

### 8.9 功能管理 `/admin` — AdminView（需登入）

**版面**
- 深色左側欄（`background: var(--color-ink-1)`）：7 個區塊切換 + 登出
- 右側：`AdminTable` 元件

**7 個資料區塊**：實習經歷、作品集、課外活動、社會參與、文學作品、論文文獻、持股資料

**AdminTable（`src/components/admin/AdminTable.vue`）**
```ts
Props: title, columns, rows, ids
Emits: add, edit(id), delete(id)
```

---

### 8.10 登入 `/danieladmin` — LoginView

- 黃色邊框卡片，呼叫 `mockLogin(email, password)`（讀取 `.env.local`）
- 登入成功 → `auth.login()` → redirect `/admin`

---

### 8.11 未授權 `/403` — ForbiddenView

- 大型「403」字樣（96px，primary 黃色）
- 按鈕：前往登入 / 回首頁

---

## 九、Auth 與導覽列

### `stores/auth.ts`
- `isLoggedIn`, `user: { name, email } | null`
- `login(userData)` / `logout()`

### AppNavbar
- 固定頂部，`background: var(--color-primary)`
- Logo：圓形（`border-radius: 50%`），文字 "D"
- 未登入：5 個公開連結；已登入：額外顯示論文/理財/功能管理
- RWD < 768px：漢堡選單

### AppFooter
- `background: var(--color-ink-1)`，精簡 padding

---

## 十、已完成 / 待辦事項

### ✅ 已完成

- [x] Design Token 系統（`tokens.css`）
- [x] TypeScript 介面定義（7 個型別檔）
- [x] Mock API 層（8 個模組）
- [x] Pinia Auth Store + Vue Router（Navigation Guard）
- [x] AppNavbar（圓形 Logo、RWD）、AppFooter
- [x] **全站回到頂端按鈕**（App.vue，scroll > 300px 浮現）
- [x] **Favicon D 垂直水平置中**（`dominant-baseline='central'`）
- [x] HomeView（HeroCard + 5 個子元件）
- [x] **HeroCard 社群連結修正**（Instagram: `_daniellife_`、LinkedIn: `yenting2003`）
- [x] **座右銘更新**：「你不需要很厲害才能開始 / 但至少要勇於嘗試」
- [x] ActivitiesView（領導 + 社團 + **Leaflet 世界地圖** + 3 個 Modal）
- [x] **造訪地圖互動**（hover 高亮、click → TravelEntry modal、zoom/drag）
- [x] **新增旅行日記 popup**（人事時地物 form + 4 格照片上傳 + 洲別顏色繼承）
- [x] SocialView（ESG / SDGs 篩選 + Modal）
- [x] **LiteratureView 白底台鐵懷舊風**（全面改色，移除暗色背景）
- [x] MarketView（MarketOverviewPanel + TradingView Forex + FRED + World Bank）
- [x] **總經指標 美國 / 台灣 切換**（World Bank API，`wbCountry` 切換）
- [x] NewsView（新聞分頁 + AI 聊天室 UI + **ITIS 警告 banner**）
- [x] FinanceView（指標卡 + SVG 甜甜圈 + 持股表）★
- [x] ThesisView（便利貼 Kanban + drag-drop + 文獻篩選 + Notion 按鈕）★
- [x] LoginView（`/danieladmin`）、ForbiddenView、AdminView + AdminTable ★


- [x] **FastAPI 後端骨架**（28 個 endpoint、JWT、CORS、lifespan `create_all`）
- [x] **MySQL Schema**（15 張資料表，SQLAlchemy ORM auto-create）
- [x] **JWT 認證**（POST /api/auth/login → Bearer token，localStorage 持久化）
- [x] **前後端串接**：activities / finance / thesis 換成真實 apiFetch
- [x] **seed.py**（一鍵填入所有 mock 初始資料）

### ⏳ 待開發（前後端）

- [ ] NewsView AI 聊天室接通 GitHub Models（GPT-4o）
- [ ] Notion OAuth 串接（ThesisView 文獻同步）
- [ ] 旅遊照片上傳持久化（目前 ObjectURL，需後端 file upload endpoint）
- [ ] ITIS HTML proxy：`GET /api/news/taiwan?date=YYYY-M-D`
- [ ] Homepage / Social / Literature API 串接（目前仍用 mock data）

### ⏳ 待部署

- [ ] Docker（前後端穩定後建立）

---

## 十一、MySQL 資料庫 Schema

> Engine: InnoDB / Charset: utf8mb4_unicode_ci
> 由 SQLAlchemy `Base.metadata.create_all()` 在首次啟動時自動建立。
> 15 張表，`timeline_events.work_id → literature_works.id` 為唯一 FK；其餘無跨表約束。

### 正規化說明

| 層級 | 狀態 | 說明 |
|------|------|------|
| 1NF | ⚠️ 部分 JSON | `photos` / `tech` / `links` 存為 JSON 字串（`TEXT`），非原子值 |
| 2NF | ✅ | 無部分依賴 |
| 3NF | ✅ | 無遞移依賴 |
| FK  | ⚠️ 部分 FK | `timeline_events.work_id → literature_works.id`（nullable）；其餘單用戶無需跨表約束 |

---

### `users`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `name` | VARCHAR(100) NOT NULL | 顯示名稱 |
| `email` | VARCHAR(255) NOT NULL UNIQUE | 登入帳號，index |
| `hashed_password` | VARCHAR(255) NOT NULL | bcrypt hash |
| `created_at` | DATETIME | server_default NOW() |

---

### `internships`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `company` | VARCHAR(200) NOT NULL | 公司名稱 |
| `department` | VARCHAR(200) NOT NULL | 部門 + 職稱 |
| `start_date` | DATE NULL | 開始月份（日固定為 01）|
| `end_date` | DATE NULL | 結束月份；NULL 表示「至今」|
| `contribution` | TEXT NOT NULL | 貢獻描述 |
| `photos` | TEXT default `[]` | JSON 字串陣列（圖片 URL）|

> API 回傳額外計算欄位 `period: str`（如 `"2024/07 – 2024/09"`），由 start/end 格式化。

---

### `projects`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `title` | VARCHAR(200) NOT NULL | 專案名稱 |
| `type` | VARCHAR(20) NOT NULL | `finance` \| `code` \| `UIUX` |
| `tech` | TEXT default `[]` | JSON 字串陣列（技術標籤）|
| `people` | INT default 1 | 團隊人數 |
| `summary` | TEXT NOT NULL | 簡介 |
| `links` | TEXT default `[]` | JSON 字串陣列（GitHub / YouTube URL）|

---

### `cert_items`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `category` | VARCHAR(20) NOT NULL | `language` \| `finance` |
| `name` | VARCHAR(200) NOT NULL | 證照名稱（如 `TOEIC`）|
| `level` | VARCHAR(100) NULL | 等級 / 分數（如 `865`、`N4`）|
| `progress` | INT default 0 | 進度百分比（0–100）|

---

### `academic_milestones`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `label` | VARCHAR(200) NOT NULL | 學校名稱 |
| `sublabel` | VARCHAR(200) NOT NULL | 科系 |
| `year` | VARCHAR(10) NOT NULL | 年份 |
| `x` | DOUBLE NOT NULL | SVG 曲線 x 座標 |
| `y` | DOUBLE NOT NULL | SVG 曲線 y 座標 |

---

### `future_plans`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `horizon` | VARCHAR(20) NOT NULL | `short` \| `mid-short` \| `mid` |
| `content` | TEXT NOT NULL | 計畫內容 |
| `order` | INT default 0 | 顯示順序 |

---

### `experiences`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `type` | VARCHAR(20) NOT NULL | `leadership` \| `club` |
| `title` | VARCHAR(200) NOT NULL | 職務 / 社團名稱 |
| `organization` | VARCHAR(200) NOT NULL | 組織 / 學校 |
| `start_date` | DATE NULL | 開始月份（日固定為 01）|
| `end_date` | DATE NULL | 結束月份；NULL 表示「至今」|
| `contribution` | TEXT NOT NULL | 貢獻描述 |
| `photos` | TEXT default `[]` | JSON 字串陣列（圖片 URL）|

> API 接受 `period: str`（前端傳 `"YYYY/MM – YYYY/MM"`），後端自動拆解成 start/end 儲存。
> 回傳時亦包含 `startDate` / `endDate`（ISO）與計算欄位 `period`。

---

### `travel_entries`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `country` | VARCHAR(100) NOT NULL | 國家（中文，如 `日本`）|
| `city` | VARCHAR(100) NOT NULL | 城市 |
| `continent` | VARCHAR(50) NOT NULL | 洲別 key（`Asia` / `Europe` / …）|
| `visited_at` | DATE NOT NULL | 到訪日期；API 回傳 ISO `"YYYY-MM-DD"` |
| `journal` | TEXT NULL | 旅行日記 |
| `companions` | TEXT NULL | 同行者（人）|
| `activities` | TEXT NULL | 做了什麼（事）|
| `purchases` | TEXT NULL | 購買了什麼（物）|
| `photos` | TEXT default `[]` | JSON 字串陣列（圖片 URL）|

---

### `social_activities`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `name` | VARCHAR(200) NOT NULL | 活動名稱 |
| `organization` | VARCHAR(200) NOT NULL | 主辦 / 合作組織 |
| `esg_type` | VARCHAR(20) NOT NULL | `Environmental` \| `Social` \| `Governance` |
| `sdg_numbers` | TEXT default `[]` | JSON 整數陣列（如 `[3, 13]`），SDG 編號 1–17 |
| `period_from` | DATE NOT NULL | 開始日期 |
| `period_to` | DATE NULL | 結束日期；NULL 表示單日或持續中 |
| `contribution` | TEXT NOT NULL | 具體貢獻 |
| `reflection` | TEXT NOT NULL default `""` | 個人反思 |
| `photo_url` | VARCHAR(500) NULL | 封面圖片 URL |

---

### `timeline_events`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `grade_label` | VARCHAR(100) NOT NULL | 就讀階段（如 `高中 / 高一`）|
| `award_title` | VARCHAR(200) NOT NULL | 獎項 / 賽事名稱 |
| `result` | VARCHAR(100) NOT NULL | 得獎結果（如 `散文組 佳作`）|
| `date` | DATE NOT NULL | 比賽 / 頒獎日期；API 回傳 `"YYYY.MM.DD"` |
| `work_id` | INT NULL FK | → `literature_works.id`；可連結對應作品 |

---

### `literature_works`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `title` | VARCHAR(200) NOT NULL | 作品名稱 |
| `age_written` | INT NULL | 創作時年齡 |
| `period` | DATE NULL | 創作月份（日固定 01）；API 回傳 `"YYYY.MM"` |
| `awards` | TEXT NOT NULL default `""` | 得獎紀錄（完整描述字串）|
| `summary` | TEXT NOT NULL | 摘要 / 節錄（卡片顯示）|
| `full_text` | TEXT NULL | 全文（可選）|

---

### `holdings`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `symbol` | VARCHAR(20) NOT NULL | 股票代碼（如 `00713`）|
| `name` | VARCHAR(200) NOT NULL | 股票名稱 |
| `currency` | VARCHAR(5) NOT NULL | `TWD` \| `USD` |
| `broker` | VARCHAR(100) NOT NULL | 券商（如 `國泰世華`）|
| `shares` | DOUBLE NOT NULL | 持股數量 |
| `avg_price` | DOUBLE NOT NULL | 平均成本價 |
| `market_price` | DOUBLE NOT NULL | 現價（手動更新）|
| `dividend` | DOUBLE default 0 | 累計股息 |

> 計算欄位（不存 DB，由 Pydantic `@computed_field` 回傳）：
> `currentValue = shares × market_price`、`pnl = (market_price − avg_price) × shares`、`returnRate = pnl / (avg_price × shares) × 100`

---

### `thesis_notes`（singleton）

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | 永遠只有 1 筆 |
| `content` | TEXT NOT NULL | 碩論筆記 Markdown |
| `updated_at` | DATETIME | server_default NOW() + onupdate |

---

### `thesis_ideas`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `title` | VARCHAR(200) NOT NULL | 便利貼標題 |
| `content` | TEXT NOT NULL | 想法內容 |
| `status` | VARCHAR(20) NOT NULL default `pending` | `pending` \| `approved` \| `rejected` |
| `created_at` | DATETIME | server_default NOW() |

---

### `thesis_papers`

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INT PK AUTO | |
| `topic` | VARCHAR(100) NOT NULL | 主題標籤（如 `LLM`）|
| `name` | TEXT NOT NULL | 論文完整標題 |
| `journal` | VARCHAR(300) NOT NULL | 期刊名稱 |
| `authors` | VARCHAR(500) NOT NULL | 作者列表 |
| `year` | INT NOT NULL | 發表年份 |
| `purpose` | TEXT NOT NULL | 研究目的 |
| `contribution` | TEXT NOT NULL | 研究貢獻 |

---

## 十二、環境變數

### 前端（`src/.env.local`，不 commit）

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `VITE_API_URL` | `http://localhost:8000` | FastAPI Base URL |

### 後端（`backend/.env`，不 commit）

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `DATABASE_URL` | `mysql+pymysql://root:@localhost:3306/daniellife` | MySQL 連線字串 |
| `SECRET_KEY` | `change-me-…` | JWT 簽名金鑰（32 字元以上）|
| `ALGORITHM` | `HS256` | JWT 演算法 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080`（7天）| Token 有效期 |
| `ADMIN_EMAIL` | `admin@daniellife.com` | DB 無用戶時的 fallback 帳號 |
| `ADMIN_PASSWORD` | `changeme` | DB 無用戶時的 fallback 密碼 |
| `FRONTEND_ORIGIN` | `http://localhost:5173` | CORS allow origin |
| `ITIS_BASE_URL` | ITIS URL | 台灣新聞 proxy 來源 |

> 兩個 `.env` 檔均已加入各自 `.gitignore`，永遠不會被 commit。

---

## 十三、已知限制與注意事項

| 項目 | 說明 |
|------|------|
| 台灣地圖高亮 | `world-atlas` 110m 解析度下台灣面積過小可能不顯示；ISO numeric 158 已設定 |
| FRED iframe | 不加多餘 params，否則月頻指標顯示 sad face 錯誤 |
| Yahoo Finance CORS | `query2.finance.yahoo.com` 在 browser 環境 CORS 受限，MarketOverviewPanel 已有 fallback |
| ITIS 台灣新聞 | CORS-restricted HTML-only，前端無法直接 fetch，需後端 proxy |
| 旅遊照片 | 目前為 `URL.createObjectURL`（session-only），後端上線前無法持久化 |
| mockLogin | 預設帳密 `admin@daniellife.com` / `changeme`；`.env.local` 可覆蓋 |
