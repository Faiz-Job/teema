import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_teema():
    url = "https://b2b.teema.org.tw/CompanyList.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": url
    }
    
    session = requests.Session()
    all_companies = []

    try:
        # 1. 抓取第一頁
        print("正在抓取第 1 頁...")
        res = session.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')

        def extract_names(s):
            # 根據您觀察到的 ID 結構抓取公司名稱
            links = s.select('a[id*="lnkCompanyName"], a[id*="hlCompanyName"]')
            return [{"公司名稱": l.get_text(strip=True)} for l in links if l.get_text(strip=True)]

        all_companies.extend(extract_names(soup))

        # 2. 模擬點擊 ctl02, ctl03, ctl04, ctl05
        # 這裡 i 對應您看到的編號
        for i in range(2, 6):
            target = f'ctl00$ContentPlaceHolder1$Repeater1$ctl0{i}$lnkPage'
            print(f"正在模擬點擊分頁按鈕：{target}...")

            # 每次 PostBack 都要攜帶最新的隱藏欄位值
            payload = {
                "__EVENTTARGET": target,
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": soup.find("input", {"name": "__VIEWSTATE"})["value"],
                "__VIEWSTATEGENERATOR": soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"],
                "__EVENTVALIDATION": soup.find("input", {"name": "__EVENTVALIDATION"})["value"],
            }

            # 必須使用 POST 方法
            res = session.post(url, headers=headers, data=payload)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            p_data = extract_names(soup)
            if not p_data:
                print(f"警告：在 {target} 未抓到資料。")
                break
                
            all_companies.extend(p_data)
            print(f"成功抓取分頁資料，累計 {len(all_companies)} 筆")
            time.sleep(2)

    except Exception as e:
        print(f"執行出錯: {e}")

    # 儲存 CSV
    if all_companies:
        df = pd.DataFrame(all_companies).drop_duplicates()
        df.to_csv("teema_companies.csv", index=False, encoding="utf-8-sig")
        print(f"🎉 任務完成！共存檔 {len(df)} 筆資料。")

if __name__ == "__main__":
    scrape_teema()
