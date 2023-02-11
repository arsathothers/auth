from django.shortcuts import render,HttpResponseRedirect,redirect
from basic_app.forms import UserForm, UserProfileInfoForm

# Imports used to work with login page
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout

# below is the demo special page on which we have mentioned we need login to view
def special(request):
    return HttpResponse("You are logged in, Nice")

# Create your views here.
# Rendered login page below
def index(request):
    return render(request, "basic_app/index.html")

# Rendered logout page
# Here we have used @login_required, so django will require login to run this function
@login_required
def user_logout(request):
    # logout(request is the django build in function)
    logout(request)
    # below we are redirecting to home page once the user has logged out and the log out has taken care by logout(request)
    return redirect("basic_app:index")
# below line will also work if uncommented and this will redirect to google.com and home page i.e. index page
#     return redirect("https://google.com")
#     return HttpResponseRedirect("index")


# Written code for register page and rendered registration page
def register(request):
    registered = False

    # If the user filled the form and post datas then have validating forms and it's datas
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # .is_valid is the prebuild methods for form we dont write it separtely anywhere. Here we are checking is the both forms are valid or not?
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # below we have hasing the password using .set_password and to do this we have added password hashers section in settings.py
            user.set_password(user.password)
            user.save()
            # for now have set commit as false, this will prevent getting errors due to data collision
            # for now we are not committing changes in db, checking the profile form is profile uploaded then save else no
            profile = profile_form.save(commit=False)

            # below we have set one-to-one relationship with user model from below the user on right hand side is model and it's defined under model
            # Here we have imported User module from django.contrib.auth.model and it will take care users datas
            # also on below profile is the data which we received from the user
            profile.user = user
            # Saving profile picture if they upload
            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            # changing the variable = True if everything is fine in form
            registered = True
        # else throwing error
        else:
            print(user_form.errors, profile_form.errors)
    # if the user not posting any data then setting the variable user_form = UserForm() & profile_form = UserProfileInfoForm(), this will use to display the registration page
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    #     Below we are passing context as dictionary but here not mentioned as context = variable instead passing directly as dict and the variable registered we have using within this function. so passing it
    return render(request, "basic_app/registration.html",
                  {"user_form": user_form,
                   "profile_form" : profile_form,
                   "registered": registered})

def user_login(request):
    print("Hellow main")
    if request.method == 'POST':
        print("Hellow")
        # below we are getting the username from the html page named as username
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        # Using django build in user authentication
        user = authenticate(username=username, password=password)
        # checking the user passed the authentication and logged in, active
        if user:

            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse("basic_app:index"))

            else:
                return HttpResponseRedirect("ACCOUNT NOT ACTIVE")

        else:
            print("Someone try to login gas failed")
            print("username: {} and password {}". format(username,password))
            return HttpResponseRedirect("invalid login details supplied")

    # if user didn't submit anything then
    else:
        return render(request, "basic_app/login.html", {})