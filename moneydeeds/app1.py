

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from sendemail1 import sendmail
import smtplib


  
app = Flask(__name__)
  
app.secret_key = 'a'

  
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'Yb3d6OreHO'
app.config['MYSQL_PASSWORD'] = 'yUdTQJdNSq'
app.config['MYSQL_DB'] = 'Yb3d6OreHO'
mysql = MySQL(app)
@app.route('/')

def homer():
    return render_template('home.html')

@app.route('/register', methods =['GET', 'POST'])
def registet():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, email,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            TEXT = "Hello "+username + ",\n\n"+ """Thanks for registring at MONEYDEED$ """ 
            #message  = 'Subject: {}\n\n{}'.format("moneydeeds", TEXT)
            sendmail(TEXT,email)
            #sendgridmail(email,TEXT)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = '' 
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password ),)

        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
            
        
        else:
            msg = 'Incorrect username / password !'
    return render_template('/login.html', msg = msg)

@app.route('/dashboard')
def dash():
    
    return render_template('dashboard.html')

@app.route('/wallet',methods =['GET', 'POST'])
def apply():
     msg = ''
     if request.method == 'POST' :
         #user_id= session["id"]
         #balance = "SELECT skills FROM job where userid = id"
         cursor = mysql.connection.cursor()
         cursor.execute('SELECT * FROM credit WHERE userid = % s', (session['id'], ))
         account = cursor.fetchone()
         income = request.form.get("income")

         if account != None:
          print(account)
          #username = request.form['username']
          #email = request.form['email']
          balance = account[1]  + float(request.form.get("income"))
          #income = float(request.form.get("income"))
          print(balance)
          cursor.execute('UPDATE credit SET income = % s WHERE userid = % s', (balance,session['id'], ))
          
         else: 
          cursor.execute('INSERT INTO credit VALUES (% s, % s)', (session['id'],income))   
         mysql.connection.commit()
         msg = 'You have successfully added your money to your wallet !'
         session['loggedin'] = True

         #designation= request.form['designation']
         #income = request.form['income']
        # reason = request.form['s']
        
         
         #cursor = mysql.connection.cursor()
         #account[4] = account[4] + int(income)
         #cursor.execute('INSERT INTO job VALUES (% s, % s, % s, % s,% s, % s)', (session['id'],username, email,designation,income,reason))
		 
         #sql = "UPDATE job SET skills = balance WHERE userid = id"       
                    
     elif request.method == 'POST':
         msg = 'Please fill out the form !'
     return render_template('wallet.html', msg = msg)

@app.route('/debit',methods =['GET', 'POST'])
def debit():
    msg =''
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        username = request.form['username']
        email = request.form['email']
        debit = request.form['debit']
        reason = request.form['s']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM credit WHERE userid = % s', (session['id'], ))
        account = cursor.fetchone()
        print(account)
         
        balance = account[1]  - float(request.form.get("debit"))
        print(balance)
         
        cursor.execute('UPDATE credit SET income = % s WHERE userid = % s', (balance,session['id'], ))
         
#        cursor.execute('INSERT INTO job VALUES (% s, % s, % s)', (session['id'],debit,reason))
        mysql.connection.commit()
        msg = 'You have successfully debited your money from your wallet !'
        session['loggedin'] = True
         
        if balance == 0 or balance < 0:
            TEXT = "Hello   "+username + ", \n\n"+ """ALERT: You have exceeded your limit """ 
            sendmail(TEXT,email)
        
         
         
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('debit.html', msg = msg)
        


        
 


@app.route('/display')
def display():
    print(session["username"],session['id'])
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM user WHERE id = % s', (session['id'],))
    account = cursor.fetchone()
    print("accountdislay",account)
    
    cursor.execute('SELECT * FROM credit WHERE userid = % s', (session['id'], ))
    acct = cursor.fetchone()
    print(acct)    

    
    return render_template('display.html',account = account, acct = acct)

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

    
if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port = 8080)