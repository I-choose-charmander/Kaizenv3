
def calculate_bmr(weight, feet, inches, age, sex):
    kg = (weight / 2.2)
    cm = ((feet * 12) + inches) * 2.54


    if sex == 'Male':
        bmr = ((10*kg) + (6.25*cm) - (5.00*float(age)) + 5.00)
        return bmr
    else:
        bmr = (10*(kg) + (6.25*cm) - (5*float(age)) - 161)
        return bmr
    
def calculate_tdee(bmr,activity_level,goal):
    if goal == 'Muscle Gain':
        pre_tdee = bmr * activity_level 
        tdee =  pre_tdee + (pre_tdee * .05)
        return tdee
    elif goal == 'Fat Loss':
        pre_tdee = bmr * activity_level 
        tdee =  pre_tdee - (pre_tdee * .2)
        return tdee
    else:
        return bmr * activity_level

def calculate_macros(tdee, weight):
    protein = weight 
    fat = weight * .4
    carbs = (tdee - (protein * 4 + fat * 9))/4
    macro = {'Protein': protein, 'Fat':fat, "Carb":carbs}
    return macro

