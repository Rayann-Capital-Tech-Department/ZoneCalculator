import Credentials


# Store all the input information

class recipe:
    def __init__(self, inputRecipe):
        self.inputRecipe = inputRecipe
        self.ingredients_blocks = {}
        self.ingredients_units = {}

        # Start at 1 to ignore the header row
        for i in range(1, len(self.inputRecipe)):
            self.ingredients_blocks[self.inputRecipe[i][0]] = self.inputRecipe[i][1]
            self.ingredients_units[self.inputRecipe[i][0]] = self.inputRecipe[i][2]


# Get the index row of the input food in the ingredient list
def getInputIndex(inputFoodName, nutrition_info, index_inputted_food):
    # Counter is the index of food in the input recipe
    counter = 0

    for i, x in enumerate(nutrition_info):
        # If food appears in the nutrition_infor list, append the food's index row into an array to store
        if inputFoodName[counter] in x:
            index_inputted_food.append(i)
            counter += 1
            if counter == len(inputFoodName):  # Break if all the inputted food checked
                break
    print(index_inputted_food)
    return index_inputted_food


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
