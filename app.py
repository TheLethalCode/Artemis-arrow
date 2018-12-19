from flask import Flask, render_template, request,flash,redirect
import mysql.connector
import database
import config

mydb = mysql.connector.connect(host=config.Config.MYSQL_DATABASE_HOST,user=config.Config.MYSQL_DATABASE_USER,passwd=config.Config.MYSQL_DATABASE_PASSWORD)
mycursor = mydb.cursor()
mycursor.execute("USE Artemis")
if mycursor == None:
	database.makedatabase()


app= Flask('__main__')
app.config.from_object('config.Config')

@app.route('/')

def main():
	return render_template('index.html')


@app.route('/signup',methods=['POST','GET'])
def signup():

	if request.method=='GET':
		return redirect('/profile',code = 301)
	
#	mycursor.execute('SELECT * FROM people WHERE username = \'noone\';')
#	myresult = mycursor.fetchall()
#	print(type(myresult))
#	print(myresult)
	
	_firstname = request.form['firstname']
	_lastname = request.form['lastname']
	_email = request.form['email']
	_username = request.form['username']
	_password = request.form['password']
	_confpassword = request.form['conf-password']

	if not _firstname and _lastname and _email and _username and _password and _confpassword:
		flash('All fields for signup are not filled!','invalid')
#		print('HERE')
	elif(_password!=_confpassword):
		flash('Password should be same as confirmation password')
#		print('HEr')
	else:
		mycursor.execute('SELECT * FROM people WHERE username = \''+_username+'\';')
		myresult = mycursor.fetchall()
		if not myresult:
			mycursor.execute('SELECT * FROM people WHERE email = \''+_email+'\';')
			myresult = mycursor.fetchall()
			if not myresult:
				sql = "INSERT INTO people VALUES (%s, %s,%s,%s,%s)"
				val = (_firstname,_lastname,_email,_username,_password)
				mycursor.execute(sql, val)
				mydb.commit()
				flash('Registered Successfully','valid')
				return redirect('/profile',code=302)
#				print('DONE')				
			else:
				flash('Email ID registered!!!','invalid')
		else:
			flash('Username exists!!!','invalid')

	return redirect('/',code=302)





@app.route('/profile')

def showprofile():
	return render_template('profile.html')



@app.route('/songs')

def songs():
	pass

@app.route('/anime')

def anime():
	pass

@app.route('/books')

def books():
	pass

@app.route('/drive')

def drive():
	pass

if __name__ == '__main__':

	app.run('0.0.0.0',8080)




