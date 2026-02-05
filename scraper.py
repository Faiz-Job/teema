import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_teema():
    base_url = "https://b2b.teema.org.tw/CompanyList.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    all_companies = []
    
    # 假設抓取前 5 頁作為範例，若要全部抓取可調整範圍
    for page in range(1, 6):
        print(f"正在抓取第 {page} 頁...")
        params = {"page": page} # 根據網站實際分頁參數調整
        
        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=10)
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 根據網頁結構定位公司名稱所在的標籤 (此處為示意，需視網頁 HTML 調整)
            items = soup.find_all('div', class_='company-item') 
            
            for item in items:
                name = item.find('h3').text.strip() if item.find('h3') else "未知公司"
                all_companies.append({"公司名稱": name})
                
            time.sleep(1) # 避免請求過快被封鎖
        except Exception as e:
            print(f"抓取失敗: {e}")
            break

    df = pd.DataFrame(all_companies)
    df.to_csv("teema_companies.csv", index=False, encoding="utf-8-sig")
    print("抓取完成，檔案已儲存為 teema_companies.csv")

if __name__ == "__main__":
    scrape_teema()
