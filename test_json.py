from  flask import Flask
import simplejson as s_json

from flask import jsonify
import json



app = Flask(__name__)

"""keyboard={
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

keyboard={"DefaultHeight": True,
		"BgColor": "#FFFFFF",
		"Buttons": [{
			"Columns": 6,
			"Rows": 1,
			"BgColor": "#2db9b9",
			"BgMediaType": "gif",
			"BgMedia": "http://www.url.by/test.gif",
			"BgLoop": True,
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



@app.route('/')
def get_current_user():
    k=s_json.dumps(keyboard)
    print(k)
    return """ <html><body>
    </body></html>"""
if __name__=="__main__":
    app.run()