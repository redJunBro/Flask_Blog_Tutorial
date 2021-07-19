from main import *
from flask import Blueprint

blueprint = Blueprint ("member", __name__, url_prefix="/member")
@blueprint.route("/join", methods=["GET", "POST"])
def member_join():
    if request.method == "POST":
        print('전송완료')
        name = request.form.get("name", type=str)
        emeil = request.form.get("emeil", type=str)
        pass1 = request.form.get("pass1", type=str)
        pass2 = request.form.get("pass2", type=str)

        if name == "" or emeil == "" or pass1 == "" or pass2 == "":
            flash("입력되지 않은 값이 있습니다.")
            return render_template("join.html", title="회원가입")
        if pass1 != pass2:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("join.html", title="회원가입")

        members = mongo.db.members
        cnt = members.find({"emeil": emeil}).count()
        if cnt > 0:
            flash("중복된 이메일 입니다.")
            return render_template("join.html", title="회원가입")

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)
        post = {
            "name": name,
            "emeil": emeil,
            "pass": pass1,
            "joindate": current_utc_time,
            "logintime": "",
            "logincount": 0,
        }

        members.insert_one(post)

        return redirect(url_for("board.lists"))
    else:
        return render_template("join.html", title="회원가입")


@blueprint.route("/login", methods=["GET", "POST"])
def member_login():
    if request.method == "POST":
        emeil = request.form.get("emeil")
        password = request.form.get("pass1")
        next_url = request.form.get("next_url")
        members = mongo.db.members
        data = members.find_one({"emeil": emeil})

        if data is None:
            flash("회원정보가 없습니다")
            return redirect(url_for("member.member_login"))
        else:
            if data.get("pass") == password:
                session["emeil"] = emeil
                session["name"] = data.get("name")
                session["id"] = str(data.get("_id"))
                session.permanent = True
                if next_url is not None:
                    return redirect(next_url)
                else:
                    return redirect(url_for("board.lists"))

            else:
                flash("비밀번호가 일치하지않습니다.")
                return redirect(url_for("member.member_login"))
        return ""
    else:
        next_url = request.args.get("next_url", type=str)
        if next_url is not None:
            return render_template("login.html", next_url=next_url, title="로그인")
        else:
            return render_template("login.html", title="로그인")


@blueprint.route("/logout")
def member_logout():
    del session["name"]
    del session["emeil"]
    del session["id"]
    flash("로그아웃되었습니다.")
    return redirect(url_for("board.lists"))
