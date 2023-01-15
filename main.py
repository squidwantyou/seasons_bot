#!/usr/bin/env python
from flask import Flask, request
import api

app = Flask(__name__)

@app.route('/',methods=["POST"] )
def post_data():
	if request.get_json().get('message_type') == 'group' :
		gid = request.get_json().get('group_id')
		uid = request.get_json().get('sender').get('user_id')
		message = request.get_json().get('raw_message')
		if gid == 144744787:
			api.keyword(message,uid,gid)
	return 'OK'

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=5701)
