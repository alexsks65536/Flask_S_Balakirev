from werkzeug.security import generate_password_hash
from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Создаем переменную для работы с БД
# создаем конфигурацию и указываем название БД и расположение в корне
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # создаем переменную для доступа к БД


class Users(db.Model):  # Создаем класс - это имя таблицы БД с описанием полей
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):  # вспомогательный метод ля отображения класса в консоли
        return f"<users {self.id}>"


class Profiles(db.Model):  # Создаем класс - это имя таблицы БД с описанием полей
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # внешний ключ для связи с таблицей 'Users'

    def __repr__(self):  # вспомогательный метод ля отображения класса в консоли
        return f"<profiles {self.id}>"


@app.route("/")
def index():
    info = []
    try:
        info = Users.query.all()
    except:
        print("Ошибка чтения из БД")

    return render_template("index.html", title="Главная", list=info)


@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        # здесь должна быть проверка введенных данных
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], psw=hash)
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

    return render_template("register.html", title="Регистрация")


if __name__ == "__main__":
    app.run(debug=True)
