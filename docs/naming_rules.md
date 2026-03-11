# MAPLAB Image Naming Rules — v1.2 (2026-03-11)
> 核心原則：所有圖片命名須包含「地點/活動識別 + 類型 + 描述關鍵字」，
> 以支援 SEO、廣告追蹤與跨部門查找。
> 統一格式確保 GA4/Clarity 天眼系統可連結每張素材到轉換數據。
---
## Pattern 1：活動照片 (Event Photo)
```
EVT{YYYYMMDD}_{item_id}_{location}_{description}_{seq:02d}.webp
```
- 範例：`EVT20260310_DES-CKE-001_tainan_candybar_01.webp`
- 範例：`EVT20260815_APP-SAL-003_kaohsiung_outdoor-wedding_02.webp`
| 欄位 | 說明 |
|------|------|
| `EVT{YYYYMMDD}` | 活動日期，對應 EVENT_MASTER.event_id |
| `{item_id}` | 菜單品項 ID（TYPE-SUBTYPE-SEQ3）；無特定品項可省略 |
| `{location}` | 地點英文：tainan / kaohsiung / taichung |
| `{description}` | kebab-case 描述：candybar / outdoor-wedding / buffet-setup |
| `{seq:02d}` | 序號 01–99，同活動同品項多張時遞增 |
| `.webp` | 由 transformer.py 統一轉換 |
---
## Pattern 2：食物／通用素材 (Food / Stock Photo)
```
foodphoto-{cuisine}-{dish}-{YYYYMMDD}-{seq:03d}.webp
```
- 範例：`foodphoto-taiwanese-braised-pork-rice-20260310-001.webp`
- 範例：`foodphoto-dessert-caramel-pudding-20260815-003.webp`
| 欄位 | 說明 |
|------|------|
| `foodphoto` | 固定前綴，標示通用食物素材 |
| `{cuisine}` | 料理類別：taiwanese / western / dessert / buffet |
| `{dish}` | kebab-case 菜名英文：braised-pork-rice |
| `{YYYYMMDD}` | 拍攝日期 |
| `{seq:03d}` | 序號 001–999 |
使用時機：非特定活動的食物照、菜單示意圖、ASSET_MASTER 通用素材庫。
---
## Pattern 3：SEO 部落格圖片 (SEO Blog Image)
```
{ground}-{type}-{keyword}.avif   ← 優先
{ground}-{type}-{keyword}.webp   ← 平台不支援 avif 時
```
- 範例：`tainan-corporate-opening-buffet-catering.avif`
- 範例：`tainan-birthday-party-dessert-table.avif`
- 範例：`kaohsiung-wedding-outdoor-catering.avif`
| 欄位 | 說明 |
|------|------|
| `{ground}` | 地點：tainan / kaohsiung / taichung |
| `{type}` | 活動類型：corporate-opening / birthday-party / wedding / graduation |
| `{keyword}` | 服務關鍵字：buffet-catering / dessert-table / outdoor-catering |
**Alt Text 規則（RankMath SOP）**
格式：`台南{活動類型}外燴{描述} - MAPLAB Kitchen`
→ 由 archiver.py 讀取 ASSET_MASTER.alt_text 欄位自動填入 Notion。
---
## Pattern 4：廣告素材 (Ad Creative)
```
AD_{platform}_{campaign}_{creative_id}_{size}_{seq:02d}.webp
```
- 範例：`AD_meta_birthday2026_CRE001_1080x1080_01.webp`
- 範例：`AD_google_corporate2026_CRE003_1200x628_02.webp`
| 欄位 | 說明 |
|------|------|
| `{platform}` | 投放平台：meta / google / line |
| `{campaign}` | 活動名稱：birthday2026 / corporate2026 / wedding2026 |
| `{creative_id}` | 素材識別碼 CRE001–CREnnn，對應 ASSET_MASTER.creative_id |
| `{size}` | 廣告尺寸：1080x1080 / 1200x628 / 1080x1920 |
| `{seq:02d}` | 序號 01–99，同 creative 多張變體時遞增 |
**UTM 追蹤欄位（存入 ASSET_MASTER）**
| 欄位 | 值 |
|------|----|
| utm_source | meta / google / line |
| utm_medium | cpc / paid_social |
| utm_campaign | birthday2026 / corporate2026 |
| utm_content | creative_id |
| lp_version | v1 / v2 / v3（對應落地頁版本）|
| cta_variant | line / phone / form |
---
## 品項 ID 格式 — TYPE-SUBTYPE-SEQ3
```
{TYPE}-{SUBTYPE}-{SEQ3}
```
**TYPE（大類）**
| 代碼 | 意義 |
|------|------|
| APP | 前菜/輕食 (Appetizer) |
| SOU | 湯品 (Soup) |
| MAI | 主菜 (Main Course) |
| STA | 澱粉/主食 (Starch) |
| VEG | 蔬菜 (Vegetable) |
| DES | 甜點 (Dessert) |
| BEV | 飲品 (Beverage) |
| DEC | 裝飾/佈置 (Decoration) |
**SUBTYPE 範例**
| 代碼 | 意義 |
|------|------|
| DES-CKE | 蛋糕類 |
| DES-CAN | 糖果/喜糖類 |
| APP-SAL | 沙拉類 |
| MAI-SEA | 海鮮主菜 |
| MAI-MEA | 肉類主菜 |
SEQ3：3 位數序號，從 001 開始。
範例：`DES-CKE-001`（焦糖布丁蛋糕）、`APP-SAL-003`（凱薩沙拉）、`MAI-SEA-007`（煙燻鮭魚）
---
## 快速對照表
| 使用情境 | Pattern | 格式 |
|----------|---------|------|
| 活動照片（外燴現場） | Pattern 1 EVT | `EVT{YYYYMMDD}_{item_id}_{loc}_{desc}_{seq}.webp` |
| 食物/菜單示意圖（非特定活動） | Pattern 2 foodphoto | `foodphoto-{cuisine}-{dish}-{date}-{seq}.webp` |
| SEO 部落格/網站圖片 | Pattern 3 SEO | `{ground}-{type}-{keyword}.avif` |
| 廣告素材（Meta/Google/LINE） | Pattern 4 AD | `AD_{platform}_{campaign}_{cid}_{size}_{seq}.webp` |
| 品項 ID（菜單/裝飾道具） | item_id | `{TYPE}-{SUBTYPE}-{SEQ3}`（如 DES-CKE-001）|
