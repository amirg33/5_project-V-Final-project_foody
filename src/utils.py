import pandas as pd

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

