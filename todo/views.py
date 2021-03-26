from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect


def home(request):
    'Show home page'
    return render(request, 'home.html')


def login(request):
    'User login'
    # Get values from the POST request
    if request.method == 'POST':
        username = request.POST.get('txt_username')
        password = request.POST.get("txt_password")
        cursor = connection.cursor()
        
        sql = "select * from users where username=%s and password=%s"
        val = (username, password)
        cursor.execute(sql, val)
        record = cursor.fetchall()
        if record: # Login success
            request.session['user'] = record[0][3]
            request.session['user_id'] = record[0][0]
            # return render(request, 'todo.html', {'user':request.session['user']})
            return redirect('/todo/todo')
        else: # Login fail
            return render(request, 'login.html', {'message':'Invalid username or password'})
    else:
        return render(request, 'login.html')


def register(request):
    'new user registration'
    # Get values from the post request
    if request.method == 'POST':
        username = request.POST.get('txt_username')
        password = request.POST.get("txt_password")
        name = request.POST.get("txt_name")
        gender = request.POST.get("gender")
        phone = request.POST.get("txt_phone")
        dob = request.POST.get("txt_dob")

        try:
            cursor = connection.cursor()
            sql = "insert into users values(null, %s, %s, %s, %s, %s, %s )"
            val = (username, password, name, gender, phone, dob )
            cursor.execute(sql, val)
            success = ""
            fail = ""

            id = cursor.lastrowid
            if id:
                success = "Registration success"
            else:
                fail = "Regisration failed"
            return render(request, 'register.html', {'success': success, 'fail':fail})
        except Exception as e:
            return render(request, 'register.html', {'fail':str(e)})

    else:
        return render(request, 'register.html')


def todo(request):
    'Show todos'
    # Redirect to home page if not logged in 
    if not request.session.get('user'):
        return redirect('/todo/login/')

    # Show todos stored in database
    user_id = request.session['user_id']
    user = request.session['user']
    sql = "select * from todos  where user_id=%s "
    val=[str(user_id)]
    cursor = connection.cursor()
    cursor.execute(sql, val)
    records = cursor.fetchall()
    return render(request, 'todo.html', {'user': user, 'todos':records})


def save(request):
    'Save to do'
    # Get values from the request
    title = request.POST.get('txt_title')
    content = request.POST.get("txt_description")
    user_id = request.session['user_id']

    #  Save todo too database
    cursor = connection.cursor()
    sql = "insert into todos values(null, %s, %s, %s )"
    val = (title, content, str(user_id) )
    cursor.execute(sql, val)
    return redirect('/todo/todo')


def delete(request):
    'Delete to do from database on clicking delete button'
    id = request.GET.get('id')
    cursor = connection.cursor()
    sql = "delete from todos where todo_id=%s"
    val = (str(id))
    cursor.execute(sql, val)
    return redirect('/todo/todo')


def logout(request):
    'Logout from the application'
    request.session.clear()
    return redirect('/todo')