from django import forms
from .models import Expense, BMR, StockData, Profile, RunningMacro, Food

class BMRForm(forms.ModelForm):
    #save_to_profile = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    class Meta:
        model = BMR
        fields =[
            'age',
            'feet',
            'inches',
            'weight',
            'sex',
            'activity_level',
            'goal',
            'save_to_profile'
        ]

        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'feet': forms.NumberInput(attrs={'class': 'form-control'}),
            'inches': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'activity_level': forms.Select(attrs={'class': 'form-control'}),
            'goal': forms.Select(attrs={'class': 'form-control'})
        }

class MacroIntakeForm(forms.ModelForm):
    
    class Meta:
        model = RunningMacro
        fields = (
            'tdee_intake',
            'protein_intake',
            'carb_intake',
            'fat_intake'
                )
        widget = {
            'tdee_intake': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein_intake': forms.NumberInput(attrs={'class': 'form-control'}),
            'carb_intake': forms.NumberInput(attrs={'class': 'form-control'}),
            'fat_intake': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
class BudgetForm(forms.Form):
    GOAL_CHOICES = [("Monthly Breakdown", "Monthly Breakdown"), ("Emergency Fund", "Emergency Fund"), ("Purchase", "Purchase"),("Build", 'Save/Invest') ]
    income = forms.IntegerField(label="Income")
    expenses = forms.IntegerField(label="Expenses")
    savings = forms.IntegerField(label='Current Savings')
    goal = forms.ChoiceField(choices=GOAL_CHOICES)
    extra = forms.IntegerField(label='Enter a number for you goal', required=False)

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'income', 
            'name',
            'price'
        ]
        widgets = {
            'income': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class StockForm(forms.ModelForm):
    class Meta:
        model = StockData
        fields = [
            'ticker'
        ]
        widget = {
            'ticker': forms.TextInput(attrs={'class':'form-control'}),    
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'location',
            'birth_date'
        ]

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = [
            'food'
        ]
        widget = {
            'food' : forms.CharField()
        }

class CreateUserForm(forms.Form):
    pass

class RecipeForm (forms.Form):
    FOODS_DIETS = [("paleo","Paleo"),("vegan","Vegan"),("keto","Keto"),("mediterranean","Mediterranean")]
    diet = forms.ChoiceField(choices=FOODS_DIETS, required=False)

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()