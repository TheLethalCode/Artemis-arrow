from flask import Flask, render_template, request, flash, redirect
from flask_session import Session
import sqlite3 as sql
import connection as cn
import config
import os

DATABASE = cn.DATABASE
cn.get_db()

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),"templates")
STATIC_DIR = os.path.join(os.path.dirname(__file__),"static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config.from_object('config.Config')
session = Session()
session.init_app(app)


@app.route('/')
def main():
	return render_template('index.html')


@app.route('/signup',methods=['POST','GET'])
def signup():

	if request.method=='GET':
		return redirect('/profile',code = 301)
	
	try:
		con = sql.connect(DATABASE)

		fnm = request.form['firstname']
		lnm = request.form['lastname']
		email = request.form['email']
		unm = request.form['username']
		pwd = request.form['password']
			
		if not fnm and lnm and email and unm and pwd:
			flash('All fields for signup are not filled!','invalid')

		else:
			cur = con.cursor()
			result = cur.execute(
						'SELECT * FROM users WHERE username=?;',(unm,)
						).fetchall()
			
			if not result:
				result = cur.execute(
					'SELECT * FROM users WHERE email=?;',(email,)
					).fetchall()
				
				if not result:
					cur.execute("INSERT INTO users " + 
								"(fname,lname, email, uname, password) " +
								"VALUES (?,?,?,?,?)",(fnm,lnm,email,unm,pwd)
								)
					con.commit()
					flash('Registered Successfully','valid')
					msg = "Record successfully added"

				else:
					flash('Email ID already exists!','invalid')
			
			else:
				flash('Username exists!','invalid')
	
	except:
		con.rollback()
		msg = "Error in Insert Operation"

	con.close()		  
	return render_template("aftersignup.html",msg=msg)
	

@app.route('/profile',methods=['POST', 'GET'])
def profile():

	if request.method == 'POST':

		email = request.form['email']
		pwd = request.form['password']
		
		con = sql.connect(DATABASE)
		cur = con.cursor()
		results = cur.execute(
				"SELECT password FROM users WHERE email=?",(email,)
				).fetchall()
		for row in results:
			if(row[0]==pwd):
				msg="login succcessfull"
				return render_template("profile.html",msg=msg)
			else:
				msg="login unsuccessful"
				return render_template("index.html",msg=msg)
	return render_template("index.html")

@app.route('/logout')
def logout():
	return render_template("index.html")

if __name__ == '__main__':
   app.run(debug = True)
