name: Run Scraper

on:
  workflow_dispatch: # 讓你可以手動點擊按鈕執行

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: 檢出程式碼
        uses: actions/checkout@v3

      - name: 設定 Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: 安裝套件
        run: pip install -r requirements.txt

      - name: 執行爬蟲
        run: python scraper.py

      - name: 上傳結果
        uses: actions/upload-artifact@v4
        with:
          name: scraper-results
          path: teema_companies.csv
