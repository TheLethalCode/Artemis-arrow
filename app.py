from flask import Flask, render_template, request
import sqlite3 as sql

app= Flask('__main__')


@app.route('/')
def main():
	return render_template('index.html')

@app.route('/aftersignup',methods = ['POST', 'GET'])
def aftersignup():
	if request.method == 'POST':
		try:
			fnm = request.form['firstname']
			lnm = request.form['lastname']
			email = request.form['email']
			unm = request.form['username']
			pwd = request.form['password']
			
			with sql.connect("da1.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO users (fname,lname,email,uname,password)VALUES (?,?,?,?,?)",(fnm,lnm,email,unm,pwd) )
				con.commit()
				msg = "Record successfully added"
		except:
			sql.connect("da1.db").rollback()
			msg = "error in insert operation"
			  
		return render_template("aftersignup.html",msg=msg)
		con.close()

@app.route('/profile',methods=['POST', 'GET'])
def profile():
		if request.method == 'POST':
			email = request.form['email']
			pwd = request.form['password']
			con = sql.connect("da1.db")
			f=0
			cursor=con.execute("select * from users")
			for row in cursor:
				if(row[2]==email and row[4]==pwd):
					msg="login succcessfully"
					f=1
					return render_template("profile.html",msg=msg)
			if(f==0):
				msg="login unsuccessfull"
				return render_template("index.html",msg=msg)


if __name__ == '__main__':
   app.run(debug = True)
