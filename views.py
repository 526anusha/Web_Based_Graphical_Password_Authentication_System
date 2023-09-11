from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
import pymysql
from django.core.files.storage import FileSystemStorage

global username, password, contact, email, address


def UserLogin(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'GraphPassword',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    password = row[1]
                    break
        if password != 'none':
            output = '<center><img src="/static/password/'+password+'" alt="" width="400" height="300"  id="myImgId" onmousemove="getPos(event)"/></center>'
            context= {'data':output}
            return render(request, 'ShowAuthenticateImage.html', context)
        if password == 'none':
            context= {'data':'Invalid username'}
            return render(request, 'Login.html', context)


def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def Reset(request):
    if request.method == 'GET':
       return render(request, 'Reset.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})


def getSpotValue(spot):
    arr = spot.split(",")
    values = []
    values.append(int(arr[0].strip()))
    values.append(int(arr[1].strip()))
    return values

def authspots(old_spot, new_spot):
    auth = False
    old_x = old_spot[0]
    old_y = old_spot[1]
    previous_x = old_x - 10
    forward_x = old_x + 10
    previous_y = old_y - 10
    forward_y = old_y + 10
    if new_spot[0] >= previous_x and new_spot[0] <= forward_x and new_spot[1] >= previous_y and new_spot[1] <= forward_y:
        auth = True
    return auth

def PasswordAuthAction(request):
    if request.method == 'POST':
        global username
        spot1 = getSpotValue(request.POST.get('t1', False))
        spot2 = getSpotValue(request.POST.get('t2', False))
        spot3 = getSpotValue(request.POST.get('t3', False))
        spot4 = getSpotValue(request.POST.get('t4', False))
        password = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'GraphPassword',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,spot1,spot2,spot3,spot4 FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    old_spot1 = getSpotValue(row[1])
                    old_spot2 = getSpotValue(row[2])
                    old_spot3 = getSpotValue(row[3])
                    old_spot4 = getSpotValue(row[4])
                    if authspots(old_spot1, spot1) and authspots(old_spot2, spot2) and authspots(old_spot3, spot3) and authspots(old_spot4, spot4):
                        password = "success"
                        break
        if password == "success":
            context= {'data':'Welcome '+username+"<br/>Login successfull"}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid spot selection'}
            return render(request, 'Login.html', context)             
                    

def PasswordAction(request):
    if request.method == 'POST':
        global username, password, contact, email, address
        spot1 = request.POST.get('t1', False)
        spot2 = request.POST.get('t2', False)
        spot3 = request.POST.get('t3', False)
        spot4 = request.POST.get('t4', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'GraphPassword',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO register(username,password,contact,email,address,spot1,spot2,spot3,spot4) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"','"+spot1+"','"+spot2+"','"+spot3+"','"+spot4+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'Signup Process Completed'}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Error in signup process'}
            return render(request, 'Register.html', context)     

def RegisterAction(request):
    if request.method == 'POST':
        global username, password, contact, email, address
        username = request.POST.get('t1', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        password = request.FILES['t2'].name
        myfile = request.FILES['t2']
        fs = FileSystemStorage()
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'GraphPassword',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,email FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break
                if row[1] == email:
                    output = email+" Email id already exists"
                    break
        if output == "none":
            fs.save('GraphPasswordApp/static/password/'+password, myfile)
            output = '<center><img src="/static/password/'+password+'" alt="" width="400" height="300"  id="myImgId" onmousemove="getPos(event)"/></center>'
            context= {'data':output}
            return render(request, 'ShowImage.html', context)
        else:
            context= {'data':output}
            return render(request, 'Register.html', context)
    

def ViewUsers(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Username','Password Image','Contact No','Email ID','Address','Spot1','Spot2','Spot3','Spot4']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'GraphPassword',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>"+font+row[0]+"</td>"
                output+='<td><img src=/static/password/'+row[1]+' height=100 width=100/></td>'
                output += "<td>"+font+row[2]+"</td>"
                output += "<td>"+font+row[3]+"</td>"
                output += "<td>"+font+row[4]+"</td>"
                
                output += "<td>"+font+row[5]+"</td>"
                output += "<td>"+font+row[6]+"</td>"
                output += "<td>"+font+row[7]+"</td>"
                output += "<td>"+font+row[8]+"</td>"
        context= {'data':output}        
        return render(request, 'ViewUsers.html', context)

def UpdatePassword(request):
    if request.method == 'POST':
        global username, password
        spot1 = request.POST.get('t1', False)
        spot2 = request.POST.get('t2', False)
        spot3 = request.POST.get('t3', False)
        spot4 = request.POST.get('t4', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'GraphPassword',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update register set password='"+password+"',spot1='"+spot1+"',spot2='"+spot2+"',spot3='"+spot3+"',spot4='"+spot4+"' where username='"+username+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'Password Reset Process Completed'}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Error in reset password'}
            return render(request, 'Reset.html', context)  


def ResetAction(request):
    if request.method == 'POST':
        global username, password
        password = request.FILES['t1'].name
        myfile = request.FILES['t1']
        fs = FileSystemStorage()
        fs.save('GraphPasswordApp/static/password/'+password, myfile)
        output = '<center><img src="/static/password/'+password+'" alt="" width="400" height="300"  id="myImgId" onmousemove="getPos(event)"/></center>'
        context= {'data':output}
        return render(request, 'ShowResetImage.html', context)
        
def AdminLoginAction(request):
    if request.method == 'POST':
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if user == 'admin' and password == 'admin':
            context= {'data':'Welcome '+user}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid login'}
            return render(request, 'AdminLogin.html', context)
            
        
        
