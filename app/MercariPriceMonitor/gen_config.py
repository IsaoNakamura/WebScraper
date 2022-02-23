import os
import sys

# 実行ファイルのディレクトリ絶対パスを取得
EXECFILE_DIR = os.path.dirname(os.path.abspath(__file__))

# 入力ファイルの格納場所は、実行ファイルディレクトリからの相対パスで指定できる
SRC_DIR = os.path.join(EXECFILE_DIR, './')

# 自作モジュールの格納場所は、実行ファイルディレクトリからの相対パスで指定できる
sys.path.append(os.path.join(EXECFILE_DIR, '../../'))
# internal import
from lib.util_json import UtilJson

LINE_ACCESS_TOKEN = "xxxx"
GOOGLE_ACCESS_KEY_FILEPATH = "xxxx.json"
GOOGLE_WORKBOOK_KEY = "xxxx"

if __name__ == '__main__':
    # エントリポイント
    try:
        config = {
            "target_url": "https://jp.mercari.com",
            "interval_sec": 900,
            "line_api_setting": {
                "access_token": LINE_ACCESS_TOKEN
            },
            "google_api_setting": {
                "access_key_filepath": GOOGLE_ACCESS_KEY_FILEPATH,
                "workbook_key": GOOGLE_WORKBOOK_KEY
            },
            "gssheet_setting": {
                "query_sheet": {
                    "sheet_name": "RETRO_QUERY",
                    "header_row": 2,
                    "key_header": "query_id",
                    "beg_column": "A",
                    "end_column": "H",
                    "number_headers": [
                        "high_price",
                        "low_price",
                        "market_price"
                    ]
                },
                "searched_sheeet": {
                    "sheet_name": "RETRO_SEARCHED",
                    "header_row": 2,
                    "key_header": "link",
                    "beg_column": "A",
                    "end_column": "F",
                    "number_headers": [
                        "price"
                    ]
                }
            }
        }
        UtilJson.save_json(config, SRC_DIR, 'config')
        exit(0)
    except Exception as err:
        print(err)
        exit(1)
