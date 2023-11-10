from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# функція відображення
def show_registration(request):
    #якщо метод відпраки пост, то:
    if request.method == "POST":
        #виймаються данні з реквест.пост
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        #перевіряеться якщо згначення двох перемінних однакові
        if password == password_confirm:
            #робимо спробу
            try:
                # створюеться елемент у бд
                User.objects.create_user(username=username, password=password)
                # юзер перенаправляеться на сторінку з таким ім'ям
                return redirect("successfulreg")
            # у разі помилки
            except IntegrityError:
                #рендериться хтмл файл
                return render(request, "userapp/reg.html", context={"text_error" : "This user exsists"})
        else:
            #рендериться хтмл файл
            return render(request, "userapp/reg.html", context={"text_error" : "passwords aren't the same"})
    #рендериться хтмл файл
    return render(request, "userapp/reg.html")

# функція відображення
def successful_registartion(request):
    #рендериться хтмл файл
    return render(request, "userapp/successful_reg.html")

# функція відображення
def view_login(request):
    # якщо метод відправки пост
    if request.method == "POST":
        #витягуються перемінні
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Возвращает None, если такого пользователя нет. Если он есть - возвращает запись юзера из БД
        user = authenticate(request, username=username, password=password)
        #якщо все таки такий юзер є:
        if user is not None:
            #створюеться сесія
            login(request, user)
            #юзер перенаправляеться на сторінку з таким ім'ям
            return redirect("successful_log")
        # Додаткове завдання: дописати код, що буде відображати помилку користувачеві на сторінці,
        # у разі, якщо користувач неправильно ввів логін або пароль
        # else:
            # error: password or login isnt correct
    #рендериться хтмл файл
    return render(request, 'userapp/login.html' )

# функція відображення
def show_successful_login(request):
    # перевірка чи юзер увійшов
    if request.user.is_authenticated:
        #рендериться хтмл файл
        return render(request, "userapp/succesful_login.html")
    # якщо не увійшов
    else:
        #юзер перенаправляеться на сторінку з таким ім'ям
        return redirect("login")

#функція відображення
def user_logout(request):
    # а тут сесії кінець
    logout(request)
    #юзер перенаправляеться на сторінку з таким ім'ям
    return redirect("login")