<h1 align=center> ZoneCalculator </h1>

## Purpose 
  
  **Zone Calculator** has three main uses:
  
   ① Calculate the amount of ingredients needed, calories, carbonhydrates, fats, protein, sodium and sugar of each food in the recipe that the users make and based on the amount of zone blocks that they want
    
   ② Calculate the total value of each nutrients that the recipe brings to the users
    
   ③ Print out the dietary restriction fact of the recipe that the users input
  
## Manual

### Input
**Instruction**

  - The input is a table with 3 columns, including:
 
    + Name of Food: The first character of the food is capitalized (it needs to be exact the same as the name of food in the ingredients data files)
    + Tags
    + Cooking Method
    + *Number of Zone Blocks* or *Amount* : Can be either natural or float numbers. If it is float, use `.` instead of `,`.
    + Units: can be grams, teaspoon, tablespoon, pieces, cups
    
  - The number of rows is based on the users' recipe 

**Sample Input**
Name | Tags | Cookind Method |Zone Blocks |Units
:---: | :---: | :---: | :---: | :---: |
Potato |  | Boiled | 2 | g
Carrots |  | Cooked | 1.5 | g
Mushrooms |  | Raw | 1.5 | g
Beef | Chuckeye  | Cooked | 5 | g
Olive oil |  |  | 5 | tsp

Name | Amount |Units
:---: | :---: | :---:
Potato - boiled|2|g
Carrots|1|cups
Olive oil|5|teaspoon




### Output
The output of the zone calculations will be display in a table. The table will dispay the input foods' name, zone blocks and nutrients; the total value of nutrients for the whole recipe and the dietary restriction.

**Sample Output**

Name | Zone Blocks |Needed|Calories|Carbonhydrates|fats|protein|sodium|sugar
:---: | :---: | :---:| :---: | :---:| :---: | :---:| :---: | :---:
Potato - boiled|2|150 g|88|18|0|4|16|0
Carrots|1|1 cup|38|9|0|1|65|4
Olive oil|5|5/3 tsp|66|0|8|0|0|0
