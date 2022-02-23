import time

import gspread
#Googleの各サービスへアクセスできるservice変数を生成
from oauth2client.service_account import ServiceAccountCredentials

class UtilGspread():
    def __init__(self) -> None:
        try:
            pass
        except Exception as err:
            print(err)
            raise
    
    def __del__(self) -> None:
        try:
            pass
        except Exception as err:
            print(err)
            raise

    # GoogleSpreadSheetのワークブックを取得
    @classmethod
    def get_workbook(cls, gspread_sheetkey:str, gspread_accesskey_filepath:str) -> None:
        #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        #秘密鍵ファイルパスをクレデンシャル変数に設定
        credentials = ServiceAccountCredentials.from_json_keyfile_name(gspread_accesskey_filepath, scope)
        #OAuth2の資格情報を使用してGoogle APIにログイン
        gc = gspread.authorize(credentials)
        #共有設定したスプレッドシートを取得
        workbook = gc.open_by_key(gspread_sheetkey)
        return workbook

    @classmethod
    def calc_cellname(cls, column:str, row:int) -> str:
        return column + str(row)

    @classmethod
    def calc_cellrange(cls, beg_column:str, beg_row:int, end_column:str, end_row:int):
        return "{}{}:{}{}".format(beg_column, beg_row, end_column, end_row)

    @classmethod
    def load_sheet_items(cls, worksheet, gssheet_setting) -> None:
        try:
            key_header = gssheet_setting['key_header']
            beg_column = gssheet_setting['beg_column']
            end_column = gssheet_setting['end_column']
            header_row = gssheet_setting['header_row']
            number_headers = gssheet_setting['number_headers']
            
            table = worksheet.get_values("{}:{}".format(beg_column, end_column))
            items = {}
            headers = None
            for i, line in enumerate(table):
                if i < (header_row-1):
                    continue
                if i == (header_row-1):
                    # header行の場合
                    headers = line
                else:
                    item = {}
                    key = None
                    for x, header in enumerate(headers):
                        value = line[x]
                        if len(value)<=0:
                            item[header] = None
                        else:
                            if header in number_headers:
                                item[header] = int(value)
                            else:
                                item[header] = value
                        if header == key_header:
                            key = item[header]
                    item["row"] = (i+1)
                    if key is not None:
                        items[key] = item
                    else:
                        break
            return items, headers
        except Exception as err:
            print(err)
            raise

    @classmethod
    def load_sheet_items_with_retry(
        cls,
        worksheet,
        gssheet_setting,
        retry_cnt:int=5,
        wait_sec:float=1.0
    ) -> None:
        try:
            for i in range(retry_cnt):
                try:
                    return cls.load_sheet_items(worksheet, gssheet_setting)
                except Exception as err:
                    print('except error. retry={}'.format(i))
                time.sleep(wait_sec)
            return []
        except Exception as err:
            print(err)
            raise

    @classmethod
    def update_worksheet_with_retry(
        cls,
        worksheet,
        save_cel,
        save_lines,
        retry_cnt:int=5,
        wait_sec:float=1.0
    ) -> None:
        try:
            for i in range(retry_cnt):
                try:
                    return worksheet.update(save_cel, save_lines)
                except Exception as err:
                    print('except error. retry={}'.format(i))
                time.sleep(wait_sec)
            return None
        except Exception as err:
            print(err)
            raise