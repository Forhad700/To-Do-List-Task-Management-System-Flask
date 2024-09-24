from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

@app.route("/")
def home():
    filter_param = request.args.get("filter")
    if filter_param == "completed":
        todo_list = Todo.query.filter_by(complete=True).all()
    else:
        todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    if not title:
        return "Title is required", 400
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            return "Title is required", 400
        todo.title = title
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", todo=todo)

@app.errorhandler(500)
def internal_error(error):
    return "An internal error occurred. Please try again later.", 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
