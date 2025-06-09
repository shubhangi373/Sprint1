from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ComplaintForm, UserRegisterForm
from .models import Complaint

@login_required
def dashboard(request):
    if request.user.username == 'kavita':
        # Admin sees all complaints
        complaints = Complaint.objects.all()
    else:
        # Normal users see only their own complaints
        complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'complaints': complaints})

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'register.html')

def is_admin(user):
    return user.is_superuser
   

def home(request):
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        complaints = Complaint.objects.all()
    else:
        complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'complaints': complaints})

@login_required
def submit_complaint(request):
    return render(request, 'complaint_form.html', {'form': form})
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('dashboard')
    else:
        form = ComplaintForm()
    return render(request, 'complaint_form.html', {'form': form})

@user_passes_test(is_admin)
def update_status(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    if request.method == 'POST':
        complaint.status = request.POST['status']
        complaint.save()
        return redirect('dashboard')
    return render(request, 'update_status.html', {'complaint': complaint})
