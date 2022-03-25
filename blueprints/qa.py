from flask import Blueprint, render_template, g, request, flash, redirect, url_for
from decrators import login_verify
from models import QuestionModel, QuestionValidate
from exts import db

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    questions = QuestionModel.query.all()
    return render_template("index.html", que=questions)


@bp.route("/question/public", methods=['POST', 'GET'])
@login_verify
def public_question():
    if request.method == "GET":
        return render_template("public.html")
    else:
        form = QuestionValidate(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            q_model = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(q_model)
            db.session.commit()
            return redirect("/")
        else:
            flash("Format Error!")
            return redirect(url_for("qa.public_question"))
