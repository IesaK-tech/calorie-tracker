#This is the python file that i will be pushing into Github
# I will be making a Calorie Tracking Application - A simple app which will track daily calorie intake.

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
    5 : ("Exrtremely active (physical job or training twice/day)",1.9) #extremely active
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
        if os.path.getsize(datafile) == 0:
            return None
        with open(datafile, 'r') as file:
            return json.load(file)
    else:
        return None

def get_user_input():

    print("Calorie Calculator")
    print("\nLets set up your profile to calculate your calorie intake needs.\n")

    #Find Weight
    while True:
        try:
            weight = float(input("Enter your weight (kg): "))
            if weight > 0:
                break
            else: 
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
            age = int(input("Please enter your age: "))
            if age > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    while True:
            gender = input("please enter your gender (m/f): ").lower()
            if gender in ['m','f']:
                break
            else:
                print("Please enter 'm' for male and 'f' for female.")
    print("\n" + "="*50)
    print("              ACTIVITY LEVELS")
    print("="*50 + "\n")

    while True:
        try:
            activity_level = int(input("\n\n 1: Little to no excersize \n 2: Lightly active (1-3 days/week) \n 3: Moderately active (excersize 3-5 times a week) \n 4: Very active (excersize 6-7 times a week) \n 5: Extremely active (Physical job or training twice/day) \n\n Select your activity level (1-5): "))
            if activity_level in activity_multipliers:
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.") 

    return {
        "weight" : weight,
        "height" : height,
        "age" : age,
        "gender" : gender,
        "activity_level" : activity_level
    }

def display_results(user_data,daily_calories):
    """
    this will display it nicely for the user
    """

    print("\n" + "="*50)
    print("           YOUR DAILY CALORIE NEEDS")
    print("="*50)
    print(f"\nBased on your profile:")
    print(f"  Weight: {user_data['weight']} kg")
    print(f"  Height: {user_data['height']} cm")
    print(f"  Age: {user_data['age']} years")
    print(f"  Gender: {'Male' if user_data['gender'] == 'm' else 'Female'}")
    print(f"  Activity: {activity_multipliers[user_data['activity_level']][0]}")
    print(f"     \nYour daily calorie target: {daily_calories} calories")

#I want to add a calorie logging section, which is what i will do here
#I will first create a timestamp function which takes the time and date of when the calories are logged

def get_todays_key():
        return datetime.now().strftime("%d-%m-%Y")

#This will return how many calories the user has logged today.
#Logs are stored in userdata['log'] as a dictionary of {date : entries}
#Each entry is displayed as {'descripiton : stri, 'calories':int, 'time': str}
def get_calories_consumed(user_data):
    today =get_todays_key()
    log = user_data.get("log",{})
    todays_entries = log.get(today,[])
    return  sum(entry["calories"] for entry in todays_entries)

def display_calorie_summary(user_data):
    #This will print todays progress
    today = get_todays_key()
    daily_target = user_data["daily_calories"]
    consumed = get_calories_consumed(user_data)
    remaining = daily_target - consumed

    log = user_data.get("log", {})
    todays_entries = log.get(today, [])

    print(f"\nCALORIE LOG - {today}")

    if todays_entries:
        print("\nWhat you have logged today:")
        for i, entry in enumerate(todays_entries, 1):
            print(f"   {i}. {entry['description']} - {entry['calories']} cal ({entry['time']})")
    else:
        print("\n Nothing has been logged yet today.")

    print(f"\nDaily target : {daily_target} calories")
    print(f"Consumed : {consumed} calories")

    if remaining >=0:
        print(f"Remaining : {remaining} calories")
    else:
        print(f"Over by : {abs(remaining)} calories")

def log_calories(user_data):

    today = get_todays_key()

    if "log" not in user_data:
        user_data["log"] = {}
    if today not in user_data["log"]:
        user_data["log"][today] = []

    print("\nLOG YOUR CALORIES")

    valid_meals = ['breakfast', 'lunch', 'dinner', 'snack']

    while True:
        while True:
            description = input(
                "\nWhat was this meal? (Breakfast, Lunch, Dinner, Snack): "
            ).lower().strip()

            if description in valid_meals:
                description = description.capitalize()
                break
            else:
                print("Please choose between Breakfast, Lunch, Dinner or Snack.")
        while True:
            try:
                calories = int(input(f"How many calories in your '{description}'? "))
                if calories >= 0:
                    break
                else:
                    print("Calories cannot be negative.")
            except ValueError:
                print("Please enter a whole number.")

        timestamp = datetime.now().strftime("%H:%M")
        entry = {
            "description": description,
            "calories": calories,
            "time": timestamp
        }

        user_data["log"][today].append(entry)

        consumed = get_calories_consumed(user_data)
        remaining = user_data["daily_calories"] - consumed

        print(f"\nAdded! You have consumed {consumed} calories today.")

        if remaining >= 0:
            print(f"{remaining} calories remaining.")
        else:
            print(f"You're {abs(remaining)} calories over your target!")

        while True:
            add_more = input("\nWould you like to add another entry? (y/n): ").lower().strip()

            if add_more in ['y', 'n']:
                break
            else:
                print("Please input either 'y' or 'n'.")

        if add_more == 'n':
            save_data(user_data)
            break

        save_data(user_data)
        display_calorie_summary(user_data)

def edit_calories(user_data):
    """
    This lets me edit the calories by fetching the data that i have logged today and then letting me relog the calories.
    """
    today = get_todays_key()
    log = user_data.get("log",{})
    todays_entries = log.get(today, [])

    if not todays_entries:
        print("\n Please log something so that it can be editable!")
        return
    
    print("\n" + "=" * 50)
    print("              EDIT TODAYS ENTRIES")
    print("=" * 50)
    print("          What you have logged today:")
    for i, entry in enumerate(todays_entries, 1):
        print(f"   {i}. {entry['description']} - {entry['calories']} cal ({entry['time']})")
    print("="*50)

    while True:
        try:
            entry_num = int(input("\nEnter the number of the entry to edit (0 to cancel): "))
            if entry_num == 0:
                print("Edit cancelled.")
                return
            if 1 <= entry_num <= len(todays_entries):
                break
            else:
                print(f"Please enter a number between 1 and {len(todays_entries)}.")
        except ValueError:
            print("Please enter a valid number.")

    #Allows me to edit entries
    entry_index = entry_num - 1
    entry = todays_entries[entry_index]

    print(f"\n  Selected: {entry['description']} - {entry['calories']} cal")
    print("\n  What would you like to do?")
    print("    0 - Cancel")
    print("    1 - Edit calories")
    print("    2 - Delete this entry")

    while True:
        action = input("\n Enter your choice: ").strip()

        if action == '1':
            while True:
                try:
                    new_calories = int(input(f"\nCurrent calories: {entry['calories']}\nNew Calories:"))
                    if  new_calories >= 0:
                        entry['calories'] = new_calories
                        print('Calories Updated!')
                        return calorie_menu
                    else:
                        print('Cannot accept negative Calories, please enter a positive number.')
                except ValueError:
                    print("Please enter a valid number.")
                    return entry_num
        elif action == '2':
            confirm = input(f"\nDelete '{entry['description']}'? (y/n): ").lower()
            if confirm == 'y':
                todays_entries.pop(entry_index)
                print('Entry Deleted!')
                save_data(user_data)
                display_calorie_summary(user_data)
                return calorie_menu
            else:
                print('Deletion canelled.')
                return entry_num
        elif action == '0':
            print('Edit Cancelled.')
            return entry_num
        else:
            print("Invalid choice. Choose between 0,1 and 2.")
            return edit_calories(user_data)
    
def calorie_menu(user_data):
    """
    The main menu will be shown after a profile is loaded and the options will be:
    L - Log calories for today
    V - View todays summary
    E - Edit Todays Entries
    Q - Quit (giving a message too)
    """
    while True:
        print("\n" + "="*50)
        print("                   MAIN MENU")
        print("="*50)
        print("  \n        L - Log calories")
        print("        V - View calories")
        print("        E - Edit calories")
        print("        Q - Quit")
        choice = input("\nEnter your choice: ").lower().strip()

        if choice == 'l':
            log_calories(user_data)
        elif choice == 'v':
            display_calorie_summary(user_data)
        elif choice == 'q':
            print("\nGoodbye! Stay on track!\n")
            return
        elif choice == 'e':
            edit_calories(user_data)
        else:
            print(" Invalid option. Please enter L, E or Q.")
def main():
    previous_data = load_data()
    if previous_data:
        print("Previous Data has been found")
        print(f"Previous result: {previous_data.get('daily_calories', 'N/A')} calories")
        while True:
            """"
            With this next part of code (the while true statement), i was having difficulties looping my logic as in the terminal, when i would put anything but y or n, it would say choose between y or n
            it would terminate the session right after, AI had told me to use a while true statement and taught me why it works, because of this i was able to implement this logic throughout my programme and also learn effectively too
            """
                
            use_previous = input("\nWould you like to use previous data (y/n): ").lower().strip()

            if use_previous == 'y':
                user_data = previous_data
                daily_calories = user_data['daily_calories']
                break

            elif use_previous == 'n':
                user_data = get_user_input()
                daily_calories = calculate_bmr(
                    user_data['weight'],
                    user_data['height'],
                    user_data['age'],
                    user_data['gender'],
                    user_data['activity_level']
                )
                user_data['daily_calories'] = daily_calories
                break

            else:
                print("Please choose between 'y' or 'n'.")
        consumed = get_calories_consumed(user_data)
        if consumed > 0:

            print (f"\nWelcome back! You've already logged {consumed} calories")
            display_calorie_summary(user_data)
        else:
            print(f"\nNothing logged yet today. Your target is {daily_calories} calories.")
            """
            On line 307, there was a bug which was causing there to be a problem with the terminal interface, it was showing all the data in a not so tidy way of the users profile, the code before was:
            print(f"\n  Nothing logged yet today. Your target is {user_data['daily_calories']} calories."). I spent alot of time looking for the bug so i asked claude to help me find it, it had found the bug and explained that python
            in some edge cases can cause the system to priont out the whole dictionary reference when its in an f string. Just putting {daily_calories} was enough to fix it. Using claude was beneficial as it helped me understand how Python can
            behave when it comes to niche bugs and different edge cases.
            """        
        calorie_menu(user_data)    
        return
            
    user_data = get_user_input()

    daily_calories = calculate_bmr(
        user_data['weight'],
        user_data['height'],
        user_data['age'],
        user_data['gender'],
        user_data['activity_level']
    )

    user_data['daily_calories'] = daily_calories
    display_results(user_data, daily_calories)
    save_data(user_data)
    calorie_menu(user_data)

if __name__ == "__main__":
    main()
    