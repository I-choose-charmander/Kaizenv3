from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from dotenv import load_dotenv
from .models import Expense,StockData,Profile,BMR,RunningMacro,DailyTotal
from .forms import BMRForm,BudgetForm,ExpenseForm,StockForm,ProfileForm,FoodForm,MacroIntakeForm
from .macrocalc import calculate_bmr,calculate_tdee, calculate_macros
from .budgetcalc import monthly_budget


import requests
import json
import os
from datetime import date

load_dotenv()




def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def get_macro_values(request):
    if request.method == "POST":
        form = BMRForm(request.POST)
        if form.is_valid():
            bmr_instance = form.save(commit=False)
            bmr_instance.user = request.user

            weight = bmr_instance.weight
            feet = bmr_instance.feet
            age = bmr_instance.age
            inches = bmr_instance.inches
            sex = bmr_instance.sex
            activity_level = bmr_instance.activity_level
            goal = bmr_instance.goal

            bmr = calculate_bmr(weight, feet, inches, age, sex)
            calories = calculate_tdee(bmr, activity_level, goal)
            macros = calculate_macros(calories, weight)

            tdee = round(calories)
            protein = round(macros['Protein'])
            carb = round(macros['Carb'])
            fat = round(macros['Fat'])

            bmr_instance.tdee = tdee
            bmr_instance.protein = protein
            bmr_instance.carb = carb
            bmr_instance.fat = fat

            user_bmr_data = {
                'tdee': tdee,
                'protein': protein,
                'carb': carb,
                'fat': fat
            }

            # Check if there is an existing BMR instance for the user
            existing_bmr = BMR.objects.filter(user=request.user).order_by('-id').first()
            if existing_bmr and bmr_instance.save_to_profile:
                # Overwrite the existing instance
                existing_bmr.age = bmr_instance.age
                existing_bmr.feet = bmr_instance.feet
                existing_bmr.inches = bmr_instance.inches
                existing_bmr.weight = bmr_instance.weight
                existing_bmr.sex = bmr_instance.sex
                existing_bmr.activity_level = bmr_instance.activity_level
                existing_bmr.goal = bmr_instance.goal
                existing_bmr.tdee = bmr_instance.tdee
                existing_bmr.protein = bmr_instance.protein
                existing_bmr.carb = bmr_instance.carb
                existing_bmr.fat = bmr_instance.fat
                existing_bmr.save()
            else:
                bmr_instance.save()

            return render(request, 'macro_results.html', {'user_bmr_data': user_bmr_data})
    else:
        form = BMRForm()
    
    return render(request, 'macro.html', {'form': form})

@login_required(login_url='/login/')
def food_intake(request):
    if request.method == 'POST':
        form = MacroIntakeForm(request.POST)
        if form.is_valid():
            user_intake = form.save(commit=False)
            user_intake.user = request.user
            user_intake.save()
            return redirect('food')
    else:
        form = MacroIntakeForm()
            
    queryset = RunningMacro.objects.filter(user=request.user, date=date.today()).all()
    
    total_p = total_c = total_f = total_tdee = 0

    if queryset.exists():

        total_p = sum(rm.protein_intake for rm in queryset)
        total_c = sum(rm.carb_intake for rm in queryset)
        total_f = sum(rm.fat_intake for rm in queryset)
        total_tdee = sum(rm.tdee_intake for rm in queryset)
    
    daily,create  = DailyTotal.objects.get_or_create(user=request.user,date=date.today())
    daily.total_protein_intake = total_p
    daily.total_carb_intake = total_c
    daily.total_fat_intake = total_f
    daily.total_tdee_intake = total_tdee
    daily.save()

    total = {
    'tdee': total_tdee,
    'protein': total_p,
    'carb': total_c,
    'fat': total_f
    }
    context = {'data': total, 'query':queryset, 'form':form}    
    return render(request, 'food.html', context)

@login_required(login_url='/login/')
def delete_meal(request, id):
    queryset = RunningMacro.objects.get(user=request.user, id=id)
    queryset.delete()
    return redirect('food')

@login_required(login_url='/login/')
def update_meal(request, id):
    queryset = RunningMacro.objects.get(user=request.user, id=id)

    if request.method == 'POST':
        form = MacroIntakeForm(request.POST)
        if form.is_valid():
            tdee_intake = form.cleaned_data['tdee_intake']
            protein_intake = form.cleaned_data['protein_intake']
            carb_intake = form.cleaned_data['carb_intake']
            fat_intake = form.cleaned_data['fat_intake']

            queryset.tdee_intake = tdee_intake
            queryset.protein_intake = protein_intake
            queryset.carb_intake = carb_intake
            queryset.fat_intake = fat_intake
            queryset.save()
        return redirect('food')
    else:
        form = MacroIntakeForm()
    context = {'form':form}
    return render(request,'update_meal.html', context)

@login_required(login_url='/login/')   
def daily_totals_view(request):
    # Get or create the DailyTotals for the current date
    daily,created = DailyTotal.objects.get_or_create(user=request.user, date=date.today())
    
    # If created, it means it's a new day and totals are already set to zero by default
    if created:
        daily.total_protein_intake = 0
        daily.total_carb_intake = 0
        daily.total_fat_intake = 0
        daily.total_tdee_intake = 0
        daily.save()

    existing_bmr = BMR.objects.filter(user=request.user).first()
    
    remaining_tdee = existing_bmr.tdee - daily.total_tdee_intake
    remaining_protein = existing_bmr.protein - daily.total_protein_intake
    remaining_carb = existing_bmr.carb - daily.total_carb_intake
    remaining_fat = existing_bmr.fat - daily.total_fat_intake


    total = {
            'tdee': remaining_tdee,
            'protein': remaining_protein,
            'carb':remaining_carb,
            'fat': remaining_fat,
            'date':daily.date
            }
    context = {'data':total, 'query':existing_bmr,'daily':daily}
    
    return render(request, 'running_macros.html', context)

def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username).first
            if not user_obj:
                messages.error(request, 'Username not found')
                return redirect('/')
            user_auth = authenticate(username=username, password=password)
            if user_auth: 
                login(request, user_auth)
                return redirect('home')
            messages.error(request,'Wrong Password')
            return redirect('/login/')
        except Exception as e:
            messages.error(request, 'Something went wrong')
            return redirect('/login/')   
    return render(request,'login.html')

@login_required(login_url='/login')
def profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        user_data = {
            'bio': user_profile.bio,
            'location': user_profile.location,
            'birth_date': user_profile.birth_date
        
        }
    except Profile.DoesNotExist:
        user_data = {
            'bio': '',
            'location': '',
            'birth_date': '',
        }
    return render(request, 'profile.html',{'user_data':user_data})

@login_required(login_url='/login')
def update_profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('profile')  # Redirect to the profile view after saving
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'update_profile.html', {'form': form})

def register_page(request):
    if request.method == "POST":
        try:

            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request,"Username is taken")
                return redirect('/register/')
            user_obj = User.objects.create_user(username=username,email=email,password=password)
            user_obj.save()
            messages.success(request,"Account has been created.")
            return redirect('/login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register')
    return render(request, 'register.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def pdf(request):
    if request.method == 'POST': 
        data = request.POST 
        income = int(data.get('income')) 
        name = data.get('name') 
        price = int(data.get('price', 0))
  
        Expense.objects.create( 
            income=income, 
            name=name, 
            price=price, 
        ) 
        return redirect('pdf') 
  
    queryset = Expense.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter( 
            name__icontains=request.GET.get('search')) 
  
    # Calculate the total sum 
    total_sum = sum(expense.price for expense in queryset) 
    # Get the username 
    username = request.user.username

    
  
    context = {'expenses': queryset, 'total_sum': total_sum, 'username':username} 
    return render(request, 'pdf.html', context)

@login_required(login_url='/login')
def macro_results(request):
    user_bmr = BMR.objects.filter(user=request.user).order_by('-id').first()
    if user_bmr:
        user_bmr_data = {
            'tdee': user_bmr.tdee,
            'protein': user_bmr.protein,
            'carb': user_bmr.carb,
            'fat': user_bmr.fat
        }
    else:
        user_bmr_data = {
            'tdee': '',
            'protein': '',
            'carb': '',
            'fat': ''
        }
         
    return render(request, 'macro_results.html', {'user_bmr_data': user_bmr_data})

def get_api_data(request):
    query = request.POST.get('query')
    api_key = os.getenv('API_KEY_NIX')
    app_id = os.getenv('APP_ID_NIX')
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers={
            'Content-Type': 'application/json',
            'x-app-id': app_id,
            'x-app-key': api_key,
                }
    search = {
         'query' : query 
    }

    response = requests.post(url,headers=headers,data=json.dumps(search))
    if response.status_code == 200:
        data2 = response.json()
        for item in data2['foods']:
             #data.append(item)
             
             serving = item['serving_unit']
             grams = item['serving_weight_grams']
             calories_of_food = item['nf_calories']
             fats = item['nf_total_fat']
             carbo = item['nf_total_carbohydrate']
             protien = item['nf_protein']

             data = {'Food': query, 'Serving_size': serving, 'Grams':grams,
                     'Calories': calories_of_food, 'Protien':protien, "Carbohydrates":carbo, 'Fats':fats}

             
        return render(request, 'food_api.html', {'data': data})
    error= f'Request failed with status code {response.status_code}'
    form = FoodForm()
    return render(request, 'food.html', {'error': error,'form':form})

def food_result(request):
    return render(request,'food_api.html')
