import sys
import os
import json
import requests
from bs4 import BeautifulSoup
import time
import mysql.connector
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import demoji

class JomotyScraper:
    def __init__(self, base_url, prefecture):
        self.base_url = base_url
        self.prefecture = prefecture
        self.session = requests.Session()
        self.setup_logging()

    def setup_logging(self):
        # logsフォルダが存在しない場合は作成
        if not os.path.exists('logs'):
            os.makedirs('logs')

        log_filename = f'logs/jomoty_scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        handler = RotatingFileHandler(log_filename, maxBytes=10*1024*1024, backupCount=5)
        logging.basicConfig(level=logging.INFO, handlers=[handler],
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def get_last_page_number(self):
        url = f"{self.base_url}/p-1"
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        last = soup.select_one("li.last a")
        return int(last.text.strip()) if last else None
    
    def get_target_links(self, max_pages=5):
        all_links = []
        last_page = self.get_last_page_number()
        max_pages = min(max_pages, last_page) if last_page else max_pages
        # for i in range(1, 2 + 1): # テスト用コード
        for i in range(1, max_pages + 1):
            url = f"{self.base_url}/p-{i}"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            articles = soup.select('li.p-articles-list-item')

            for article in articles:
                closed = article.select_one('div.p-item-close-text')
                if closed and '受付終了' in closed.text:
                    continue

                page_link = article.select_one('div.p-item-title a')
                if page_link:
                    all_links.append(page_link.get('href'))

            if not articles:
                break

            time.sleep(0.1)
        
        logging.info(f"取得したリンクの数: {len(all_links)}")
        return all_links
    
    def get_post_details(self, target_links):
        post_details = []
        for link in target_links:
            details = self.add_post_info(link)
            if details:
                post_details.append(details)
        return post_details
        
    def add_post_info(self, link):
        try:
            response = self.session.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            gender_element = soup.select_one('td.p-article-column-key:contains("投稿者") + td.p-article-column-value div')
            gender = gender_element.text.strip() if gender_element else "性別情報なし"

            region_element = soup.select_one('td.p-article-column-key:contains("地域") + td.p-article-column-value')
            region = region_element.text.strip() if region_element else "地域情報なし"

            activity_place_element = soup.select_one('td.p-article-column-key:contains("活動場所") + td.p-article-column-value')
            activity_place = activity_place_element.text.strip() if activity_place_element else "活動場所情報なし"

            history_elements = soup.select('div.p-article-history div')
            created_at = updated_at = None
            for element in history_elements:
                text = element.text.strip()
                if "作成" in text:
                    created_at_str = text.replace("作成", "").strip()
                    created_at = self.convert_date_format(created_at_str)
                elif "更新" in text:
                    updated_at_str = text.replace("更新", "").strip()
                    updated_at = self.convert_date_format(updated_at_str)

            title_element = soup.select_one('h1.p-article-title')
            title = title_element.text.strip() if title_element else "タイトル情報なし"

            logging.info(f"Gender: {gender}, URL: {link}, Region: {region}, Activity Place: {activity_place}, Created: {created_at}, Updated: {updated_at}, Title: {title}")

            return {
                "gender": gender,
                "url": link,
                "region": region,
                "activity_place": activity_place,
                "created_at": created_at,
                "updated_at": updated_at,
                "title": title,
                "prefecture": self.prefecture  # 都道府県情報を追加
            }
        except Exception as e:
            logging.error(f"エラーが発生しました: {link} - {str(e)}")
            return None

    def convert_date_format(self, date_string):
        try:
            # '2024年10月26日 17:50' 形式の文字列をdatetimeオブジェクトに変換
            dt = datetime.strptime(date_string, '%Y年%m月%d日 %H:%M')
            # 'YYYY-MM-DD HH:MM:SS' 形式に変換
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            logging.error(f"日付の変換に失敗しました: {date_string}")
            return None

class DatabaseHandler:
    def __init__(self, db_config):
        self.db_config = db_config

    def save_to_database(self, post_details, prefecture):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

        # テーブルが存在しない場合は作成
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jomoty_posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            prefecture VARCHAR(20),
            title VARCHAR(255),
            gender VARCHAR(20),
            url VARCHAR(255),
            region VARCHAR(100),
            activity_place VARCHAR(255),
            created_at DATETIME,
            updated_at DATETIME,
            scraped_at DATETIME
        )
        """)

        # 既存のデータを削除するかどうかをフラグで制御
        sql = "DELETE FROM jomoty_posts WHERE prefecture = %s"
        pre = (prefecture, )
        cursor.execute(sql, pre)

        # 新しいデータを挿入
        for post in post_details:
            sql = """INSERT INTO jomoty_posts 
                     (prefecture, title, gender, url, region, activity_place, created_at, updated_at, scraped_at)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (
                post['prefecture'],
                self.remove_emoji_and_newlines(post['title']),
                post['gender'],
                post['url'],
                post['region'],
                post['activity_place'],
                post['created_at'] if post['created_at'] else None,
                post['updated_at'] if post['updated_at'] else None,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            cursor.execute(sql, values)

        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"{len(post_details)} 件の投稿をデータベースに保存しました")

    def generate_sql_file(self, post_details, prefecture):
        # sqlフォルダが存在しない場合は作成
        if not os.path.exists('sql'):
            os.makedirs('sql')

        output_file = f'sql/update_jomoty_posts_{prefecture}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql'
        sql_content = self.generate_sql_string(post_details, prefecture)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sql_content)

        logging.info(f"SQL文を {output_file} に出力しました")
        return sql_content

    def generate_sql_string(self, post_details, prefecture):
        sql_lines = []
        # sql_lines.append("START TRANSACTION;")
        sql_lines.append("DELETE FROM jomoty_posts where {prefecture};")
        sql_lines.append("INSERT INTO jomoty_posts (prefecture, title, gender, url, region, activity_place, created_at, updated_at, scraped_at) VALUES")

        value_lines = []
        for post in post_details:
            values = (
            	post['prefecture'].replace("'", "''"),
                self.remove_emoji_and_newlines(post['title']).replace("'", "''"),
                post['gender'].replace("'", "''"),
                post['url'].replace("'", "''"),
                post['region'].replace("'", "''"),
                post['activity_place'].replace("'", "''"),
                f"'{post['created_at']}'" if post['created_at'] else 'NULL',
                f"'{post['updated_at']}'" if post['updated_at'] else 'NULL',
                f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'"
            )
            
            value_line = f"('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}', '{values[5]}', {values[6]}, {values[7]}, {values[8]})"
            
            value_lines.append(value_line)

        sql_lines.append(",\n".join(value_lines) + ";")
        # sql_lines.append("COMMIT;")

        return "\n".join(sql_lines)

    def generate_json_file(self, post_details, prefecture):
        # jsonフォルダが存在しない場合は作成
        if not os.path.exists('json'):
            os.makedirs('json')

        output_file = f'json/jomoty_posts_{prefecture}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(post_details, f, ensure_ascii=False, indent=2)

        logging.info(f"JSONデータを {output_file} に出力しました")

    def remove_emoji_and_newlines(self, text):
        # 絵文字を削除
        text_without_emoji = demoji.replace(string=text, repl="")
        
        # 改行を削除
        clean_text = text_without_emoji.replace('\n', '')
        
        return clean_text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <prefecture>")
        sys.exit(1)

    prefecture = sys.argv[1]
    start_time = datetime.now()
    logging.info(f"スクレイピング開始: {start_time}")

    base_url = f'https://jmty.jp/{prefecture}/com'
    db_config = {
        'host': 'localhost',
        'user': 'sail',
        'password': 'password',
        'database': 'laravel'
    }
    scraper = JomotyScraper(base_url, prefecture)
    db_handler = DatabaseHandler(db_config)
    
    target_links = scraper.get_target_links(max_pages=5)
    logging.info(f"取得したターゲットリンクの数: {len(target_links)}")

    post_details = scraper.get_post_details(target_links)
    logging.info(f"{len(post_details)} 件の投稿の詳細をスクレイピングしました")

    # SQLファイルの生成
    sql = db_handler.generate_sql_file(post_details, prefecture)

    # JSONファイルの生成
    db_handler.generate_json_file(post_details, prefecture)

    # データベースに保存
    db_handler.save_to_database(post_details, prefecture)

    end_time = datetime.now()
    logging.info(f"スクレイピング終了: {end_time}")
    logging.info(f"実行時間: {end_time - start_time}")

    # 結果の表示（コンソール出力）
    print(f"スクレイピングされた投稿の総数: {len(post_details)}")