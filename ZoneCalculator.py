from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
from fractions import Fraction

# Manual before running the code
# Step 1: change the service_account_file to company one
# Step 2: Change the ID of three spreadsheets
# Step 3: Change the name of the sheet to sheet1 for all of three spreadsheets


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# If modifying these scopes, delete the file token.pickle.

# Step 1: The ID of the spreadsheets
ingredientSheet_ID = '1VkSVE1wUSWzIL6tL7iz9D4fsSvkgSY7svvwkmLb9_e0'
inputListSheet_ID = '1ecMsdBj8GK1HL2ps-ouV0Zu3fqLD-BYmCylM5KZb_MA'
outputListSheet_ID = '1fV96CIiY57L4Xje0Kr7BLIwt0Gjoyuq1B4-mpIamkVk'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

# Step 2: Access the spreadsheet tab and get the values inside each spreadsheet

input_recipe = sheet.values().get(spreadsheetId=inputListSheet_ID,
                                  range="sheet1!A1:C6").execute()
values_input_recipe = input_recipe.get('values', [])

ingredient_list = sheet.values().get(spreadsheetId=ingredientSheet_ID,
                                     range="sheet1!A1:W6").execute()
values_ingredient_list = ingredient_list.get('values', [])

# Step 3: Write the header for columns of output file

headerList = [["Name", "Zone Blocks", "Needed", "calories", "carbohydrates", "fats", "protein", "sodium", "sugar"]]


# Step 4: Append the inputted units, name of food and zone blocks into array

inputted_units = []
inputted_names = []
inputted_zoneblocks = []

for i in range(1, len(values_input_recipe)):
    inputted_units.append(values_input_recipe[i][2])
    inputted_names.append(values_input_recipe[i][0])
    inputted_zoneblocks.append(values_input_recipe[i][1])

# Step 5: Find the index row of the inputted name of foods

index_inputted_food = []

# Get the number of inputted name of food
foodNameLength = len(inputted_names)

counter = 0

for i, x in enumerate(values_ingredient_list):
    if inputted_names[counter] in x:
        index_inputted_food.append(i)
        counter += 1

# Step 6: Create variables for storing the results

# Store the column of each property inside the ingredient list
calories_column = 9
carbs_column = 10
fats_column = 11
protein_column = 12
sodium_column = 13
sugar_column = 14

gram_column = 2
ml_column = 3
tablespoon_column = 4
teaspoon_column = 5
cups_column = 6
oz_column = 7
pieces_column = 8

# Final results array
total_results_output = []
total_results_output.extend(headerList)

# Variables to calculate the sum of each property
total_calories = 0
total_carbs = 0
total_fats = 0
total_protein = 0
total_sodium = 0
total_sugar = 0

# Step 7: Calculate
for i in range(len(values_input_recipe) - 1):
    # Array stores calculated results for each food

    eachFoodResult = []

    # Check the inputted unit and set the column

    if inputted_units[i] == "grams":
        units_column = gram_column
    elif inputted_units[i] == "mL":
        units_column = ml_column
    elif inputted_units[i] == "tbsp":
        units_column = tablespoon_column
    elif inputted_units[i] == "tsp":
        units_column = teaspoon_column
    elif inputted_units[i] == "cups":
        units_column = cups_column
    elif inputted_units[i] == "oz":
        units_column = oz_column
    else:
        units_column = pieces_column

    # Conver "," to "."
    zoneblocks = inputted_zoneblocks[i].replace(",", ".")
    units_value = values_ingredient_list[index_inputted_food[i]][units_column].replace(",", ".")
    calories_value = values_ingredient_list[index_inputted_food[i]][calories_column].replace(",", ".")
    carbs_value = values_ingredient_list[index_inputted_food[i]][carbs_column].replace(",", ".")
    fats_value = values_ingredient_list[index_inputted_food[i]][fats_column].replace(",", ".")
    protein_value = values_ingredient_list[index_inputted_food[i]][protein_column].replace(",", ".")
    sodium_value = values_ingredient_list[index_inputted_food[i]][sodium_column].replace(",", ".")
    sugar_value = values_ingredient_list[index_inputted_food[i]][sugar_column].replace(",", ".")

    # Calculate for each property
    if inputted_units[i] == "tbsp" or inputted_units[i] == "tsp":
        needed = str(Fraction(float(zoneblocks) * float(units_value)).limit_denominator(10)) + " tbsp" # To convert
        # into fraction for table spoon and teaspoon
    elif inputted_units[i] == "tsp":
        needed = str(Fraction(float(zoneblocks) * float(units_value)).limit_denominator(10)) + " tsp"
    else:
        needed = str(round(float(zoneblocks) * float(units_value), 0)) + " " + str(inputted_units[i])

    calories = round(float(zoneblocks) * float(calories_value))
    total_calories += calories
    carbs = round(float(zoneblocks) * float(carbs_value))
    total_carbs += carbs
    fats = round(float(zoneblocks) * float(fats_value))
    total_fats += fats
    protein = round(float(zoneblocks) * float(protein_value))
    total_protein += protein
    sodium = round(float(zoneblocks) * float(sodium_value))
    total_sodium += sodium
    sugar = round(float(zoneblocks) * float(sugar_value))
    total_sugar += sugar

    # Append to array each food for printing out result of each food
    eachFoodResult.extend(
        [[inputted_names[i], inputted_zoneblocks[i], needed, calories, carbs, fats, protein, sodium, sugar]])
    total_results_output.extend(eachFoodResult)

    # Reset values of each food's properties to calculate the next inputted food
    needed = 0
    calories = 0
    carbs = 0
    fats = 0
    protein = 0
    sodium = 0
    sugar = 0

    # Append total result for each properties

total_results_output.extend(
    [["", "", "TOTAL", str(total_calories) + " " + "kcal", str(total_carbs) + " " + "g", str(total_fats) + " " + "g",
      str(total_protein) + " " + "g", str(total_sodium) + " " + "mg", str(total_sugar) + " " + "g"]])


request_1 = sheet.values().update(spreadsheetId=outputListSheet_ID, range="sheet1!A1",
                                  valueInputOption="USER_ENTERED", body={"values": total_results_output}).execute()


