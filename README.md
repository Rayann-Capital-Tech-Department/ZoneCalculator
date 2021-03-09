<h1 align=center> ZoneCalculator </h1>

## Purpose 
  
  **Zone Calculator** has three main uses:
  
   ① Calculate the amount of ingredients needed, calories, carbonhydrates, fats, protein, sodium and sugar of each food in the recipe that the users make and based on the amount of zone blocks that they want
    
   ② Calculate the total value of each nutrians that the recipe brings to the users
    
   ③ Print out the dietary restriction fact of the recipe that the users input
  
## Manual

### Input
**Instruction**

  - The input is a table with 3 columns, including:
 
    + Name of Food: The first character of the food is capitalized (it needs to be exact the same as the name of food in the ingredients data files)
    + Number of Zone Blocks: Can be either natural or float numbers. If it is float, use `.` instead of `,`.
    + Units: 
    
  - The number of rows is based on the recipe of the users 

**Sample Input**
Name | Zone Blocks |Units
:---: | :---: | :---:
Potato - boiled|2|g
Carrots|1|cups
Olive oil|5|teaspoon

### Output
The output of the zone calculations will be display in a table. The table will dispay the input foods' name, zone blocks and nutrians; the total value of nutrians for the whole recipe and the dietary restriction.

**Sample Output**

Name | Zone Blocks |Needed| Calories | Carbonhydrates| fats|protein|sodium|sugar
:---: | :---: | :---:| :---: | :---:| :---: | :---:| :---: | :---:
Potato - boiled|2|150 g|9|88||18|0|4|16
Carrots|1|1 cup|38|9|0|1|65|4
Olive oil|5|5/3 tsp|66|0|8||0|0|0
