from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        keyword = params.get('keyword', [''])[0]
        results = []
        if keyword:
            url = f"https://movies.yahoo.com.tw/moviesearch_result.html?keyword={keyword}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            try:
                res = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(res.text, 'html.parser')
                items = soup.find_all('div', class_='release_info')
                for item in items:
                    name_tag = item.find('div', class_='release_movie_name').a
                    results.append({
                        "title": name_tag.text.strip(),
                        "link": name_tag['href'],
                        "poster": item.find_previous('div', class_='release_foto').img['src']
                    })
            except: pass
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(results).encode())
