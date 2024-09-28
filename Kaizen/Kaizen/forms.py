from django import forms
from .models import Expense, BMR, StockData, Profile, RunningMacro

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
            'protein_intake',
            'carb_intake',
            'fat_intake',
            'tdee_intake'
                )
        widget = {
            'protein_intake': forms.NumberInput(attrs={'class': 'form-control'}),
            'carb_intake': forms.NumberInput(attrs={'class': 'form-control'}),
            'fat_intake': forms.NumberInput(attrs={'class': 'form-control'}),
            'tdee_intake': forms.NumberInput(attrs={'class': 'form-control'}),
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

class FoodForm(forms.Form):
    query = forms.CharField()