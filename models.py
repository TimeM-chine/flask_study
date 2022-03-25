from exts import db
from datetime import datetime
import wtforms
from wtforms.validators import length, email, equal_to


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)


class UserValidate(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    create_time = db.Column(db.DateTime, default=datetime.now)

    author = db.relationship("UserModel", backref="questions")


class QuestionValidate(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=100)])
    content = wtforms.StringField(validators=[length(min=5)])


class FormValidate(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    user_name = wtforms.StringField(validators=[length(min=6, max=20)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    confirm_password = wtforms.StringField(validators=[equal_to("password")])

    def validate_captcha(self, field):
        captcha = field.data
        print("field", field)
        print("captcha", captcha, "self.captcha", self.captcha, "self.captcha.data", self.captcha.data)
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha.lower() != captcha_model.captcha.lower():
            raise wtforms.ValidationError("captcha wrong!")

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("user exists!")
