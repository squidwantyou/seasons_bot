#!/usr/bin/env python
from flask import Flask, request
import api_seasons
import api_puzzle
# import api_private

app = Flask(__name__)

@app.route('/',methods=["POST"] )
def post_data():
        if request.get_json().get('message_type') == 'group' :
                gid = request.get_json().get('group_id')
                uid = request.get_json().get('sender').get('user_id')
                message = request.get_json().get('raw_message')
                if gid == 144744787:
                        pass
                        # api_seasons.keyword(message,uid,gid)
                elif gid == 530879511:
                        api_puzzle.keyword(message,uid,gid)
                elif gid == 528343595:
                        api_puzzle.keyword(message,uid,gid)
                else:
                        api_puzzle.keyword(message,uid,gid)
        elif request.get_json().get('message_type') == 'private' :
            uid = request.get_json().get('sender').get('user_id')
            message = request.get_json().get('raw_message')
            api_private.keyword(message,uid,gid=None)
        return 'OK'

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0',port=5701)
