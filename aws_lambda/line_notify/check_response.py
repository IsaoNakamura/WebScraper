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


if __name__ == '__main__':
    # エントリポイント
    try:
        resfile = os.path.join(SRC_DIR, "response.json")
        arguments = sys.argv
        # - で始まるoption
        options = [option for option in arguments if option.startswith('-')]
        if '--resfile' in options:
            resfile_position = arguments.index('--resfile')
            resfile = arguments[resfile_position + 1]
        res = UtilJson.load_json(resfile)
        # if not 'StatusCode' in res:
        #     exit(1)
        # if res['StatusCode'] != 200:
        #     exit(1)
        if res != 200:
            exit(1)
        exit(0)
    except Exception as err:
        print(err)
        exit(1)
