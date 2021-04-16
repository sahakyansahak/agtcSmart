from flask import *
import sqlite3
import os
import flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = '1502'
socketio = SocketIO(app)

#cmd = "python3 recognize_video.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle"
cmd1 = "python3 read.py"
cmd2 = "python3 solar.py"

#subprocess.Popen(cmd2, shell=True)
#subprocess.Popen(cmd1, shell=True)
#subprocess.Popen(cmd, shell=True)


temps = []
users = dict()

@app.route('/', methods=['GET', 'POST'])
def index():
	if g.user:
		return redirect(url_for('home'))
	if request.method == 'POST':
		session.pop('user', None)
		conn = sqlite3.connect("DB/user.db")
		c = conn.cursor()
		tables = get_tables()
		if len(tables) > 0:
			for i in tables:
					print("SELECT * FROM " + i[0])
					if request.form['password'] == c.execute("SELECT * FROM " + i[0]).fetchall()[0][1].strip() and request.form['username'] == c.execute("SELECT * FROM " + i[0]).fetchall()[0][0].strip():
						#print(c.execute("SELECT * FROM '" + str(i[0]) + " ' ").fetchall()[0][1].strip())
						#send_uname = i[0]
						#new_uname = i[0]
						session['user'] = request.form['username']
						return redirect(url_for('home'))

		else:
			if request.form['password'] == 'admin' and request.form['username'] == 'admin':
				#sned_uname = "aaa"
				#new_uname = "Admin"гет
				print("Uname set")
				session['user'] = request.form['username']
				return redirect(url_for('f_login'))

	return render_template('login1.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
	if g.user:
		return render_template('index.html', user=session['user'])
	else:
		return index()

@app.route("/log", methods=['GET', 'POST'])
def log():
	return index()


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'not'

@app.route('/get_curr_us', methods=['GET', 'POST'])
def get_curr_us():
	conn = sqlite3.connect("DB/user.db")
	c = conn.cursor()
	return jsonify(c.execute("SELECT * FROM " + getsession()).fetchall())


@app.route('/s_sys', methods=['GET', 'POST'])
def s_sys():
	global users
	if 1:
		# print(users[getsession()])
		return jsonify(users[getsession()])
	else:
		return "0"



@app.route('/valod', methods=['GET', 'POST'])
def valod():
    print(1)
    while getsession() != 'not':
        session.pop('user', None)
    print(1)
    return "11"


def get_tables():
	conn = sqlite3.connect("DB/user.db")
	c = conn.cursor()
	return c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()


@socketio.on('state')
def give(args):
	global users
	print(args)
	emit('thank', "thankyou")
	users[str(args["id"])] = args["states"]
	#print(users)

@socketio.on('hello')
def test_connect():
	emit('st', {'id': 1})

@app.route('/s/<id>/<switch>/<state>', methods = ['POST', 'GET'])
def s(id, switch, state):
	print('State change')
	socketio.emit('switch', {"id" : id, "switch" : switch, "state" : state})
	return "11"

@app.route('/h/<id>/<heat>/<temp>', methods = ['POST', 'GET'])
def h(id, heat, temp):
	print('State change heating')
	socketio.emit('heating', {"id" : id, "heat" : heat, "temp" : temp})
	return "11"


if __name__ == "__main__":
	print("Started")
	app.config['SESSION_TYPE'] = 'filesystem'
	app.debug = True
	#app.run(port=8002, host="0.0.0.0")
	socketio.run(app, port=8002, host="0.0.0.0")