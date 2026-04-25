import requests
from bs4 import BeautifulSoup

def movie_crawler():
    # 讓使用者輸入關鍵字
    keyword = input("請輸入想搜尋的電影片名關鍵字: ")
    
    # 搜尋 URL
    search_url = f"https://movies.yahoo.com.tw/moviesearch_result.html?keyword={keyword}"
    
    # 加入 Headers 模擬瀏覽器，這就是你說的避開 robots.txt 限制的常用手段
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 抓取電影資訊區塊
        items = soup.find_all('div', class_='release_info')
        
        print(f"\n找到 {len(items)} 筆相關結果：\n" + "="*50)
        
        for item in items:
            # 1. 抓取片名與連結
            name_tag = item.find('div', class_='release_movie_name').find('a')
            title = name_tag.text.strip()
            link = name_tag['href']
            
            # 2. 抓取海報 (海報通常在 release_info 旁邊的 release_foto 裡)
            foto_div = item.find_previous_sibling('div', class_='release_foto')
            img_tag = foto_div.find('img') if foto_div else None
            img_url = img_tag['src'] if img_tag else "無海報網址"
            
            print(f"【片名】：{title}")
            print(f"【介紹頁】：{link}")
            print(f"【海報】：{img_url}")
            print("-" * 50)
            
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    movie_crawler()