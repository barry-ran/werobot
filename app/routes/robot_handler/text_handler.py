
from enum import IntEnum
from flask import current_app
from .. import executor
from ...log import Log
from ...third_party.movie import Movie


class TextHandlerState(IntEnum):
    NULL = 1
    SEARCH_MOVIE = 2


class TextHandler(object):
    NULL_TEXT_STATE_TIP = '请在菜单中选择要执行的操作'

    my_werobot = None

    @staticmethod
    def init_handler(my_werobot):
        TextHandler.my_werobot = my_werobot

    @staticmethod
    def text_handler(message, session):
        Log.logger().info('text handler:{}'.format(message.content))

        if not 'text_handler_state' in session:
            return TextHandler.NULL_TEXT_STATE_TIP

        try:
            if session['text_handler_state'] == TextHandlerState.SEARCH_MOVIE:
                return TextHandler.search_movie_handler(message, session)
        except Exception as e:
            Log.logger().exception(e)
            return str(e)

        return TextHandler.NULL_TEXT_STATE_TIP

    @staticmethod
    def set_text_handler_to_search_movie(session):
        TextHandler.set_text_handler_state(
            session, TextHandlerState.SEARCH_MOVIE)

    @staticmethod
    def set_text_handler_state(session, state):
        session['text_handler_state'] = state

    @staticmethod
    def search_movie_handler(message, session):
        TextHandler.set_text_handler_state(session, TextHandlerState.NULL)
        # 交由线程去执行耗时任务
        executor.submit(TextHandler.search_movie, message, session)
        return '正在搜索...'

    @staticmethod
    def search_movie(message, session):
        Log.logger().info('begin search movie:{}'.format(message.content))
        movies = Movie.search(message.content)
        Log.logger().info('end search movie:{}'.format(message.content))
        text = "以下结果来源网络，如有侵权，请联系公众号删除（建议复制到浏览器打开）：\n"

        for movie in movies:
            text += movie.title + ':' + movie.url + '\n'
            # 微信公众号限制回复最多2048字节：len(text.encode())
            if len(text.encode()) >= 2048:
                break
        Log.logger().info('send result:{}'.format(text))
        TextHandler.my_werobot.client.send_text_message(message.source, text)
