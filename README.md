# 早安陽光｜每日早安圖自動推播

每天早上 7:00，自動挑一張早安圖，發給「早安陽光」所有好友。設定好之後不用再管。

## 一次性設定（約 15 分鐘）

### 1. 建立 GitHub 專案
1. 到 github.com 註冊（已有帳號就登入）。
2. 右上角「+」→「New repository」。
3. 名稱填 `sunnymorning`，選 **Public**（公開，LINE 才抓得到圖片），按「Create repository」。

### 2. 上傳檔案
1. 在新專案頁面點「uploading an existing file」。
2. 解壓縮 zip 後，把**裡面的所有檔案和資料夾**拖進去（不是拖 zip 本身）。
3. 往下捲，按「Commit changes」。
4. 檢查專案裡有沒有 `.github` 資料夾。若沒有（有些電腦會漏掉隱藏資料夾）：
   - 「Add file」→「Create new file」
   - 檔名欄輸入 `.github/workflows/daily.yml`（打斜線會自動變資料夾）
   - 把 zip 裡 `.github/workflows/daily.yml` 的內容整段貼進去，Commit。

### 3. 放入權杖（加密保存）
1. 專案頁面 →「Settings」→ 左側「Secrets and variables」→「Actions」。
2. 「New repository secret」。
3. Name 填 `LINE_TOKEN`（要完全一樣，全大寫）。
4. Secret 貼上你的 Channel access token，按「Add secret」。
> 權杖是帳號的鑰匙，只貼在這裡，不要貼到別處。

### 4. 先試跑，再正式測
1. 專案上方「Actions」→ 若出現提示，按「I understand…enable」。
2. 左側點「每日早安圖」→ 右邊「Run workflow」。
3. 預設 dry_run 是 `true`（只檢查不發送）。按綠色按鈕，等 1 分鐘，點進去看紀錄：
   應該會看到「今天的圖」和「圖片網址檢查：HTTP 200」。
4. 沒問題後再按一次，把 dry_run 改成 `false`，這次會真的發給好友（目前只有你自己，剛好測試）。
5. 看 LINE 有沒有收到圖。

完成！之後每天早上 7:00 會自動發送。

## 日常使用

- **新增圖片**：把圖丟進 `images/` 資料夾（1080×1080 的 JPG，不要太大，1MB 內）。程式依檔名順序輪播，圖越多不重複的天數越長。
- **節日專屬圖**：放進 `special/`，檔名用「月-日.jpg」，例如 `special/12-25.jpg`，當天就會用它。（資料夾不存在就自己建立）
- **生日圖**：放在 `birthday/`，目前沒有自動使用，之後可放進圖文選單。
- 目前 19 張，輪播 19 天一輪。

## 注意事項

- 發送時間可能比 7:00 晚幾分鐘，GitHub 的排程有時會延遲。
- GitHub 如果長時間沒有專案活動，會停用排程。本專案每月 1 號會自動更新一個檔案來避免，但如果哪天收到 GitHub 的通知信說排程被停用，到 Actions 頁面按「Enable」就好。
- 每次群發都會計入 LINE 官方帳號的每月訊息則數，好友多了請到 LINE 後台確認方案。
- 圖片網址依賴專案是 Public，不要改成 Private。
