from . import db


class WebsiteNavigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024), index=True, unique=True)
    logo_url = db.Column(db.String(1024), index=True)
    main_type = db.Column(db.String(50), index=True)
    second_type = db.Column(db.String(50), index=True)
    search_json = db.Column(db.String(1024), index=True, default='')
    network_quality = db.Column(db.Integer, index=True, default=10)
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    @classmethod
    def get_rand_online_movie_website(cls, rand):
        websites = cls.query.filter(WebsiteNavigation.second_type == '在线电影').order_by(
            WebsiteNavigation.network_quality).limit(rand)
        urls = []
        for website in websites:
            urls.append(website)
        return urls
