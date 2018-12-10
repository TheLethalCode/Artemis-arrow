from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
      return render_template('intro.html')

@app.route('/signup')
def signup():
      return render_template('signup.html')

@app.route('/aftersignup',methods = ['POST', 'GET'])
def aftersignup():
   if request.method == 'POST':
      try:
            fnm = request.form['firstname']
            lnm = request.form['lastname']
            age = request.form['age']
            email = request.form['emailaddress']
            pwd = request.form['password']
         
            with sql.connect("da1.db") as con:
                  cur = con.cursor()
                  cur.execute("INSERT INTO user (fname,lname,age,email,password)VALUES (?,?,?,?,?)",(fnm,lnm,age,email,pwd) )
            
                  con.commit()
                  msg = "Record successfully added"
      except:
            sql.connect("da1.db").rollback()
            msg = "error in insert operation"
      
      return render_template("aftersignup.html")
      con.close()

@app.route('/login')
def login():
      return render_template('login.html')

@app.route('/afterlogin',methods=['POST', 'GET'])
def afterlogin():
      if request.method == 'GET':
            email = request.form['emailaddress']
            pwd = request.form['password']
            con = sql.connect("da1.db")
            cursor=con.execute("select * from user")
            rows = cursor.fetchall()
            f=0
            for r in rows:
                  if(r[3]==email and r[4]==pwd):
                        msg="login successfully"
                        return render_template("login.html")
                        f=1
            if(f==0):
                  msg="login unsuccessfull"
                  return render_template("login.html")
            con.close()

@app.route('/mainpage')
def mainpage():
      return render_template("mainpage.html")

if __name__ == '__main__':
   app.run(debug = True)
