from flask import Flask, session, g
import config
from exts import db, mail
from flask_migrate import Migrate

from models import UserModel
from blueprints import qa_bp, user_bp

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)

migrate = Migrate(app, db)


@app.before_request
def before_request():
    userid = session.get("userid")
    if userid:
        user = UserModel.query.filter_by(id=userid).first()
        if user:
            g.user = user
        else:
            g.user = None


# 请求 -> before_request -> 视图函数 -> 返回模板 -> context_processor
@app.context_processor
def context_processor():
    """
    百度到的
    1. 如上述代码那样， context_processor 作为一个装饰器修饰一个函数
    2. 函数的返回结果必须是 dict, 然后其 key 将会作为变量在所有模板中可见
    """
    if hasattr(g, "user"):
        return {"user_name": g.user.user_name}
    return {}
    # 由于不知名的原因，这里返回的东西会直接被渲染进网页中，暂时还不明白


if __name__ == '__main__':
    app.run()
