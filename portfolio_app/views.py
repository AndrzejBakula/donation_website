from django.shortcuts import render, redirect
from django.http import JsonResponse
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
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session["logged"] = True
            request.session["user_id"] = user.pk
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


class FormView(View):
    def get(self, request):
        if_user = request.user
        is_user_logged = if_user.is_authenticated
        if is_user_logged == True:
            categories = Category.objects.all().order_by("name")
            institutions = Institution.objects.all().order_by("name")
            ctx = {
                "categories": categories,
            }
            return render(request, "form.html", ctx)
        return redirect("/login")
    
    def post(self, request):
        print(request.POST)
        categories = request.POST.getlist("categories")
        institution = request.POST.get("organization")
        institution = Institution.objects.get(pk=int(institution))
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        quantity = request.POST["bags"]
        address = request.POST["address"]
        phone_number = request.POST["phone"]
        city = request.POST["city"]
        zip_code = request.POST["postcode"]
        pick_up_date = request.POST["data"]
        pick_up_time = request.POST["time"]
        pick_up_comment = request.POST["more_info"]

        donation = Donation.objects.create(quantity=quantity, institution=institution, address=address, phone_number=phone_number, city=city, zip_code=zip_code, pick_up_date=pick_up_date, pick_up_time=pick_up_time, pick_up_comment=pick_up_comment)
        donation.categories.add(*categories)
        donation.user = user
        donation.save()
        
        return redirect("/form_confirmation")



def get_institutions_by_categories(request):
    categories = request.GET.get("categories")
    print(categories)
    if categories is None:
        institutions = Institution.objects.all().values()
    else:
        institutions = Institution.objects.filter(categories__in=categories).distinct().values()
    
    institutions_list = list(institutions)
    return JsonResponse(institutions_list, safe=False)


class FormConfirmationView(View):
    def get(self, request):
        return render(request, "form-confirmation.html")


class UserView(View):
    def get(self, request):
        user = request.session["user_id"]
        user = User.objects.get(id=user)
        
        ctx = {
            "user": user
        }
        return render(request, "user.html", ctx)