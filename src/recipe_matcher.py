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
This function does not explude all the ingredients, as if someone does not like Garlic, any ingredient that contains garlic should be taken out, that is why i have created the other excluder. 
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
"""
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
"""

def ingredient_selector_partial_matches(df, ingredients_list, *args):
    '''
    Function to select recipes containing ingredients that include the specified phrases
    (partial matches) and return a filtered DataFrame by those ingredients only.
    '''
    if not args:
        return df

    required_keywords = {ing.lower() for ing in args if ing in ingredients_list}

    def contains_required_ingredient(ingredient_list):
        # Check if the ingredient list contains the required keywords as part of the ingredients
        return any(all(keyword in ingredient.lower() for keyword in required_keywords) 
                   for ingredient in ingredient_list)

    return df[df['ingredients'].apply(contains_required_ingredient)].reset_index(drop=True)



"""
def All_restrictions_list(df, restrictions=None, ingredients_list=None, required_ingredients=None, excluded_ingredients=None, include_common_ingredients=False, common_ingredients=None):
    '''
    Apply a combination of filters to the DataFrame based on dietary restrictions, required ingredients, and ingredients to exclude.
    Optionally includes common ingredients in the filtering process.
    Sorts the filtered DataFrame by weighted rating and resets the index.
    '''

    # If only selected ingredients are to be included, combine them with common ingredients
    if include_common_ingredients and common_ingredients is not None:
        required_ingredients = list(set(required_ingredients + common_ingredients)) if required_ingredients else common_ingredients

    # Apply dietary restrictions filter
    if restrictions:
        df = filter_restrictions(df, *restrictions)

    # Filter for recipes containing all required ingredients
    if required_ingredients and ingredients_list:
        df = ingredient_selector(df, ingredients_list, *required_ingredients)

    # Exclude recipes with any of the disliked ingredients
    if excluded_ingredients and ingredients_list:
        df = ingredient_excluder(df, ingredients_list, *excluded_ingredients)

    # Sort the DataFrame by weighted rating and reset the index
    return df.sort_values('weighted_rating', ascending=False).reset_index(drop=True)
"""

def All_restrictions_list(df, restrictions=None, ingredients_list=None, required_ingredients=None, excluded_ingredients=None, use_partial_matches=False, common_ingredients=None):
    '''
    Apply a combination of filters to the DataFrame based on dietary restrictions, required ingredients, 
    ingredients to exclude, and optionally include common ingredients in the filtering process.
    '''

    # Apply dietary restrictions filter
    if restrictions:
        df = filter_restrictions(df, *restrictions)

    # Apply ingredient filters
    if required_ingredients and ingredients_list:
        if use_partial_matches:
            # Filter for recipes containing ingredients with partial matches
            df = ingredient_selector_partial_matches(df, ingredients_list, *required_ingredients)
        else:
            # Filter for recipes containing all required ingredients
            df = ingredient_selector(df, ingredients_list, *required_ingredients)

    # Include common ingredients if enabled
    if use_partial_matches and common_ingredients:
        df = df[df['ingredients'].apply(lambda ingredients: any(common_ingredient in ingredients for common_ingredient in common_ingredients))]

    # Exclude recipes with any of the disliked ingredients
    if excluded_ingredients and ingredients_list:
        df = ingredient_excluder(df, ingredients_list, *excluded_ingredients)

    return df.sort_values('weighted_rating', ascending=False).reset_index(drop=True)



