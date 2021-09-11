from django.contrib import admin
from django.urls import path
from .views import acceptorder, adminorders, authenticateuser, customerwelcomeview, addpizza, adminhomepageview, adminloginview, authenticateadmin, declineorder, deletepizza, homepageview, homepageviewredirect, logoutadmin, placeorder, signupuser, updatepizza, updatepizzaview, userloginview, userlogout, userorders

urlpatterns = [
    path('django/', admin.site.urls),
    path('', homepageview, name = 'homepage'),
    path('home/', homepageviewredirect, name = 'home'),
    path('admin/', adminloginview, name = "adminloginpage"),
    path('adminauthenticate/', authenticateadmin),
    path('admin/homepage/', adminhomepageview, name = 'adminhomepage'),
    path('adminlogout/', logoutadmin),
    path('addpizza/', addpizza),
    path('deletepizza/<int:pizzapk>/', deletepizza),
    path('signupuser/', signupuser),
    path('loginuser/', userloginview, name = 'userloginpage'),
    path('customer/welcome/', customerwelcomeview, name = 'customerhomepage'),
    path('customer/authenticate/', authenticateuser),
    path('userlogout/', userlogout),
    path('placeorder/', placeorder),
    path('userorders/', userorders),
    path('adminorders/',adminorders),
    path('acceptorder/<int:orderpk>/', acceptorder),
    path('declineorder/<int:orderpk>/', declineorder),
    path('updatepizza/<int:pizzapk>/', updatepizzaview, name='updatepizzaview'),
    path('updatepizza/<int:pizzapk>/update/', updatepizza),
]