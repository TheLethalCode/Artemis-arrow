import os

class Config:
	APPLICATION_ROOT = os.path.dirname(__file__)
	DEBUG = True
	SESSION_TYPE = 'filesystem'
	SECRET_KEY = 'choose any valid secret key'.encode('utf8')


