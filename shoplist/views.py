from django.shortcuts import render


def index(request):
    return render(
        request,
        'indexNotAuth.html'
    )


def auth(request):
    return render(
        request,
        'login.html'
    )


def authorrecipe(request):
    return render(
        request,
        'authorRecipe.html'
    )


def changepassword(request):
    return render(
        request,
        'password_change_form.html'
    )


def custompage(request):
    return render(
        request,
        'customPage.html'
    )


def favorite(request):
    return render(
        request,
        'favorite.html'
    )


def formchangerecipe(request):
    return render(
        request,
        'formChangeRecipe.html'
    )


def formrecipe(request):
    return render(
        request,
        'formRecipe.html'
    )


def myfollow(request):
    return render(
        request,
        'myFollow.html'
    )


def reg(request):
    return render(
        request,
        'reg.html'
    )


def resetpassword(request):
    return render(
        request,
        'password_reset_form.html'
    )


def shoplist(request):
    return render(
        request,
        'shopList.html'
    )


def singlepage(request):
    return render(
        request,
        'singlePage.html'
    )


def singlepagenotauth(request):
    return render(
        request,
        'singlePageNotAuth.html'
    )
