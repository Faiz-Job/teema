import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def scrape_teema():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # 初始化空檔案，確保上傳步驟不會失敗
    pd.DataFrame(columns=["公司名稱"]).to_csv("teema_companies.csv", index=False, encoding="utf-8-sig")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        url = "https://b2b.teema.org.tw/CompanyList.aspx"
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        all_companies = []
        page_num = 1

        while True:
            print(f"🚀 正在爬取第 {page_num} 頁...")
            
            # 等待公司名稱欄位出現
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id*="hlCompanyName"]')))
            except TimeoutException:
                print("等待超時，可能已到最後一頁。")
                break
            
            # 獲取當前頁面公司名稱
            items = driver.find_elements(By.CSS_SELECTOR, 'a[id*="hlCompanyName"]')
            for item in items:
                name = item.text.strip()
                if name:
                    all_companies.append({"公司名稱": name})
            
            print(f"✅ 第 {page_num} 頁抓取完畢，目前累計 {len(all_companies)} 筆資料")

            # 尋找「下一頁」按鈕
            # 根據常見結構搜尋包含 ">" 符號的連結或特定 ID
            try:
                # 優先尋找文字包含 ">" 的按鈕，這通常是分頁列的「下一頁」
                next_btn = driver.find_element(By.XPATH, "//a[contains(text(), '>')]")
                
                # 滾動到按鈕位置並點擊
                driver.execute_script("arguments[0].scrollIntoView();", next_btn)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", next_btn)
                
                page_num += 1
                time.sleep(3) # 緩衝時間，避免請求過快
            except NoSuchElementException:
                print("🏁 找不到下一頁按鈕，抓取結束。")
                break

        # 最終儲存不重複資料
        if all_companies:
            df = pd.DataFrame(all_companies).drop_duplicates()
            df.to_csv("teema_companies.csv", index=False, encoding="utf-8-sig")
            print(f"🎉 任務大功告成！總計抓取 {len(df)} 筆公司名單。")

    except Exception as e:
        print(f"❌ 執行發生錯誤: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    scrape_teema()
