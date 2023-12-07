import pandas as pd
import ast


def extract_and_count(df, column_name):
    """
    Extracts unique values from a column containing lists,
    counts their occurrences, and returns a new DataFrame
    with this information.

    Returns:
    pd.DataFrame: A new DataFrame with two columns: 'unique_value' and 'count'.
    """

    # Extract all items from the lists in the specified column
    all_items = []
    for i in df[column_name].dropna():
        # Convert string representation of list to actual list
        if isinstance(i, str):
            i = eval(i)
        all_items.extend(i)

    # Count occurrences of each unique item
    item_counts = pd.Series(all_items).value_counts()

    # Create a new DataFrame from the counts
    new_df = pd.DataFrame({
        'unique_value': item_counts.index,
        'count': item_counts.values
    })

    return new_df


def aggregate_unique_lists(df, column_name):
    """
    Aggregates all the lists from a specified column into a single list of unique elements.

    Parameters:
    df (pd.DataFrame): DataFrame to process.
    column_name (str): Name of the column containing lists or string representations of lists.

    Returns:
    list: A single list containing all unique elements from the lists in the specified column.
    """

    unique_elements = set()
    for item in df[column_name].dropna():
        # Convert string representation of list to actual list if necessary
        if isinstance(item, str):
            try:
                item = ast.literal_eval(item)
            except ValueError:
                continue  # Skip items that cannot be converted

        # Check if the item is a list and add its elements to the set
        if isinstance(item, list):
            unique_elements.update(item)
        else:
            unique_elements.add(item)

    return list(unique_elements)

# Remove elements enclosed in double quotes
def strip_string(ingredients_list):
    return [ingredient for ingredient in ingredients_list if not (ingredient.startswith('"') or ingredient.endswith('"'))]

def capitalize_after_period(text):
    # Convert to string in case of non-string types like float (NaN values)
    text = str(text)

    sentences = text.split('. ')
    capitalized_sentences = [sentence.capitalize() for sentence in sentences]
    return '. '.join(capitalized_sentences)


def load_common_ingredients(ingredients_list):
    """
    Filters a list of ingredients, returning only those which are common household staples.

    Parameters:
    ingredients_list (list): The list of ingredients to filter.

    Returns:
    list: A list containing only common household ingredients.
    """

    # Define a set of common ingredients based on the provided list
    common_ingredients_set = {
        'salt', 'sugar', 'olive oil', 'flour', 'garlic cloves', 'pepper', 'brown sugar',
        'all-purpose flour', 'baking powder', 'baking soda', 'vegetable oil', 'vanilla',
        'black pepper', 'cinnamon', 'garlic powder', 'vanilla extract', 'oil', 'honey',
        'onions', 'garlic clove', 'unsalted butter', 'soy sauce', 'mayonnaise', 'paprika',
        'chicken broth', 'worcestershire sauce', 'extra virgin olive oil', 'cornstarch',
        'fresh ground black pepper', 'parsley', 'chili powder', 'ground cinnamon', 'nutmeg',
        'cayenne pepper', 'granulated sugar', 'ground cumin', 'kosher salt', 'powdered sugar',
        'fresh lemon juice', 'heavy cream', 'margarine', 'dried oregano', 'garlic salt',
        'egg yolks', 'red pepper flakes', 'cider vinegar', 'bay leaves', 'peanut butter',
        'ground cloves', 'seasoning salt', 'red pepper', 'white vinegar', 'fresh thyme',
        'salt & pepper', 'sesame seeds', 'hot sauce', 'beef broth', 'ground coriander',
        'italian seasoning', 'black olives', 'maple syrup', 'whole milk', 'bread', 'turmeric',
        'cayenne', 'green chilies', 'fresh rosemary', 'cocoa', 'dark brown sugar'
    }

    # Filter the input list based on common ingredients
    filtered_common_ingredients = [ingredient for ingredient in ingredients_list if ingredient in common_ingredients_set]

    return filtered_common_ingredients

def split_and_save_df(df, file_path, part_size):
    """
    Splits a DataFrame into two parts and saves them as separate CSV files.

    Parameters:
    df (pd.DataFrame): The DataFrame to split.
    file_path (str): The base file path for saving.
    part_size (int): The number of rows in the first part.
    """
    df_part1 = df.iloc[:part_size]
    df_part2 = df.iloc[part_size:]

    df_part1.to_csv(f"{file_path}_part1.csv", index=False)
    df_part2.to_csv(f"{file_path}_part2.csv", index=False)

def rating_to_stars(rating):
    if rating >= 4.5:
        return "⭐⭐⭐⭐⭐"  # 5 stars
    elif rating >= 3.7:
        return "⭐⭐⭐⭐"   # 4 stars
    elif rating >= 2.9:
        return "⭐⭐⭐"    # 3 stars
    elif rating >= 2.1:
        return "⭐⭐"     # 2 stars
    else:
        return "⭐"      # 1 star