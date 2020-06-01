# -*- coding: utf-8 -*-
"""
Created on Tue May 26 21:51:05 2020

@author: shrey
"""

from flask import Flask, render_template, request,session,redirect,url_for, jsonify, abort
from flask_socketio import SocketIO, emit
from utils.calculator import evaluate

# Create the application instance
app = Flask(__name__, template_folder="templates")
app.secret_key = "hijibiji"
socketio = SocketIO(app)
history = []


#@app.route('/', methods= ['POST', 'GET'])
#@app.route('/login', methods= ['POST', 'GET'])
#def login():
#    if request.method == 'POST':
#        username = request.form['username']
#        session['username'] = username
#        return redirect(url_for("getCalculation"))
#
#    return '''<form method = "POST">
#Username <input type="text" name = "username">
#<input type="submit">
#</form> '''

def getCalculationFunction(operation):
    #can improve this later
    try:
        return eval(operation)
    except:
        return None

def addOperation(operation, result):
    if len(history) >= 10:
        history.pop(0)
    calc = operation + ' = ' + str(result)
    history.append(calc)
    
@app.route('/getHistory/', methods=['GET'])
def getHistory():
    try:
        return (jsonify({'history':history}), 200)
    except:
        abort(400)

@app.route('/', methods= ['POST', 'GET'])
def getCalculation():
    if request.method == 'POST':
        try:
            operation = request.form['operation']
#            if getCalculationFunction(operation):
#                addOperation(operation, getCalculationFunction(operation))
#                print(history)
#                return render_template("index.html", result= getCalculationFunction(operation))
            res = evaluate(operation)
            addOperation(operation, res)
            return render_template("index.html", result= res)
        except Exception as err:
            return "Error encountered: {}".format(err)
#        else:
#            abort(400)
        #return "User {} calculated {}".format(session['username'], getCalculationFunction(operation))
    else:
        return render_template("index.html")


        
@socketio.on('/new_operation/')
def notifyUsers(data):
    operation = data['operation']
    try:
        result = evaluate(operation)
        message = operation + ' = ' + str(result)
        emit('result', result)
        emit('notification', message, broadcast = True, include_self = False)
    except:
        pass
      

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
#    app.run(debug=True)
    socketio.run(app)
