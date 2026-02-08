#This is the python file that i will be pushing into Github
# I will be making a Calorie Tracking Application - A simple app which will track daily calorie intake.
#This will be against my BMR, wanted to do TDEE but it is alot more complicated :/

import json #This will allow me to save and load data from files
import os #This will chceck if files exist
from datetime import datetime #This will timestamp when someone has inputted their calories
import tkinter as tk
from tkinter import ttk

datafile = "calorie_data.json"

#This will let me add to the BMR of how active someone is
activity_multipliers = {
    1 : ("little to no excersize",1.2), #Sedentary
    2 : ("lightly active (1-3 days/week)", 1.375), #Lightly active
    3 : ("Moderately active (exercise 3-5 days/week)", 1.55), #moderately active
    4 : ("Very active (exercise 6-7 days/week)",1.725), #very active
    5 : ("Exrtremely active( physical job or training twice/day",1.9) #extremely active
}

def calculate_bmr(weight, height, age, gender, activity_level):
    
    """
    As stated in my projects section of github, i will be calculating BMR with the Mifflin-St Jeor
    Equation. This will then be multiplied by activity_multiplier which is dependent on what the user chooses
    Parameters:
    weight: float
        weight in kilograms
    height: float
        height in cm
    age: int
        age in years
    gender: string
        'm' for male, 'f' for female
    activity_level: int
        Numbered 1-5 which will represent activity level

    This will return:
    float: Daily calorie intake (BMR * activity level)

    Calculation to find out BMR:  

    Men: BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age(years) + 5
    Women: BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age(years) - 161

    """

    if gender.lower() == 'm':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    #Getting the activity multiplier from the dictionary we created
    activity_multiplier = activity_multipliers[activity_level][1]

    #Calculating the daily calories by multipying bmr with activity multipler
    daily_calories = bmr * activity_multiplier

    #rounding the calories to a whole number/integer as following the goal
    return round(daily_calories)

#SAVING DATA TO A FILE

def save_data(user_data):
    with open(datafile, 'w') as file:
        json.dump(user_data, file, indent=4)

    print("The Data has been saved!")

#Loading the data from a file. So that it can save data.

def load_data():
    if os.path.exists(datafile):
        with open(datafile, 'r') as file:
            return json.load(file)
    else:
        return None
 ###I want to add a GUI at this point in time so i think it will be good to add now than later

def get_user_input():

    print("Calorie Calculator")
    print("\nLets set up your profile to calculate your calorie intake needs.\n")

    #Find Weight
    while True:
        try:
            weight = float(input("Enter your weight (kg): "))
            if weight > 0:
                break 
            print("Weight must be positive, try again!")
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            height = float(input("Please enter your height (cm): "))
            if height > 0:
                break
            else:
                print("Height must be positive, please try again.")
        except ValueError:
            print("Please enter a valid number ")

    while True:
        try:
            age = int(input("Please enter your height"))
            if age > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    while True:
            gender = input("please enter your gender (m/f): ").lower()
            if gender == ['m','f']:
                break
            else:
                print("Please enter 'm' for male and 'f' for female.")

            