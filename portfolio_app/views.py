from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from portfolio_app.models import Donation, Institution


class LandingPageView(View):
    def get(self, request):
        bags = Donation.objects.all().aggregate(Sum("quantity"))
        institutions = Institution.objects.all().order_by("name")
        insts_count = institutions.count()
        ctx = {
            "bags": bags,
            "institutions": institutions,
            "insts_count": insts_count
        }
        return render(request, "index.html", ctx)


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    
    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        # user = authenticate(username=username, password=password)
        user = User.objects.get(username=username)
        if user is not None:
            login(request, user)
            request.session["logged"] = True
            return redirect("/")
        return redirect("/register")
        

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            request.session["logged"] = False
        return redirect("/")


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")
    
    def post(self, request):
        name = request.POST["name"]
        surname = request.POST["surname"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        message = ""
        if password != password2:
            message = "Proszę podać dwa takie same hasła"
            ctx = {
                "name": name,
                "surname": surname,
                "email": email,
                "message": message
            }
            return render(request, "register.html", ctx)
        elif name in ("", None) or surname in ("", None) or email in ("", None) or password in ("", None):
            message = "Proszę wypełnić wszystkie pola"
            ctx = {
                "name": name,
                "surname": surname,
                "email": email,
                "message": message
            }
            return render(request, "register.html", ctx)
        else:
            user = User.objects.create(password=password, username=email, first_name=name, last_name=surname)
            message = f"Dodano nowego użytkownika {user.first_name} {user.last_name}. Proszę się zalogować."
            ctx = {
                "message": message
            }
            return render(request, "login.html", ctx)


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")