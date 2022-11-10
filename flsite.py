from flask import Flask, render_template, url_for, request

app = Flask(__name__)

menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}
        ]


@app.route("/index")
@app.route("/")
def index():
    print(url_for('index'))
    return render_template('base.html', menu=menu)


@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title='О сайте Flask', menu=menu)


@app.route("/profile/<username>")  # int: float: path:
def profile(username):
    return f"Пользователь: {username}"


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        print(request.form)
    print(url_for('contact'))
    return render_template('contact.html', title='Обратная связь', menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
