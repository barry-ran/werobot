from werobot import WeRoBot
import werobot
from flask import current_app
from .robot_handler.text_handler import TextHandler
from .robot_handler.image_handler import ImageHandler
from ..log import Log

my_werobot = WeRoBot(token='werobot')
my_werobot.config["APP_ID"] = current_app.config['WEROBOT_ID']
my_werobot.config["APP_SECRET"] = current_app.config['WEROBOT_SECRET']
werobot.logger.enable_pretty_logging(Log.logger(), level='info')

TextHandler.init_handler(my_werobot)
ImageHandler.init_handler(my_werobot)

# 自定义菜单
my_werobot.client.create_menu({
    "button": [
        {
            "name": "影音娱乐",
            "sub_button": [
                {
                    "type": "click",
                    "name": "搜电影",
                    "key": "CLICK_MENU_SEARCH_MOVIE"
                },
                {
                    "type": "view",
                    "name": "影视VIP接口",
                    "url": "http://www.yiquvip.com/"
                }
            ]
        },
        {
            "name": "实用工具",
            "sub_button": [
                {
                    "type": "click",
                    "name": "图片转文字",
                    "key": "CLICK_MENU_OCR"
                },
            ]
        },
    ]})


@my_werobot.key_click("CLICK_MENU_OCR")
def menu_ocr(message, session):
    ImageHandler.set_image_handler_to_ocr(session)
    ImageHandler.update_ocr_timeout(session)
    my_werobot.client.send_text_message(message.source, '进入图片转文字模式，可以直接发图片给我')


@my_werobot.key_click("CLICK_MENU_SEARCH_MOVIE")
def menu_ocr(message, session):
    TextHandler.set_text_handler_to_search_movie(session)
    my_werobot.client.send_text_message(
        message.source, '欢迎使用电影搜索功能，可以直接发电影名给我')


@my_werobot.text
def text_handler(message, session):
    return TextHandler.text_handler(message, session)


@my_werobot.image
def image_handler(message, session):
    return ImageHandler.image_handler(message, session)
