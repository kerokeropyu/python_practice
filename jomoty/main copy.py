import requests
from bs4 import BeautifulSoup
import time

class JomotyScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get_last_page_number(self):
        url = f"{self.base_url}/p-1"
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        last = soup.select_one("li.last a")
        return int(last.text.strip()) if last else None
    
    # 一覧からリンクを取得
    def get_target_links(self, max_pages=5):
        all_links = []
        last_page = self.get_last_page_number()
        max_pages = min(max_pages, last_page) if last_page else max_pages

        for i in range(1, max_pages + 1):
            url = f"{self.base_url}/p-{i}"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            page_links = soup.select('div.p-item-title a')

            for page_link in page_links:
                all_links.append(page_link.get('href'))

            if not page_links:
                break

            time.sleep(0.1)

        return all_links
    
    # 取得したリンクから女性の投稿のURLのみ取得
    def filter_female_posts(self, target_links):
        filtered_links = []
        for link in target_links:
            # 各リンクにアクセスして女性の投稿かどうかを判断するロジック
            # 例: 投稿の内容を解析し、女性の投稿と判断されたらリストに追加
            if self.is_female_post(link):
                filtered_links.append(link)
        return filtered_links
        
    # 女性の投稿のみ取得
    def is_female_post(self, link):
        try:
            response = self.session.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 性別情報を含む要素を探す
            gender_element = soup.select_one('td.p-article-column-key:contains("投稿者") + td.p-article-column-value div')
            
            if gender_element:
                gender = gender_element.text.strip()
                print(gender)
                return gender == "女性"
            else:
                print(f"性別情報が見つかりません: {link}")
                return False
        except Exception as e:
            print(f"エラーが発生しました: {link} - {str(e)}")
            return False
# 使用例
if __name__ == "__main__":
    base_url = 'https://jmty.jp/hyogo/com'
    scraper = JomotyScraper(base_url)
    
    target_links = scraper.get_target_links(max_pages=5)
    woman = scraper.filter_female_posts(target_links)

    # 結果の表示
    print(f"Total links found: {len(target_links)}")
    # for link in target_links[:10]:  # 最初の10件のみ表示
    #     print(link)