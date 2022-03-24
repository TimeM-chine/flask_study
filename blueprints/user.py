from flask import Blueprint, render_template, request, url_for, redirect, jsonify, session, flash
from exts import mail, db
from flask_mail import Message
import random
import string
from models import EmailCaptchaModel, FormValidate, UserModel, UserValidate
from datetime import datetime
from werkzeug import security

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = UserValidate(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and security.check_password_hash(user.password, password):
                session['userid'] = user.id
                return redirect("/")
            else:
                flash("Password or mail is wrong.")
                return redirect(url_for("user.login"))
        else:
            flash("The format of password or mail is wrong.")
            return redirect(url_for("user.login"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('user.login'))


@bp.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        form = FormValidate(request.form)
        if form.validate():
            print("验证成功")
            user_name = form.user_name.data
            password = form.password.data
            email = form.email.data
            hash_password = security.generate_password_hash(password)
            user_model = UserModel(user_name=user_name, password=hash_password, email=email)
            db.session.add(user_model)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            print("form", form.form_errors)
            return redirect(url_for("user.register"))


@bp.route("/captcha", methods=['POST'])
def get_captcha():
    email = request.form.get("email")
    my_letter = string.ascii_letters + string.digits
    captcha = "".join(random.sample(my_letter, 4))

    data = Message(
        subject="final test",
        recipients=[email],
        body="this is your final test,wish you could pass.{}".format(captcha)
    )
    captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
    if captcha_model:
        captcha_model.captcha = captcha
        captcha_model.create_time = datetime.now()
        db.session.commit()
    else:
        captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
        db.session.add(captcha_model)
        db.session.commit()
    mail.send(data)
    return jsonify({"code": 200})
