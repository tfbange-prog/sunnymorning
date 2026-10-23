"""每天挑一張早安圖，用 LINE 官方帳號群發給所有好友。

用法（通常由 GitHub 自動執行，不用手動跑）：
  環境變數 LINE_TOKEN     = Channel access token（放在 GitHub Secrets）
  環境變數 DRY_RUN=1      = 只試跑，不真的發送

挑圖規則：
  1. 如果 special/MM-DD.jpg 存在（例如 special/12-25.jpg），當天就用它（節日、節氣專用）
  2. 否則依日期輪播 images/ 資料夾裡的圖，依檔名排序，輪完再從頭開始
"""
import os
import re
import sys
import json
import uuid
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
TZ = timezone(timedelta(hours=8))  # 台北時間
EPOCH = datetime(2026, 1, 1, tzinfo=TZ).date()


def pick_image(today):
    md = today.strftime('%m-%d')
    # 節日專屬圖：最外層的 special_12-25.jpg，或 special/12-25.jpg
    for rel in ('special_%s.jpg' % md, 'special/%s.jpg' % md):
        if os.path.exists(os.path.join(ROOT, rel)):
            return rel
    # 每日輪播圖：檔名 d01.jpg、d02.jpg…，放在最外層或 images/ 資料夾都可以
    pool = []
    for folder in ('', 'images'):
        path = os.path.join(ROOT, folder)
        if os.path.isdir(path):
            for f in os.listdir(path):
                if re.match(r'^d\d+\.(jpg|jpeg|png)$', f, re.I):
                    pool.append((f.lower(), f if not folder else folder + '/' + f))
    if not pool:
        sys.exit('找不到早安圖：請把 d01.jpg、d02.jpg… 放在專案最外層')
    pool = [rel for _, rel in sorted(pool)]
    return pool[(today - EPOCH).days % len(pool)]


def raw_url(rel_path):
    repo = os.environ.get('GITHUB_REPOSITORY', 'OWNER/REPO')
    branch = os.environ.get('GITHUB_REF_NAME', 'main')
    return 'https://raw.githubusercontent.com/%s/%s/%s' % (repo, branch, urllib.parse.quote(rel_path))


def main():
    now = datetime.now(TZ)
    today = now.date()
    rel = pick_image(today)
    url = raw_url(rel)
    print('日期：%s  今天的圖：%s' % (today, rel))
    print('圖片網址：%s' % url)

    dry = os.environ.get('DRY_RUN')
    # 先確認圖片網址真的打得開
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=20) as r:
            print('圖片網址檢查：HTTP %s %s' % (r.status, r.headers.get('Content-Type')))
    except Exception as e:
        print('圖片網址檢查失敗：%s' % e)
        if not dry:
            sys.exit(1)

    if dry:
        print('試跑模式：不發送。')
        return

    token = os.environ.get('LINE_TOKEN')
    if not token:
        sys.exit('找不到 LINE_TOKEN，請到 GitHub 的 Secrets 設定')

    body = {'messages': [{'type': 'image', 'originalContentUrl': url, 'previewImageUrl': url}]}
    req = urllib.request.Request(
        'https://api.line.me/v2/bot/message/broadcast',
        data=json.dumps(body).encode('utf-8'),
        method='POST',
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token,
            # 同一天重試不會重複發送
            'X-Line-Retry-Key': str(uuid.uuid5(uuid.NAMESPACE_URL, 'sunnymorning-' + str(today))),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print('發送成功：HTTP %s' % r.status)
    except urllib.error.HTTPError as e:
        print('發送失敗：HTTP %s %s' % (e.code, e.read().decode('utf-8', 'replace')))
        sys.exit(1)


if __name__ == '__main__':
    main()
