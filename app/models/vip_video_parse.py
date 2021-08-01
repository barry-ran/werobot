from . import db
from sqlalchemy.sql.expression import func


class VipVideoParse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parse_url = db.Column(db.String(1024), index=True, unique=True)
    network_quality = db.Column(db.Integer, index=True, default=10)

    @classmethod
    def get_rand_parse_url(cls, rand):
        db_urls = cls.query.order_by(VipVideoParse.network_quality).limit(rand)
        urls = []
        for url in db_urls:
            urls.append(url.parse_url)

        return urls

    # 告诉 Python 如何打印这个类的对象。我们将用它来调试
    def __repr__(self):
        return '<parse_url %r>' % (self.parse_url)
