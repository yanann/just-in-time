from flask import Flask
from flask import request

app = Flask(__name__)

#Slack verification
@app.route('/verification', methods=['POST'])

def verification():
	content = request.is_json
	if content['type'] == 'url_verification':
		return Response(content['challenge'], mimetype = "text/plain", status = 200)
	else:
		return Response(status=404)


