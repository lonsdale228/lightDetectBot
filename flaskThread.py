



def flaskStart(botStateMain):
    import datetime

    from flask import Flask

    from currentstate import getNowTime

    app = Flask(__name__)
    app.config['ENV'] = 'development'

    @app.route("/")
    def login():
        return "Hello World!"

    @app.route("/beba", methods=['POST','GET'])
    def success():

        #if not botStateMain["getReq"]:
        botStateMain.timeLastPOST=getNowTime().timestamp()
        print("POST Received",botStateMain.timeLastPOST)
        return "this is success"

    app.run(host="127.0.0.1", port=1242)