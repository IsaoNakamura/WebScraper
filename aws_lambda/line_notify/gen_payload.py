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

# LINE_END_POINT = "https://notify-api.line.me/api/notify"

PAYLOAD_FORMAT = {
    #"url": LINE_END_POINT,
    "message": ""
}

if __name__ == '__main__':
    # エントリポイント
    try:
        payload = PAYLOAD_FORMAT
        arguments = sys.argv
        # - で始まるoption
        options = [option for option in arguments if option.startswith('-')]
        # if '--url' in options:
        #     url_position = arguments.index('--url')
        #     url = arguments[url_position + 1]
        #     payload['url']=url
        if '--message' in options:
            message_position = arguments.index('--message')
            message = arguments[message_position + 1]
            payload['message']=message
        UtilJson.save_json(payload, SRC_DIR, 'payload')
        exit(0)
    except Exception as err:
        print(err)
        exit(1)
