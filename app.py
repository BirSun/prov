from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.types import Boolean

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"
#app = Flask(__name__, instance_relative_config=True)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    #done = db.Column(db.Boolean, default=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User: {self.email}>'

db.create_all()

#test = User.query.all()
#print(test[0])


#CREATE RECORD
#new_user = User(id=4, name="Nils Eklund", email="eklund@gmail.com", done=1)
#db.session.add(new_user)
#db.session.commit()

@app.route('/')
def home():
    ##READ ALL RECORDS
    all_users = db.session.query(User).all()
    return render_template("index.html", Users=all_users)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        new_user = User(
            name=request.form["name"],
            email=request.form["email"],
            #done=request.form["done"]

        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")
"""
@app.route("/edit/<user_id>", methods=["POST", "GET"])
def edit_note(user_id):
    if request.method == "POST":
        edit(user_id, text=request.form['text'], done=request.form['done'])
    elif request.method == "GET":
        delete(user_id)
    return redirect("/", code=302)
"""
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD

        user_id = request.form["id"]
        print(user_id)
        user_to_update = User.query.get(user_id)
        print(user_to_update)
        user_to_update.name = request.form["name"]
        db.session.commit()

        return redirect(url_for('home'))
    user_id = request.args.get("id")
    user_selected = User.query.get(user_id)
    return render_template("edit_rating.html", user=user_selected)

#@app.route("/edit_done", methods=["GET", "POST"])
#@app.route("/edit_done", methods=["POST"])
#test
#def edit_done(user_id):

@app.route("/edit_done/<id>", methods=["POST", "GET"])
def edit_done(id):

    if request.method == "POST":
        # UPDATE RECORD

        #user_id = request.form["id"]
        print(id)
        print("test")
        #user_to_update = User.query.get(user_id)

        #user_to_update.done = request.form["done"]
        #db.session.commit()
    elif request.method == "GET":
        print("prov")
        print(id)
        user_to_update = User.query.get(id)
        print(user_to_update.name)
        print(user_to_update.done)
        print(user_to_update)
        #user_to_update.done = request.form["done"]
        #done = request.form["done"]
        #print(done)
        update_user(id)
        return redirect("/", code=302)
        #return redirect(url_for('home'))
        #user_id = request.args.get("id")
        #user_selected = User.query.get(user_id)
        #return render_template("index.html", user=user_selected)
        #return render_template("edit_rating.html", user=user_selected)

@app.route("/complete/<string:user_id>")
def complete(user_id):
    todo = User.query.filter_by(id=user_id).first()

    print(todo.done)
    todo.done = not todo.done
    print("true to false")
    print(todo.done)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/complete_false/<string:user_id>")
def complete_false(user_id):
    todo = User.query.filter_by(id=user_id).first()

    print(user_id)
    print(todo.done)
    todo.done = True
    print(todo.done)
    print("false to true")
    db.session.commit()
    return redirect(url_for("home"))

#update = user.query.filter_by(uid=id).first
#update.approved = True
#usr.session.commit()

@app.route("/delete")
def delete():
    user_id = request.args.get('id')

    # DELETE A RECORD BY ID
    user_to_delete = User.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=False)
