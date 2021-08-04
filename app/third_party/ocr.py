# -*- coding: utf-8 -*

from aip import AipOcr
from flask import current_app


def ocr_aip_url(url):
    try:
        client = AipOcr(
            current_app.config['OCR_APP_ID'], current_app.config['OCR_API_KEY'], current_app.config['OCR_SECRET_KEY'])

        # https://ai.baidu.com/ai-doc/OCR/7kibizyfm
        options = {}
        options["language_type"] = "CHN_ENG"
        #options["detect_direction"] = "true"
        #options["detect_language"] = "true"
        #options["probability"] = "true"

        resp = client.basicGeneralUrl(url, options)

        if 'error_msg' in resp.keys():
            return u'图片识别失败: {}'.format(resp["error_msg"])

        result = ''
        for item in resp['words_result']:
            if result != '':
                result = result + '\n'
            result = result + item['words']

        return result
    except Exception as e:
        return u'图片识别异常: {}'.format(str(e))


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def ocr_aip_path(path):
    try:
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

        # https://ai.baidu.com/ai-doc/OCR/7kibizyfm
        options = {}
        options["language_type"] = "CHN_ENG"
        #options["detect_direction"] = "true"
        #options["detect_language"] = "true"
        #options["probability"] = "true"

        image = get_file_content(path)
        resp = client.basicGeneral(image, options)

        if 'error_msg' in resp.keys():
            return u'图片识别失败: {}'.format(resp["error_msg"])

        result = ''
        for item in resp['words_result']:
            if result != '':
                result = result + '\n'
            result = result + item['words']

        return result
    except Exception as e:
        return u'图片识别异常: {}'.format(str(e))

# print ocr_aip_url('https://cdn.learnku.com/uploads/images/202008/20/51094/DiV8QB39oJ.jpeg!large')
