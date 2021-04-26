from __future__ import print_function

from fractions import Fraction

import Credentials
import helperFunctions

sheet_metadata = Credentials.service.spreadsheets().get(
    spreadsheetId=Credentials.inputListSheet_ID).execute()
sheets = sheet_metadata.get('sheets', '')

# Step 2: Access the spreadsheet tab and get the values inside each spreadsheet

# Loop through all the sheets inside the input spreadsheet
for sheet in sheets:
    print(sheet["properties"]["title"])
    # Get the name of the input and output sheet
    input_recipe_sheet = sheet["properties"]["title"]
    output_recipe_sheet = sheet["properties"]["title"]

    # Get the sheet Index of the input sheet Name
    sheetIndex = helperFunctions.getSheetIndex(
        Credentials.inputListSheet_ID, input_recipe_sheet)

    # Get the range of input file
    rangeInputS = input_recipe_sheet + \
                  helperFunctions.getRange(Credentials.inputListSheet_ID, sheetIndex)
    rangeOutputS = output_recipe_sheet + "!A1"

    # Create output sheet with input recipe name

    # Add new worksheet into spreadSheet with ID: outputListID and title: sheet_name
    helperFunctions.add_sheets(
        Credentials.outputListSheet_ID, output_recipe_sheet)

    input_recipe = Credentials.sheet.values().get(spreadsheetId=Credentials.inputListSheet_ID,
                                                  range=rangeInputS).execute()
    values_input_recipe = input_recipe.get('values', [])

    # Skip the empty row in the recipe list
    for i in values_input_recipe:
        if not i:
            values_input_recipe.remove([])

    rangeIngredientS = "sheet1" + \
                       helperFunctions.getRange(Credentials.ingredientSheet_ID, 0)

    ingredient_list = Credentials.sheet.values().get(spreadsheetId=Credentials.ingredientSheet_ID,
                                                     range=rangeIngredientS).execute()
    values_ingredient_list = ingredient_list.get('values', [])

    # Step 3: Write the header for columns of output file
    headerList = [values_input_recipe[0][i]
                  for i in range(0, len(values_input_recipe[0]) - 1)]

    # Check if the input is ZoneBlocks or Amount
    zoneBlockMode = True
    if "Amount" in headerList:
        zoneBlockMode = False
    else:
        headerList.append("Needed")

    # Get the header list of the input recipe
    headerList.extend(helperFunctions.ingredientList(
        values_ingredient_list, 2).nutrientsName)
    headerList = [headerList]

    # Step 4: Append the inputted units, name of food and zone blocks (or amount) into array
    inputted_amount = helperFunctions.recipe(
        values_input_recipe).ingredients_amount_input
    inputted_units = helperFunctions.recipe(
        values_input_recipe).ingredients_units
    print(inputted_units)
    inputted_names = [values_input_recipe[i][0]
                      for i in range(1, len(values_input_recipe))]
    inputted_tags = [values_input_recipe[i][1]
                     for i in range(1, len(values_input_recipe))]
    inputted_cookingM = [values_input_recipe[i][2]
                         for i in range(1, len(values_input_recipe))]

    # Array stores name, tags and cooking methods for each food
    inputted_names_cookingM_tags = []
    for i in range(1, len(values_input_recipe)):
        eachFoodTagC = [values_input_recipe[i][0], values_input_recipe[i][1], values_input_recipe[i][2]]
        inputted_names_cookingM_tags.append(eachFoodTagC)

    # Step 5: Find the index row of the inputted name of foods
    index_inputted_food = []
    helperFunctions.getInputIndex(inputted_names_cookingM_tags, values_ingredient_list, index_inputted_food)
    print(index_inputted_food)
    # Step 6: Create variables for storing the results

    # Store the column of each property inside the ingredient list
    measure_col = helperFunctions.ingredientList(
        values_ingredient_list, 2).measurement_col
    nutrition_col = helperFunctions.ingredientList(
        values_ingredient_list, 2).nutrients_col
    dietary_restrict_col = helperFunctions.ingredientList(
        values_ingredient_list, 2).dietary_restriction_col

    # Final results array
    total_results_output = []
    total_results_output.extend(headerList)

    # Dietary Restriction for whole food
    recipe_restriction_dict = helperFunctions.ingredientList(
        values_ingredient_list, 2).recipe_restriction
    # Array to store the name of the diet
    recipe_restriction_array = [i for i in recipe_restriction_dict]
    zone_Unfavorable = []
    # Dictionary to calculate the sum of each property
    total_nutrients_values = helperFunctions.total_nutritions_values(
        values_ingredient_list)

    # Step 7: Calculate
    for i in range(len(values_input_recipe) - 1):
        # Array stores calculated results for each food
        eachFoodResult = []
        eachFoodRow = []
        if zoneBlockMode:  # If zoneblocks inputted, add column of inputted zoneblocks, otherwise no need
            eachFoodResult.extend(
                [inputted_names[i], inputted_tags[i], inputted_cookingM[i], inputted_amount[inputted_names[i]]])
        else:
            eachFoodResult.extend(
                [inputted_names[i], inputted_tags[i], inputted_cookingM[i]])

        # Check the inputted unit and set the column
        units_column = 0
        for propertyS in measure_col:
            if inputted_units[inputted_names[i]] == propertyS:
                units_column += measure_col[inputted_units[inputted_names[i]]]
                break
            if inputted_units[inputted_names[i]] == "":
                continue

        units_value = values_ingredient_list[index_inputted_food[i]][units_column]
        print(units_value)

        # Get the value of each property inside the info list
        nutrients_values = helperFunctions.ingredientList(values_ingredient_list,
                                                          index_inputted_food[i]).nutrients_values
        dietary_values = helperFunctions.ingredientList(values_ingredient_list,
                                                        index_inputted_food[i]).dietary_restriction_values
        # Calculate for each property

        if zoneBlockMode:
            if inputted_units[inputted_names[i]] == "tbsp" or inputted_units[inputted_names[i]] == "tsp":
                needed = str(Fraction(float(inputted_amount[inputted_names[i]]) * float(units_value)).limit_denominator(
                    10)) + " " + str(inputted_units[inputted_names[i]])
            else:
                needed = str(round(float(inputted_amount[inputted_names[i]]) * float(units_value))) + " " + str(
                    inputted_units[inputted_names[i]])
        else:
            needed = inputted_amount[inputted_names[i]] + \
                     " " + inputted_units[inputted_names[i]]

        eachFoodResult.append(needed)
        # Calculate the total nutrients values for each nutrient

        for nutrient in nutrients_values:
            if zoneBlockMode:
                nutrients_values[nutrient] = round(
                    nutrients_values[nutrient] * float(inputted_amount[inputted_names[i]]))
                total_nutrients_values[nutrient] = round(
                    total_nutrients_values[nutrient] + nutrients_values[nutrient])
            else:
                nutrients_values[nutrient] = round(
                    float(inputted_amount[inputted_names[i]]) / float(units_value) * float(nutrients_values[nutrient]))
                total_nutrients_values[nutrient] = round(total_nutrients_values[nutrient] + nutrients_values[nutrient])
            eachFoodResult.append(nutrients_values[nutrient])

        # Append to array each food for printing out result of each food
        total_results_output.extend([eachFoodResult])

        # Loop to check the dietary restriction
        counter_Unfavorable = 0
        for j in recipe_restriction_array:
            if values_ingredient_list[index_inputted_food[i]][dietary_restrict_col[j]] == "no":
                recipe_restriction_dict[j] = "no"
        if values_ingredient_list[index_inputted_food[i]][dietary_restrict_col["zone-favorable"]] == "no":
            if inputted_cookingM[i] != "" and inputted_tags[i] != "":
                zone_Unfavorable.append(
                    " - ".join([inputted_names[i], inputted_cookingM[i], inputted_tags[i]]))
            elif inputted_cookingM[i] == "" and inputted_tags[i] != "":
                zone_Unfavorable.append(
                    " - ".join([inputted_names[i], inputted_tags[i]]))
            elif inputted_cookingM[i] != "" and inputted_tags[i] == "":
                zone_Unfavorable.append(
                    " - ".join([inputted_names[i], inputted_cookingM[i]]))
            else:
                zone_Unfavorable.append(inputted_names[i])
    zone_Unfavorable_text = ", ".join(zone_Unfavorable)

    # Check if the ingredient is sugar free or not
    if total_nutrients_values["sugar (g)"] == 0:
        sugar_free = "yes"
    else:
        sugar_free = "no"

    # Array to print out the total nutrients values
    totalNutrientsArray = []
    numberOfEmptyColumn = 0
    for i in headerList[0]:
        if i == "Needed" or i == "Amount":
            break
        totalNutrientsArray.append("")

    totalNutrientsArray.append("TOTAL")

    for nutrition in total_nutrients_values:
        totalNutrientsArray.append(str(total_nutrients_values[nutrition]))

    total_results_output.extend([totalNutrientsArray])

    # Adding a new empty row to separate the content
    total_results_output.extend([[""]])

    # Array to print out the dietary restriction
    restrictionArray = ["", "", "sugar-free"]
    for restriction in dietary_restrict_col:
        if restriction == "zone-favorable":
            restriction = "zone-Unfavorable"
        restrictionArray.append(restriction)

    total_results_output.extend([restrictionArray])

    # Array to print out to the recipe
    recipe_restriction = ["", "", sugar_free]
    for restriction_values in recipe_restriction_dict.values():
        recipe_restriction.append(restriction_values)
    recipe_restriction.append(zone_Unfavorable_text)

    # Append the dietary restriction facts into the total results output
    total_results_output.extend([recipe_restriction])

    # Syntax to write out the 2D array into the google spreadsheet
    request_1 = Credentials.sheet.values().update(spreadsheetId=Credentials.outputListSheet_ID, range=rangeOutputS,
                                                  valueInputOption="USER_ENTERED",
                                                  body={"values": total_results_output}).execute()
