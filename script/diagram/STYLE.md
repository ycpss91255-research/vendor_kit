# 圖面樣式規範

所有 `.drawio` 圖都照這份畫。來源是 `gen57.py` 的樣式常數與 `legend_flow`／`legend_arch`／`page()`／`band()`／`tree()`，以及 `disc_v1_a.py`、`disc_v1_b.py`、`disc_v1_c.py` 的實際用法。本檔只管格式，不管方塊裡寫什麼；圖上的名詞一律用根目錄 `CONTEXT.md` 的詞。

style 字串都是完整的，直接貼進 `<mxCell style="...">`。

## 1. 顏色語意

一個顏色只代表一件事。**填色表示類型**（外部、image、容器、主機軟體、repo、檔案），**紅框表示「VK 開發的」**，兩者分開，才能在同一格上同時表達。容器（泳道）與方塊用同一組顏色，意思相同。

| 顏色 | 填色 | 代表 |
|---|---|---|
| 紅框 | 框線 `#b85450`、粗 2，不填色 | VK 開發的東西。只用框線表示，填色留給類型，所以可以疊在任何類型上（例如深紫底加紅框 = VK 的容器） |
| 綠 | `#d5e8d4` | 使用 VK 的 repo（使用者的 repo）|
| 黃 | `#FFF4C3` | 外部：使用者、外部系統 |
| 淡紫 | `#e1d5e7`（框 `#9673a6`）| image |
| 深紫 | `#c9b8e8`（框 `#7e57c2`）| 容器；流程頁上是「在引擎容器內執行的 recipe」 |
| 灰 | `#CCCCCC` | 主機上既有的軟體 |
| 白 | `#ffffff` | 最小單元（架構頁）／步驟（流程頁） |
| 淺灰 | `#f5f5f5` | 分組，無狀態意義 |

### 1.1 容器（泳道）

模組、repo、外部角色這一層用泳道。標題列高 38、字 18 粗體、黑框 2。

深紫加紅框：VK 的容器（例如引擎）。紅框表示 VK 開發的，填色表示類型

```
swimlane;html=1;rounded=1;startSize=38;fontStyle=1;fontSize=18;container=1;collapsible=1;recursiveResize=0;fillColor=#c9b8e8;swimlaneFillColor=#ffffff;strokeColor=#b85450;strokeWidth=2;
```

綠：使用 VK 的 repo

```
swimlane;html=1;rounded=1;startSize=38;fontStyle=1;fontSize=18;container=1;collapsible=1;recursiveResize=0;fillColor=#d5e8d4;swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;
```

黃：外部（使用者、外部系統）

```
swimlane;html=1;rounded=1;startSize=38;fontStyle=1;fontSize=18;container=1;collapsible=1;recursiveResize=0;fillColor=#FFF4C3;swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;
```

淡紫：image（框線用紫，不用黑）

```
swimlane;html=1;rounded=1;startSize=38;fontStyle=1;fontSize=18;container=1;collapsible=1;recursiveResize=0;fillColor=#e1d5e7;swimlaneFillColor=#ffffff;strokeColor=#9673a6;strokeWidth=2;
```

深紫：不是 VK 開發的容器（框線用紫）

```
swimlane;html=1;rounded=1;startSize=38;fontStyle=1;fontSize=18;container=1;collapsible=1;recursiveResize=0;fillColor=#c9b8e8;swimlaneFillColor=#ffffff;strokeColor=#7e57c2;strokeWidth=2;
```

淺灰：分組（無狀態意義；流程頁的情境分組也用它）

```
swimlane;html=1;rounded=1;startSize=38;fontStyle=1;fontSize=18;container=1;collapsible=1;recursiveResize=0;fillColor=#f5f5f5;swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;
```

泳道標題太長、放在較小的子容器裡時，只把 `fontSize=18` 改成 `fontSize=16`，其他不動。

### 1.2 方塊（最小單元）

方塊框線 1、字 14。框線色用 `light-dark(#000000,#9577A3)`，深色模式才看得見。

白：最小單元／步驟

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);fontSize=14;strokeWidth=1;
```

灰：主機上既有的軟體

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#CCCCCC;strokeColor=light-dark(#000000,#9577A3);fontSize=14;strokeWidth=1;
```

紅：VK 的模組（畫成單格時）

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=light-dark(#000000,#9577A3);fontSize=14;strokeWidth=1;
```

黃：外部的東西（畫成單格時）

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF4C3;strokeColor=light-dark(#000000,#9577A3);fontSize=14;strokeWidth=1;
```

紫：image／container；流程頁上是在引擎容器內執行的 recipe（框線紫、粗 2）

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=14;strokeWidth=2;
```

### 1.3 擴充色（流程頁需要時才用）

以下幾種出自 `disc_v1_b.py`／`disc_v1_c.py`，只在頁面真的需要這個區分時才用，用了就要進圖例。

藍：引擎在容器內做的步驟。流程頁要把「啟動器（主機）做的」和「引擎（容器內）做的」分開時，白 = 啟動器、藍 = 引擎，這時紫只代表 image。

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;strokeWidth=2;spacingLeft=6;spacingRight=6;
```

橙底色 `#ffe6cc` 只用在「需人處理」的終點橢圓，見 2.3。

## 2. 形狀語意

### 2.1 判斷（黃菱形）

一個菱形只放一個問句；每個出邊標「是／否」或條件。

```
rhombus;whiteSpace=wrap;html=1;fillColor=#FFF4C3;strokeColor=#000000;strokeWidth=2;fontSize=14;
```

### 2.2 起點／終點（綠橢圓）

```
ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#000000;strokeWidth=2;fontSize=14;
```

### 2.3 錯誤終止（紅橢圓）與需人處理（橙橢圓）

紅橢圓 = 失敗終止。

```
ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#000000;strokeWidth=2;fontSize=14;
```

橙橢圓 = 需人處理（結束了，但要使用者做某件事再重跑）。只在流程頁需要把它和失敗分開時用。

```
ellipse;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#000000;strokeWidth=2;fontSize=14;
```

跨頁出入口：白底虛線橢圓，文字寫「來自「X」頁」或「續「X」頁」。

```
ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=14;dashed=1;
```

橢圓與菱形的文字要加內距，draw.io 才會以內接矩形折行（`check_overflow.shape_spacing`）：橢圓 `spacingLeft`／`spacingRight` = round(寬 × 0.146)、`spacingTop`／`spacingBottom` = round(高 × 0.146)；菱形兩個係數都是 0.25。例如 180×50 的橢圓補 `spacingLeft=26;spacingRight=26;spacingTop=7;spacingBottom=7;`。

### 2.4 檔案（虛線框）

白底虛線框 = 檔。流程頁與架構頁上指 repo 檔或 VK 檔。

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);fontSize=14;strokeWidth=1;dashed=1;
```

### 2.5 資料夾（實線框）

白底實線框 = 資料夾。和檔案的差別只有虛線。

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);fontSize=14;strokeWidth=1;
```

目錄樹頁（`tree()`）的資料夾與檔案靠左、等寬字，字改 12：

資料夾

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);fontSize=12;strokeWidth=1;align=left;spacingLeft=8;fontFamily=Courier New;
```

檔案

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);fontSize=12;strokeWidth=1;dashed=1;align=left;spacingLeft=8;fontFamily=Courier New;
```

目錄樹的排法：一列一個節點，列高 42（框高 38）；每深一層往右縮 26，框寬同步減 26；節點右邊隔 10 放一格用途說明（說明格用第 5 節的定義格 style）。

### 2.6 補充便條（白便條）

```
shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#ffffff;strokeColor=#999999;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;fontSize=12;
```

### 2.7 待處理便條（PEND，黃便條）

等使用者回覆或還沒解決的問題。文字第一行以「⚠ 待你回覆：」開頭，逐條編號。

```
shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#fff2cc;strokeColor=#d6b656;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;fontSize=12;
```

### 2.8 泳道

架構頁的泳道用 1.1 的顏色容器。流程頁的情境分組用淺灰泳道（1.1 最後一個）；頁面擠時改用小標題版（標題列 30、字 12）：

```
swimlane;html=1;rounded=1;startSize=30;fontStyle=1;fontSize=12;container=1;collapsible=1;recursiveResize=0;fillColor=#f5f5f5;swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;
```

流程頁的欄頭（誰做的那一欄）二選一，同一份圖統一：

純文字欄頭

```
text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;
```

灰底欄頭格

```
rounded=0;whiteSpace=wrap;html=1;fillColor=#e6e6e6;strokeColor=#999999;strokeWidth=1;fontSize=12;fontStyle=1;align=center;
```

### 2.9 標題

```
text;html=1;fontSize=18;fontStyle=1;align=left;verticalAlign=middle;
```

### 2.10 說明文字

圖例右邊的線型說明、泳道裡的一行附註用無框文字。

```
text;html=1;whiteSpace=wrap;align=left;verticalAlign=middle;fontSize=12;strokeColor=none;fillColor=none;
```

## 3. 圖例

**每頁都要有圖例。** 圖例只放本頁用得到的項目；本頁出現的每種顏色、形狀、線型都要在圖例裡找得到。

### 3.1 位置與排法

- 放在主體正下方：x = 40，y = 主體最低點 + 40。
- 項目由左往右排，項目之間隔 20。
- 一列高 60：泳道型項目高 60、貼齊列頂；方塊、便條、橢圓高 40，往下偏 10 置中；菱形高 60。
- 一列項目總寬不超過 1260，超過就換列，列距 66。
- 最後一個項目右邊放一格線型說明（2.10 的說明文字 style，寬 300、高 60），只放在第一列。
- 圖例格的 id 一律 `<頁前綴>_lg<n>`，線型說明 `<頁前綴>_lgt`，追加項 `<頁前綴>_lgx_<鍵>`。`extract_pages.py` 靠這個 id 分辨圖例與內容，lint 的顏色規則也靠它，不要改。

### 3.2 圖例項目長什麼樣

圖例項目是一個實際的樣本，字寫「顏色：意思」。顏色類的泳道項目用「圖例泳道」style（標題列 34、字 14、不當容器）：

```
swimlane;html=1;rounded=1;startSize=34;fontStyle=1;fontSize=14;container=0;collapsible=0;fillColor=#f8cecc;swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;
```

換色時只換 `fillColor`；紫色同時把 `strokeColor` 換成 `#9673a6`。其餘項目直接用第 1、2 節的 style。

| 鍵 | 樣本 style | 圖例文字 | 寬 × 高 |
|---|---|---|---|
| red | 圖例泳道（紅）| 紅：VK 要開發的模組 | 200 × 60 |
| green | 圖例泳道（綠）| 綠：使用 VK 的 repo | 200 × 60 |
| yellow | 圖例泳道（黃）| 黃：外部（使用者、外部系統）| 220 × 60 |
| purple | 圖例泳道（紫）| 紫：image／container | 200 × 60 |
| neutral | 圖例泳道（淺灰）| 淺灰：分組（無狀態意義）| 200 × 60 |
| flowgroup | 圖例泳道（淺灰）| 淺灰：情境分組（無狀態意義）| 220 × 60 |
| pimg | 紫方塊 | 紫：image／container | 200 × 40 |
| precipe | 紫方塊 | 紫：recipe（在引擎容器內執行）| 240 × 40 |
| blue | 藍方塊 | 藍：引擎做的（容器內）| 170 × 40 |
| white | 白方塊 | 白：最小單元 | 120 × 40 |
| step | 白方塊 | 白：步驟 | 88 × 40 |
| grey | 灰方塊 | 灰：主機上既有的軟體 | 170 × 40 |
| folder | 資料夾 | 實線框：資料夾 | 120 × 40 |
| file | 檔案 | 虛線框：repo 檔 | 150 × 40 |
| optfile | 檔案 | 虛線框：可有可無的檔 | 170 × 40 |
| rhomb | 黃菱形 | 黃：判斷 | 110 × 60 |
| startend | 綠橢圓 | 綠：起點／終點 | 130 × 40 |
| err | 紅橢圓 | 紅：錯誤終止 | 130 × 40 |
| human | 橙橢圓 | 橙：需人處理 | 130 × 40 |
| entry | 虛線橢圓 | 白虛線橢圓：跨頁出入口 | 220 × 40 |
| note | 白便條 | 便條：補充說明 | 130 × 40 |
| pend | 黃便條 | 黃便條：待處理問題 | 170 × 40 |

### 3.3 架構頁的圖例（`legend_arch`）

- 固定項，依序：red、green、yellow、pimg、white。
- 條件項，頁上有才加在固定項後面：neutral、grey、folder、file／optfile、note、pend。
- 線型說明：

  ```
  實線 = 傳輸內容（線上文字 = 傳什麼）
  虛線 = 只在特定情況發生
  ```

  頁上沒有虛線就只留第一行。

### 3.4 流程頁的圖例（`legend_flow`）

- 固定項，依序：flowgroup、rhomb；接著 startend、err（頁上有起訖、錯誤終止才放，一般都有）；precipe（頁上有在引擎容器內執行的步驟才放）；step。
- 條件項，頁上有才加在後面：human、blue、file、note、entry、pend。
- 線型說明：

  ```
  實線 = 執行順序（指向檔案時 = 寫入／讀取）
  虛線 = 之後才會發生
  ```

  頁上沒有虛線就只留第一行。

### 3.5 其他頁（表格、目錄樹、名詞頁）

照同一套規則，只放本頁用到的樣本；表格頁至少放分組、白格、表頭這幾類，並用線型說明交代表格怎麼讀（例：「表格：一列一件事」）。

## 4. 版面

### 4.1 頁面

- 基準畫布 1600 × 1100（`page()` 的預設）。內容以左上 (20, 20) 起算，左邊距 40。
- 實際紙張由 `page()` 自動裁：頂層格子的右下角再加 40。內容多時可以長高，但寬不超過 1650、高不超過 2400；超過就拆頁。
- `mxGraphModel` 固定屬性：`dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" math="0" shadow="0"`。
- 根格：`<mxCell id="0" style="strokeWidth=2;"/><mxCell id="1" parent="0" style="strokeWidth=2;"/>`。
- 頁的持久鍵是 `<diagram id>`，不是頁名也不是頁序；改名、換順序都不能換 id。

### 4.2 標題列

- **標題寫在頁名，頁面上不放標題格**。頁名只寫這頁是什麼（例如「VK 整體架構」），不加括號說明怎麼讀 —— 怎麼讀交給圖例的線型說明。
- 泳道從 (20, 40) 開始排。
- 待處理便條與標題同列、靠右：x = 1080，y = 12，寬 520，高依文字（行數 × 12 × 1.3 + 8 以上）。沒有待處理事項就不放。

### 4.3 架構頁的泳道

- 由左到右依資料流排直欄：外部（黃）→ image（紫）→ VK（紫容器，內含紅模組）→ 使用 VK 的 repo（綠）。
- 直欄頂端 y = 140，同一頁的直欄等高（1100 畫布下高 940）；欄與欄之間至少隔 20，中間要走線的欄距留到能放線上文字。
- 模組（紅泳道）放在 VK 容器內：容器內左邊距 20、頂端從 50 開始；模組上下至少隔 60（放線與線上文字）。
- 方塊放在模組內：第一格 (12, 45)，也就是標題列 38 下面再空 7。

### 4.4 流程頁的版面

流程頁不分泳道，版面規則見第 7 節。

### 4.5 方塊尺寸與間距

- 最小方塊 88 × 40。同一模組內的方塊等寬，橫向間距 4（格距 92）、縱向間距 7（格距 47）。
- 模組寬 = 12 + 方塊數 × 92；只放一列方塊時模組高 130。
- 字 14 是預設；格子多、字多的頁改 12（把 `fontSize=14` 換成 `fontSize=12`，長方形再加 `spacingLeft=6;spacingRight=6;`）。同一頁同類格子字級一致。
- 高度依文字算：行數 × 字級 × 1.3 + 8，不得小於 40。字不能溢出格子，`check_overflow.py` 會擋。
- 一格一件事：有兩件事就拆成兩格。

### 4.6 連線

所有連線都用正交線：

```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=default;strokeWidth=2;align=center;verticalAlign=bottom;spacingBottom=6;fontFamily=Helvetica;fontSize=12;fontColor=default;labelBorderColor=none;labelBackgroundColor=none;endArrow=block;endFill=1;
```

在這個基底後面依需要追加：

| 用途 | 追加 |
|---|---|
| 指定出入點 | `exitX=…;exitY=…;exitDx=0;exitDy=0;entryX=…;entryY=…;entryDx=0;entryDy=0;` |
| 虛線 | `dashed=1;` |
| 雙向（讀寫兩邊都有） | `startArrow=block;startFill=1;` |
| 垂直線、文字放線右 | `align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;` |
| 垂直線、文字放線左 | `align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;` |
| 水平線、文字放線下 | `verticalAlign=top;spacingTop=6;spacingBottom=0;` |

- 預設文字在水平線上方 6。文字沿線的位置用 `<mxGeometry x="-1…1" relative="1">` 調（-1 起點、1 終點）。
- 需要繞路時用 `<Array as="points">` 給轉折點，線不得穿過格子、不得壓到別條線的文字。
- 菱形只從底端中央或左右兩側出線。

### 4.7 線上文字與線型

- 架構頁：線上文字 = 這條線傳的資料（名詞，不寫動作），例如「dist 內容」「印記」。沒有文字的線不要畫。
- 流程頁：線代表執行順序，一般不寫字；判斷的出邊寫「是／否」或條件；指向檔案的線寫「寫入／讀取／建立」。
- 實線：架構頁 = 傳輸內容；流程頁 = 執行順序（指向檔案時 = 寫入／讀取）。
- 虛線：架構頁 = 只在特定情況發生；流程頁 = 之後才會發生。
- 線型的意思寫在圖例的線型說明裡（3.3、3.4），每頁都要有。

## 5. 頁面結構

一頁由上到下：

1. **標題列**：左邊標題（4.2），右邊待處理便條（有才放）。
2. **欄頭列**：流程頁才有，y = 60～64（4.4）。架構頁沒有欄頭，泳道自己的標題列就是欄頭。
3. **主體**：架構頁的直欄泳道（4.3），或流程頁的情境分組（4.4）。補充便條放在它說明的東西旁邊。
4. **圖例**：主體下方 40（第 3 節）。每頁都有。
5. **本頁名詞**（選用）：圖例下方；標題「本頁名詞」（字 13 粗體、靠左），下面兩欄表格，名詞與定義照抄 `CONTEXT.md`，只列本頁用到的。

本頁名詞表的兩種格：

名詞格

```
rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=12;fontStyle=1;align=left;spacingLeft=6;strokeWidth=1;
```

定義格（也是一般表格內容格）

```
rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=12;align=left;spacingLeft=6;strokeWidth=1;
```

## 6. 架構頁的補充規則（第 1 頁定稿時確立）

- **形狀統一用圓角方塊**。類型只靠填色區分，不用立方體、圓柱這類形狀；判斷用的菱形只出現在流程頁。
- **格子裡只寫名字，不寫類型也不寫說明**。「引擎 image」寫成「引擎」，類型交給填色與圖例。說明性的文字屬於流程頁。
- **線上文字寫傳的資料，不寫類型**。例如寫「dist 內容」「引擎程式」，不寫「工具 image」。
- **字不得壓到線或泳道邊框**。泳道之間至少留 100，讓線上文字落在空白處；畫完匯出成圖逐格檢查。
- **能對齊就拉直線**。兩端的格子調到同一條水平或垂直線上，避免轉彎；真的對不齊才加轉折點。
- **排緊**：泳道高度由最高那欄決定，其餘欄的格子往上貼。

## 7. 流程頁的規則（2026-09-29 定案）

這一節優先於前面各節裡講到流程頁的部分（1.1 的深紫、1.3 的藍、2.1～2.3 的黃綠紅橙、2.8 的淺灰情境分組、3.4 的彩色圖例）。架構頁照舊。

- **流程圖只畫要設計的流程**：不分「使用者／主機／引擎」泳道，也不標哪一步由誰做。流程裡的東西都還沒做出來，所以不用紅框標「VK 開發的」。
- **不上顏色**：所有格子白底黑框。靠形狀分類型：
  - 判斷 = 菱形（`rhombus`，白底、框粗 2）
  - 起點、終點 = 橢圓（`ellipse`，白底、框粗 2）；終點橢圓裡寫退出碼
  - 步驟 = 圓角方塊（`rounded=1`，白底、框粗 1）
- **標區塊用虛線框**：要標出一段流程屬於哪個區塊（例如「逐檔處理初始檔」），畫一個有名字的虛線框把那段圍起來。樣式 `rounded=1;dashed=1;fillColor=none;strokeColor=#666666;verticalAlign=top;align=left;spacingLeft=8;fontSize=14;`。虛線框放在格子下層，不是容器。
- **版面**：主流程直排一欄；分支往右排，迴圈回線走左側；多個結果匯回同一處時用右側匯流線。
- **使用者視角**：常用指令的流程頁（add、upgrade、dev）只畫使用者看得到的判斷與結果。執行紀錄、進度檔、預檢、取件細節、「要改先問」的 `-y`／CI 規則各自畫在共用頁。
- **圖例**：菱形「判斷」、橢圓「起點／終點」、圓角方塊「步驟」、虛線框「區塊」，外加文字「數字 = 退出碼；實線 = 執行順序」。
