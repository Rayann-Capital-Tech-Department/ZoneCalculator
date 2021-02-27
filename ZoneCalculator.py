from __future__ import print_function

from fractions import Fraction

import Credentials
import helperFunctions

# Step 2: Access the spreadsheet tab and get the values inside each spreadsheet

# Get the name of the input and output sheet
input_recipe_sheet = input("Enter the input name worksheet: ")
output_recipe_sheet = input("Enter the output name worksheet: ")

rangeInputS = input_recipe_sheet + "!A1:C5"
rangeOutputS = output_recipe_sheet + "!A1"

# Create output sheet with input recipe name

# Add new worksheet into spreadSheet with ID: outputListID and title: sheet_name

helperFunctions.add_sheets(Credentials.outputListSheet_ID, output_recipe_sheet)

input_recipe = Credentials.sheet.values().get(spreadsheetId=Credentials.inputListSheet_ID,
                                              range=rangeInputS).execute()
values_input_recipe = input_recipe.get('values', [])

ingredient_list = Credentials.sheet.values().get(spreadsheetId=Credentials.ingredientSheet_ID,
                                                 range="sheet1!A1:W6").execute()
values_ingredient_list = ingredient_list.get('values', [])

# Step 3: Write the header for columns of output file

headerList = [["Name", "Zone Blocks", "Needed", "calories", "carbohydrates", "fats", "protein", "sodium", "sugar"]]

# Step 4: Append the inputted units, name of food and zone blocks into array

inputted_zoneblocks = helperFunctions.recipe(values_input_recipe).ingredients_blocks
inputted_units = helperFunctions.recipe(values_input_recipe).ingredients_units

inputted_names = [values_input_recipe[i][0] for i in range(1, len(values_input_recipe))]
# Step 5: Find the index row of the inputted name of foods

index_inputted_food = []

helperFunctions.getInputIndex(inputted_names, values_ingredient_list, index_inputted_food)

# Step 6: Create variables for storing the results

# Store the column of each property inside the ingredient list

gram_column = 2
ml_column = 3
tablespoon_column = 4
teaspoon_column = 5
cups_column = 6
oz_column = 7
pieces_column = 8

calories_column = 9
carbs_column = 10
fats_column = 11
protein_column = 12
sodium_column = 13
sugar_column = 14

vegan_column = 15
vegetarian_column = 16
glutenF_column = 17
lacosteF_column = 18
paleo_column = 19
whole30_column = 20
zone_column = 21
zoneFav_column = 22

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

# Array to store all the property


# Step 7: Calculate
for i in range(len(values_input_recipe) - 1):
    # Array stores calculated results for each food

    eachFoodResult = []

    # Reset values of each food's properties to calculate the next inputted food
    needed = 0
    calories = 0
    carbs = 0
    fats = 0
    protein = 0
    sodium = 0
    sugar = 0

    # Check the inputted unit and set the column

    if inputted_units[inputted_names[i]] == "grams":
        units_column = gram_column
    elif inputted_units[inputted_names[i]] == "mL":
        units_column = ml_column
    elif inputted_units[inputted_names[i]] == "tbsp":
        units_column = tablespoon_column
    elif inputted_units[inputted_names[i]] == "tsp":
        units_column = teaspoon_column
    elif inputted_units[inputted_names[i]] == "cups":
        units_column = cups_column
    elif inputted_units[inputted_names[i]] == "oz":
        units_column = oz_column
    else:
        units_column = pieces_column

    # Get the value of each property inside the info list

    units_value = values_ingredient_list[index_inputted_food[i]][units_column]
    calories_value = values_ingredient_list[index_inputted_food[i]][calories_column]
    carbs_value = values_ingredient_list[index_inputted_food[i]][carbs_column]
    fats_value = values_ingredient_list[index_inputted_food[i]][fats_column]
    protein_value = values_ingredient_list[index_inputted_food[i]][protein_column]
    sodium_value = values_ingredient_list[index_inputted_food[i]][sodium_column]
    sugar_value = values_ingredient_list[index_inputted_food[i]][sugar_column]

    # Calculate for each property
    if inputted_units[inputted_names[i]] == "tbsp" or inputted_units[inputted_names[i]] == "tsp":
        needed = str(Fraction(float(inputted_zoneblocks[inputted_names[i]]) * float(units_value)).
                     limit_denominator(10)) + " tbsp"  # To convert
        # into fraction for table spoon and teaspoon
    elif inputted_units[inputted_names[i]] == "tsp":
        needed = str(Fraction(float(inputted_zoneblocks[inputted_names[i]]) * float(units_value)).
                     limit_denominator(10)) + " tsp"
    else:
        needed = str(round(float(inputted_zoneblocks[inputted_names[i]]) * float(units_value), 0)) \
                 + " " + str(inputted_units[inputted_names[i]])

    propertyArray = [calories, carbs, fats, protein, sodium, sugar]
    property_valueArray = [calories_value, carbs_value, fats_value, protein_value, sodium_value, sugar_value]
    totalPropertyArray = [total_calories, total_carbs, total_fats, total_protein, total_sodium, total_sugar]

    for j in range(len(propertyArray)):
        propertyArray[j] = round(float(inputted_zoneblocks[inputted_names[i]]) * float(property_valueArray[j]))
        totalPropertyArray[j] += propertyArray[j]

    # Append to array each food for printing out result of each food
    eachFoodResult.extend(
        [[inputted_names[i], inputted_zoneblocks[inputted_names[i]], needed, calories, carbs, fats, protein, sodium,
          sugar]])

    total_results_output.extend(eachFoodResult)

# Add restrict
vegan = "yes"
vegetarian = "yes"
gluten_free = "yes"
lacoste_free = "yes"
paleo = "yes"
whole_30 = "yes"
zone = "yes"
zone_Unfavorable = ""

if total_sugar == 0:
    sugar_free = "yes"
else:
    sugar_free = "no"

for i in range(len(values_input_recipe) - 1):
    if values_ingredient_list[index_inputted_food[i]][vegan_column] == "no":
        vegan = "no"
    elif values_ingredient_list[index_inputted_food[i]][vegetarian_column] == "no":
        vegetarian = "no"
    elif values_ingredient_list[index_inputted_food[i]][glutenF_column] == "no":
        gluten_free = "no"
    elif values_ingredient_list[index_inputted_food[i]][lacosteF_column] == "no":
        lacoste_free = "no"
    elif values_ingredient_list[index_inputted_food[i]][paleo_column] == "no":
        paleo = "no"
    elif values_ingredient_list[index_inputted_food[i]][whole30_column] == "no":
        whole_30 = "no"
    elif values_ingredient_list[index_inputted_food[i]][zone_column] == "no":
        zone = "no"
    elif values_ingredient_list[index_inputted_food[i]][zoneFav_column] == "no":
        zone_Unfavorable += inputted_names[i]

total_results_output.extend(
    [["", "", "TOTAL", str(total_calories) + " " + "kcal", str(total_carbs) + " " + "g", str(total_fats) + " " + "g",
      str(total_protein) + " " + "g", str(total_sodium) + " " + "mg", str(total_sugar) + " " + "g"]])

total_results_output.extend([["", "", "", "", "", "", "", ""]])
total_results_output.extend(
    [["sugar-free", "vegan", "vegetarian", "gluten-free", "lactose-free", "paleo", "whole 30", "zone",
      "zone-unfavorable"]])

total_results_output.extend(
    [[sugar_free, vegan, vegetarian, gluten_free, lacoste_free, paleo, whole_30, zone, zone_Unfavorable]])

request_1 = Credentials.sheet.values().update(spreadsheetId=Credentials.outputListSheet_ID, range=rangeOutputS,
                                              valueInputOption="USER_ENTERED",
                                              body={"values": total_results_output}).execute()
