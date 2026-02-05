import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_teema():
    # 這是電電公會 B2B 的精確網址
    url = "https://b2b.teema.org.tw/CompanyList.aspx"
    
    # 加入更完整的 Browser Headers，模擬真人行為
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    all_companies = []
    
    # 我們先嘗試抓取第 1 到第 3 頁
    for page in range(1, 4):
        print(f"嘗試抓取第 {page} 頁...")
        
        try:
            # 根據網站觀察，分頁參數通常是頁碼
            target_url = f"{url}?company=&page={page}"
            response = requests.get(target_url, headers=headers, timeout=20)
            
            if response.status_code != 200:
                print(f"連線失敗，狀態碼：{response.status_code}")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 精確定位：TEEMA 的公司名稱通常在 class="comp-name" 或特定的 <a> 標籤內
            # 這裡使用更廣泛的搜尋方式
            links = soup.select('a[href*="CompanyDetail.aspx"]')
            
            for link in links:
                name = link.get_text(strip=True)
                if name and len(name) > 1: # 過濾掉空字串或單一字元
                    all_companies.append({"公司名稱": name})
            
            print(f"第 {page} 頁抓取成功，目前累計 {len(all_companies)} 筆資料")
            time.sleep(3) # 增加延遲避免被鎖 IP
            
        except Exception as e:
            print(f"抓取過程中發生錯誤: {e}")

    # 儲存結果
    if all_companies:
        df = pd.DataFrame(all_companies).drop_duplicates()
        df.to_csv("teema_companies.csv", index=False, encoding="utf-8-sig")
        print(f"任務完成！共存檔 {len(df)} 筆不重複資料。")
    else:
        print("警告：完全沒有抓到資料，可能網頁結構已改變或被阻擋。")

if __name__ == "__main__":
    scrape_teema()
