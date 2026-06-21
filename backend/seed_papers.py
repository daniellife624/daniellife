"""
Seed all 21 AIS DA Seminar papers into thesis_papers table.
Clears existing rows and inserts all 21 records.
  cd backend
  python seed_papers.py
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models.thesis import ThesisPaper

Base.metadata.create_all(bind=engine)


def clean(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    return text.strip()


PAPERS = [
    dict(
        topic="Artificial Intelligence",
        name="Explainable Artificial Intelligence (XAI) in auditing.",
        journal="International Journal of Accounting Information Systems",
        authors="Zhang, C. A., Cho, S., & Vasarhelyi, M.",
        year=2022,
        purpose=clean("本研究旨在向審計實務工作者與學術界介紹「可解釋人工智慧 (XAI)」技術，以解決日益複雜的 AI 與機器學習模型在審計應用中所面臨的「黑盒子」挑戰。研究探討 XAI 技術如何協助審計團隊符合現行審計準則（如 PCAOB）中對於審計證據與工作底稿的嚴格記錄要求。同時，本研究利用預測「重大不實表達風險」的具體審計任務，實際演示 LIME 與 SHAP 等主流 XAI 分析方法，藉此幫助使用者理解模型決策邏輯，全面提升 AI 應用在查核過程中的透明度與可審計性。"),
        contribution=clean("1. **解決黑箱挑戰**：首次系統性地將 XAI 引入審計文獻，有效克服 ML 模型的黑盒子問題，增加審計 AI 的透明度與法規遵循性。<br>2. **橋接審計準則**：將計算機科學的 XAI 技術對接至現行審計證據與底稿準則，為國家級審計機關與前線查核員提供明確指引。<br>3. **實證方法優劣**：透過真實財報重編資料（包含 XGBoost 演算法與真實案例），實證比較多種 XAI 方法，發現 SHAP 比 LIME 能更精確識別出導致重編的財務紅旗指標（如應收與收入問題）。<br>4. **推動實務應用**：為從業人員提供具體工具（如反事實解釋、PDP），協助提升其專業懷疑態度並實現負責任的 AI 審計應用。"),
    ),
    dict(
        topic="Data Visualization",
        name="The effects of visualization and interactivity on calibration in financial decision-making.",
        journal="Behavioral Research in Accounting",
        authors="Tang, F., Hess, T. J., Valacich, J. S., & Sweeney, J. T.",
        year=2014,
        purpose=clean("本研究旨在探討「視覺化 (Visualization)」與「互動性 (Interactivity)」如何影響財務決策者的<span color=\"blue\">**準確度、自信心與校準程度 (Calibration)**</span>。隨著技術進步，財務數據多以動態視覺化呈現，但過去文獻多僅關注準確度，忽略了決策者常有的「過度自信」問題。本研究希望釐清，單獨或同時提供視覺化與互動性工具時，是否會改變決策任務的認知特徵，進而影響使用者的決策品質。最終期盼透過實驗找出最佳介面設計，幫助使用者在財務決策時達到自信心與準確度的完美契合。"),
        contribution=clean("1. **理論視角創新**：結合「準確度」與「自信心」同步檢視，證實<span color=\"blue\">**僅單獨評估準確度會導致對決策成效的理解不完整**</span>。<br>2. **突破傳統框架**：超越傳統靜態圖表比較，證實「互動式視覺化」具獨特價值，單一的互動或視覺化工具無法達到同等效果。<br>3. **改善決策校準**：實證發現單獨提供視覺化或互動性會導致決策者「過度自信」；<span color=\"blue\">**唯有兩者結合，方能同步提升準確度與自信心，達成完美校準**</span>。<br>4. **實務系統設計指引**：建議系統開發者在設計現代財務資訊系統（如 XBRL）時，務必將互動性深度整合進視覺化工具中。"),
    ),
    dict(
        topic="Text Mining",
        name="When is a liability not a liability? Textual analysis, dictionaries, and 10‐Ks.",
        journal="The Journal of Finance",
        authors="Loughran, T., & McDonald, B.",
        year=2011,
        purpose=clean("本研究的主要目的在於檢驗過往文本分析中廣泛使用、專為心理學與社會學開發的哈佛字典（Harvard Dictionary），是否能有效轉化並應用於商業與財務領域（如10-K財報）。作者試圖量化跨領域字典在財務文本中產生的「錯誤分類」程度與雜訊問題。為了解決此限制，本研究旨在開發專為財務領域量身打造的情緒字表（包含 Fin-Neg 等六種新字表），並導入 tf.idf 詞彙權重方法來削弱高頻詞彙的影響。最終目的為驗證這些財務專屬的文本情緒指標，是否能有效關聯並解釋股票報酬、交易量、報酬波動率、未預期盈餘以及企業舞弊等關鍵財務變數。"),
        contribution=clean("1. **揭露跨領域字典的誤判陷阱**：證實哈佛字典應用於財報時，高達73.8%的負面詞彙（如tax、cost、liability）實為財務中性詞，且部分詞彙（如mine、cancer）甚至會引發特定產業的虛假相關。<br>2. **開發財務領域專屬字典**：建立了包含財務專屬負向（Fin-Neg）、不確定性、訴訟與情態助動詞等六大字表，大幅降低錯誤分類率，成為後續財務文本研究的標準工具。<br>3. **證實 tf.idf 權重技術的優越性**：發現採用 tf.idf 權重方案能有效降低高頻詞雜訊；一旦使用此技術，即使是原本充滿雜訊的哈佛字典，也能大幅提升其對財務變數的解釋能力。<br>4. **驗證文本情緒的經濟實質意涵**：實證指出，10-K財報的負向與特殊語氣能顯著反映短期股票報酬下跌、異常交易量與未來波動率上升，並有助於識別遭遇財報舞弊及內部控制缺失的企業。<br>5. **確立正確的文本分析方法論**：強烈警告研究者不應盲目套用非商業領域的字表，確立了資料科學必須結合「領域知識」進行文字探勘的學術典範。"),
    ),
    dict(
        topic="Machine Learning",
        name="Machine learning improves accounting estimates: Evidence from insurance payments.",
        journal="Review of Accounting Studies",
        authors="Ding, K., Lev, B., Peng, X., Sun, T., & Vasarhelyi, M. A.",
        year=2020,
        purpose=clean("本研究旨在探討「機器學習（Machine learning）」技術是否能取代或輔助傳統的人工決策，以大幅改善財報中「主觀會計估計」的準確性與可靠性。研究<span color=\"blue\">**聚焦於美國產物保險業的「損失準備金（Loss reserves）」資料**</span>，藉由比較機器學習模型與實際管理階層在財報上揭露的初估數字，驗證機器學習演算法是否能產生比管理層更精確的未來理賠損失估計值，並<span color=\"blue\">**測試機器能否克服人類因避稅或平滑盈餘等動機所導致的操縱偏誤**</span>，藉此為審計人員與企業提供一種客觀獨立的估計生成工具。"),
        contribution=clean("1. **證實機器學習優越性：** 機器學習在五分之四的產險業務中，預測損失準備的精準度顯著超越企業管理階層，且將管理層預估值納入演算法可進一步提升準確度。<br>2. **克服人為操縱偏誤：** 實證結果證明，傳統管理階層常因避稅、平滑盈餘及監理壓力而扭曲財報估計；而<span color=\"blue\">**機器學習模型能有效免疫這些主觀誘因干擾**</span>。<br>3. **實務應用與查核價值：** 研究首創將機器學習直接應用於會計餘額估計，為企業與會計師（查核人員）提供一套客觀的「標竿工具」。當人為估計大幅偏離機器預測時可發出警訊，進而提升財報可靠性與投資人價值。"),
    ),
    dict(
        topic="Large Language Model",
        name="Generative AI in financial reporting.",
        journal="Stanford University Graduate School of Business Research Paper",
        authors="Blankespoor, E., deHaan, E., & Li, Q.",
        year=2025,
        purpose=clean("本研究旨在探討企業在財務報導編製過程中（特別是撰寫揭露文本），實際採用生成式人工智慧（GAI）的程度與影響。隨著 ChatGPT 等大型語言模型的普及，GAI 有助於降低寫作成本並提高可讀性，但也伴隨資訊準確度與資安風險。因此，作者運用 AI 偵測工具分析 <span color=\"blue\">**2010 至 2024 年美國企業財報**</span>，建立 GAI 使用率的基準認知，並檢驗哪些資源受限的企業更傾向採用 GAI，同時探討 GAI 是否改變了財務報告的可讀性、語氣與具體性，為後續會計研究奠定基礎。"),
        contribution=clean("1. **確立實際採用規模**：證實企業確已導入 GAI，2024 年高達 4.5% 的新增文本（如 IPO 說明或風險因素）由 GAI 撰寫，但幅度遠低於業界誇大預期，反映企業仍持謹慎態度。<br>2. **揭示使用者特徵**：<span color=\"blue\">**缺乏資源的「小企業」、無投資人關係（IR）主管、遇重大經濟事件及審計公費較低的企業，因成本考量更積極採用 GAI。**</span><br>3. **闡明對文本特性的影響**：真實應用的 GAI 文本多半具有更高可讀性、更正向的語氣且包含更具體的量化細節，暗示管理層可能藉 GAI 刻意美化財報並經過嚴格的編修介入。<br>4. **方法論創新**：驗證了 <span color=\"green\">**GPTZero 在財務語境中的極高準確率**</span>，替未來審計與資本市場 AI 應用研究提供可靠的量化偵測框架。"),
    ),
    dict(
        topic="Machine Learning",
        name="Financial statement fraud detection: An analysis of statistical and machine learning algorithms.",
        journal="A Journal of Practice & Theory",
        authors="Perols, J.",
        year=2011,
        purpose=clean("本研究目的旨在解決財報舞弊偵測領域中常見的<span color=\"blue\">**「高度類別不平衡」（舞弊樣本極少）與「高度成本不平衡」（漏抓舞弊代價遠高於誤判）**</span>兩大獨特問題。有別於過去文獻多在平衡假設下評估模型，本研究比較了羅吉斯迴歸、類神經網路、支援向量機、決策樹及集成學習等六種分類演算法，在不同舞弊機率與誤判成本假設下的實際效用。同時，研究進一步探討在訓練模型時應採用何種事前機率與成本比例最為合適，並試圖從眾多文獻指出的財報變數中，篩選出真正能提升分類器準確度的核心預測變數。"),
        contribution=clean("1. **翻轉文獻認知：** 在符合現實的高不平衡特徵（事前舞弊率 0.6%、錯漏成本 1:20）假設下，證實計算簡單且易於解釋的「羅吉斯迴歸」與「支援向量機 (SVM)」表現異常優異，推翻了過去認為類神經網路 (ANN) 較佳的觀點。<br>2. **精煉預測變數：** 研究從 42 個舞弊變數中，證實多數變數屬冗餘。<span color=\"blue\">**僅「會計師更換、總裁決性應計項目、四大會計師查核、應收帳款、達到分析師預期、未預期的員工生產力」6 項變數具備高度且一致的預測效用**</span>，大幅降低資料蒐集難度。<br>3. **優化實務審計：** 提供主管機關 (SEC) 與審計人員開發風險模型時的直接指引。針對訓練模型參數，證實模型訓練階段的舞弊機率設定，應<span color=\"blue\">**根據實際母體的預期錯誤成本進行動態下調，以最大化偵測效用**</span>。"),
    ),
    dict(
        topic="Large Language Model",
        name="From transcripts to insights: Uncovering corporate risks using generative AI.",
        journal="Chicago Booth Research Paper",
        authors="Kim, A., Muhn, M., & Nikolaev, V.",
        year=2024,
        purpose=clean("本研究旨在探討「生成式人工智慧（Generative AI，如 ChatGPT）」工具，能否協助投資人從非結構化的企業財報會議紀錄中，精準衡量企業面臨的複雜風險。作者針對<span color=\"red\">**「政治風險」、「氣候變遷風險」與「AI 風險」**</span>建立企業層級的風險暴露指標。研究目的是驗證大型語言模型（LLMs）結合其一般知識所產出的風險評估，是否比傳統基於字典的「雙詞彙（Bigram）」方法更能有效預測未來的股價波動率、企業實質投資決策與創新應對行為，進而確認 AI 技術在低成本金融風險分析上的龐大潛力。"),
        contribution=clean("1. **創新風險衡量**：證實生成式 AI 能低成本且高精準地量化企業風險，其表現不僅超越傳統雙詞彙 (Bigram) 模型，更能精準捕捉 AI 衝擊等新興風險。<br>2. **彰顯通用知識價值**：GPT 結合推論能力的「風險評估」指標，其預測力顯著優於單純提煉內容的「風險摘要」。<br>3. **預測市場波動**：AI 量化出的高風險暴露，能精確預測未來股票的隱含波動率與異常波動率。<br>4. **連結企業實質決策**：高風險能有效解釋企業資本投資的下降，並驅動相應的避險行動（如增加政治遊說、申請綠能或 AI 專利）。<br>5. **資產定價意義**：氣候與 AI 風險在股市中具備定價能力，投資組合結果顯示其具有年化 6.36%~6.72% 顯著的超額報酬 (Alpha)。"),
    ),
    dict(
        topic="Large Language Model",
        name="The impact of generative AI on information processing: Evidence from the ban of ChatGPT in Italy.",
        journal="Journal of Accounting and Economics",
        authors="Bertomeu, J., Lin, Y., Liu, Y., & Ni, Z.",
        year=2025,
        purpose=clean("本篇論文的研究目的旨在探討「生成式人工智慧（如 ChatGPT）的出現與採用，是否能實質降低資訊摩擦並提升資本市場的資訊效率」。過去理論認為降低資訊處理成本能改善市場效率，但實證上面臨<span color=\"red\">**企業與個人採用AI時機與程度不一的挑戰**</span>。為突破此限制，作者利用 2023 年 3 月底義大利政府因隱私保護疑慮而突發性封鎖 ChatGPT 的事件作為自然實驗（外生衝擊）。透過檢視義大利國內金融分析師在 ChatGPT 禁用期間，其<span color=\"blue\">**資訊處理能力、預測行為（數量與準確度）的變化，以及這些變化如何進一步影響市場對盈餘公告的反應與買賣價差**</span>，藉此確立 AI 科技對金融市場資訊環境的實際因果影響。"),
        contribution=clean("1. **填補文獻空白**：首創利用「義大利禁用ChatGPT」為自然實驗，提供生成式AI影響資本市場資訊效率的因果證據。<br>2. **揭示AI對分析師的實質幫助**：結果顯示<span color=\"green\">**禁用AI會使分析師預測數量下降約21%、絕對預測誤差增加0.95%**</span>，且被迫依賴易處理的宏觀/產業資訊，證明AI能有效提升資訊處理的質與量。<br>3. **驗證「弭平資訊落差」假說**：禁用期間義大利股市買賣價差顯著擴大（約增加1.5倍標準差），盈餘公告的市場反應也變得更強烈，顯示<span color=\"green\">**AI普及有助於降低投資人之間的資訊不對稱**</span>。<br>4. **引入AI檢測創新指標**：成功將自然語言處理領域的「困惑度」與「突發性」指標應用於財金研究，精確衡量分析師報告中的AI使用痕跡。"),
    ),
    dict(
        topic="Text Mining",
        name="Large‐sample evidence on firms' year‐over‐year MD&A modifications.",
        journal="Journal of Accounting Research",
        authors="Brown, S. V., & Tucker, J. W.",
        year=2011,
        purpose=clean("本研究旨在探討上市公司「管理階層討論與分析（MD&A）」年度修改程度的資訊有用性。過去受限於人工分析文本的成本，難以進行大樣本研究。為此，作者引入向量空間模型（VSM）開發出衡量文本修改程度的量化指標，藉此解答<span color=\"blue\">**三個核心問題：第一，公司面臨較大經濟變動時，是否會對MD&A進行更大幅度修改？第二，投資人與財務分析師是否會利用MD&A修改所蘊含的新資訊？第三，管理層的MD&A修改行為及市場反應是否隨時間產生趨勢上的改變？**</span>"),
        contribution=clean("1. **創新大樣本分析工具**：首度將向量空間模型(VSM)應用於會計文本，成功量化MD&A的年度修改程度，為敘述性揭露研究開創先河。<br>2. **揭示MD&A聚焦長期現金流**：相較於短期盈餘變化，管理層更傾向針對「流動性與資本資源(LCR)」的改變去大幅修改MD&A。<br>3. **市場參與者反應分歧**：股票投資人會對MD&A修改產生顯著股價反應；但分析師卻未據此修正次年盈餘預測。<br>4. **資訊有用性隨時間下降**：近十年MD&A篇幅雖因法規變長，但制式化現象加劇，股價反應在2000年後已不再顯著，揭示了資訊量不等於資訊品質的現實。"),
    ),
    dict(
        topic="Large Language Model",
        name="Bloated disclosures: Can ChatGPT help investors process information?",
        journal="Chicago Booth Research Paper",
        authors="Kim, A. G., Muhn, M., & Nikolaev, V.",
        year=2024,
        purpose=clean("本研究旨在探討**大型語言模型 (LLMs)** 於處理複雜企業揭露資訊的經濟實用性。主要研究目的有三：<span color=\"blue\">**第一，檢驗生成式 AI 摘要是否能有效為投資人萃取對公司估值有直接影響的關鍵資訊；第二，比較摘要與原始文本在解釋股價反應上的資訊含量差異；第三，提出並驗證一項全新指標—「資訊臃腫度」 (Disclosure Bloat)，探討企業財報中無關緊要的冗長內容，究竟會緩解還是加劇資本市場的資訊摩擦現象**</span>。"),
        contribution=clean("1. **首創生成式 AI 財務應用**：首次運用大型語言模型 (LLMs) 分析財務揭露，證實 AI 摘要能有效保留關鍵資訊，幫助受限於注意力的投資人過濾雜訊，大幅提升資訊處理效率。<br>2. **提出全新「資訊臃腫度」指標**：創新發明 Bloat 指標，精準量化文字中冗餘與不相關的內容，在實證上超越傳統文本可讀性 (Fog index) 與樣板化 (Boilerplate) 指標，為衡量揭露品質提供新視角。<br>3. **揭示冗長資訊的負面經濟後果**：實證結果發現，臃腫的揭露不僅無助於市場理解，反而顯著加劇投資人間的資訊不對稱 (推升買賣價差與知情交易機率)，尤其是管理層刻意混淆的「裁量性臃腫」危害最深。"),
    ),
    dict(
        topic="Large Language Model",
        name="Corporate responses to generative AI: Early evidence from conference calls.",
        journal="Review of Accounting Studies",
        authors="Jia, N., Li, N., Ma, G., & Xu, D.",
        year=2025,
        purpose=clean("本研究旨在探討 2022 年 11 月 ChatGPT 發布此一破壞性創新事件後，不同特徵之企業管理階層對生成式人工智慧 (GAI) 的認知與應對方式。透過分析法說會逐字稿中 GAI 討論的頻率、語氣（正/負向）及是否具備實質行動計畫，探究企業的創新強度、資安威脅、勞工 AI 曝險與顧客營運特徵如何影響其對 GAI 的反應，並進一步檢驗這些管理層的討論是否能為資本市場與投資人提供具資訊含量的決策訊號。"),
        contribution=clean("1. **揭示早期反應：** 證實 ChatGPT 發布後法說會 GAI 討論激增，且近 84% 呈正向語氣、97% 包含具體行動，顯示企業普遍視 GAI 為契機。<br>2. **釐清異質衝擊：** 發現專利密集、高資安威脅、高勞工 AI 曝險及服務導向產業的企業，顯著增加 GAI 行動討論。<br>3. **驗證資訊價值：** 經理人討論 GAI (尤其是具體計畫) 會引發顯著的股市異常報酬與交易量，且主要由機構投資人驅動。<br>4. **排除 AI 漂洗：** 結合招募數據，證實討論 GAI 的企業發布了 3 倍以上的 AI 職缺，確認其為實質投資而非空談。"),
    ),
    dict(
        topic="Data Visualization",
        name="Effects of data visualization choices on psychophysiological responses, judgment, and audit quality.",
        journal="Journal of Information Systems",
        authors="Rose, A. M., Rose, J. M., Rotaru, K., Sanderson, K. A., & Thibodeau, J. C.",
        year=2022,
        purpose=clean("本研究旨在探討不同的大數據資料視覺化（Data Visualization）選擇如何影響<span color=\"blue\">**使用者的心理生理反應（Psychophysiological Responses）**</span>，並檢驗這些視覺化技術對審計人員判斷（Auditor Judgment）與審計品質的影響。研究透過測量不同視覺化格式所引起的<span color=\"blue\">**「喚起（Arousal）」程度**</span>，分析高喚起的視覺化是否會導致審計人員在面對反證（Disconfirming Evidence）時，提升專業懷疑態度並調整其決策。此外，本研究也探討大數據資料來源的可靠性（Data Reliability）如何與喚起程度產生交互作用，進而影響審計人員對證據的評估與依賴。"),
        contribution=clean("1. **證實視覺化格式會影響心理生理喚起**：文字雲（Word Cloud）比長條圖（Bar Graph）能引起顯著更高的瞳孔反應與更強烈的負面情緒，且不會降低審計證據評估的效率。<br>2. **提升專業懷疑態度**：當視覺化能促進高喚起時，審計人員會更關注反證，進而增加計畫性的實質測試審計時數（Budgeted Audit Hours）。<br>3. **促進資料可靠性的整合與考量**：在面對高喚起的視覺化時，審計人員更能將大數據底層資料的「可靠性」整合至判斷中，精準下調對不實收入的認列金額。<br>4. **方法論創新**：引入瞳孔測量與自動面部表情分析等神經科學工具至會計資訊系統（AIS）研究，有助於未來實務部署新分析工具前進行有效測試。"),
    ),
    dict(
        topic="XBRL",
        name="Measuring accounting reporting complexity with XBRL.",
        journal="The Accounting Review",
        authors="Hoitash, R., & Hoitash, U.",
        year=2018,
        purpose=clean("本研究的主要目的為發展並驗證一個全新的「會計報導複雜度 (Accounting Reporting Complexity, 簡稱 ARC)」衡量指標，以解決過去常使用的營運或語意複雜度指標無法直接且精確反映會計準則難度的侷限。作者利用企業在 10-K 財務報告中所揭露的不重複 XBRL 標籤數量來建構此客觀指標。研究旨在測試 ARC 是否能有效捕捉財務報表編製上的複雜度，檢驗其與財務報導品質降低（如財報重編、內部控制重大缺失）及審計成本增加（如查核延遲、審計費用提高）之間的關聯性。同時，本研究也試圖證明 ARC 在統計解釋力與經濟顯著性上，皆優於傳統的複雜度代理變數。"),
        contribution=clean("1. **建立創新客觀指標**：成功開發基於 XBRL 大數據的 ARC 指標，能廣泛應用於所有 SEC 申報公司，彌補傳統指標缺乏與會計準則直接連結的缺點。<br>2. **實證對財報與審計之衝擊**：實證結果確切指出，ARC 顯著提升了財報不實表達與內部控制缺失的機率，並導致審計費用提高與查核延遲。<br>3. **展現卓越解釋力與敏感度**：證實 ARC 在預測財報品質上，具備比營運或語意指標更高的模型解釋力與經濟顯著性，且能靈敏捕捉併購或重組等重大經濟事件帶來的複雜度變動。<br>4. **具備向下拆解的微觀分析能力**：證明 ARC 可細分至特定會計科目（如存貨、租賃、稅務），並精準預測該科目的出錯機率，為未來會計研究提供了強大的控制與調節變數工具。"),
    ),
    dict(
        topic="Text Mining",
        name="The evolution of 10-K textual disclosure: Evidence from Latent Dirichlet Allocation.",
        journal="Journal of Accounting and Economics",
        authors="Dyer, T., Lang, M., & Stice-Lawrence, L.",
        year=2017,
        purpose=clean("研究的主要目的在於量化分析1996年至2013年間，美國企業10-K年報文字揭露特徵（如長度、可讀性、制式化與冗餘性等）的演變趨勢。為了突破過去難以大樣本分析文本內容的限制，作者導入自然語言處理技術「隱含狄利克雷分布（LDA）」，將龐大的財報文本客觀拆解為150個潛在主題。研究試圖釐清，年報篇幅的暴增與文本品質的改變，究竟是源於企業面臨的經濟基本面變化（如業務複雜度增加），還是因為遵循FASB與SEC新頒布的監管與揭露規範所致。"),
        contribution=clean("1. **量化揭露趨勢**：證實年報長度翻倍，且制式化、僵固與冗餘程度大幅上升，而可讀性、具體性與硬資訊比例顯著下降。<br>2. **釐清劣質文本元凶**：透過LDA證實長度暴增與品質惡化幾乎完全歸因於三項新規範：公允價值、內部控制及風險因子揭露，而非企業基本面改變。<br>3. **揭示法規不對稱影響**：發現當新規範對公司相關性較低時，企業更傾向以制式化、難懂且缺乏硬資訊的無效文本來應付合規。<br>4. **推廣創新方法**：首創將LDA應用於會計文本分析，證明其能有效客觀地解構巨量財報的深層主題。"),
    ),
    dict(
        topic="Artificial Intelligence",
        name="Is artificial intelligence improving the audit process?",
        journal="Review of Accounting Studies",
        authors="Fedyk, A., Hodson, J., Khimich, N., & Fedyk, T.",
        year=2022,
        purpose=clean("本研究目的旨在探討「人工智慧 (AI) 對審計品質、效率及勞動市場的具體影響」。過去文獻多流於概念討論或問卷調查，受限於缺乏企業層級的客觀 AI 量化數據。為突破此限制，<span color=\"blue\">**本文利用 31 萬份大規模履歷庫，精準識別美國 36 大會計師事務所的 AI 人才聘用狀況以衡量 AI 投資**</span>。研究主要探問三個核心問題：<span color=\"green\">**導入 AI 能否有效降低財報重編機率以提升審計品質？AI 是否能降低審計成本並提高效率？AI 的自動化預測能力是否會取代現有審計人員（特別是初階員工）的勞動力？**</span>"),
        contribution=clean("1. **提升審計品質**：實證 AI 投資顯著降低財報重編機率。AI 人力每增加一個標準差，整體重編機率降 5%、重大重編降 1.4%，證明 AI 強化了預測與異常偵測能力。<br>2. **促進審計效率**：審計公費隨 AI 導入呈「遞延性下降」（第一至三年分別降 0.9%、1.5%、2.1%），員工平均創造的公費收益顯著提高。<br>3. **改變勞動結構（初階人力替代）**：<span color=\"red\">**首度證實白領被取代**</span>。AI 對中高階主管無影響，但投資三年後初階人力減少 5.7%，四年後大減 11.8%。<br>4. **驗證技術主導權**：釐清<span color=\"red\">**審計品質的提升完全源於「會計師」的中央 AI 佈局**</span>，而非依賴客戶端的技術升級。"),
    ),
    dict(
        topic="Large Language Model",
        name="When LLMs go abroad: Foreign bias in AI financial predictions.",
        journal="Working paper",
        authors="Cao, S., Wang, C. C., & Xiang, Y.",
        year=2025,
        purpose=clean("本研究旨在探討大型語言模型（LLMs）在進行跨國財務預測時，是否會因訓練資料的地理空間與新聞涵蓋落差，而產生系統性偏誤。作者比較美國 ChatGPT 與中國 DeepSeek 對中國上市公司的股價預測，藉此檢驗是否會出現反轉人類「本國偏誤」的「外國偏誤」現象。同時，研究釐清此偏誤究竟源於「資訊取得限制」（缺乏當地負面新聞），還是「模型功能限制」（如參數編碼或提示語誘發），為跨國 AI 投資分析提供重要風險警示。"),
        contribution=clean("1. **發現 AI 外國偏誤現象**：首次實證美國 ChatGPT 對中國企業的股價預測顯著高出中國 DeepSeek 約 12.5%（且誤差較高），反轉了人類常見的「本國偏誤」。<br>2. **揭示偏誤的核心機制**：證實此偏誤源自跨國「空間資訊落差」（美國訓練集缺乏中國當地的負面新聞）。一旦在提示中注入當地新聞，或評估資訊透明的交叉上市企業，偏誤即顯著縮小或消失。<br>3. **排除提示功能干擾**：透過虛構企業安慰劑測試、中文提示語與聯網搜索測試，證實偏誤並非模型架構或語言誘發所致。<br>4. **跨國投資實務指引**：提醒投資人 LLM 會繼承跨國資訊不對稱，使用 AI 進行海外分析時應補充當地語系資訊，呼籲監管機構重視訓練資料的透明度。"),
    ),
    dict(
        topic="Inline XBRL",
        name="Initial evidence on the market impact of the iXBRL adoption.",
        journal="Accounting Horizons",
        authors="Luo, X., Wang, T., Yang, L., Zhao, X., & Zhang, Y.",
        year=2023,
        purpose=clean("本篇論文的研究目的主要為回應美國證券交易委員會 (SEC) 的呼籲，評估企業採用內嵌式可延伸商業報告語言 (iXBRL) 對資本市場帶來的實際經濟影響。過去的 XBRL 由於機器可讀數據與人類可讀的 HTML 財報分離，容易導致資料不一致且存在申報時間落差。因此，本研究旨在檢驗將兩者合而為一的 iXBRL 格式，是否能有效降低投資人的資訊獲取與處理成本。具體而言，本研究欲探討 iXBRL 的採用是否能提升市場的「資訊效率」（即降低股票報酬漂移並加快資訊反映至股價的速度），並檢驗其是否能在長期顯著降低市場的「資訊不對稱」。"),
        contribution=clean("1. **顯著提升資訊效率**：實證結果證實，採用 iXBRL 能降低資訊處理複雜度，顯著減少財報發布後的股票報酬漂移 (Drift) 現象，並加快財務資訊融入公司股價的速度。<br>2. **長期降低資訊不對稱**：與過去傳統 XBRL 只能短暫降低資訊不對稱不同，iXBRL 成功在財報發布後一個月以上，維持降低異常買賣價差的長期效果。<br>3. **造福一般散戶投資人**：iXBRL 大幅降低了數據閱讀門檻，顯著帶動缺乏專業資源的「散戶投資人」增加財報的下載與使用量，有效縮小大戶與散戶間的資訊落差。<br>4. **改善弱勢資訊環境**：當公司缺乏分析師追蹤，或是機構法人持股比例較低時（即原本資訊環境較差），iXBRL 提升效率與降低不對稱的作用會更加顯著。<br>5. **降低企業資金成本**：實證額外發現，透過提升資訊傳播效率，採用 iXBRL 有助於顯著降低公司下一年度的權益資金成本。"),
    ),
    dict(
        topic="Text Mining",
        name="Tone management.",
        journal="The Accounting Review",
        authors="Huang, X., Teoh, S. H., & Zhang, Y.",
        year=2014,
        purpose=clean("本研究旨在探討企業管理層在發布盈餘新聞稿時，是否會進行「語調管理」，以及資本市場與投資人對此的反應。由於單一量化指標無法完整反映公司的經濟狀況，管理層有極大空間透過自願性新聞稿的文字修辭來引導市場。因此，本研究的核心目的在於檢驗：<span color=\"blue\">**當新聞稿出現與當期量化績效不符的「異常正面語調」時，究竟是為了向投資人傳遞未來良好的基本面資訊（Inform），還是出於代理問題與策略性動機，用以掩飾疲弱的績效來誤導投資人（Misinform）**</span>。"),
        contribution=clean("1. **證實語調意在誤導**：異常正面語調會預測未來較差的盈餘與現金流，證明管理層藉此掩蓋基本面疲軟，而非提供有用資訊。<br>2. **揭示策略性動機**：當面臨盈餘剛好達標、未來財報重編、現金增資（SEO）或併購（M&A）等需推升股價的事件時，異常正面語調顯著增加；反之，發放 CEO 認股權需打壓股價時，則會壓低語調。<br>3. **發現投資人會被短暫欺騙**：市場在公告當下會對異常正面語調產生過度的正向反應，但隨後的一至兩季會發生顯著的股價修正與反轉下跌。<br>4. **拓展盈餘管理文獻**：當公司面臨「資產負債表過度膨脹」而無法進一步操縱應計利潤時，更傾向轉而使用不受會計準則限制的語調管理。"),
    ),
    dict(
        topic="Text Mining",
        name="Annual report readability, current earnings, and earnings persistence.",
        journal="Journal of Accounting and Economics",
        authors="Li, F.",
        year=2008,
        purpose=clean("本研究的主要目的在於探討企業年報的「可讀性（Readability）」與公司「當期績效」及「未來盈餘持續性」之間的關聯。過去關於企業揭露的文獻多聚焦於揭露的數量，較少系統性地分析詞彙特徵。因此，作者利用計算<span color=\"blue\">**語言學中的迷霧指數（Fog index）**</span>與<span color=\"blue\">**文本長度**</span>，實證檢驗「管理階層混淆假說（Management obfuscation hypothesis）」。具體而言，本研究試圖驗證當公司績效不佳時，管理階層是否會刻意將年報寫得冗長且複雜以增加資訊處理成本；並進一步檢驗複雜的年報是否被用來掩飾「短暫性的好消息」或「持續性的壞消息」，同時探索其他語言風格（如<span color=\"green\">**因果關係、情緒詞彙**</span>）對未來盈餘的預測能力。"),
        contribution=clean("1. **證實當期績效與可讀性呈顯著負相關**：研究結果顯示，當期盈餘較低或虧損的公司，其年報確實更長且更難閱讀（Fog 指數較高），不過此現象在經濟意義上的影響幅度相對微小。<br>2. **揭示可讀性對盈餘持續性的負面影響**：對於獲利公司而言，年報越複雜難懂，其正向盈餘在未來的持續性就越低。其經濟影響力極大，年報複雜度增加對盈餘持續性的負面衝擊，幾乎等同於總應計項目增加的影響。<br>3. **提供大樣本的「管理階層混淆假說」證據**：本研究為首篇大樣本分析，證實管理階層會策略性地利用複雜的語言特徵來隱藏短暫的好消息，強烈支持了不完全揭露假說。<br>4. **開創全新的資訊揭露品質指標**：突破過去僅衡量揭露「數量」的限制，證明了年報的「詞彙特徵」與「可讀性」本身即可作為衡量揭露品質與預測未來盈餘品質的重要實證指標。"),
    ),
    dict(
        topic="XBRL",
        name="Do managers use extension elements strategically in the SEC's tagged data for financial statements? Evidence from XBRL complexity.",
        journal="Journal of Information Systems",
        authors="Huang, F., No, W. G., & Vasarhelyi, M. A.",
        year=2019,
        purpose=clean("本研究旨在探討企業經理人是否會「策略性地」利用 XBRL（可延伸商業報導語言）中的擴充標籤，來增加美國證券交易委員會（SEC）強制申報文件的複雜度。基於「不完全揭露假說」，績效不佳的企業有動機混淆財務資訊以減緩市場反應。因此，本研究旨在驗證三個假說：(1) 企業績效是否與 XBRL 複雜度呈負相關；(2) 當正向盈餘持續性較低或負向盈餘持續性較高時，XBRL 申報是否更複雜；(3) 若企業先天的營運或財報文本較複雜，上述策略性增加複雜度的現象是否更為顯著。"),
        contribution=clean("1. **證實策略性混淆**：實證結果顯示，企業績效越差，或當好消息短暫、壞消息持續時，經理人越會大量使用擴充標籤來提高 XBRL 複雜度，藉此混淆資訊。<br>2. **揭示先天複雜度加乘效應**：結果指出，當企業本身的營運或文本越複雜，經理人策略性操作 XBRL 擴充標籤的程度就越嚴重。<br>3. **開拓文獻新領域**：將傳統聚焦於資訊發布時機與文本難度的「策略性報導文獻」，成功延伸至機器可讀的標籤數據（Tagged data）領域。<br>4. **釐清學界爭論**：為「過度使用擴充標籤是否為經理人裁量行為」之學術爭辯，提供了經理人確實會進行策略性操作的實證解答。<br>5. **提供監管政策意涵**：提醒 SEC 與投資人，不必要的擴充標籤不僅是技術不熟練，更可能源於經理人的資訊隱匿策略，有助於未來監管政策的制定。"),
    ),
    dict(
        topic="Text Mining",
        name="FinBERT: A large language model for extracting information from financial text.",
        journal="Contemporary Accounting Research",
        authors="Huang, A. H., Wang, H., & Yang, Y.",
        year=2023,
        purpose=clean("本研究主要目的為開發並驗證一個專為金融領域量身打造的先進大型語言模型——**「FinBERT」**。過往財務文本分析多依賴忽略上下文的傳統字典（如 LM 字典），或使用缺乏金融專業領域知識的通用型預訓練模型（如通用版 BERT）。因此，作者利用龐大的財務文本（包含<span color=\"blue\">**財報、分析師報告與法說會紀錄**</span>）來預訓練 FinBERT。其核心目的是為了探討 FinBERT 在「情感分類」與「ESG 議題標籤」等關鍵任務上，表現是否能顯著超越傳統字典及 LSTM、SVM 等各類機器學習演算法，並進一步檢驗其在小樣本環境與市場真實反應解釋力上的應用價值。"),
        contribution=clean("1. **全面突破分類準確率**：FinBERT 在情感分類（準確率 88.2%）與 ESG 討論標籤（準確率 89.5%）的表現上，皆大幅超越傳統 LM 字典與其他深度學習模型。<br>2. **精準捕捉負面情感與語境**：憑藉學習過金融專屬詞庫（Unique-FinVocab），FinBERT 能有效結合上下文，精準辨識常被其他模型誤判的負面財務資訊。<br>3. **大幅降低人工標註成本**：即便**訓練樣本大幅縮減至 10%**，FinBERT 仍能維持極高的準確率，有效解決機器學習需耗費鉅資建立標註資料的痛點。<br>4. **貼近真實市場股價反應**：相較於其他模型容易低估文本資訊的經濟意涵（低估幅度達 18% 至 48%），由 FinBERT 衡量出的法說會語氣，與投資人的真實市場反應具備最高的關聯性與解釋力。"),
    ),
]


def seed_papers():
    db = SessionLocal()
    try:
        existing = db.query(ThesisPaper).count()
        if existing >= 21:
            print(f"thesis_papers: already has {existing} rows, skip")
            return

        db.query(ThesisPaper).delete()
        db.commit()

        db.add_all([ThesisPaper(**p) for p in PAPERS])
        db.commit()
        print(f"thesis_papers: seeded {len(PAPERS)} rows")
    finally:
        db.close()


if __name__ == "__main__":
    seed_papers()
    print("Done.")
