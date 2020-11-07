"""portfolio_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from portfolio_app.views import LandingPageView, LoginView, LogoutView, RegisterView
<<<<<<< HEAD
from portfolio_app.views import Step1View
=======
from portfolio_app.views import Step1View, Step2View, Step3View, Step4View, Step5View
>>>>>>> parent of 5cbae01... WRONG TURN!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name="register"),
<<<<<<< HEAD
    path('step1/', Step1View.as_view(), name="step1")
=======
    path('step1/', Step1View.as_view(), name="step1"),
    path('step2/', Step2View.as_view(), name="step2"),
    path('step3/', Step3View.as_view(), name="step3"),
    path('step4/', Step4View.as_view(), name="step4"),
    path('step5/', Step5View.as_view(), name="step5")
>>>>>>> parent of 5cbae01... WRONG TURN!
]
