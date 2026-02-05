from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

def scrape_teema():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    all_companies = []

    try:
        url = "https://b2b.teema.org.tw/CompanyList.aspx"
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # 這裡設定抓取前 5 頁
        for p in range(1, 6):
            print(f"目前正在處理第 {p} 頁...")
            time.sleep(3) 
            
            # 抓取當前頁面的公司名稱
            links = driver.find_elements(By.CSS_SELECTOR, 'a[id*="hlCompanyName"]')
            for l in links:
                name = l.text.strip()
                if name: all_companies.append({"公司名稱": name})
            
            print(f"第 {p} 頁完成，目前累計 {len(all_companies)} 筆")

            if p < 5:
                # 根據您的觀察，ID 邏輯是 ctl02, ctl03...
                btn_id = f"ctl00_ContentPlaceHolder1_Repeater1_ctl0{p+1}_lnkPage"
                try:
                    next_btn = wait.until(EC.element_to_be_clickable((By.ID, btn_id)))
                    next_btn.click()
                except:
                    print(f"找不到按鈕 {btn_id}，可能已到末頁。")
                    break

    except Exception as e:
        print(f"錯誤: {e}")
    finally:
        driver.quit()

    if all_companies:
        df = pd.DataFrame(all_companies).drop_duplicates()
        df.to_csv("teema_companies.csv", index=False, encoding="utf-8-sig")
        print(f"🎉 成功抓取 {len(df)} 筆。")

if __name__ == "__main__":
    scrape_teema()
