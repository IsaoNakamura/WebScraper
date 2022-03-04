import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_OPTIONS = [
    '--headless',                 # headlessモードを使用する
    '--no-sandbox',
    '--disable-gpu',              # headlessモードで暫定的に必要なフラグ(そのうち不要になる)
    '--disable-extensions',       # すべての拡張機能を無効にする。ユーザースクリプトも無効にする
    '--proxy-server="direct://"', # Proxy経由ではなく直接接続する
    '--proxy-bypass-list=*'       # すべてのホスト名
]

class UtilSelenium():
    def __init__(self) -> None:
        self.driver = None
        try:
            self.driver = UtilSelenium._get_driver_chrome()
        except Exception as err:
            print(err)
            raise
    
    def __del__(self) -> None:
        try:
            self.quit()
        except Exception as err:
            print(err)
            raise
    
    def quit(self) -> None:
        try:
            if self.driver is not None:
                self.driver.quit()
                self.driver = None
        except Exception as err:
            print(err)
            raise

    # Chromeドライバー(selenium)を取得
    @classmethod
    def _get_driver_chrome(cls, chrome_options:list=CHROME_OPTIONS):
        try:
            # chromedriverの設定
            options = Options()
            for opt in chrome_options:
                options.add_argument(opt)  
            driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
            return driver
        except Exception as err:
            print(err)
            raise
        
    def get_price_biccamera(self, url:str):
        try:
            self.driver.get(url)
            # 明示的な待機
            self.driver.implicitly_wait(20)
            # 定義済みの条件で待機
            wait = WebDriverWait(self.driver, 20)
            wait.until( EC.visibility_of_element_located( (By.CLASS_NAME, "bcs_single") ) )
            bcs_single = self.driver.find_element(by=By.CLASS_NAME, value="bcs_single")
            bcs_price = bcs_single.find_element(by=By.CLASS_NAME, value="bcs_price")
            strong_tag = bcs_price.find_element(by=By.TAG_NAME, value="strong")
            bcs_stock = bcs_single.find_element(by=By.CLASS_NAME, value="bcs_stock")
            stock = bcs_stock.find_element(by=By.TAG_NAME, value="span").text
            product = bcs_single.get_attribute('data-item-name')
            price = int(strong_tag.get_attribute('content'))
            return price, stock, product
        except Exception as err:
            print(err)
            raise

    def get_price_amazon(self, url:str):
        try:
            self.driver.get(url)
            # 明示的な待機
            self.driver.implicitly_wait(20)
            # 定義済みの条件で待機
            wait = WebDriverWait(self.driver, 20)
            wait.until( EC.visibility_of_element_located( (By.ID, "productTitle") ) )
            product_elem = self.driver.find_element(by=By.ID, value="productTitle")
            product = product_elem.text
            #print("product={}".format(product))
            
            wait.until( EC.visibility_of_element_located( (By.ID, "availability") ) )
            availability = self.driver.find_element(by=By.ID, value="availability")
            stock_elem = availability.find_element(by=By.CLASS_NAME, value="a-size-medium")
            # stock = stock_elem.text
            # print("stock={}".format(stock))
            # 在庫有 = [ "在庫あり。", "残り*点 ご注文はお早めに"]
            # 在庫無 = [ "", "在庫状況について"]
            price = None
            if (len(stock_elem.text)<=0) or stock_elem.text == '在庫状況について' :
                stock = '在庫無'
            else:
                stock = '在庫有'
                # wait.until( EC.visibility_of_element_located( (By.ID, "corePrice_feature_div") ) )
                # price_elem = self.driver.find_element(by=By.ID, value="corePrice_feature_div")
                wait.until( EC.visibility_of_element_located( (By.ID, "priceblock_ourprice") ) )
                price_elem = self.driver.find_element(by=By.ID, value="priceblock_ourprice")
                # print(price_elem.text) # '￥50,586'
                price = price_elem.text
                price = price.replace('￥','')
                price = price.replace(',','')
                if len(price) > 0:
                    price = int(price)
                # print("price={}".format(price))
            # print("parseAmazon: {:.2f}[sec]".format(time.time()-beg_time))
            return price, stock, product
        except Exception as err:
            print(err)
            raise

    def get_items_mercari(self, url:str, keywords:str, category:str) -> list:
        try:
            print(keywords)
            # https://jp.mercari.com/search
            # ?keyword=
            # &t1_category_id=5&category_id=5
            # &status=on_sale
            url_query = url + '/search'
            if keywords is not None:
                url_query = url_query + '?keyword=' + keywords
            if category is not None:
                url_query = url_query + '&' + category
            url_query += '&status=on_sale'
            self.driver.get(url_query)
            # 明示的な待機
            self.driver.implicitly_wait(20)
            # 定義済みの条件で待機
            wait = WebDriverWait(self.driver, 20)
            wait.until( EC.visibility_of_element_located((By.ID, "search-result")) )
            search_result = self.driver.find_element(by=By.ID, value="search-result")
            item_num = search_result.find_element(by=By.TAG_NAME, value="mer-text")
            print(item_num.text)
            if item_num.text == '0件':
                return []
            
            wait.until( EC.visibility_of_element_located((By.ID, "item-grid")) )
            item_grid = self.driver.find_element(by=By.ID, value="item-grid")
            #items = item_grid.find_elements(by=By.TAG_NAME, value="mer-item-thumbnail")
            wait.until( EC.visibility_of_element_located((By.TAG_NAME, "a")) )
            items = item_grid.find_elements(by=By.TAG_NAME, value="a")
            market_items = []
            for item in items:
                wait.until( EC.visibility_of_element_located((By.TAG_NAME, "mer-item-thumbnail")) )
                thumbnail = item.find_element(by=By.TAG_NAME, value="mer-item-thumbnail")
                #name = thumbnail.get_attribute('item-name')
                market_item = {
                    # "name": item.get_attribute('item-name'),
                    # "alt": item.get_attribute('alt'),
                    "name": item.text, #thumbnail.get_attribute('alt'),
                    "thumb": thumbnail.get_attribute('src-webp'),
                    "price": int(thumbnail.get_attribute('price')),
                    "link": item.get_attribute('href'),
                    "image": item.screenshot_as_png
                }
                market_items.append(market_item)
            return market_items
        except Exception as err:
            print(err)
            raise

    def get_items_mercari_with_retry(
        self,
        url:str,
        keywords:str,
        category:str,
        retry_cnt:int=5,
        wait_sec:float=1.0
    ) -> list:
        try:
            for i in range(retry_cnt):
                try:
                    return self.get_items_mercari(url, keywords, category)
                except Exception as err:
                    print('except error. retry={}'.format(i))
                time.sleep(wait_sec)
            return []
        except Exception as err:
            print(err)
            raise
