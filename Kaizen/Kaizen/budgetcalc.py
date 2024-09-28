def monthly_budget(income,expenses):
    transactions = {}
    savings = income * .3
    essential = income * .5
    spending = income - (savings + essential)

    if expenses > essential:
        essential += spending
        spending = 0    
    difference = expenses - essential
    transactions = {
    'savings' : savings,
    'essential' : essential,
    'spending': spending,
    'difference': difference

    }
    return transactions
