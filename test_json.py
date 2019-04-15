from  flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def get_current_user():
    return jsonify(username="admin",
                   email="admin@localhost",
                   id=42)
if __name__=="__main__":
    app.run()