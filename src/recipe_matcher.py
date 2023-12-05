def filter_restrictions(df, *args):
    '''
    Filter the DataFrame based on dietary restrictions. 
    Returns recipes that do not contain any of the specified restrictions (e.g., dairy, gluten).
    '''
    if not args:
        return df

    def meets_criteria(restriction_list):
        # Check if none of the specified restrictions are in the recipe's restrictions
        return not any(restriction in restriction_list for restriction in args)

    # Apply the filter
    return df[df['restrictions'].apply(meets_criteria)].reset_index(drop=True)



def ingredient_selector(df, ingredients_list, *args):
    '''
    Function to select recipes containing all specified ingredients and return a filtered DataFrame by those ingredients only.
    '''
    if not args:
        return df  # If no ingredients are specified, return the original DataFrame

    # Create a set of required ingredients from args
    required_ingredients = {ing for ing in args if ing in ingredients_list}

    # Filter DataFrame to include recipes with all of the required ingredients
    return df[df['ingredients'].apply(lambda ingredients: required_ingredients.issubset(ingredients))].reset_index(drop=True)



def ingredient_excluder(df, ingredients_list, *args):
    '''
    Function to exclude recipes containing any of the specified ingredients or those containing parts of these ingredients 
    and return a filtered DataFrame excluding those recipes.
    '''
    if not args:
        return df  # If no ingredients are specified, return the original DataFrame

    # Create a set of disliked ingredient keywords from args
    disliked_keywords = {ing for ing in args if ing in ingredients_list}

    def contains_disliked_ingredient(ingredient_list):
        # Check if any ingredient in the list contains any of the disliked keywords
        return not any(disliked_keyword in ingredient for ingredient in ingredient_list for disliked_keyword in disliked_keywords)

    # Filter DataFrame to exclude recipes containing any of the disliked ingredients
    return df[df['ingredients'].apply(contains_disliked_ingredient)].reset_index(drop=True)


"""
def ingredient_excluder(df, ingredients_list, *args):
    '''
    Function to exclude recipes containing any of the specified ingredients and return a filtered DataFrame excluding those recipes.
    '''
    if not args:
        return df  # If no ingredients are specified, return the original DataFrame

    # Create a set of disliked ingredients from args
    disliked_ingredients = {ing for ing in args if ing in ingredients_list}

    # Filter DataFrame to exclude recipes containing any of the disliked ingredients
    return df[df['ingredients'].apply(lambda ingredients: not disliked_ingredients.intersection(ingredients))].reset_index(drop=True)
"""

def All_restrictions(df, restrictions=None, ingredients_list=None, required_ingredients=None, excluded_ingredients=None):
    '''
    Apply a combination of filters to the DataFrame based on dietary restrictions, required ingredients, and ingredients to exclude.
    Sorts the filtered DataFrame by weighted rating and resets the index.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    restrictions (list): List of dietary restrictions to exclude.
    ingredients_list (list): Comprehensive list of all possible ingredients.
    required_ingredients (list): Ingredients that must be in the recipes.
    excluded_ingredients (list): Ingredients that must not be in the recipes.

    Returns:
    pd.DataFrame: Filtered and sorted DataFrame.
    '''

    # Apply dietary restrictions filter
    if restrictions:
        df = filter_restrictions(df, restrictions)

    # Filter for recipes containing all required ingredients
    if required_ingredients and ingredients_list:
        df = ingredient_selector(df, ingredients_list, *required_ingredients)

    # Exclude recipes with any of the disliked ingredients
    if excluded_ingredients and ingredients_list:
        df = ingredient_excluder(df, ingredients_list, *excluded_ingredients)

    # Sort the DataFrame by weighted rating and reset the index
    return df.sort_values('weighted_rating', ascending=False).reset_index(drop=True)



def All_restrictions_list(df, restrictions=None, ingredients_list=None, required_ingredients=None, excluded_ingredients=None):
    '''
    Apply a combination of filters to the DataFrame based on dietary restrictions, required ingredients, and ingredients to exclude.
    Sorts the filtered DataFrame by weighted rating and resets the index.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    restrictions (list): List of dietary restrictions to exclude.
    ingredients_list (list): Comprehensive list of all possible ingredients.
    required_ingredients (list): Ingredients that must be in the recipes.
    excluded_ingredients (list): Ingredients that must not be in the recipes.

    Returns:
    pd.DataFrame: Filtered and sorted DataFrame.
    '''

    # Apply dietary restrictions filter
    if restrictions:
        df = filter_restrictions(df, *restrictions)  # Unpack the list

    # Filter for recipes containing all required ingredients
    if required_ingredients and ingredients_list:
        df = ingredient_selector(df, ingredients_list, *required_ingredients)  # Unpack the list

    # Exclude recipes with any of the disliked ingredients
    if excluded_ingredients and ingredients_list:
        df = ingredient_excluder(df, ingredients_list, *excluded_ingredients)  # Unpack the list

    # Sort the DataFrame by weighted rating and reset the index
    return df.sort_values('weighted_rating', ascending=False).reset_index(drop=True)






