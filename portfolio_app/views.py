from django.shortcuts import render
from django.db.models import Sum
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


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")