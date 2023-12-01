# 5_project-V-Final-project_foody

## Things to do

- Add the count of the ratings and the avg rating to the df_2 dataframe
- List of ingredients that should be always at home (salt, pepper, flour, eggs, etc)
- get the best rating as a result, as a recomendation

### Ingredients

- Should be displayed directly at the User interface for selection and fast typing (search botton for faster selection)

#### Day-to-Day Process

- Dataframe: Cleanig (EDA)
  - Tags
  - Nutrition
  - Steps
  - Ingredients --> needs to be extracted from the DataFrame: create another DataFrame with the unique values of all the ingredients
  - Raiting of each dish
- Recipe Matching Algorithm
  - Functions that allow you to filter by each ingrdient
  - ¿? Partial Matches / Common substitutions
  - ¿? Common variations algorithm (Tomatoe --> Tomatoes)
- Display the results
  - Ingredients to be selected
  - seperated by food category (Dairy, vegetables, meat, gluten, etc)

### Idea:

- Insetad of using the dataset to show the information of the recipe, use the webpage, as names are simply the name + recipe_id

### To do List for Wednesday

- ~~Create a new data Frame of the count of the ratings and calculate the avg~~
  - ~~Append and merge these to the Df_2~~
- EDA the Data Frame and delete anythign not relevant
- change column names if needed
- create ingredients data frame
  - Group ingredients in different categories
- Start working on creating the filters
  - How do I want to filter for the different Dairies / Gluten Free / etc

### To do list for Thursday

- Ingredients --> Get only the most relevant ones
  - maybe take the first 300
  - Create a dictionary that will find and equal the values
  - Create categories of these ingredients
- tags --> Need to be sorted: too many
  - take the first 100 maybe and use the most relevant tags
- steps --> Put that as well for each recipe

### To do list for Friday
