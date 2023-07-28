from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views.generic.detail import DetailView
from django.contrib.auth import login, authenticate, logout
from .models import Todo,User
from users.forms import SignUpForm, AccountAuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,TodoForm

from django.http import HttpResponse
from django.conf import settings


class UserView(DetailView):
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user

def assign_domain_admin(user):
    if not User.objects.filter(domain=user.domain, is_domain_admin=True).exists():
        user.is_domain_admin = True
        user.save()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            raw_password = form.cleaned_data.get('password1')
            raw_name = form.cleaned_data.get('email')
            
            res = str(raw_name[raw_name.index('@') + 1 : ])
            print(user.email)
            user.domain = res
            user.save()
            print(user.domain)
            user = authenticate(request, email=user.email, password=raw_password)

            if user is not None:
                login(request, user)
            else:
                print("user is not authenticated")
            assign_domain_admin(user)

            if user.is_domain_admin == False:
                user.is_active = False
            
            user.save()
            return redirect('users:profile')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request, *args, **kwargs):
    user = request.user

    mytodo = Todo.objects.all()
    context = {"mytodo":mytodo,
	    "user":user}
    
    if user.is_authenticated: 
        return render(request, "users/profile.html", context)
    

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        print(user.is_active)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            
            if user:
                newcontext = {"mytodo":mytodo,"user":user}
                login(request, user)
                if destination:
                    return redirect(destination)
                return render(request, "users/profile.html", newcontext)
    
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "users/login.html", context)

def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

def logout_view(request):
	logout(request)
	return redirect("home")

@login_required
def createtodo(request):
    if request.method == 'GET':
        user = request.user
        mytodo = Todo.objects.all()
        context = {
              "mytodo":mytodo,
              "form":TodoForm(),
              "user":user
		}
        return render(request, "users/todo.html", context)
    else:
        try:
            form = TodoForm(request.POST)
            if form.is_valid():
                  newtodo = form.save()
                  newtodo.user = request.user
                  newtodo.save()
                #   return redirect('www.facebook.com')

            # newtodo = form.save(commit=False)
            # newtodo.user = request.user
            # newtodo.save()
            return redirect('/accounts/todo')
        except ValueError:
            return render(request, "users/todo.html", {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})
        
def updateTodo(request, pk):
	todo = Todo.objects.get(id=pk)

	form = TodoForm(instance=todo)

	if request.method == 'POST':
		form = TodoForm(request.POST, instance=todo)
		if form.is_valid():
			form.save()
			return redirect('/accounts/todo')

	context = {'form':form}

	return render(request, "users/updateTodo.html", context)




def deleteTodo(request, pk):
	item = Todo.objects.get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('/accounts/todo')

	context = {'item':item}
	return render(request, 'users/delete.html', context)

def index(request):
     return render(request,'users/index.html')