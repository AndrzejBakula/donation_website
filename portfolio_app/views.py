from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from portfolio_app.models import Donation, Institution, Category


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
        user = authenticate(username=username, password=password)
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
            user = User.objects.create(username=email, first_name=name, last_name=surname)
            user.set_password(password)
            user.save()
            message = f"Dodano nowego użytkownika {user.first_name} {user.last_name}. Proszę się zalogować."
            ctx = {
                "message": message
            }
            return render(request, "login.html", ctx)

CATEGORIES = []
BAGS = 0
ORGANIZATION = None

class Step1View(View):
    def get(self, request):
        if_user = request.user
        is_user_logged = if_user.is_authenticated
        if is_user_logged == True:
            cats = Category.objects.all().order_by("name")
            return render(request, "step1.html", {"cats": cats})
        return redirect("/login")
    
    def post(self, request):
        checked = request.POST.getlist("categories")
        if len(checked) != 0:
            categories = []
            for i in checked:
                categories.append(Category.objects.get(id=int(i)))
            CATEGORIES = categories
            cats = Category.objects.all().order_by("name")
            return render(request, "step1.html", {"accepted": "accepted", "cats": cats})
        return redirect("/step1")


class Step2View(View):
    def get(self, request):
        orgs = Institution.objects.all().order_by("name")
        return render(request, "step3.html", {"orgs": orgs})
    
    def post(self, request):
        bags = request.POST.get("bags")
        if bags != 0:
            BAGS = int(bags)
            return render(request, "step3.html")
        return redirect("/step2")


class Step3View(View):
    def get(self, request):
        orgs = Institution.objects.all().order_by("name")
        return render(request, "step3.html", {"orgs": orgs})
    
    def post(self, request):
        organization = request.POST.get("organization")
        if organization != None:
            ORGANIZATION = organization
            return render(request, "step4.html")
        return redirect("/step3")