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


