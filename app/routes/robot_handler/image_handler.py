from enum import IntEnum
from datetime import datetime, timedelta
from .. import executor
from ...third_party.ocr import ocr_aip_url
from ...log import Log


class ImageHandlerState(IntEnum):
    NULL = 1
    OCR = 2


class ImageHandler(object):
    NULL_IMAGE_STATE_TIP = '请在菜单中选择要执行的操作'

    my_werobot = None

    @staticmethod
    def init_handler(my_werobot):
        ImageHandler.my_werobot = my_werobot

    @staticmethod
    def image_handler(message, session):
        if not 'image_handler_state' in session:
            return ImageHandler.NULL_IMAGE_STATE_TIP

        if session['image_handler_state'] == ImageHandlerState.OCR:
            return ImageHandler.ocr_image_handler(message, session)

        return ImageHandler.NULL_IMAGE_STATE_TIP

    @staticmethod
    def set_image_handler_to_ocr(session):
        ImageHandler.set_image_handler_state(session, ImageHandlerState.OCR)

    @staticmethod
    def set_image_handler_state(session, state):
        session['image_handler_state'] = state

    @staticmethod
    def update_ocr_timeout(session):
        session['image_handler_timeout'] = (
            datetime.now() + timedelta(minutes=5)).timestamp()

    @staticmethod
    def ocr_image_handler(message, session):
        # 已经超时
        if not 'image_handler_timeout' in session:
            return ImageHandler.NULL_IMAGE_STATE_TIP

        # 判断是否超时
        timestamp = session['image_handler_timeout']
        timeout = datetime.fromtimestamp(timestamp)
        now_time = datetime.now()
        if now_time > timeout:
            del session['image_handler_timeout']
            return ImageHandler.NULL_IMAGE_STATE_TIP

        # 没有超时，则更新时间
        ImageHandler.update_ocr_timeout(session)

        # 交由线程去执行耗时任务
        executor.submit(ImageHandler.request_ocr, message, session)
        return '正在识别...'

    @staticmethod
    def request_ocr(message, session):
        source = message.source

        Log.logger().info('start ocr')
        text = ocr_aip_url(message.img)
        # os.remove(img_path)
        Log.logger().info('end ocr')

        # 微信公众号限制回复最多2048字节：len(text.encode())
        if len(text.encode()) <= 2048:
            ImageHandler.my_werobot.client.send_text_message(source, text)
            return

        Log.logger().info('send long text')
        # 大于2048字节则按照字符裁剪：utf8一般2-4个字节表示一个字符，这里按照三个字节一个字符估算
        text_len = len(text)
        cut_limit = int(2048/3 - 10)
        pos = 0
        while True:
            if pos + cut_limit < text_len:
                ImageHandler.my_werobot.client.send_text_message(
                    source, text[pos:pos+cut_limit])
                pos = pos + cut_limit
            else:
                ImageHandler.my_werobot.client.send_text_message(
                    source, text[pos:])
                break


if __name__ == "__main__":
    print('hello')
