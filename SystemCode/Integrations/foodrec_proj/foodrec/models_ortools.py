from __future__ import print_function
from ortools.linear_solver import pywraplp

import pandas as pd


# Constants and Global variables
DATA_FoodName_INDEX = -1
DATA_FoodGroup_INDEX = -1
DATA_CarbohydrateAmount_g_INDEX = -1
DATA_EnergyAmount_kcal_INDEX = -1
DATA_ProteinAmount_g_INDEX = -1
DATA_TotalFatAmount_g_INDEX = -1

food_data = None
csv_file = 'Dataset/FoodDatabase.csv'
NUM_FOOD = 50


def readFoodData(csv_file):
    # Reading only the 1st 'NUM_FOOD' rows for now, for the selected columns
    df = pd.read_csv(csv_file)[['FoodName','FoodGroup','CarbohydrateAmount_g','EnergyAmount_kcal','ProteinAmount_g','TotalFatAmount_g']]
    
    # Update the index here for the data arrays to point to different nutrients
    global DATA_FoodName_INDEX, DATA_FoodGroup_INDEX, DATA_CarbohydrateAmount_g_INDEX, \
        DATA_EnergyAmount_kcal_INDEX, DATA_ProteinAmount_g_INDEX, DATA_TotalFatAmount_g_INDEX
    DATA_FoodName_INDEX = 0
    DATA_FoodGroup_INDEX = 1
    DATA_CarbohydrateAmount_g_INDEX = 2
    DATA_EnergyAmount_kcal_INDEX = 3
    DATA_ProteinAmount_g_INDEX = 4
    DATA_TotalFatAmount_g_INDEX = 5

    global food_data
    food_data = df.head(NUM_FOOD).to_numpy()


# This optimizer only takes input parameter as 'EnergyAmount_kcal'
def optimizer1(EnergyAmount_kcal):
    # Create the mip solver with the CBC backend
    solver = pywraplp.Solver('optimizer1',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # Declare the objective function
    objective = solver.Objective()

    # Declare an array to hold the variable value whether the food is selected, which is 0 or 1 for each food
    food = [[]] * len(food_data)
    # The coeficient for the objective function is the amount of calories for the corresponding food
    for i in range(0, len(food_data)):
        food[i] = solver.IntVar(0.0, 1.0, food_data[i][DATA_FoodName_INDEX])
        objective.SetCoefficient(food[i], food_data[i][DATA_EnergyAmount_kcal_INDEX])

    # Minimize the calories
    objective.SetMinimization()

    # Additional contrainst -> within the 90% - 110% of recommended calories
    constraint = solver.Constraint(EnergyAmount_kcal * 0.9, EnergyAmount_kcal * 1.1)
    for i in range(0, len(food_data)):
        constraint.SetCoefficient(food[i], food_data[i][DATA_EnergyAmount_kcal_INDEX])

    # Solve!
    status = solver.Solve()

    foodIndex_result = []

    if status == solver.OPTIMAL:
        print('An optimal solution was found.')
        print('Objective value =', solver.Objective().Value())
        for i in range(0, len(food_data)):
            if food[i].solution_value() > 0:
                foodIndex_result.append(i)
                # print('%s = %f' % (data[i][0], food[i].solution_value()))

    else:  # No optimal solution was found.
        if status == solver.FEASIBLE:
            print('A potentially suboptimal solution was found.')
        else:
            print('The solver could not solve the problem.')

    return foodIndex_result

# Optimizer 2 for KETO optimization
def optimizer_Dennis_1(EnergyAmount_kcal,CarbohydrateAmount_g,ProteinAmount_g,TotalFatAmount_g ):

    # Create the mip solver with the CBC backend
    solver = pywraplp.Solver('optimizer_Dennis_1',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # Declare the objective function
    objective = solver.Objective()

    # Declare an array to hold the variable value whether the food is selected, which is 0 or 1 for each food
    food = [[]] * len(food_data)
    # The coeficient for the objective function is the amount of calories for the corresponding food
    for i in range(0, len(food_data)):
        food[i] = solver.IntVar(0.0, 1.0, food_data[i][DATA_FoodName_INDEX])
        objective.SetCoefficient(food[i], food_data[i][DATA_EnergyAmount_kcal_INDEX])

    # Minimize the calories
    objective.SetMinimization()

    # Constraint0  Calories -> within the 90% - 110% of recommended 
    constraint0 = solver.Constraint(EnergyAmount_kcal * 0.9, EnergyAmount_kcal * 1.1)
    # Constraint1  Carbohydrate -> within the 90% - 110% of recommended 
    constraint1 = solver.Constraint(CarbohydrateAmount_g * 0.1 , CarbohydrateAmount_g * 1000  )
    # Constraint2  Protein -> within the 90% - 110% of recommended 
    constraint2 = solver.Constraint(ProteinAmount_g * 0.1 , ProteinAmount_g * 1000 )
    # Constraint3  Fat -> within the 90% - 110% of recommended 
    constraint3 = solver.Constraint(TotalFatAmount_g * 0.1 , TotalFatAmount_g * 1000 )
    for i in range(0, len(food_data)):
        constraint0.SetCoefficient(food[i], food_data[i][DATA_EnergyAmount_kcal_INDEX])
        constraint1.SetCoefficient(food[i], food_data[i][DATA_CarbohydrateAmount_g_INDEX])
        constraint2.SetCoefficient(food[i], food_data[i][DATA_ProteinAmount_g_INDEX])
        constraint3.SetCoefficient(food[i], food_data[i][DATA_TotalFatAmount_g_INDEX])

    # Solve!
    status = solver.Solve()

    foodIndex_result = []

    if status == solver.OPTIMAL:
        print('An optimal solution was found.')
        print('Objective value =', solver.Objective().Value())
        for i in range(0, len(food_data)):
            if food[i].solution_value() > 0:
                foodIndex_result.append(i)
                # print('%s = %f' % (data[i][0], food[i].solution_value()))

    else:  # No optimal solution was found.
        if status == solver.FEASIBLE:
            print('A potentially suboptimal solution was found.')
        else:
            print('The solver could not solve the problem.')

    return foodIndex_result


def run_optimizer(EnergyAmount_kcal,CarbohydrateAmount_g,ProteinAmount_g,TotalFatAmount_g):
    return optimizer_Dennis_1(EnergyAmount_kcal,CarbohydrateAmount_g,ProteinAmount_g,TotalFatAmount_g )


# For quick testing without Django
def main():
    readFoodData(csv_file)
    foodIndex_result = run_optimizer(EnergyAmount_kcal=500, CarbohydrateAmount_g =1,ProteinAmount_g = 50 , TotalFatAmount_g = 50 )
    for i in foodIndex_result:
        print('%s' % food_data[i][DATA_FoodName_INDEX], end ='' )
        print(' (Calories=%skcal)' % food_data[i][DATA_EnergyAmount_kcal_INDEX], end ='' )
        print(' (Carbo=%sg)' % food_data[i][DATA_CarbohydrateAmount_g_INDEX],end ='')
        print(' (Protein=%sg)' % food_data[i][DATA_ProteinAmount_g_INDEX],end ='')
        print(' (Fat=%sg)' % food_data[i][DATA_TotalFatAmount_g_INDEX])

if __name__ == '__main__':
    main()
