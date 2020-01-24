from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def createuser(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return render(request, 'index.html')
    password = request.POST['password']
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=request.POST['first_name'],
                                   last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
    request.session['userid'] = new_user.id
    return redirect('/success')


def dashboard(request):
    if request.session.get('userid') is None:
        return redirect('/')
    user = User.objects.filter(id=request.session['userid'])
    granted_wishes = Wish.objects.filter(granted=True)
    context = {
        "user": user[0],
        "wish": Wish.objects.filter(user_wished=User.objects.get(id=user[0].id), granted=False),
        "granted": granted_wishes
    }
    return render(request, "dashboard.html", context)


def login(request):
    errors = {}
    EMAIL_REGEX = re.compile(
        r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if len(request.POST['email']) == "" or not EMAIL_REGEX.match(request.POST['email']):
        errors['email'] = 'Invalid E-Mail'
    if len(request.POST['password']) < 8:
        errors['password'] = 'Password must be at least 8 characters'
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/success')
    for k, v in errors.items():
        messages.error(request, v)
    return render(request, 'index.html')


def logout(request):
    request.session.clear()
    return redirect('/')


def createwish(request):
    if request.session.get('userid') is None:
        return redirect('/')
    user = User.objects.filter(id=request.session['userid'])
    context = {
        "user": user[0],
        "wish": Wish.objects.filter(user_wished=User.objects.get(id=user[0].id))
    }
    return render(request, "new_wish.html", context)


def addwish(request):
    if request.session.get('userid') is None:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    errors = Wish.objects.validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return render(request, 'new_wish.html')
    Wish.objects.create(
        name=request.POST['name'], description=request.POST['description'], granted=False, user_wished=user)
    return redirect('/success')


def removewish(request, id):
    if request.session.get('userid') is None:
        return redirect('/')
    item = Wish.objects.get(id=id)
    item.delete()
    return redirect('/success')


def editwish(request, id):
    if request.session.get('userid') is None:
        return redirect('/')
    item = Wish.objects.get(id=id)
    context = {
        "item": item
    }
    return render(request, 'edit_item.html', context)


def updatewish(request, id):
    if request.session.get('userid') is None:
        return redirect('/')
    item = Wish.objects.get(id=id)
    errors = Wish.objects.validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return render(request, 'edit_item.html')
    item.name = request.POST['name']
    item.description = request.POST['description']
    item.save()
    return redirect('/success')


def grantwish(request, id):
    if request.session.get('userid') is None:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    item = Wish.objects.get(id=id)
    item.granted = True
    item.granted_by = user
    item.save()
    return redirect('/success')


def viewstats(request):
    if request.session.get('userid') is None:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    wish = Wish.objects.filter(
        user_wished=User.objects.get(id=user.id), granted=False)
    granted_wishes = Wish.objects.filter(
        granted=True, user_wished=User.objects.get(id=user.id))
    granted_wishes_total = Wish.objects.filter(
        granted=True)
    granted = granted_wishes
    context = {
        "outstanding": len(wish),
        "fulfilled": len(granted),
        "total_granted": len(granted_wishes_total)
    }
    return render(request, "stats.html", context)
