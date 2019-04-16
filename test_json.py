from  flask import Flask

from flask import jsonify
import json



app = Flask(__name__)

keyboard="""{
		"DefaultHeight": true,
		"BgColor": "#FFFFFF",
		"Buttons": [{
			"Columns": 6,
			"Rows": 1,
			"BgColor": "#2db9b9",
			"BgMediaType": "gif",
			"BgMedia": "http://www.url.by/test.gif",
			"BgLoop": true,
			"ActionType": "open-url",
			"ActionBody": "www.tut.by",
			"Image": "www.tut.by/img.jpg",
			"Text": "Key text",
			"TextVAlign": "middle",
			"TextHAlign": "center",
			"TextOpacity": 60,
			"TextSize": "regular"
		    }]
	    }
        """

@app.route('/',methods=['GET'])
def get_current_user():
    return json.loads(keyboard)
if __name__=="__main__":
    app.run()