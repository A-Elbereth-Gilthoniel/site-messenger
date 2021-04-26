from flask import Flask, render_template, session, request, redirect
import requests
import datetime


app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'Brain2132dsfed_wdqdw_123e'
link = 'http://127.0.0.1:5000/'
server_link = 'http://127.0.0.1:8080/'
username = ''


@app.route('/')
def intro():
    global username
    zareg = session.get('zareg', 0)
    if zareg == 0:
        return render_template('intro.html', link='http://127.0.0.1:5000/log_in/')
    else:
        username = session['username']
        return redirect('/chat/General_Chat')


@app.route('/log_in/', methods=['post', 'get'])
def login():
    global username
    global link
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #TODO
        a = requests.get(f'{server_link}checking', params={'email': email, 'password': password})
        b = a.json()
        if b[''] != 'Error':
            username = b[''][1]
            session['username'] = username
            session['zareg'] = 1
            return redirect('/chat/General_chat/')
        else:
            return 'Ошибка'
    return render_template('intro2.html', link=link)


@app.route('/registration', methods=['post', 'get'])
def registration():
    global link
    global username
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        rep_pass = request.form.get('repeat_password')
        username2 = request.form.get('username')
        if password == rep_pass:
            username = username2
            requests.post(f'{server_link}reg', json={'email': email, 'username': username, 'password': password})
            session['username'] = username
            session['zareg'] = 1
            return redirect('/chat/General_chat/')
    return render_template('registration.html', link=link)


@app.route('/chat/<number>/')
def chats(number):
    return render_template('chats.html', Username=session['username'])


if __name__ == '__main__':
    app.run()
