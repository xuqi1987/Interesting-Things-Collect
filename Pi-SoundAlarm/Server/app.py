#! /usr/bin/python
# -*- coding:utf-8 -*-


from flask import Flask,jsonify
from sensor import Sensor

app = Flask(__name__)
se = Sensor()

@app.route('/sound')
def sound():
    se.setup()
    return jsonify(id=se.get())

    pass
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)
