from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, RegisterForm

from user.models import User


User = get_user_model()


def index(request):
    user = User.objects.filter(id=request.user.id).first()
    username = user.username if user else "Anonymous User!"
    print("Logged in?", request.user.is_authenticated)
    if request.user.is_authenticated is False:
        username = "Anonymous User!"
    print(username)
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
         #   remember_me = form.cleaned_data.get("remember_me")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                print("Check eamil before")
                user = User.objects.get(username=username)
                print("Check eamil after")

            except User.DoesNotExist:
                print("User DoesNot Exist")
                pass
            else:
                if user.check_password(raw_password):
                    print("Login Check Success")
                    msg = None
                    login(request, user)
                    is_ok = True
                    
                    return render(request, "index.html", {"form": form})
                

                    # if not remember_me:
                    #     request.session.set_expiry(0)				
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요
    logout(request)					
    return HttpResponseRedirect("/")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
@login_required
def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    page = int(request.GET.get("p", 1))
    users = User.objects.all().order_by("-id")

    # TODO: 9. user 목록은 pagination이 되게 해주세요
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "users.html", {"users": users})
