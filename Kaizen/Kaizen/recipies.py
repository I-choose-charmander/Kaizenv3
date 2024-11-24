from django.db.models import F, FloatField
from django.db.models.functions import Cast
from django.db.models import Q
import pandas as pd
from .models import DailyTotal

def search_near_match(value, threshold=0.8):
    results = Recipe.objects.annotate(
        similarity=ExpressionWrapper(
            F('protein') * threshold,
            output_field=FloatField()
        )
    ).filter(Q(similarity__lte=F('protein') * 1.2) & Q(similarity__gte=F('protein') * 0.8))
    
    return results


def mealChoice(meal):
# Load your CSV file
    path = r'C:\Users\faiin\OneDrive\Documents\Kaizen App\Kaizen\Kaizen\All_Diets.csv'
    df = pd.read_csv(path,header=0)

    # Define the value to match
    match_value = meal
    # Retrieve rows that match the value
    matching_rows = df[df['Diet_type'] == match_value]


    return matching_rows

def filtered_meals(meals,calories,protien,carb,fat):
    """Filters a list of dictionaries based on 3 input parameters."""

    filtered_data = []
    for item in meals:
        if item['Calories'] == calories and item['Protien'] == protien and item['Carbohydrates'] == carb and item['Fats'] == fat:
            filtered_data.append(item)
        elif item['Protien'] == protien and item['Carbohydrates'] == carb and item['Fats'] == fat:
            filtered_data.append(item)
        elif item['Carbohydrates'] == carb and item['Fats'] == fat:
            filtered_data.append(item)
        elif item['Protien'] == protien and item['Fats'] == fat:
            filtered_data.append(item)
        elif item['Carbohydrates'] == carb and item['Protien'] == protien:
            filtered_data.append(item)
        elif item['Calories'] == calories:
            filtered_data.append(item)
        elif item['Protien'] == protien:
            filtered_data.append(item)
        elif item['Carbohydrates'] == carb:
            filtered_data.append(item)
        elif item['Fats'] == fat:
            filtered_data.append(item)
        else:
            item = 'Could not find anything to match'
            filtered_data.append(item)
    return filtered_data