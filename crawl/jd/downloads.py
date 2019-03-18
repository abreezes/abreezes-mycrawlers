import requests

class Downlaod:

    @classmethod
    def download(cls,url):
        """下载"""
        response = requests.get(url)
        if response.status_code != 200:
            return
        return response.text