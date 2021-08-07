# werobot
我的微信公众号后台

主要功能（期待更多功能可以直接提建议给公众号）：
- vip视频解析
- 电影搜索
- 图片转文字
- 技术文章

微信扫码即可体验：

![](docs/image/coderbox.jpg)

# 开发相关
主要使用python语言开发，使用flask、werobot等开源库。

基于我的另一个开源项目[flask-scaffolding](https://github.com/barry-ran/flask-scaffolding)作为脚手架，可以实现flask项目的快速开发与部署。

如果希望本地调试该项目，除了参考[flask-scaffolding](https://github.com/barry-ran/flask-scaffolding)配置开发环境并初始化数据库，还需要在app目录提供.env文件：
```
# flask 密钥（开发可选）
SECRET_KEY="****"

# 数据库连接信息（必须）
DEV_DATABASE_URL='****'

# 微信公众号相关密钥（必须）
WEROBOT_ID='****'
WEROBOT_SECRET='****'

# 百度ai的图片转文字接口需要（不调试该功能可以不提供）
OCR_APP_ID='****'
OCR_API_KEY='****'
OCR_SECRET_KEY='****'
```
