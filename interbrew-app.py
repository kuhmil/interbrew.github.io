from flask import Flask, render_template, request
app = Flask(__name__, template_folder='templates')
import sqlite3
# Retrieve data from database
def getData():
	conn=sqlite3.connect('interbrew.db')
	print("connecting to db")
	curs=conn.cursor()
	for row in curs.execute("SELECT * FROM DATA ORDER BY time DESC LIMIT 1"):
		date = str(row[0])
		time = str(row[1])
		temp = row[2]
	conn.close()
	return date, time, temp
# main route
@app.route("/")
def index():
	date, time, temp= getData()
	templateData = {
		'date': date,
		'time': time,
		'temp': temp
	}
	return render_template('index.html', **templateData)
	#return flask.render_template('index.html', **templates)
if __name__ == "__main__":
   app.run(host='0.0.0.0',port=2000, debug=False)
   #app.debug=True
  # app.run()
