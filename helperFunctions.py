import Credentials


# Function to get the index of the sheet inside the spreadsheet
def getSheetIndex(IDFiles, sheetName):
    sheet_metadata = Credentials.service.spreadsheets().get(spreadsheetId=IDFiles).execute()
    sheets = sheet_metadata.get('sheets', '')
    sheetIndex = 0

    for i in sheets:
        if i["properties"]["title"] == sheetName:
            sheetIndex = i["properties"]["index"]
    return sheetIndex


# Function to get the range of the data inside the documents
def getRange(IDFiles, sheetIndex):
    res = Credentials.service.spreadsheets().get(spreadsheetId=IDFiles, fields='sheets('
                                                                               'data/rowData'
                                                                               '/values'
                                                                               '/userEnteredValue,'
                                                                               'properties(index,'
                                                                               'sheetId,'
                                                                               'title))').execute()
    sheetName = res['sheets'][sheetIndex]['properties']['title']
    lastRow = len(res['sheets'][sheetIndex]['data'][0]['rowData'])
    lastColumn = max([len(e['values']) for e in res['sheets'][sheetIndex]['data'][0]['rowData'] if e])

    string = ""
    # Convert index column into string as the column inside the spreadsheet
    while lastColumn > 0:
        lastColumn, remainder = divmod(lastColumn - 1, 26)
        string = chr(65 + remainder) + string
    return "!A1:" + string + str(lastRow)


# Store all the input information

class recipe:
    def __init__(self, inputRecipe):
        self.inputRecipe = inputRecipe
        self.ingredients_blocks = {}
        self.ingredients_units = {}

        # Start at 1 to ignore the header row
        for i in range(1, len(self.inputRecipe)):
            self.ingredients_blocks[self.inputRecipe[i][0]] = self.inputRecipe[i][3]
            self.ingredients_units[self.inputRecipe[i][0]] = self.inputRecipe[i][4]


# Class to store data of ingredient
class ingredientList:
    def __init__(self, ingredient, indexFood):
        self.ingredient = ingredient
        self.indexFood = indexFood
        # Dictionary for getting column
        self.measurement_col = {}
        self.nutrients_col = {}
        self.dietary_restriction_col = {}
        self.recipe_restriction = {}

        # Dictionary for storing name of each nutrition, dietary restriction value
        self.nutrients_values = {}
        self.dietary_restriction_values = {}
        self.inputFood_nutrients_values = {}
        self.nutrientsName = []

        # Function to get the column of each property in the first row
        counter = 0  # Counter to check the number of
        for i in range(len(self.ingredient[0])):  # Loop through all the elements of the first row array
            if self.ingredient[0][i] == "":
                counter += 1
                continue
            if counter == 1:  # After the first empty column, the next columns will be measurement column
                self.measurement_col[self.ingredient[0][i]] = i
            elif counter == 2:  # After the second empty column, the next columns will be nutrients column
                self.nutrientsName.append(self.ingredient[0][i])
                self.nutrients_col[self.ingredient[0][i]] = i

                # Store the value of nutrients property of food with index row
                self.nutrients_values[self.ingredient[0][i]] = 0
                self.nutrients_values[self.ingredient[0][i]] += float(self.ingredient[self.indexFood][
                                                                          self.nutrients_col[self.ingredient[0][i]]])

            elif counter == 3:  # After the third empty column, the next columns will be dietary restriction column
                self.dietary_restriction_col[self.ingredient[0][i]] = i
                # Store the dietary restriction text into dictionary
                self.dietary_restriction_values[self.ingredient[0][i]] = self.ingredient[self.indexFood][
                    self.dietary_restriction_col[self.ingredient[0][i]]]
                if self.ingredient[0][i] != "zone-favorable":
                    self.recipe_restriction[self.ingredient[0][i]] = "yes"


# Get the index row of the input food in the ingredient list
def getInputIndex(inputFoodNameTagsMethod, nutrition_info, index_inputted_food):
    # Counter is the index of food in the input recipe
    counter = 0

    for inputFood in inputFoodNameTagsMethod:
        for i, x in enumerate(nutrition_info):
            # If food appears in the nutrition_infor list, append the food's index row into an array to store
            if inputFood == (x[0] + x[1] + x[2]):
                index_inputted_food.append(i)
                counter += 1
            if counter == len(inputFoodNameTagsMethod):  # Break if all the inputted food checked
                break

    return index_inputted_food


# Function to initialize value for all the total values of each nutrients appeared on the ingredient list
def total_nutritions_values(ingredient):
    total_nutrients_values = {}
    count = 0
    for i in range(len(ingredient[0])):
        # Check the index of empty column
        if ingredient[0][i] == "":
            count += 1
            continue
        # Check if there is second empty column, if yes, the next columns will be nutrients columns
        if count == 2:
            total_nutrients_values[ingredient[0][i]] = 0

    return total_nutrients_values


# Function creates new worksheet into sheet_name worksheet with ID: outputListID
def add_sheets(outputListID, sheet_name):
    try:
        request_body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name,
                        'tabColor': {
                            'red': 0.44,
                            'green': 0.99,
                            'blue': 0.50
                        }
                    }
                }
            }]
        }

        # Update the worksheet
        response = Credentials.sheet.batchUpdate(
            spreadsheetId=outputListID,
            body=request_body
        ).execute()

        return response
    except Exception as e:
        print(e)
