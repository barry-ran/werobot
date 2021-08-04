import json
import re
from urllib.parse import urljoin
from lxml import etree
from ..log import Log
from ..util.requests_helper import RequestsHelper
from ..models.website_navigation import WebsiteNavigation


class Movie(object):
    def __init__(self, thumbnail, url, title, director, stars, type, introduction):
        self.thumbnail = thumbnail
        self.url = url
        self.title = title
        self.director = director
        self.stars = stars
        self.type = type
        self.introduction = introduction

    # 告诉 Python 如何打印这个类的对象。我们将用它来调试
    def __repr__(self):
        return 'thumbnail:{}\n url:{}\n title:{}\n director:{}\n stars:{}\n type:{}\n introduction:{}\n'.format(self.thumbnail,
                                                                                                                self.url, self.title, self.director, self.stars, self.type, self.introduction)

    @classmethod
    def search(cls, key):
        try:
            websites = WebsiteNavigation.get_rand_online_movie_website(5)
            search_results = []
            for website in websites:
                movies = cls.search_from_json(key, website.search_json)
                # 相对路径转绝对路径
                for movie in movies:
                    movie.url = urljoin(website.url, movie.url)
                    print('search movie:', movie.url)

                search_results += movies

                # 找到了就不再继续找了
                if len(search_results) > 0:
                    break

            return search_results
        except Exception as e:
            Log.logger().exception(e)
            return []

    @classmethod
    def parse_movie_item(cls, result, search_json_obj, key):
        if key + '_xpath' not in search_json_obj['movie_item'].keys():
            return ''

        xpath = search_json_obj['movie_item'][key + '_xpath']
        if len(xpath) == 0:
            return ''
        item = result.xpath(xpath)
        if isinstance(item, list):
            if len(item) > 0:
                item = item[0]
            else:
                item = ""
        item = ''.join(item).strip()

        if key + '_re' in search_json_obj['movie_item'].keys():
            xpath = search_json_obj['movie_item'][key + '_re']
            if len(xpath) != 0:
                pattern = re.compile(xpath)
                find = pattern.findall(item)
                item = find[0] if len(find) != 0 else ''

        return item

    @classmethod
    def search_from_json(cls, key, search_json):
        print('search_json:\n', search_json)
        search_json_obj = json.loads(search_json)
        html = RequestsHelper.download_html(search_json_obj['url'].format(key))
        if len(html) == 0:
            Log.logger().info('download_html failed:{}'.format(
                search_json_obj['url'].format(key)))
            return []

        et_html = etree.HTML(html)
        items = et_html.xpath(search_json_obj['movie_item_xpath'])

        ret_results = []
        print('movie item len:', len(items))
        for result in items:
            thumbnail = cls.parse_movie_item(
                result, search_json_obj, 'thumbnail')
            url = cls.parse_movie_item(result, search_json_obj, 'url')
            title = cls.parse_movie_item(result, search_json_obj, 'title')
            director = cls.parse_movie_item(
                result, search_json_obj, 'director')
            stars = cls.parse_movie_item(result, search_json_obj, 'stars')
            type = cls.parse_movie_item(result, search_json_obj, 'type')
            introduction = cls.parse_movie_item(
                result, search_json_obj, 'introduction')

            ret_results.append(Movie(thumbnail, url, title,
                               director, stars, type, introduction))

        return ret_results


if __name__ == "__main__":
    if True:
        search_json_string = ('{"url": "https://www.ahrmgg.com/ppyssearch.html?wd={}",'
                              '"movie_item_xpath": "//ul[@class=\'stui-vodlist__media col-pd clearfix\']/li",'
                              '"movie_item": {'
                              '"thumbnail_xpath": "./div[@class=\'thumb\']/a/@data-original", '
                              '"url_xpath":"./div[@class=\'detail\']/h3/a/@href", '
                              '"title_xpath":"./div[@class=\'detail\']/h3/a/text()",'
                              '"director_xpath":"./div[@class=\'detail\']/p[1]/text()",'
                              '"stars_xpath":"./div[@class=\'detail\']/p[2]/text()",'
                              '"type_xpath":"./div[@class=\'detail\']/p[3]/text()"'
                              '}'
                              '}')

        print(Movie.search_from_json('恶人', search_json_string))
