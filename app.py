#from flask import Flask
from flask import redirect, render_template, request, session, Flask, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = "1234"
db = SQLAlchemy(app)

@app.route("/")
def index():
	sql = "SELECT id, topic, created_at FROM polls WHERE visible=TRUE ORDER BY id DESC"
	result = db.session.execute(text(sql))
	polls = result.fetchall()
	return render_template("index.html", polls=polls)


@app.route("/sign_up")
def sign_up():
	return render_template("sign_up.html")

@app.route("/new_user", methods=["POST"])
def new_user():
	username = request.form["username"]
	password = request.form["password"]
	groupA = False
	groupB = False
	groupC = False
	groupD = False
	admin = False
#	if len(username) > 11 or len(password) < 3 or  len(password) > 12:
#		return render_template("sign_up_fail.html")
	if db.session.execute(text("SELECT FROM users WHERE username=:username"), {"username":username}).fetchone() is not None :
		return render_template("sign_up_fail.html")
	if username and password:
#		hash_value = generate_password_hash(password)
		sql = "INSERT INTO users (username, password, groupA, groupB, groupC, groupD, admin) VALUES (:username, :password, :groupA, :groupB, :groupC, :groupD, :admin)"
#		db.session.execute(text(sql), {"username":username, "password":hash_value, "groupA":groupA, "groupB":groupB, "groupC":groupC, "groupD":groupD, "admin":admin})
		db.session.execute(text(sql), {"username":username, "password":password, "groupA":groupA, "groupB":groupB, "groupC":groupC, "groupD":groupD, "admin":admin})
		db.session.commit()
		session["username"] = username
#		session["csrf_token"] = secrets.token_hex(16)
		return redirect("/")
	return redirect("/sign_up")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/loginuser",methods=["POST"])
def login_user():
	username = request.form["username"]
	password = request.form["password"]
	sql = text("SELECT id, password FROM users WHERE username=:username")
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if not user:
		return render_template("login_fail.html")
	else:
#		hash_value = user.password
#		if check_password_hash(hash_value, password):
#			session["username"] = username
#			session["csrf_token"] = secrets.token_hex(16)
#			return redirect("/")
		if password == password:
			print(user.password)
			session["username"] = username
			return redirect("/")

		else:
			return render_template("login_fail.html")

@app.route("/logout")
def logout():
	del session["username"]
	return redirect("/")

@app.route("/new")
def new():
	return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
	topic = request.form["topic"]
	username = session["username"]
	sql = "INSERT INTO polls (topic, created_at, created_by, visible) VALUES (:topic, NOW(), :username, TRUE) RETURNING id"
	result = db.session.execute(text(sql), {"topic":topic, "username":username})
	poll_id = result.fetchone()[0]
	choices = request.form.getlist("choice")
	for choice in choices:
		if choice != "":
			sql = "INSERT INTO choices (poll_id, choice) VALUES (:poll_id, :choice)"
			db.session.execute(text(sql), {"poll_id":poll_id, "choice":choice})
#	if session["csrf_token"] != request.form["csrf_token"]:
#		abort(403)
	db.session.commit()
	return redirect("/")

@app.route("/poll/<int:id>")
def poll(id):
	username = session["username"]
	sql = "SELECT topic FROM polls WHERE id=:id"
	result = db.session.execute(text(sql), {"id":id})
	topic = result.fetchone()[0]
	sql = "SELECT id, choice FROM choices WHERE poll_id=:id"
	result = db.session.execute(text(sql), {"id":id})
	choices = result.fetchall()
	return render_template("poll.html", id=id, topic=topic, choices=choices)

@app.route("/answer", methods=["POST"])
def answer():
	poll_id = request.form["id"]
	answers = request.form.getlist("answer")
	for answer in answers:
		if "answer" in request.form:
			choice_id = request.form["answer"]
			sql = "INSERT INTO answers (choice_id, sent_at) VALUES (:choice_id, NOW())"
			db.session.execute(text(sql), {"choice_id":choice_id})
#		if session["csrf_token"] != request.form["csrf_token"]:
#			abort(403)
		db.session.commit()
	username = session["username"]
	return redirect("/result/" + str(poll_id))

@app.route("/result/<int:id>")
def result(id):
	sql = "SELECT topic FROM polls WHERE id=:id"
	result = db.session.execute(text(sql), {"id":id})
	topic = result.fetchone()[0]
	sql = "SELECT c.choice, COUNT(a.id) FROM choices c LEFT JOIN answers a " \
		"ON c.id=a.choice_id WHERE c.poll_id=:poll_id GROUP BY c.id"
	result = db.session.execute(text(sql), {"poll_id":id})
	choices = result.fetchall()
	return render_template("result.html", topic=topic, choices=choices)

@app.route("/manage")
def manage():
	username = session["username"]
	if db.session.execute(text("SELECT admin FROM users WHERE username=:username"), {"username":username}).fetchone()[0] == True:
		sql = "SELECT id, topic, created_at FROM polls WHERE visible=TRUE ORDER BY id DESC"
		result = db.session.execute(text(sql))
	else:
		sql = "SELECT id, topic, created_at FROM polls WHERE created_by=:username AND visible=TRUE ORDER BY id DESC"
		result = db.session.execute(text(sql), {"username":username})
	polls = result.fetchall()
	return render_template("manage.html", polls=polls)

@app.route("/delete/<int:id>")
def delete(id):
	sql = "UPDATE polls SET visible=FALSE WHERE id=:id"
	db.session.execute(text(sql), {"id":id})
	db.session.commit()
	return redirect("/manage")
