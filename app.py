import os
from flask import Flask, render_template, request


app= Flask('__main__')
app.root_path = os.path.dirname(os.path.abspath(__file__))


@app.route('/')

def main():
	return render_template('index.html')


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




