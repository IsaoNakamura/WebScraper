import time

import requests

END_POINT = "https://notify-api.line.me/api/notify"

class UtilLineNotify():
    def __init__(self, config:dict):
        self.url = END_POINT
        self.access_token = config['access_token']

    def post_linenotify(self, message, image=None):
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {'message': message}
        files = None
        if image is not None:
            files = {'imageFile': image}
        requests.post(self.url, headers=headers, params=payload, files=files)

    def post_linenotify_with_retry(
        self,
        message, 
        image=None,
        retry_cnt:int=5,
        wait_sec:float=1.0
    ) -> None:
        try:
            for i in range(retry_cnt):
                try:
                    return self.post_linenotify(message, image)
                except Exception as err:
                    print('except error. retry={}'.format(i))
                time.sleep(wait_sec)
            return None
        except Exception as err:
            print(err)
            raise