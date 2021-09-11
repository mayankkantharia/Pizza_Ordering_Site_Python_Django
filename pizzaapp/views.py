from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomerModel, OrderModel, PizzaModel

def adminloginview(request):
    return render(request, "pizzaapp/adminlogin.html")

def authenticateadmin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)    
    # user exists
    if user is not None and user.username == "admin":
        login(request, user)
        return redirect('adminhomepage')          
    # user doesn't exists
    if user is None:
        messages.add_message(request,messages.ERROR,"Invalid Credentials")
        return redirect('adminloginpage')
        
def adminhomepageview(request):
    if not request.user.is_authenticated:
        return redirect('adminloginpage')
    context = {'pizzas' : PizzaModel.objects.all()}
    return render(request, "pizzaapp/adminhomepage.html",context)

def logoutadmin(request):
    logout(request)
    return redirect('adminloginpage')

def addpizza(request):
    # code to add pizza
    name = request.POST['pizza']
    price = request.POST['price']
    if name == '' or price == '':
        messages.add_message(request, messages.ERROR, "Please Enter Details")
    else:
        PizzaModel(name = name, price = price).save()
    return redirect('adminhomepage')

def deletepizza(request, pizzapk):
    PizzaModel.objects.filter(id = pizzapk).delete()
    return redirect('adminhomepage')

def updatepizza(request, pizzapk):
    new_entered_pizza = request.POST['pizzz_name_update']
    new_entered_price = request.POST['pizzz_price_update']
    if new_entered_pizza == '' or new_entered_price == '':
        messages.add_message(request, messages.ERROR, "Enter Details")
        s = '/updatepizza/' + str(pizzapk) + '/'
        return redirect(s) 
    else:
        newpizza = PizzaModel.objects.filter(id = pizzapk)[0]
        newpizza.name = new_entered_pizza
        newpizza.price = new_entered_price
        newpizza.save()
        return redirect('adminhomepage')    
    
def updatepizzaview(request, pizzapk):
    # code to view edit field
    context = {'pizzapk': pizzapk}         
    return render(request, "pizzaapp/updatepizza.html", context)

def homepageview(request):
    return render(request,"pizzaapp/homepage.html")

def homepageviewredirect(request):
    return render(request,"pizzaapp/homepage.html")

def signupuser(request):
    username = request.POST['username']
    password = request.POST['password']
    phoneno = request.POST['phoneno']
    address = request.POST['address']
    # if username already exists
    if User.objects.filter(username = username).exists():
        messages.add_message(request, messages.ERROR, "User already exists")
        return redirect('homepage')
    # if user name doesn't exists
    User.objects.create_user(username = username, password = password).save()
    lastobject = len(User.objects.all())-1
    CustomerModel(userid = User.objects.all()[lastobject].id, 
                  username = username, phoneno = phoneno, address = address).save()
    messages.add_message(request, messages.ERROR, "User Created Successfully")
    return redirect('homepage')

def userloginview(request):
    return render(request,"pizzaapp/userlogin.html")

def authenticateuser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)    
    # user exists
    if user is not None:
        login(request, user)
        return redirect('customerhomepage')          
    # user doesn't exists
    if user is None:
        messages.add_message(request,messages.ERROR,"Invalid Credentials")
        return redirect('userloginpage')
    
def customerwelcomeview(request):
    if not request.user.is_authenticated:
        return redirect('userloginpage')    
    username = request.user.username
    context = {'username': username, 'pizzas': PizzaModel.objects.all()}
    return render(request,'pizzaapp/customerwelcome.html',context)

def userlogout(request):
    logout(request)
    return redirect('userloginpage')

def placeorder(request):
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    username = request.user.username
    phoneno = CustomerModel.objects.filter(userid = request.user.id)[0].phoneno
    address = CustomerModel.objects.filter(userid = request.user.id)[0].address
    ordereditems = ""
    for pizza in PizzaModel.objects.all():
        pizzaid = pizza.id
        name = pizza.name
        price = pizza.price
        quantity = request.POST.get(str(pizzaid)," ")
        if str(quantity) != "0" and str(quantity) != " ":
            ordereditems = ordereditems + name + ", price : " + str(int(quantity)*int(price)) + ", quantity : " + quantity + ";"    
    OrderModel(username = username, phoneno = phoneno, address = address, ordereditems = ordereditems).save()
    messages.add_message(request,messages.SUCCESS,'Order placed successfully')     
    return redirect('customerhomepage')

def userorders(request):
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    orders = OrderModel.objects.filter(username = request.user.username)
    context = {'orders': orders}
    return render(request,'pizzaapp/userorders.html', context)

def adminorders(request):
    orders = OrderModel.objects.all()
    context = {'orders': orders}
    return render(request,'pizzaapp/adminorders.html', context)

def acceptorder(request, orderpk):
    order = OrderModel.objects.filter(id = orderpk)[0]
    order.status = "Accepted"
    order.save()
    return redirect(request.META['HTTP_REFERER'])

def declineorder(request, orderpk):
    order = OrderModel.objects.filter(id = orderpk)[0]
    order.status = "Declined"
    order.save()
    return redirect(request.META['HTTP_REFERER'])