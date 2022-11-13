import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from FDataBase import FDataBase

# конфигурация
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = '9XuKXXJp2bwGzdToyAN%Pb*cqE0cvZezNI'


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
# app.config['SECRET_KEY'] = 'oIVpBhUCgYEAzd2qlJTnDkiVe7rAlpXZ9I8GqD5n3A'


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


# menu = [{"name": "Установка", "url": "install-flask"},
#         {"name": "Первое приложение", "url": "first-app"},
#         {"name": "Обратная связь", "url": "contact"}
#         ]


# @app.route("/index")
# @app.route("/")
# def index():
#     print(url_for('index'))
#     return render_template('base.html', menu=menu)


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.route("/add_post", methods=['POST', 'GET'])
def addPost():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['title']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['title'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")


@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

# @app.route("/about")
# def about():
#     print(url_for('about'))
#     return render_template('about.html', title='О сайте Flask', menu=menu)
#
#
# @app.route("/profile/<username>")  # int: float: path:
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return f"Пользователь: {username}"
#
#
# @app.route("/contact", methods=['POST', 'GET'])
# def contact():
#     if request.method == 'POST':
#         if len(request.form['username']) > 2:
#             flash('Сообщение отправлено', category='success')
#         else:
#             flash('Ошибка отправки', category='error')
#         print(request.form)
#     print(url_for('contact'))
#     return render_template('contact.html', title='Обратная связь', menu=menu)
#
#
# @app.route("/login", methods=['POST', 'GET'])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == "alexsks" and request.form['psw'] == "1234":
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#     return render_template('login.html', title='Авторизация', menu=menu)
#
#
# @app.errorhandler(404)
# def pageNotFound(error):
#     return render_template('page404.html', title='Страница не найдена', menu=menu), 404


if __name__ == "__main__":
    app.run(debug=True)
