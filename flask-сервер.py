from flask import Flask, request, abort
from time import time
import random
import sqlite3


# con = sqlite3.connect("datas.db")
#
#
# cur = con.cursor()

# result = cur.execute("""SELECT * FROM films
#             WHERE year = 2010""").fetchall()


app = Flask(__name__)
db = []
users_db = []
chats = {}
text = ''
name = ''


class Storage:
    def __init__(self):
        pass


storage = Storage()


@app.route('/users_in_chat')
def users_in_chat():
    a = request.args['id_chat']
    return {'': chats[a]}


@app.route('/get_info_in_chat/<id_>')
def get_info_in_chat(id_):
    if 'after' in request.args:
        after = float(request.args['after'])
    else:
        after = 0
    filtered_db = []
    for i in eval('storage.db{}'.format(id_)):
        if i['time'] > after:
            filtered_db.append(i)
    return {'': filtered_db}


@app.route('/chat/<id_>', methods=['POST'])
def send_to_chat(id_):
    if id_ in list(chats.keys()):
        text = (request.json['text'])
        name = (request.json['name'])
        exec("storage.db" + id_ + ".append({'text': text, 'name': name, 'time': time()})")
        return {'ok': True}


@app.route('/')
def index():
    return '<div style="font-size: 25pt; color: red;">Внимание! Покиньте данный сайт!</div>'


 # http://127.0.0.1:8080/


@app.route('/reg', methods=['POST'])
def registration():
    user = request.json
    con = sqlite3.connect("datas.db")
    cur = con.cursor()
    cur.execute(f'INSERT INTO users(Username, Email, Password) VALUES (\'{user["username"]}\', \'{user["email"]}\', \'{user["password"]}\')')
    con.commit()
    return {'ok': True}


@app.route('/checking_mail')
def checking_mail():
    info = request.args
    a = False
    b = False
    index1 = -100
    index2 = -100
    id_chat = 'p'.join([str(i) for i in random.choices(list(range(10000)), k=10)])
    while id_chat in list(chats.keys()):
        id_chat = 'p'.join([str(i) for i in random.choices(list(range(10000)), k=10)])
    for i in range(len(users_db)):
        if users_db[i]['mail'] == info['mail']:
            index1 = i
            name = users_db[i]['name'] + ' ' + users_db[i]['surname']
            a = True
        if users_db[i]['mail'] == info['own_mail']:
            index2 = i
            name2 = users_db[i]['name'] + ' ' + users_db[i]['surname']
            b = True
        if a and b:
            users_db[index1]['chats'].append(id_chat)
            users_db[index2]['chats'].append(id_chat)
            chats[id_chat] = (name, name2)
            exec('storage.db{} = []'.format(id_chat))
            return {'': id_chat + ', ' + name}
    return {'': 'error'}


@app.route('/checking')
def checking_account():
    info = request.args
    con = sqlite3.connect("datas.db")
    cur = con.cursor()
    flist = list(cur.execute(f"SELECT * FROM users WHERE Email = \'{info['email']}\' AND Password = \'{info['password']}\'").fetchall())
    if flist:
        return {'': flist[0]}
    else:
        return {'': 'Error'}
    # for i in range(len(users_db)):
    #     if info['mail'] == users_db[i]['mail']:
    #         if info['password'] == users_db[i]['password']:
    #             return {'': users_db[i]}
    #         return {'': 'Неправильный пароль'}
    # return {'': 'Неправильная электронная почта'}


@app.route('/send', methods=['POST'])
def send_message():
    text = (request.json['text'])
    name = (request.json['name'])
    db.append({
    'text': text,
    'name': name,
    'time': time()
    })
    return {'ok': True}


@app.route('/get')
def get_message():
    if 'after' in request.args:
        after = float(request.args['after'])
    else:
        after = 0
    filtered_db = []
    for i in db:
        if i['time'] > after:
            filtered_db.append(i)
    return {'': filtered_db}


if __name__ == "__main__":
    app.run(port=8080)