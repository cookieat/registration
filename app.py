import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app=Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="1qa2ws3ed",
                        host="localhost",
                        port="5433")

cursor=conn.cursor()


#@app.route('/login/', methods=['GET'])
#def index():
#   return render_template('login.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        cursor.execute("SELECT * FROM service.users WHERE login=%s", [str(login)])
        if (len(login)>5) and (len(password)>5) and (len(name)>5):
            records = list(cursor.fetchall())
            print (records)
            if records:
                return render_template('check_error.html')
            else:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                               (str(name), str(login), str(password)))
                conn.commit()


        else:
            return render_template('registration_error.html')

        return redirect('/login/')

    return render_template('registration.html')
