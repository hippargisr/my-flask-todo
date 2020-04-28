from flask import Flask, redirect, render_template, request, escape
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "TODO"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app) 

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		data  = escape(request.form['input-data'])
		try:
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO todo(content)VALUE(%s)",[data])
			mysql.connection.commit()
			return redirect('/')
		except :
			cur.close()
			error = "May be incorrect data"
			return render_template("index.html", error = error)
	else:
		cur = mysql.connection.cursor()
		results = cur.execute("SELECT * FROM todo")
		if results > 0:
			result = cur.fetchall()
		return render_template("index.html",result = result)

@app.route("/delet/<int:id>")
def delete(id):
	print("DELETE",id)
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM todo WHERE id={}".format(id))
	mysql.connection.commit()
	cur.close()
	return redirect('/')

@app.route('/update/<int:id>', methods=["POST","GET"])
def update(id):
	cur = mysql.connection.cursor()
	res = cur.execute("SELECT * FROM todo WHERE id={}".format(id))
	if res> 0:
		task = cur.fetchone()

	if request.method == "POST":
		task_data = escape(request.form['input-data'])
		cur.execute("UPDATE todo SET content = %s WHERE id=%s",(task_data,id))
		mysql.connection.commit()
		cur.close()
		return redirect('/')
	else:
		return render_template("update.html",task = task)
if __name__ == "__main__":
	app.run(debug=True)