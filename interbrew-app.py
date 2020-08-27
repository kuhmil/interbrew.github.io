from flask import Flask, render_template, request
app = Flask(__name__)
import sqlite3
# Retrieve data from database
def getData():
	conn=sqlite3.connect('interbrew.db ')
	print("connecting to db")
	curs=conn.cursor()
	for row in curs.execute("SELECT * FROM  TEMP__data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
	conn.close()
	return time, temp
# main route 
@app.route("/")
def index():	
	time, temp= getData()
	templateData = {
		'time': time,
		'temp': temp
	}
	return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=False)
