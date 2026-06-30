# Daniellife 個人網站 — 專案全覽

> 最後更新：2026-06-30（GitHub Models AI 聊天室串接 + Docker 部署設定）

---

## 一、專案簡介

「Daniellife 會計丹尼」是周彥廷（NTU 會計碩士）的個人作品集兼履歷網站。
公開頁面面向求職、展示活動與作品；管理員頁面供本人管理所有資料。

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
| 認證 | **Google OAuth (GSI)** → 後端驗證 → JWT（python-jose） |
| 檔案上傳 | python-multipart；圖片存 `backend/uploads/{section}/`；`/uploads` StaticFiles 掛載 |
| AI 整合 | GitHub Models（`gpt-4o`，OpenAI-compatible，`POST /api/market/chat`）|

### npm 套件（非標準 Vite 預設）

| 套件 | 用途 |
|------|------|
| `leaflet` + `@types/leaflet` | ActivitiesView 世界地圖 |
| `topojson-client` + `@types/topojson-client` | TopoJSON → GeoJSON 轉換 |

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
├── assets/styles/tokens.css
├── api/
│   ├── client.ts          # apiFetch<T>、getToken()、mediaUrl(path)
│   ├── homepage.ts        # internships / projects / certs / academic / futureplans / lang-certs / cert-groups
│   ├── activities.ts      # experiences / travelEntries + photo upload/delete
│   ├── social.ts          # socialActivities + photo upload/delete
│   ├── literature.ts      # literatureWorks
│   ├── finance.ts         # holdings
│   └── thesis.ts          # thesisPapers
├── types/                 # homepage / activities / social / literature / finance / thesis
├── stores/auth.ts         # isLoggedIn / user / login() / logout()
├── router/index.ts        # 路由表 + beforeEach 守衛
├── components/
│   ├── layout/            # AppNavbar（RWD + Google OAuth 感知）/ AppFooter
│   ├── admin/
│   │   ├── AdminTable.vue   # 通用 CRUD 表格
│   │   ├── AdminSidebar.vue # 深色左側欄 + 登出
│   │   └── AdminModal.vue   # 新增/編輯 Modal + 照片管理
│   ├── homepage/
│   │   ├── HeroCard.vue          # 3 欄英雄卡（個人簡介 + 照片 + 格言）
│   │   ├── InternSection.vue     # 實習卡片 slider + Modal
│   │   ├── ProjectSection.vue    # 作品集（3 篩選 + 2×2 Grid）
│   │   ├── CertSection.vue       # 證照 3 欄 + 語言進度條動畫
│   │   ├── AcademicSection.vue   # 求學 SVG 曲線 + 汽車動畫
│   │   └── FuturePlanSection.vue # 未來規劃金字塔（3 phase）
│   ├── activities/
│   │   ├── ExperienceCard.vue    # 領導/社團卡片（照片 grid + 貢獻截斷）
│   │   ├── ExperienceModal.vue   # 課外活動詳情 Teleport Modal
│   │   ├── TravelEntryModal.vue  # 旅遊記錄詳情 Teleport Modal
│   │   └── AddTravelModal.vue    # 新增旅行日記（4 張照片上傳）
│   ├── social/
│   │   ├── ActivityCard.vue      # 社會參與卡片（ESG badge + 照片）
│   │   ├── ActivityModal.vue     # 社會參與詳情 Teleport Modal
│   │   └── FilterSidebar.vue     # ESG / SDGs checkbox 篩選 sidebar
│   ├── literature/
│   │   ├── TrainTimeline.vue     # 台鐵時間軸動畫（IntersectionObserver + RAF）
│   │   └── WorkCard.vue          # 台鐵時刻板風格文學作品卡
│   ├── thesis/
│   │   ├── ThesisNotePanel.vue   # 碩論筆記（collapsible + 編輯模式）
│   │   ├── KanbanBoard.vue       # 靈感 Kanban（3 欄 + HTML5 drag-drop + 新增 Modal）
│   │   └── PapersTable.vue       # 參考文獻表（topic/journal 篩選 + keyword 搜尋）
│   ├── news/
│   │   ├── NewsCard.vue          # 新聞卡片（標題 + 摘要 + source badge，<a> 連結）
│   │   ├── NewsList.vue          # 新聞列表（搜尋 + 地區 Tab + 分頁，自取資料）
│   │   └── ChatPanel.vue         # AI 聊天室（GitHub Models gpt-4o，打字動畫 + loading 狀態）
│   ├── market/
│   │   ├── MarketOverviewPanel.vue  # 大盤總覽（TW/US，fallback mock SVG）
│   │   ├── ForexSection.vue         # TradingView 外匯小工具（USD/JPY/EUR → TWD）
│   │   ├── YieldSection.vue         # FRED iframes（DGS10 + FEDFUNDS）
│   │   └── WorldBankSection.vue     # World Bank API（GDP/CPI，🇺🇸/🇹🇼 切換）
│   └── finance/
│       ├── MetricCards.vue       # 5 個彩色頂部邊框指標卡
│       ├── DonutChart.vue        # 可複用 SVG 甜甜圈圖（接 slices prop + CSS var 顏色）
│       └── HoldingsTable.vue     # 11 欄持股明細表（紅綠損益 + 幣別 badge）
├── views/
│   ├── HomeView.vue
│   ├── ActivitiesView.vue
│   ├── SocialView.vue
│   ├── LiteratureView.vue
│   ├── MarketView.vue
│   ├── NewsView.vue
│   ├── FinanceView.vue    # ★ 需登入
│   ├── ThesisView.vue     # ★ 需登入
│   ├── AdminView.vue      # ★ 需登入（ADMIN_EMAIL 限定）
│   ├── LoginView.vue      # /danieladmin（Google OAuth 入口）
│   └── ForbiddenView.vue
└── App.vue                # Navbar + RouterView + Footer + 回到頂端按鈕

backend/
├── app/
│   ├── main.py            # FastAPI app、CORS、/uploads StaticFiles、lifespan
│   ├── deps.py            # get_current_user：解 JWT → 比對 ADMIN_EMAIL（不查 DB）
│   ├── database.py        # SQLAlchemy engine / SessionLocal
│   ├── models/            # SQLAlchemy ORM 模型（15 張表）
│   ├── schemas/           # Pydantic v2 schemas（含 @field_validator）
│   ├── routers/
│   │   ├── auth.py        # POST /auth/google（Google ID token → JWT）
│   │   ├── homepage.py    # /api/homepage（internships 含照片、projects、certs、academic、futureplans）
│   │   ├── activities.py  # /api/activities（experiences 含照片、travel 含照片）
│   │   ├── social.py      # /api/social（含照片）
│   │   ├── literature.py  # /api/literature
│   │   ├── thesis.py      # /api/thesis
│   │   └── finance.py     # /api/finance
│   └── utils/
│       └── auth.py        # create_token / decode_token
├── seed.py                # 初始 mock 資料（experiences / travel / holdings / thesis_note / social / literature）
├── seed_papers.py         # 21 篇 AIS DA Seminar 論文一次性匯入（從 Notion 手工整理）
└── uploads/               # 上傳圖片（已加入 .gitignore）
```

---

## 五、路由表

| 路徑 | View | 備註 |
|------|------|------|
| `/` | HomeView | 公開 |
| `/activities` | ActivitiesView | 公開 |
| `/social` | SocialView | 公開 |
| `/literature` | LiteratureView | 公開 |
| `/market` | MarketView | 公開 |
| `/news` | NewsView | 公開 |
| `/finance` | FinanceView | **需登入** |
| `/thesis` | ThesisView | **需登入** |
| `/admin` | AdminView | **需登入（ADMIN_EMAIL 限定）** |
| `/danieladmin` | LoginView | 隱藏 Google OAuth 入口 |
| `/403` | ForbiddenView | 未授權導向 |

> Navigation Guard：`beforeEach` 偵測 `meta.requiresAuth`，未登入導向 `/403`。

---

## 六、認證機制

### Google OAuth 流程

1. `/danieladmin` — Google One-Tap Sign-In（GSI）彈出選帳號
2. 前端取得 Google `credential`（ID token）
3. `GET /auth/google?token={credential}` → 後端驗證 Google 公鑰
4. 後端核對 email == `ADMIN_EMAIL`（env 設定），不符合 → 403
5. 後端回傳自簽 JWT → 前端存 `localStorage.auth_token`
6. 往後所有 admin API：`Authorization: Bearer {token}`

### `deps.py` — `get_current_user`

```python
def get_current_user(credentials) -> str:
    email = decode_token(credentials.credentials)
    if not email:
        raise HTTPException(401)
    if email != settings.ADMIN_EMAIL:
        raise HTTPException(403)
    return email
# 不查 DB（Google OAuth 不建立 users 記錄）
```

---

## 七、API 模組說明

### 前端 `src/api/client.ts`

```ts
// apiFetch：自動加 Authorization header、解析 422 Pydantic errors 為可讀字串
export async function apiFetch<T>(path, options?): Promise<T>
export function getToken(): string | null
export function mediaUrl(path: string): string  // 加 VITE_API_URL 前綴
```

422 錯誤解析：`detail` 若為 array → 取每個 `e.msg`，去掉 "Value error, " 前綴，用「；」合併。

### 前端 `src/api/*.ts`

| 模組 | 主要函式 |
|------|---------|
| `homepage.ts` | `getInternships/createInternship/updateInternship/deleteInternship` + **uploadInternshipPhoto/deleteInternshipPhoto** + projects / cert-groups / lang-certs / academic / future-plans（各 CRUD）|
| `activities.ts` | experiences / travelEntries 各 CRUD + **uploadExperiencePhoto/deleteExperiencePhoto/uploadTravelPhoto/deleteTravelPhoto** |
| `social.ts` | socialActivities CRUD + **uploadSocialPhoto/deleteSocialPhoto** |
| `literature.ts` | literatureWorks CRUD |
| `finance.ts` | holdings CRUD |
| `thesis.ts` | thesisPapers CRUD |

### 後端照片 Upload 規格

```
POST /{resource}/{id}/photo  → multipart/form-data（field: "file"）→ 回傳完整物件
DELETE /{resource}/{id}/photo → 刪除檔案 → 回傳完整物件
```
- 支援：JPEG / PNG / WEBP（`image/*`）
- 最大 5MB
- 存到 `backend/uploads/{section}/` 並清理舊檔（單張覆蓋）

---

## 八、雙層驗證

### 前端 `validateForm(fd)`（AdminView.vue）

在 Admin Modal 點儲存後、呼叫 API 前：

| Section | 驗證內容 |
|---------|---------|
| internships / activities | 月份：`YYYY/MM`；periodTo 可空（→「至今」）|
| social | 日期：`YYYY-MM-DD`；periodTo 可空 |
| academic | 年份：`YYYY`；periodTo 可空 |
| travel | 日期：`YYYY-MM-DD` |
| projects | type 枚舉：`code/uiux/finance`；members 正整數 |
| holdings | currency 枚舉：`TWD/USD`；shares/avgPrice/marketPrice 正數 |
| langcerts | lang 枚舉：`en/jp`；pct 0–100 |
| certgroups | domain 枚舉：`finance/it` |
| futureplans | phase 枚舉：`short/mid-short/mid` |
| social | esgType 枚舉：`Environmental/Social/Governance` |

錯誤訊息格式：`「欄位名稱」說明`（中文，明確）

### 後端 Pydantic v2 `@field_validator`

所有 `*In` schemas 均有對應驗證，422 response 由前端 `apiFetch` 統一顯示。

---

## 九、期間欄位格式

| 場景 | 格式 | 範例 |
|------|------|------|
| 月份期間（實習/活動/作品集） | `YYYY/MM – YYYY/MM` | `2025/07 – 2025/09` |
| 持續中（月份） | `YYYY/MM – 至今` | `2024/09 – 至今` |
| 年份期間（求學） | `YYYY – YYYY` | `2021 – 2025` |
| 日期（社會參與 periodFrom/To） | `YYYY-MM-DD`（分開欄位） | `2025-03-01` |

Admin 表單均拆成 `periodFrom` + `periodTo` 兩個輸入欄位。  
`buildPeriod(from, to)` → `` `${from.trim()} – ${to.trim() || '至今'}` ``  
`parsePeriod(period)` → split on `'–'`（em dash）

---

## 十、Admin Panel 架構

### 元件結構

```
AdminView.vue          — 資料狀態 / API calls / validateForm / saveModal / deleteItem
  ├── AdminSidebar.vue — 左側深色導覽列 + 登出
  │     props: sections, currentSection
  │     emits: select(key), logout
  ├── AdminTable.vue   — 通用資料表（每個 section 一個）
  │     props: title, columns, rows, ids
  │     emits: add, edit(id), delete(id)
  └── AdminModal.vue   — 新增 / 編輯 Modal
        props: open, mode, sectionLabel, fields, initialFormData, current,
               saving, saveError, editingPhotos, editingPhotoUrl, photoUploading
        emits: close, save(formData, pendingMultiFiles, pendingSingleFile),
               upload-multi, delete-multi, upload-single-edit, delete-single-edit
```

### AdminModal 資料流

```
openAdd()  → modalInitialFormData = 空白欄位  → modalOpen = true
openEdit() → modalInitialFormData = 現有資料  → 設定 editingPhotos/editingPhotoUrl → modalOpen = true
AdminModal watch(open) → localFormData = {...initialFormData}（重置 pending photo state）
User 填表 → localFormData（本地）
點儲存 → emit('save', { formData, pendingMultiFiles, pendingSingleFile })
AdminView.handleModalSave → validateForm(fd) → saveModal(fd, files)
  ├── add mode：createXxx → 逐一 uploadXxxPhoto（pending files）→ push list
  └── edit mode：updateXxx → replaceInList
```

### 12 個管理區塊

| section key | 中文 | 照片 | 期間欄位格式 |
|-------------|------|------|-------------|
| internships | 實習經歷 | 單張（edit + add） | YYYY/MM |
| projects | 作品集 | 無 | YYYY/MM |
| activities | 課外活動 | 多張最多 4（edit + add） | YYYY/MM |
| social | 社會參與 | 單張（edit + add） | YYYY-MM-DD（分開欄位） |
| literature | 文學作品 | 無 | YYYY.MM |
| papers | 論文文獻 | 無 | 年份 YYYY |
| holdings | 持股明細 | 無 | — |
| academic | 求學歷程 | 無 | YYYY（年份） |
| futureplans | 未來規劃 | 無 | — |
| langcerts | 語言證照 | 無 | — |
| certgroups | 財會/資訊證照 | 無 | — |
| travel | 旅遊記錄 | 多張最多 4（edit + add） | YYYY-MM-DD |

---

## 十一、各頁面規格

### 11.0 全站共用

**App.vue — 回到頂端按鈕**
- `scrollY > 300px` 浮現右下角（44×44px，黃邊框白底）
- hover 變黃底；`scrollTo({ top: 0, behavior: 'smooth' })`

**Favicon（`index.html`）**
- SVG inline，圓形黃底，「D」`dominant-baseline='central'` 垂直置中

---

### 11.1 首頁 `/` — HomeView

**HeroCard（3 欄）**
- 左：姓名、台北/臺中/男/特質、職務標籤列
- 中：96px 圓形照片×2、Instagram `_daniellife_`、LinkedIn `yenting2003`
- 右：格言卡「你不需要很厲害才能開始 / 但至少要勇於嘗試」

**其他 Section**
- InternSection：橫向 scroll-snap slider + Teleport Modal
- ProjectSection：3 個 Dropdown 篩選 + 2×2 Grid
- CertSection：3 欄 + 語言進度條動畫（IntersectionObserver）
- AcademicSection：SVG 曲線 + 🚗 動畫
- FuturePlanSection：近 5 年金字塔（short / mid-short / mid）

---

### 11.2 課外活動 `/activities` — ActivitiesView

ActivitiesView 擁有：experiences / continents / leafletMap / modal state / addEntry state。

| 元件 | 職責 |
|------|------|
| `ExperienceCard` | 領導/社團卡片；左欄標題/組織/期間/貢獻截斷，右欄 2 張照片 Grid；emit `view-more` |
| `ExperienceModal` | 課外活動詳情 Teleport Modal；prop `experience` |
| `TravelEntryModal` | 旅遊記錄詳情 Teleport Modal；prop `entry`；顯示人事時地物 + 照片 |
| `AddTravelModal` | 新增旅行日記；prop `continent`；owns form state；呼叫 `createTravelEntry` + `uploadTravelPhoto`；emit `submitted` 通知父層刷新 |

**Leaflet 地圖**：440×380px；world-atlas TopoJSON；訪國黃色高亮；點擊 → TravelEntryModal。

---

### 11.3 社會參與 `/social` — SocialView

SocialView 擁有：stage1 / esgSub / appliedEsg / appliedSdg / activities / activeModal。

| 元件 | 職責 |
|------|------|
| `FilterSidebar` | ESG × SDGs checkbox 篩選；owns selectedEsg / selectedSdg；emit `apply(esg, sdg)` |
| `ActivityCard` | 社會參與卡片；ESG badge + 照片（`mediaUrl` 或 placeholder）；emit `view-more` |
| `ActivityModal` | 詳情 Teleport Modal；prop `activity` |

---

### 11.4 文學天地 `/literature` — LiteratureView

LiteratureView 擁有：timeline / works / worksSectionEl；`scrollToWork(workId)` 處理 click-work。

| 元件 | 職責 |
|------|------|
| `TrainTimeline` | 台鐵時間軸動畫；owns 全部動畫狀態（arrivedCount / animId / railFillEl 等）；IntersectionObserver 觸發/重置；emit `click-work(workId)` |
| `WorkCard` | 台鐵時刻板風格文學作品卡；有 `data-work-id` 屬性供 scrollToWork 定位高亮 |

---

### 11.5 市場資訊 `/market` — MarketView

MarketView 純組合（無自身 data state）。

| 元件 | 職責 |
|------|------|
| `MarketOverviewPanel` | 大盤總覽（TW/US），fallback mock SVG sparklines |
| `ForexSection` | TradingView mini-symbol-overview；USD/JPY/EUR → TWD；owns DOM refs |
| `YieldSection` | FRED iframes（DGS10 + FEDFUNDS）；不加多餘 params 避免 sad face 錯誤 |
| `WorldBankSection` | World Bank API；GDP/CPI；🇺🇸/🇹🇼 切換；owns wbCountry / gdpData / cpiData |

---

### 11.6 總經新聞 `/news` — NewsView

NewsView 純組合（無自身 data state）。

| 元件 | 職責 |
|------|------|
| `NewsList` | 搜尋 + US/TAIWAN Tab + 分頁（PAGE_SIZE=5）；owns region / keyword / page / items；Guardian API（key=`test`）；TAIWAN tab 有黃色 ⚠ banner |
| `NewsCard` | `<a>` 連結卡；標題 + 摘要（2-line clamp）+ source badge |
| `ChatPanel` | AI 聊天室；owns messages / chatInput / loading；呼叫 `POST /api/market/chat`（GitHub Models gpt-4o）；打字動畫泡泡 |

---

### 11.7 理財規劃 `/finance` — FinanceView（需登入）

FinanceView 擁有：holdings / summary / allocationSlices / brokerSlices（computed）。

| 元件 | 職責 |
|------|------|
| `MetricCards` | 5 個彩色頂部邊框指標卡；prop `summary: PortfolioSummary` |
| `DonutChart` | 可複用 SVG 甜甜圈；prop `slices: { label, pct, color }[]`；接受 CSS var 字串 |
| `HoldingsTable` | 11 欄持股明細表；prop `holdings: Holding[]`；紅綠損益 + 幣別 badge |

---

### 11.8 論文統整 `/thesis` — ThesisView（需登入）

ThesisView 純組合（無自身 data state）。

| 元件 | 職責 |
|------|------|
| `ThesisNotePanel` | 碩論筆記；owns data；collapsible + view/edit 模式；`getThesisNote` / `saveThesisNote` |
| `KanbanBoard` | 3 欄 Kanban + HTML5 drag-drop + 新增 Modal（Teleport）；owns ideas / draggingId / dragOverCol；`.kanban-empty` 加 `pointer-events:none` 修正空欄 drop 無效問題 |
| `PapersTable` | 參考文獻表；owns allPapers / filterTopic / filterJournal / paperKeyword；`filteredPapers` computed；搜尋用 SVG icon（已移除 Notion 同步按鈕） |

---

### 11.9 功能管理 `/admin` — AdminView（需登入）

見第十節「Admin Panel 架構」完整說明。

---

### 11.10 登入 `/danieladmin` — LoginView
- Google One-Tap Sign-In（GSI）
- 成功 → `auth.login()` → redirect `/admin`

---

### 11.11 未授權 `/403` — ForbiddenView
- 大型「403」（primary 黃色）+ 前往登入 / 回首頁

---

## 十二、後端 Schema（資料表）

> SQLAlchemy ORM auto-create on startup。MySQL InnoDB / utf8mb4_unicode_ci。

### 核心 Type 對照

| TypeScript | 後端欄位 | 格式 |
|-----------|---------|------|
| `period: string` | `period_from/to` (DATE) | `YYYY/MM – YYYY/MM`（前端組合）|
| `photos: string[]` | `photos` TEXT | JSON 字串陣列 |
| `photoUrl?: string` | `photo_url` VARCHAR(500) | 單張路徑 |
| `sdgNumbers: SdgNumber[]` | `sdg_numbers` TEXT | JSON 整數陣列 |

### 主要資料表（選列）

**`internships`**：company / dept / role / period（VARCHAR）/ contribution / photo_url

**`projects`**：name / type（ProjectType）/ techLabel / tech / members / period / core / githubUrl / youtubeUrl / star（JSON）/ createdAt

**`experiences`**（課外活動）：type / title / organization / period / contribution / photos（JSON）

**`travel_entries`**：country / city / continent / visited_at / journal / companions / activities / purchases / photos（JSON）

**`social_activities`**：name / organization / esg_type / sdg_numbers（JSON）/ period_from / period_to / contribution / reflection / photo_url

**`academic_milestones`**：school / major / period / gpa / rank / sort_order / facts（JSON）

**`future_plans`**：phase / title / subtitle / items（JSON）/ sort_order

**`lang_certs`**：lang（en/jp）/ name / score / pct

**`cert_groups`**：domain（finance/it）/ category / items（JSON）/ sort_order

**`literature_works`**：title / age_written / period / awards / summary / full_text

**`thesis_papers`**：topic / name / journal / authors / year / purpose / contribution（21 筆 AIS DA Seminar 論文已由 `seed_papers.py` 匯入）

**`thesis_ideas`**：title / content / status（`pending` / `approved` / `rejected`）

**`holdings`**：symbol / name / currency / broker / shares / avg_price / market_price / dividend

**`thesis_notes`**（singleton）：content / updated_at

---

## 十三、環境變數

### 前端（`src/.env.local`，不 commit）

| 變數 | 預設值 |
|------|--------|
| `VITE_API_URL` | `http://localhost:8000` |

### 後端（`backend/.env`，不 commit）

| 變數 | 說明 |
|------|------|
| `DATABASE_URL` | MySQL 連線字串 |
| `SECRET_KEY` | JWT 簽名金鑰（32 字元以上）|
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080`（7天）|
| `ADMIN_EMAIL` | `r14722016@g.ntu.edu.tw`（唯一管理員）|
| `FRONTEND_ORIGIN` | `http://localhost:5173` |
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID |
| `GITHUB_TOKEN` | GitHub PAT（`models:read` scope）→ GitHub Models 推論 |
| `GITHUB_MODELS_MODEL` | 預設 `gpt-4o`（可改為其他 GitHub Models 支援的模型）|

---

## 十四、開發進度

### ✅ 已完成

**前端 UI**
- [x] 全站 Design Token + AppNavbar（RWD）+ AppFooter
- [x] 全站回到頂端按鈕、Favicon D 置中
- [x] HomeView（HeroCard + 5 個子元件）
- [x] ActivitiesView（ExperienceCard / ExperienceModal / TravelEntryModal / AddTravelModal + Leaflet 地圖）
- [x] SocialView（FilterSidebar / ActivityCard / ActivityModal）
- [x] LiteratureView（TrainTimeline / WorkCard）
- [x] MarketView（MarketOverviewPanel / ForexSection / YieldSection / WorldBankSection）
- [x] NewsView（NewsList / NewsCard / ChatPanel）
- [x] FinanceView（MetricCards / DonutChart / HoldingsTable）
- [x] ThesisView（ThesisNotePanel / KanbanBoard / PapersTable）
- [x] LoginView（Google OAuth）、ForbiddenView

**元件架構重整**
- [x] `common/` → `layout/`（AppNavbar / AppFooter），App.vue 更新 import
- [x] 所有頁面完整拆分為 feature 元件（activities / social / literature / thesis / news / market / finance）
- [x] 元件組織：`layout/`（全站框架）+ feature folders（頁面專屬）+ `admin/`（後台）+ `homepage/`（首頁）

**後端 + 串接**
- [x] FastAPI 全端 API（12 個 section，含照片 upload/delete）
- [x] Google OAuth 認證取代密碼登入
- [x] `deps.py` 直接比對 JWT email vs ADMIN_EMAIL（不查 DB）
- [x] 所有 Pydantic `*In` schemas 加 `@field_validator` 二層防守
- [x] 前端 `validateForm` 一層防守 + `apiFetch` 422 error 解析
- [x] `ThesisIdeaIn` / `ThesisIdeaUpdate` status 值修正為 `pending / approved / rejected`（原錯誤值 `reading / done`）

**論文資料**
- [x] `seed_papers.py`：21 篇 AIS DA Seminar 論文全數匯入 `thesis_papers` 表（topic / name / journal / authors / year / purpose / contribution）
- [x] `PapersTable.vue`：移除 Notion 同步按鈕，搜尋 icon 改為純 SVG（黑白）
- [x] `KanbanBoard.vue`：修正空欄位 HTML5 drop 無效 bug（`.kanban-empty` 加 `pointer-events: none`）

**Admin Panel**
- [x] 12 個管理區塊（全 CRUD）
- [x] 照片管理：internships / activities / social / travel（edit + add mode）
- [x] 期間欄位拆分（periodFrom + periodTo）
- [x] AdminView 拆分為 AdminSidebar + AdminModal 元件

**AI 聊天 + 新聞**
- [x] `POST /api/market/chat`：GitHub Models gpt-4o，system prompt 財經助手，`GITHUB_TOKEN` 存 env
- [x] `ChatPanel.vue`：loading 打字動畫泡泡、disabled 狀態、`white-space: pre-wrap`（換行支援）
- [x] ITIS 台灣新聞 proxy：`GET /api/market/news?region=TAIWAN`，1hr 快取，BeautifulSoup 解析，研討會過濾
- [x] `sendChatMessage` API function（`src/api/market.ts`）

**部署**
- [x] `backend/Dockerfile`：python:3.12-slim + uvicorn
- [x] root `Dockerfile`：Node 20 build → nginx:alpine SPA
- [x] `docker-compose.yml`：db（mysql:8.0）+ backend + frontend，健康檢查 + volume
- [x] `nginx.conf`：`/api/*` + `/uploads/*` proxy to backend，SPA fallback
- [x] `requirements.txt` 補上 `python-multipart`

### ⏳ 待開發

（暫無待開發項目）

---

## 十五、安全規則

| 規則 | 說明 |
|------|------|
| `backend/.env` + `src/.env.local` | **永遠不 commit** |
| commit message | **不加 Co-Authored-By 署名** |
| git push | **push 前必須先問確認** |
| Admin 權限 | 只有 `r14722016@g.ntu.edu.tw` 能進 Admin |
| `noUncheckedIndexedAccess` | `tsconfig.app.json` 有此設定；`Record<string,string>` 存取一律加 `?? ''` |

---

## 十六、已知限制

| 項目 | 說明 |
|------|------|
| 台灣地圖高亮 | `world-atlas` 110m 解析度下台灣面積過小可能不顯示 |
| FRED iframe | 不加多餘 params，否則月頻指標顯示 sad face 錯誤 |
| Yahoo Finance CORS | Browser 環境受限，MarketOverviewPanel 已有 fallback mock |
| ITIS 台灣新聞 | CORS-restricted HTML-only，需後端 proxy（已實作） |
| GitHub Models 速率限制 | Copilot Free/Pro：15 req/min，150 req/day；公開頁面需自行評估使用量 |
| Docker 部署環境變數 | `docker-compose.yml` 讀取 `.env`，需設定 `MYSQL_ROOT_PASSWORD` + `SECRET_KEY` + `GITHUB_TOKEN` 等 |
| `noUncheckedIndexedAccess` | `tsconfig.app.json` 有、`tsconfig.json` 無（tsc --noEmit 不報錯）|
