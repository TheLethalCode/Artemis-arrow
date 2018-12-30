from flask import Flask, render_template, request, flash, redirect
from flask import send_file, url_for, after_this_request
from flask_session import Session
import requests
import sqlite3 as sql
import connection as cn
from config import Config
import os
import urllib
from dotenv import load_dotenv                               
from songs import oauth, ext_down
from anime import anime_download

load_dotenv()

DATABASE = cn.DATABASE
cn.get_db()

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),"templates")
STATIC_DIR = os.path.join(os.path.dirname(__file__),"static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config.from_object(Config)
session = Session()
session.init_app(app)


@app.route('/')
def main():
	return render_template('index.html')


@app.route('/signup',methods=['POST','GET'])
def signup():

	if request.method=='GET':
		return render_template('Register.html')
	
	try:
		con = sql.connect(DATABASE)

		fnm = request.form['firstname']
		lnm = request.form['lastname']
		email = request.form['email']
		unm = request.form['username']
		pwd = request.form['password']
		cpwd = request.form['conf-password']

		if pwd != cpwd:
			msg = "Passwords did not match"
			flash('Passwords do not match','invalid')

		else:
			cur = con.cursor()
			result = cur.execute(
						'SELECT * FROM users WHERE uname=?;',(unm,)
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
	print(msg) 
	return render_template("aftersignup.html",msg=msg)
	

@app.route('/login',methods=['POST', 'GET'])
def login():

	if request.method == 'POST':

		email = request.form['email']
		pwd = request.form['password']
		
		con = sql.connect(DATABASE)
		cur = con.cursor()
		results = cur.execute(
				"SELECT password FROM users WHERE email=?",(email,)
				).fetchall()
		if results:
			for row in results:
				if(row[0]==pwd):
					flash("login succcessful")
					return redirect("/profile")
				else:
					flash('Passwords do not match','invalid')
					return redirect("/")
		
		else:
			flash('Username does not exist','invalid')
			return redirect('/')
	
	else:
		return render_template('signin.html')


@app.route('/profile')
def profile():
	return render_template('profile.html')


@app.route('/song')
def song_list():
	song = request.args.get('song')
	results  = ext_down.video_id(song)
	
	URL = "http://localhost:5000/song_down?"

	for ind,result in enumerate(results):
		f = {
			"id" : result["id"],
			"title" : result["title"],
			"song" : song
		}
		result["url"] = URL + urllib.parse.urlencode(f)
		results[ind] = result 
	
	return render_template('songs.html', results=results)


@app.route('/song_down')
def song_down():
	
	id = request.args.get('id')
	name = request.args.get('title')
	attachment = request.args.get('song') + ".mp3"

	filename = ext_down.youtbe_dl_down(id,name)
		
	return send_file(filename,as_attachment=True,attachment_filename=attachment)


@app.route('/anime')
def anime_list():
	
	anime = request.args.get('anime')
	result = anime_download.SearchAnime(anime)

	if result["status"] == "success":
		animes = []
		for anime in result["links"]:
			anime["link"] = url_for('anime_down',name=anime["name"],url=anime["url"])
			animes.append(anime) 
		return render_template('anime.html',results=animes)

	return result["status"]


@app.route('/anime/<name>')
def anime_down(name):
	
	url = request.args.get('url')
	print(url)
	results = anime_download.getDownloadlinks(url)
	if results["status"] == "success":
		episodes = []
		for ep in results["links"]:
			ep["link"] = ep["url"]
			episodes.append(ep)
		return render_template('anime.html',results=episodes)

	return results["status"]


@app.route('/oauth2callback')
def oauth2callback():

	try:
		code=request.args.get('code')
	except:
		return "Acces denied"

	resp = oauth.ret_token(code)


@app.route('/logout')
def logout():
	return render_template("index.html")


if __name__ == '__main__':
   app.run(debug = True)
