from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.db import connection


@csrf_exempt
@api_view(['GET', 'POST'])
def home(request):
    print ("hello")
    # return HttpResponse("hello")
    return Response("hello")

@csrf_exempt
@api_view(['GET', 'POST'])
def login(request):
    'User login'
    # Get values from the POST request
    if request.method == 'POST':
        data = request.data
        username = data['username']
        password = data["password"]
        cursor = connection.cursor()
        
        sql = "select * from users where username=%s and password=%s"
        val = (username, password)
        cursor.execute(sql, val)
        record = cursor.fetchall()
        if record: # Login success
            request.session['user'] = record[0][3]
            request.session['user_id'] = record[0][0]
            return Response(json.dumps({"result":"login success"}))
        else: # Login fail
            return Response("login failed")
    else:
        return Response("hello")


@csrf_exempt
@api_view(['GET', 'POST'])
def register(request):
    'new user registration'
    # Get values from the post request
    if request.method == 'POST':
        data = request.data
        username = data['username']
        password = data["password"]
        name = data["name"]
        gender = data["gender"]
        phone = data["phone"]
        dob = data["dob"]

        try:
            cursor = connection.cursor()
            sql = "insert into users values(null, %s, %s, %s, %s, %s, %s )"
            val = (username, password, name, gender, phone, dob )
            cursor.execute(sql, val)
            result = ""

            id = cursor.lastrowid
            if id:
                result = "Registration success"
            else:
                result = "Regisration failed"
            return Response(json.dumps({"result":result}))
        except Exception as e:
            return Response(json.dumps({"result":str(e)}))

    else:
        return Response("Register")


@csrf_exempt
@api_view(['GET', 'POST'])
def todo(request):
    'Show todos'
    records = ""
    if request.method == 'POST':
        data = request.data
        username = data['username']
        records = get_todo(username)
    return Response(json.dumps(records))


@csrf_exempt
@api_view(['GET', 'POST'])
def save(request):
    'Save to do'
    # Get values from the request
    username = ""
    if request.method == 'POST':
        data = request.data
        username = data['username']
        title = data['title']
        content = data["description"]
        #  Get user id from users table 
        cursor = connection.cursor()
        sql = "select user_id from users where username = %s"
        val = [username]
        cursor.execute(sql, val)
        recrods = cursor.fetchall()
        user_id = recrods[0][0]
        #  Save todo too database
        sql = "insert into todos values(null, %s, %s, %s )"
        val = [title, content, str(user_id) ]
        cursor.execute(sql, val)
    records = get_todo(username)
    return Response(json.dumps(records))


@csrf_exempt
@api_view(['GET', 'POST'])
def delete(request):
    'Delete to do from database on clicking delete button'
    username = ""
    if request.method == 'POST':
        data = request.data
        username = data['username']
        id_todo = data['todo_id']
        #  Delete todo 
        sql = "delete from todos where todo_id=%s"
        val = [str(id_todo)]
        cursor = connection.cursor()
        cursor.execute(sql, val)
    records = get_todo(username)
    return Response(json.dumps(records))



def get_todo(username):
    'Show todos'
    # Show todos stored in database
    sql = "select todo_id, title, content from todos t \
           join users u on  t.user_id = u.user_id \
           where u.username=%s "
    val=[username]
    cursor = connection.cursor()
    cursor.execute(sql, val)
    records = cursor.fetchall()
    return records