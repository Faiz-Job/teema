import os
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
    chrome_options.add_argument("--window-size=1920,1080")
    
    # 預防性建立空檔
    pd.DataFrame(columns=["公司名稱"]).to_csv("teema_companies.csv", index=False, encoding="utf-8-sig")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        url = "https://b2b.teema.org.tw/CompanyList.aspx"
        driver.get(url)
        wait = WebDriverWait(driver, 30)

        all_companies = []
        page_num = 1

        while True:
            print(f"🚀 目前正在處理第 {page_num} 頁...")
            
            # 等待資料載入
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id*="CompanyName"]')))
            except:
                print("等待超時，可能已到末頁或網路異常。")
                break
                
            time.sleep(3) # 緩衝時間
            
            # 抓取當前頁面資料
            links = driver.find_elements(By.CSS_SELECTOR, 'a[id*="CompanyName"]')
            for l in links:
                name = l.text.strip()
                if name:
                    all_companies.append({"公司名稱": name})
            
            print(f"✅ 第 {page_num} 頁完成，目前累計 {len(all_companies)} 筆資料")

            # 儲存暫存檔，預防程式中斷
            pd.DataFrame(all_companies).drop_duplicates().to_csv("teema_companies.csv", index=False, encoding="utf-8-sig")

            # 尋找「下一頁」按鈕
            # ASP.NET 的下一頁按鈕通常是一個包含 ">" 或 "Next" 的 LinkButton
            try:
                # 尋找文字內容包含 ">" 的按鈕，這通常是下一頁的符號
                next_btns = driver.find_elements(By.XPATH, "//a[contains(text(), '>')]")
                if next_btns:
                    next_btn = next_btns[0]
                    # 滾動到該按鈕位置
                    driver.execute_script("arguments[0].scrollIntoView();", next_btn)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", next_btn)
                    page_num += 1
                    time.sleep(2)
                else:
                    print("🏁 找不到下一頁按鈕，抓取結束。")
                    break
            except Exception as e:
                print(f"停止跳頁的原因: {e}")
                break

        print(f"🎉 任務大成功！總共抓取 {len(all_companies)} 筆公司名單。")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    scrape_teema()
