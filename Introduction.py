from os import link
import streamlit as st
import pandas as pd
import numpy as np


import streamlit as st

st.title('Foody - Recipe Generator Introduction')

# Introduction text
st.write("""
Welcome to the Foody - Recipe Generator! This innovative app helps you discover delicious recipes tailored to your dietary preferences and ingredients at hand. Whether you're planning a quick meal, a healthy snack, or a gourmet feast, Foody is here to inspire your culinary journey.
""")
st.write("""
All the recipes the generator can find is from the following webpage: www.food.com""")
# Divider
st.markdown("---")

# How it works section
st.header("How It Works")
st.write("""
- **Select Preferences**: Choose from dietary restrictions like 'Dairy-Free', 'Gluten-Free', and more.
- **Pick Ingredients**: Input ingredients you have, and we'll find recipes that make the best use of them.
- **Exclude Ingredients**: Optionally, exclude ingredients you don't like or don't have.
- **Cooking Time Slider**: Adjust the slider to find recipes that fit your schedule.
- **Discover**: Explore a variety of recipes and get cooking!

Feel free to experiment with different combinations to find your perfect meal.
""")

# Divider
st.markdown("---")

# Images and suggestions (Placeholder for images)
st.header("Recipe Inspirations")
st.write("Here are some popular categories to explore:")

# Example categories with images (replace with actual image paths or URLs)
categories = ["Healthy & Fresh: KITTENCAL'S FAMOUS GREEK SALAD ", "Quick & Easy: EASY SEAFOOD COCKTAIL SAUCE", "Comfort Food: MOM'S BREAKFAST BURRITO", "Exotic: EXOTIC FRUIT SALAD"]
image_paths = ["./images/healthy.jpg", "./images/quick.jpg", "./images/comfort.jpg", "./images/exotic.jpg"]

for category, img_path in zip(categories, image_paths):
    st.image(img_path, caption=f"{category}", width=300)

# Divider
st.markdown("---")

# Final encouragement and instructions
st.header("Ready to Start?")
st.write("""
It is my pleasure to help you on your culinary adventure. Navigate to the Foody Recipe Generator tab to begin finding recipes suited just for you. Happy cooking!
""")
