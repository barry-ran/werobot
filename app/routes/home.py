import random
from flask import Blueprint, render_template
from ..log import Log
from ..models.vip_video_parse import VipVideoParse

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/', methods=['GET', 'POST'])
def index():
    default_url_name = ['http://vip.jlsprh.com/?url=', '默认']
    urls_name = get_urls_name()
    if len(urls_name) != 0:
        default_url_name = urls_name[random.randint(0, len(urls_name) - 1)]

    return render_template('index.html',
                           default_parse_url=default_url_name[0],
                           video_url='http://v.youku.com/v_show/id_XMjcxMjY5NjM1Ng==.html',
                           url_list=urls_name)


def get_urls_name():
    urls = VipVideoParse.get_rand_parse_url(10)
    urls_name = []
    count = 0
    for url in urls:
        urls_name.append([url, '推荐接口{}'.format(count)])
        count = count + 1
        Log.logger().info('get_urls_name:' + url)

    return urls_name
