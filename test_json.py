from  flask import Flask, jsonify
import simplejson as s_json


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
def get_json():
    #json_out=jsonify(keyboard)
    json_d=json.dumps(keyboard)
    print(type(json_d))
    return json_d
if __name__=="__main__":

    app.run()