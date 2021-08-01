import requests

class RequestsHelper(object):

    @classmethod
    def download_html(cls, url):
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
            r = requests.get(url, headers=header)
            return r.text
        except Exception as e:
            print('Failed downloading', url)
            print(e)
            return ''

if __name__ == "__main__":
    print(RequestsHelper.download_html('https://neihandianying.com/movie/search?q=蜜桃成熟时'))