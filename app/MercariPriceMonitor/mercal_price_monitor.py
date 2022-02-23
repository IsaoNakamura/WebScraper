import sys
import os
import time
import datetime
from typing import List

# 実行ファイルのディレクトリ絶対パスを取得
EXECFILE_DIR = os.path.dirname(os.path.abspath(__file__))

# 入力ファイルの格納場所は、実行ファイルディレクトリからの相対パスで指定できる
SRC_DIR = os.path.join(EXECFILE_DIR, './')

# 自作モジュールの格納場所は、実行ファイルディレクトリからの相対パスで指定できる
sys.path.append(os.path.join(EXECFILE_DIR, '../../'))
# internal import
from lib.util_selenium import UtilSelenium
from lib.util_line_notify import UtilLineNotify
from lib.util_gspread import UtilGspread
from lib.util_signal import UtilSignal
from lib.util_json import UtilJson

class MercariPriceScraper():
    def __init__(self, config:dict,) -> None:
        self.config = None
        self.line_notify = None
        self.price_scraper = None
        try:
            self.config = config
            UtilSignal.set_killtrap_handler()
            self.line_notify = UtilLineNotify(self.config['line_api_setting'])
            self.price_scraper = UtilSelenium()
        except Exception as err:
            print(err)
            raise
    
    def __del__(self) -> None:
        try:
            pass
        except Exception as err:
            print(err)
            raise

    def _finalize(self):
        try:
            UtilSignal.pause_kill()
            self.price_scraper.quit()
        except Exception as err:
            print(err)
        finally:
            UtilSignal.resume_kill()

    def exec(self):
        try:
            interval_sec = self.config['interval_sec']
            
            gssheet_setting = self.config['gssheet_setting']
            google_api_setting = self.config['google_api_setting']
            
            workbook_key = google_api_setting['workbook_key']
            access_key_filepath = google_api_setting['access_key_filepath']
            workbook = UtilGspread.get_workbook(workbook_key, access_key_filepath)
            
            query_sheet_name = gssheet_setting['query_sheet']['sheet_name']
            query_worksheet = workbook.worksheet(query_sheet_name)
            
            searched_sheet_name = gssheet_setting['searched_sheeet']['sheet_name']
            searched_worksheet = workbook.worksheet(searched_sheet_name)
            searched_key = gssheet_setting['searched_sheeet']['key_header']
            searched_header_row = gssheet_setting['searched_sheeet']['header_row']
            searched_beg_column = gssheet_setting['searched_sheeet']['beg_column']
            
            target_url = self.config["target_url"]
            
            while True:
                query_items, query_headers = UtilGspread.load_sheet_items_with_retry(query_worksheet, gssheet_setting['query_sheet'])
                searched_items, searched_headers = UtilGspread.load_sheet_items_with_retry(searched_worksheet, gssheet_setting['searched_sheeet'])
                for query_key in query_items:
                    query_item = query_items[query_key]
                    if query_item['title'] is None:
                        continue
                    keywords = query_item['title']
                    if query_item['consumer_game'] is not None:
                        keywords = keywords + '+' + query_item['consumer_game']
                    if query_item['keyword'] is not None:
                        keywords = keywords + '+' + query_item['keyword']
                    market_items = self.price_scraper.get_items_mercari_with_retry(target_url, keywords, query_item['category'])
                    cur_update = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                    save_beg_row = searched_header_row + len(searched_items) + 1
                    save_cel = "{}{}".format(searched_beg_column, save_beg_row)
                    save_lines = []
                    for market_item in market_items:
                        market_item_key = market_item[searched_key]
                        if market_item_key in searched_items:
                            # 市場に既に記録しているアイテムがある場合
                            pass
                        else:
                            # 市場に既に記録しているアイテムがない場合
                            searched_item = {
                                "query_id": query_key,
                                "query_title": keywords,
                                "link": market_item['link'],
                                "name": market_item['name'].split('\n')[0],
                                "price": market_item['price'],
                                "update": cur_update
                            }
                            searched_items[market_item_key] = searched_item
                            
                            # LINE通知
                            message = "{}\n{}".format(
                                market_item['name'],
                                market_item['link']
                            )
                            self.line_notify.post_linenotify_with_retry(message, market_item['image'])
                            save_line = []
                            for searched_header in searched_headers:
                                save_line.append(searched_item[searched_header])
                            save_lines.append(save_line)
                    # Googeleスプレッドシートの検索済みシートに記録
                    if len(save_lines)>0:
                        beg_time = time.time()
                        UtilGspread.update_worksheet_with_retry(searched_worksheet, save_cel, save_lines)
                        print("update gspredsheet: {:.2f}[sec]".format(time.time()-beg_time))
                print("break_time:{}[sec]".format(interval_sec))
                time.sleep(interval_sec)

        except KeyboardInterrupt:
            # Ctrl+C
            print('interrupted!')
        except Exception as err:
            print(err)
            raise
        finally:
            self._finalize()

if __name__ == '__main__':
    # エントリポイント
    try:
        config = UtilJson.load_json(os.path.join(SRC_DIR, 'config.json'))
        MercariPriceScraper(config).exec()
        exit(0)
    except Exception as err:
        print(err)
        exit(1)
    