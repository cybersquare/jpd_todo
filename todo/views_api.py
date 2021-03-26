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
        username = data['txt_username']
        password = data["txt_password"]
        print(username, password)
        cursor = connection.cursor()
        
        sql = "select * from users where username=%s and password=%s"
        val = (username, password)
        cursor.execute(sql, val)
        record = cursor.fetchall()
        if record: # Login success
            request.session['user'] = record[0][3]
            request.session['user_id'] = record[0][0]
            return Response("login succcess")
        else: # Login fail
            return Response("login fail")
    else:
        return Response("hello")