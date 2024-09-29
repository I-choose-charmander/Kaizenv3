from django.db import models 
from django.contrib.auth.models import User 
  
#Create mode for Expense 
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    income = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

class BMR(models.Model):
    SEX_CHOICES = [('Male','Male'),('Female','Female')]
    ACTIVITY_CHOICES = [(1.2,'Sedentary'), (1.375, 'Light Activity'),(1.55, 'Moderate Activity'), (1.725,'Very Active'),(1.90,'Super Activity')]
    GOAL_CHOICES = [("Muscle Gain", 'Muscle Gain'), ("Maintenace", "Maintenance"), ("Fat Loss", "Fat Loss")]


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    age = models.IntegerField()
    feet = models.IntegerField()
    inches = models.IntegerField()
    weight = models.IntegerField()
    sex = models.CharField(max_length=6,choices=SEX_CHOICES)
    activity_level = models.FloatField(choices=ACTIVITY_CHOICES)
    goal = models.CharField(max_length=11,choices=GOAL_CHOICES)
    tdee = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    carb = models.FloatField(null=True, blank=True)
    save_to_profile = models.BooleanField(default=False)

class StockData(models.Model):
    data = models.TextField(null=True)
    ticker = models.TextField(null=True)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30,blank=True)
    birth_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.user.username
    
class RunningMacro(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    tdee_intake = models.FloatField(null=True, blank=True)
    protein_intake = models.FloatField(null=True,blank=True)
    carb_intake = models.FloatField(null=True,blank=True)
    fat_intake = models.FloatField(null=True, blank=True)
    
        
class DailyTotals(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_protein_intake = models.FloatField(default=0)
    total_carb_intake = models.FloatField(default=0)
    total_fat_intake = models.FloatField(default=0)
    total_tdee_intake = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user} - {self.date}"