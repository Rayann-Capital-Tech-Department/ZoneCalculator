from __future__ import print_function

from fractions import Fraction

import Credentials
import helperFunctions

# Step 2: Access the spreadsheet tab and get the values inside each spreadsheet

# Get the name of the input and output sheet
input_recipe_sheet = input("Enter the input name worksheet: ")
output_recipe_sheet = input("Enter the output name worksheet: ")

rangeInputS = input_recipe_sheet + "!A1:C6"
rangeOutputS = output_recipe_sheet + "!A1"

# Create output sheet with input recipe name

# Add new worksheet into spreadSheet with ID: outputListID and title: sheet_name

helperFunctions.add_sheets(Credentials.outputListSheet_ID, output_recipe_sheet)

input_recipe = Credentials.sheet.values().get(spreadsheetId=Credentials.inputListSheet_ID,
                                              range=rangeInputS).execute()
values_input_recipe = input_recipe.get('values', [])

ingredient_list = Credentials.sheet.values().get(spreadsheetId=Credentials.ingredientSheet_ID,
                                                 range="sheet1!A1:AA6").execute()
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

measure_col = helperFunctions.ingredientList(values_ingredient_list, 2).measurement_col
nutritions_col = helperFunctions.ingredientList(values_ingredient_list, 2).nutrians_col
dietary_restrict_col = helperFunctions.ingredientList(values_ingredient_list, 2).dietary_restriction_col

# Final results array
total_results_output = []
total_results_output.extend(headerList)

# Dictionary to calculate the sum of each property

total_nutrians_values = helperFunctions.total_nutrions_values(values_ingredient_list)

# Array to store all the property

# Step 7: Calculate
for i in range(len(values_input_recipe) - 1):
    # Array stores calculated results for each food
    eachFoodResult = []
    eachFoodResult.extend([inputted_names[i], inputted_zoneblocks[inputted_names[i]]])

    # Check the inputted unit and set the column
    units_column = 0
    for propertyS in measure_col:
        if inputted_units[inputted_names[i]] == propertyS:
            units_column += measure_col[inputted_units[inputted_names[i]]]
            break
    units_value = values_ingredient_list[index_inputted_food[i]][units_column]
    # Get the value of each property inside the info list

    nutrions_values = helperFunctions.ingredientList(values_ingredient_list, index_inputted_food[i]).nutrians_values

    # Calculate for each property
    if inputted_units[inputted_names[i]] == "tablespoon":
        needed = str(Fraction(float(inputted_zoneblocks[inputted_names[i]]) * float(units_value)).
                     limit_denominator(10)) + " tbsp"  # To convert
        # into fraction for table spoon and teaspoon
    elif inputted_units[inputted_names[i]] == "teaspoon":
        needed = str(Fraction(float(inputted_zoneblocks[inputted_names[i]]) * float(units_value)).
                     limit_denominator(10)) + " tsp"
    else:
        needed = str(round(float(inputted_zoneblocks[inputted_names[i]]) * float(units_value), 0)) \
                 + " " + str(inputted_units[inputted_names[i]])

    eachFoodResult.append(needed)
    for nutrion in nutrions_values:
        nutrions_values[nutrion] *= round(float(inputted_zoneblocks[inputted_names[i]]))
        total_nutrians_values[nutrion] += nutrions_values[nutrion]
        eachFoodResult.append(nutrions_values[nutrion])

    # Append to array each food for printing out result of each food

    total_results_output.extend([eachFoodResult])

# Add restrict
vegan = "yes"
vegetarian = "yes"
gluten_free = "yes"
lactose_free = "yes"
paleo = "yes"
whole_30 = "yes"
zone = "yes"
zone_Unfavorable = ""

if total_nutrians_values["sugar"] == 0:
    sugar_free = "yes"
else:
    sugar_free = "no"

for i in range(len(values_input_recipe) - 1):
    if values_ingredient_list[index_inputted_food[i]][dietary_restrict_col["vegan"]] == "no":
        vegan = "no"
    elif values_ingredient_list[index_inputted_food[i]][dietary_restrict_col["vegetarian"]] == "no":
        vegetarian = "no"
    elif values_ingredient_list[index_inputted_food[i]][dietary_restrict_col["gluten-free"]] == "no":
        gluten_free = "no"
    elif values_ingredient_list[index_inputted_food[i]][dietary_restrict_col["lactose-free"]] == "no":
        lactose_free = "no"
    elif values_ingredient_list[index_inputted_food[i]][dietary_restrict_col["paleo"]] == "no":
        paleo = "no"
    elif values_ingredient_list[index_inputted_food[i]][dietary_restrict_col["whole 30"]] == "no":
        whole_30 = "no"
    elif values_ingredient_list[index_inputted_food[i]][dietary_restrict_col["zone"]] == "no":
        zone = "no"
    elif values_ingredient_list[index_inputted_food[i]][dietary_restrict_col["zone-favorable"]] == "no":
        zone_Unfavorable += inputted_names[i]

# Array to print out the total nutrians values
totalNutriansArray = ["", "", "TOTAL"]
for nutrition in total_nutrians_values:
    totalNutriansArray.append(total_nutrians_values[nutrition])

total_results_output.extend([totalNutriansArray])

# Adding a new empty row to separate the content
total_results_output.extend([[""]])

# Array to print out the dietary restriction 
restrictionArray = ["sugar-free"]
for restriction in dietary_restrict_col:
    restrictionArray.append(restriction)

total_results_output.extend([restrictionArray])

# Append the dietary restriction facts into the total results output
total_results_output.extend(
    [[sugar_free, vegan, vegetarian, gluten_free, lactose_free, paleo, whole_30, zone, zone_Unfavorable]])

# Syntax to write out the 2D array into the google spreadsheet
request_1 = Credentials.sheet.values().update(spreadsheetId=Credentials.outputListSheet_ID, range=rangeOutputS,
                                              valueInputOption="USER_ENTERED",
                                              body={"values": total_results_output}).execute()
