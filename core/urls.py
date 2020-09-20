from django.urls import path
from . import views


app_name = 'core'
urlpatterns = [
    path('', views.Home, name='Home'),
    path('detail/<slug:slug>/', views.TournamentDetail, name='Detail'),
    path('register/<slug:slug>/', views.Register, name='Register'),
    path('payment/<payment_option>/', views.PaymentView, name='Payment'),
    path('cancel/', views.CancelRegisteration, name='Cancel'),
    path('contact/', views.ContactView, name='Contact'),
    path('<slug:slug>/teams/', views.AllTeams, name='Teams'),
    path('cancel-team/', views.CancelTeamRegisteration, name='Cancel-Team'),
    path('accounts/signup/', views.Signup, name='Signup'),
    path('accounts/login/', views.Login, name='Login'),
    path('accounts/logout/', views.Logout, name='Logout'),
]
