import cleaning
import utils
import pandas as pd
import cleaning
import ast              # Change lists that are strings to actual lists
import re
import numpy as np

# Cleaning 
df = cleaning.recipes_ratings_merged_cleaned()
nutrition_df = cleaning.create_nutrition_df(df, 'nutrition', 'recipe_id')

# Utils
df_ingredients = utils.extract_and_count(df, 'ingredients')
df_tags_unique = utils.extract_and_count(df, 'tags')
ingredients_list = utils.aggregate_unique_lists(df, 'ingredients')

# 


def exploration_of_data():
    
    #df.to_json("../data/Processed/recipes_with_ratings.json", index=False)
    #df = pd.read_json("../data/Processed/recipes_with_ratings.json")

    # Converting columns in the DataFrame from string representation to actual lists.

    #df.to_csv("../data/Processed/recipes_with_ratings.csv", index=False)
    #df = pd.read_csv("../data/Processed/recipes_with_ratings.csv")
    
    #df.tags = df.tags.map(lambda x: ast.literal_eval(x))
    #df.steps = df.steps.map(lambda x: ast.literal_eval(x))
    #df.ingredients = df.ingredients.map(lambda x: ast.literal_eval(x))
    #df.nutrition = df.nutrition.map(lambda x: ast.literal_eval(x))


    def find_dairy_ingredients(ingredients_list):
    # Define the dairy categories with their keywords and exclusion terms
        dairy_categories = {
        'milk': {
            'keywords': [
                r'\bmilk\b', r'\bskim milk\b', r'\bevaporated milk\b', r'\bwhole milk\b', 
                r'\bnonfat milk\b', r'\blow-fat milk\b', r'\b2% low-fat milk\b', r'\b1% low-fat milk\b',
                r'\bcondensed milk\b', r'\bnonstick cooking spray\b', r'\b2% low-fat milk\b'
            ],
            'exclusions': ['almond', 'coconut', 'non-dairy', 'oat', 'rice', 'soy']
        },
        'yogurt': {
            'keywords': [
                r'\byogurt\b', r'\bgreek yogurt\b', r'\bplain yogurt\b', r'\bvanilla yogurt\b', 
                r'\blight sour cream\b', r'\bfat free cream cheese\b', r'\blow-fat plain yogurt\b', 
                r'\bplain fat-free yogurt\b', r'\bnonfat sour cream\b', r'\bplain breadcrumbs\b', 
                r'\bself-raising flour\b'
            ],
            'exclusions': []
        },
        'butter': {
            'keywords': [
                r'\bbutter\b', r'\bunsalted butter\b', r'\bsalted butter\b', r'\bmargarine\b', 
                r'\bcream of mushroom soup\b', r'\bcream of chicken soup\b', r'\blight cream\b', 
                r'\bsour cream\b', r'\blight sour cream\b', r'\bcreme fraiche\b', r'\bwhipped cream\b', 
                r'\bwhipped topping\b', r'\bcream cheese frosting\b'
            ],
            'exclusions': ['almond', 'apple', 'butterfly', 'butter substitute', 'butterball', 
                        'buttercup', 'butterfish', 'butterflied', 'butternut', "i can't believe it's not butter",
                        'butter beans', 'lettuce', 'peas', 'coconut', 'vegan']
        },
        'cream': {
            'keywords': [
                r'\bcream\b', r'\bheavy cream\b', r'\bwhipping cream\b', r'\bheavy whipping cream\b', 
                r'\bcream of mushroom soup\b', r'\bcream of chicken soup\b', r'\blight cream\b', 
                r'\bsour cream\b', r'\blight sour cream\b', r'\bcreme fraiche\b', r'\bwhipped cream\b', 
                r'\bwhipped topping\b', r'\bhalf-and-half\b', r'\bhalf-and-half cream\b', 
                r'\bcreamed corn\b', r'\bcream cheese frosting\b', r'\bcream sherry\b', 
                r'\bwhipped topping\b', r'\bwhipped cream\b', r'\bcreamy peanut butter\b'
            ],
            'exclusions': ['almond', 'coconut', 'non-dairy', 'non-creamy', 'soy', 'vegan']
        },
        'cheese': {
            'keywords': [
                r'\bcheese\b', r'\bparmesan cheese\b', r'\bcheddar cheese\b', r'\bmozzarella cheese\b', 
                r'\bcream cheese\b', r'\bmonterey jack cheese\b', r'\bswiss cheese\b', r'\bfeta cheese\b', 
                r'\bsharp cheddar cheese\b', r'\bblue cheese\b', r'\bvelveeta cheese\b', 
                r'\bricotta cheese\b', r'\bcottage cheese\b', r'\bprovolone cheese\b', 
                r'\bgruyere cheese\b', r'\bfontina cheese\b', r'\basiago cheese\b', 
                r'\bfresh mozzarella cheese\b', r'\bcolby-monterey jack cheese\b', 
                r'\bpart-skim mozzarella cheese\b', r'\bextra-sharp cheddar cheese\b', 
                r'\bpart-skim ricotta cheese\b', r'\bmascarpone cheese\b', 
                r'\breduced-fat cream cheese\b', r'\blight cream cheese\b', 
                r'\bmild cheddar cheese\b', r'\bextra lean ground beef\b', 
                r'\blow-fat cheddar cheese\b', r'\blow fat cottage cheese\b', ],
            'exclusions': ['non-dairy', 'soy', 'vegan', 'vegetarian']
        },
        'ice_cream': {
            'keywords': [r'\bice cream\b', r'\bgelato\b'],
            'exclusions': ['non-dairy', 'almond', 'coconut', 'soy']
        },
        'curd': {
            'keywords': [r'\bcurd\b'],
            'exclusions': ['lemon', 'lime']
        },
        'whey': {
            'keywords': [r'\bwhey\b'],
            'exclusions': []
        },
        'casein': {
            'keywords': [r'\bcasein\b'],
            'exclusions': []
        },
        'ghee': {
            'keywords': [r'\bghee\b'],
            'exclusions': []
        },
        'kefir': {
            'keywords': [r'\bkefir\b'],
            'exclusions': []
        },
        'paneer': {
            'keywords': [r'\bpaneer\b'],
            'exclusions': []
        },
        'condensed_milk': {
            'keywords': [r'\bcondensed milk\b'],
            'exclusions': ['non-dairy', 'soy']
        },
        'evaporated_milk': {
            'keywords': [r'\bevaporated milk\b'],
            'exclusions': ['non-dairy', 'soy']
        },
        'milk_powder': {
            'keywords': [r'\bmilk powder\b', r'\bdried milk\b', r'\bpowdered milk\b'],
            'exclusions': ['non-dairy', 'soy']
        }
    }


        # Function to compile regex and find matches
        def find_matches(category, ingredients):
            keywords_regex = re.compile('|'.join(category['keywords']), re.IGNORECASE)
            exclusions_regex = re.compile('|'.join(category['exclusions']), re.IGNORECASE) if category['exclusions'] else None
            return [i for i in ingredients if keywords_regex.search(i) and (not exclusions_regex or not exclusions_regex.search(i))]

        # Aggregate all dairy ingredients
        dairy = []
        for category in dairy_categories.values():
            dairy.extend(find_matches(category, ingredients_list))

        # Remove duplicates and sort
        dairy = list(set(dairy))
        dairy.sort()

        return dairy

    def find_gluten_ingredients(ingredients_list):
        # Define the gluten categories with their keywords and exclusions
        gluten_categories = {
            'grain': {
            'keywords': [
                r'\bwheat\b', r'\bflour\b', r'\bharina\b', r'\bbarley\b', r'\bbread\b', r'\brye\b',
                r'\bfarro\b', r'\bcouscous\b', r'\bkamut\b', r'\bbagel\b', 
                r'\ball-purpose flour\b', r'\bwhite flour\b', r'\bwhole wheat flour\b', r'\bself-rising flour\b', 
                r'\bunbleached flour\b', r'\bunbleached all-purpose flour\b', r'\bbreadcrumbs\b', r'\bbread flour\b', 
                r'\bbread crumbs\b', r'\bwhite bread\b', r'\bfrench bread\b', r'\bitalian bread\b',
                r'\brye flour\b', r'\brye bread\b', r'\bwhole wheat bread\b', r'\bwhole grain mustard\b',
                r'\bpie crusts\b', r'\brice krispies\b', r'\bseasoned bread crumbs\b', r'\bbaguette\b',
                r'\boreo cookies\b', r'\bgraham crackers\b', r'\bpita bread\b', r'\bsourdough bread\b',
                r'\bwonton wrappers\b', r'\brye flour\b', r'\bcroutons\b', r'\bgraham cracker crust\b', 
                r'\bflour tortilla\b', r'\bflour tortillas\b', r'\benglish muffins\b', r'\bcracker\b', 
                r'\bcrackers\b', r'\bgraham cracker pie crust\b', r'\bpretzels\b', r'\bphyllo dough\b', 
                r'\bwheat flour\b', r'\bwheat bran\b', r'\bself rising flour\b', r'\bwhite bread flour\b',
                r'\bpolenta\b', r'\bchow mein noodles\b', r'\bgraham cracker crumbs\b', r'\bwhole wheat tortillas\b',
                r'\bwheat germ\b', r'\bsourdough starter\b', r'\bflax seed meal\b', r'\bcrisco\b',
                r'\bcorn flake crumbs\b', r'\brye flour\b', r'\bflour tortilla\b', r'\bvermicelli\b'],
            'exclusions': [
                'gluten-free', 'polenta', 'rice', 'buckwheat', 'chestnut', 'coconut', 'corn', 'chickpea',
                'oat', 'bean', 'almond', 'urad dal', 'tapioca', 'soy', 'amaranth', 'besan', 'gram', 'garbanzo',
                'sorghum', 'potato', 'millet', 'manioc', 'sweetbreads', 'breadfruit', 'injera bread',
                'cornstarch', 'rice flour', 'xanthan gum', 'tapioca flour', 'gluten-free flour']
            },
        'pasta_and_varieties': {
            'keywords': [
                r'\bpasta\b', r'\brigati\b', r'\bcampanelle\b', r'\bcappelletti\b', r'\bcavatappi\b',
                r'\brigatoni\b', r'\bditali\b', r'\bpenne\b', r'\bfarfalle\b', r'\bfettuccine\b', r'\bgemelli\b',
                r'\blasagna\b', r'\bpappardelle\b', r'\btagliatelle\b', r'\bpizza\b', r'\borzo\b', r'\bmacaroni\b',
                r'\btortellini\b', r'\bspaghetti\b', r"\bmac n' cheese\b", r'\bgnocchi\b', r'\bdumplings\b', 
                r'\bpretzels\b', r'\bcookie\b', r'\blasagna noodles\b', r'\belbow macaroni\b', r'\bpenne pasta\b', 
                r'\blinguine\b', r'\bangel hair pasta\b', r'\borzo pasta\b', r'\bfettuccine\b',
                r'\bfusilli\b', r'\bmanicotti\b', r'\btortellini\b', r'\bravioli\b', r'\bcannelloni\b', 
                r'\bmacaroni and cheese mix\b', r'\bpasta shells\b', r'\bpenne rigate\b', r'\blinguine\b',
                r'\btagliatelle pasta noodles\b', r'\bcavatappi pasta\b', r'\borecchiette\b', r'\bcapellini\b',
                r'\bgnocchi\b', r'\brotini pasta\b', r'\blasagna noodle\b', r'\bno-boil lasagna noodles\b',
                r'\bcouscous\b', r'\borzo pasta\b', r'\bditalini\b', r'\bpizza dough\b', r'\bpizza crusts\b'
            ],
            'exclusions': [
                'acini di pepe', 'angel hair', 'rice', 'bucatini', 'tubetti', 'impastata ricotta', 'gluten-free', 'quinoa'
            ]
        },
        'other_gluten_sources': {
            'keywords': [
                r'\bbarley\b', r'\bflour\b', r'\blasagna\b', r'\bpasta\b', r'\bpizza\b', r'\bwheat\b', 
                r'\brye\b', r'\bspelt\b', r'\bseitan\b', r'\btriticale\b', r'\bmalt\b', r'\bbrewer\s yeast\b',
                r'\bmalted milk\b', r'\bmalt extract\b', r'\bmalt flavoring\b', r'\bmalt syrup\b',
                r'\bbeer\b', r'\bale\b', r'\bstout beer\b', r'\blager beer\b', r'\bmalt liquor\b',
                r'\bseitan\b', r'\bsoy sauce\b', r'\bteriyaki sauce\b', r'\bhoisin sauce\b',
                r'\bsoy flour\b', r'\bbarley malt\b', r'\bbarley malt syrup\b', r'\bbarley malt extract\b',
                r'\bbarley flour\b', r'\brusk\b', r'\brye flour\b', r'\brye malt\b'
            ],
            'exclusions': ['gluten-free']
        }
    }

        # Function to compile regex and find matches
        def find_matches(category, ingredients):
            keywords_regex = re.compile('|'.join(category['keywords']), re.IGNORECASE)
            exclusions_regex = re.compile('|'.join(category.get('exclusions', [])), re.IGNORECASE) if category.get('exclusions') else None
            return [i for i in ingredients if keywords_regex.search(i) and (not exclusions_regex or not exclusions_regex.search(i))]

        # Aggregate all gluten ingredients
        gluten = []
        for category in gluten_categories.values():
            gluten.extend(find_matches(category, ingredients_list))

        # Remove duplicates and sort
        gluten = list(set(gluten))
        gluten.sort()

        return gluten


    def find_nut_ingredients(ingredients_list):
        # Define the nut categories with their keywords and exclusions
        nut_categories = {
            'nuts_and_varieties': {
            'keywords': [
                r'\bnut\b', r'\balmond\b', r'\bpecan\b', r'\bpistachio\b', r'\bmacadamia\b',
                r'\bcashew\b', r'\bhickory\b', r'\bfilbert\b', 
                r'\bwalnut\b', r'\bpecans\b', r'\balmonds\b', r'\bpine nuts\b', 
                r'\bslivered almonds\b', r'\bcashews\b', r'\bmacadamia nuts\b', 
                r'\bpistachios\b', r'\bhazelnuts\b'
            ],
            'exclusions': [
                'minute', 'coconut', 'nutmeg', 'butternut', 
                'peanut', 'peanuts', 'creamy peanut butter', 'peanut butter'
            ]
        },
        }
        # Function to compile regex and find matches
        def find_matches(category, ingredients):
            keywords_regex = re.compile('|'.join(category['keywords']), re.IGNORECASE)
            exclusions_regex = re.compile('|'.join(category.get('exclusions', [])), re.IGNORECASE) if category.get('exclusions') else None
            return [i for i in ingredients if keywords_regex.search(i) and (not exclusions_regex or not exclusions_regex.search(i))]

        # Aggregate all nut ingredients
        nuts = []
        for category in nut_categories.values():
            nuts.extend(find_matches(category, ingredients_list))

        # Remove duplicates and sort
        nuts = list(set(nuts))
        nuts.sort()

        return nuts

    def find_vegetarian_ingredients(ingredients_list):
        # Define vegetarian categories with their keywords and potential exclusions (from meat_categories)
        vegetarian_categories = {
            'vegetarian_varieties': {
                'keywords': [
                    r'\bvegetables\b', r'\bfruits\b', r'\blegumes\b', r'\bbeans\b', r'\btofu\b', r'\btempeh\b', 
                    r'\blentils\b', r'\bseitan\b', r'\bnuts\b', r'\bseeds\b', r'\bwhole grains\b', r'\bherbs\b', 
                    r'\bspices\b', r'\balmond milk\b', r'\bsoy milk\b', r'\brice milk\b', r'\boat milk\b',
                    r'\bplant-based\b', r'\bquinoa\b', r'\bchia\b', r'\bflaxseed\b', r'\bpeas\b', r'\bmushrooms\b',
                    r'\bavocado\b', r'\beggplant\b', r'\bzucchini\b', r'\bsquash\b', r'\bpeppers\b', r'\btomatoes\b',
                    r'\bsweet potatoes\b', r'\bcarrots\b', r'\bcauliflower\b', r'\bbroccoli\b', r'\basparagus\b',
                    r'\bbrussels sprouts\b', r'\bspinach\b', r'\bkale\b', r'\bgarlic\b', r'\bonions\b'
                ],
                'exclusions': [
                    'meat', 'pork', 'lamb', 'chicken', 'beef', 'duck', 'buffalo', 'poultry', 'cod', 'fish', 'sushi', 
                    'tuna', 'bass', 'fillet', 'ribs', 'trout', 'anchovy', 'barramundi', 'steak', 'basa', 'tenderloin', 
                    'bison', 'angus', 'salmon', 'snapper', 'liver', 'pollo', 'plaice', 'pickerel', 'ostrich', 'roughy', 
                    'opah', 'perch', 'pike', 'ahi', 'marlin', 'crab', 'mackerel', 'loin', 'lobster', 'leg', 'sausage', 
                    'frankfurt', 'lean', 'shark', 'whale', 'dolphin', 'clam', 'kidney', 'heart', 'brain', 'tongue', 
                    'arm roast', 'bear', 'rump', 'round roast', 'broil', 'caribou', 'deer', 'blade', 'chuck', 'elk', 
                    'ham', 'turkey', 'mortadella', 'kangaroo', 'kobe', 'mahi', 'alligator', 'crocodile', 'llama', 
                    'bangus', 'bacon', 'antelope', 'veggie', 'vegetarian', 'vegan', 'meatless', 'artichoke heart', 
                    'bechamel', 'champagne', 'graham', 'chamomile', 'mace blades'
                ]
            },
            # Additional specific vegetarian categories can be added here
        }

        # Function to compile regex and find matches
        def find_matches(category, ingredients):
            keywords_regex = re.compile('|'.join(category['keywords']), re.IGNORECASE)
            exclusions_regex = re.compile('|'.join(category.get('exclusions', [])), re.IGNORECASE) if category.get('exclusions') else None
            return [i for i in ingredients if keywords_regex.search(i) and (not exclusions_regex or not exclusions_regex.search(i))]

        # Aggregate all vegetarian ingredients
        vegetarian = []
        for category in vegetarian_categories.values():
            vegetarian.extend(find_matches(category, ingredients_list))

        # Remove duplicates and sort
        vegetarian = list(set(vegetarian))
        vegetarian.sort()

        return vegetarian

    def find_vegan_ingredients(ingredients_list):
        # Define vegan categories with their keywords and potential exclusions (from vegetarian and dairy categories)
        vegan_categories = {
            'vegan_varieties': {
                'keywords': [
                    r'\bvegetables\b', r'\bfruits\b', r'\blegumes\b', r'\bbeans\b', r'\btofu\b', r'\btempeh\b', 
                    r'\blentils\b', r'\bseitan\b', r'\bnuts\b', r'\bseeds\b', r'\bwhole grains\b', r'\bherbs\b', 
                    r'\bspices\b', r'\balmond milk\b', r'\bsoy milk\b', r'\brice milk\b', r'\boat milk\b',
                    r'\bplant-based\b', r'\bquinoa\b', r'\bchia\b', r'\bflaxseed\b', r'\bpeas\b', r'\bmushrooms\b',
                    r'\bavocado\b', r'\beggplant\b', r'\bzucchini\b', r'\bsquash\b', r'\bpeppers\b', r'\btomatoes\b',
                    r'\bsweet potatoes\b', r'\bcarrots\b', r'\bcauliflower\b', r'\bbroccoli\b', r'\basparagus\b',
                    r'\bbrussels sprouts\b', r'\bspinach\b', r'\bkale\b', r'\bgarlic\b', r'\bonions\b',
                    r'\bsalt\b', r'\bsugar\b', r'\bolive oil\b', r'\bflour\b', r'\bgarlic cloves\b', r'\bpepper\b',
                    r'\bbrown sugar\b', r'\bgarlic\b', r'\ball-purpose flour\b', r'\bvegetable oil\b', r'\bvanilla\b',
                    r'\bblack pepper\b', r'\bcinnamon\b', r'\bgarlic powder\b', r'\bvanilla extract\b', r'\boil\b',
                    r'\bonions\b', r'\bcelery\b', r'\bcarrots\b', r'\bsoy sauce\b', r'\bpaprika\b',
                    r'\blemon juice\b', r'\bextra virgin olive oil\b', r'\bfresh parsley\b', r'\bcornstarch\b',
                    r'\bfresh ground black pepper\b', r'\bparsley\b', r'\bchili powder\b', r'\bground cinnamon\b',
                    r'\blemon\b', r'\bpotatoes\b', r'\bnutmeg\b', r'\bcayenne pepper\b', r'\bgranulated sugar\b',
                    r'\bground cumin\b', r'\bwalnuts\b', r'\bpecans\b', r'\bdijon mustard\b', r'\bkosher salt\b',
                    r'\bpowdered sugar\b', r'\bfresh lemon juice\b', r'\bmargarine\b', r'\bdried oregano\b',
                    r'\borange juice\b', r'\bzucchini\b', r'\braisins\b', r'\bred bell pepper\b', r'\btomato sauce\b',
                    r'\bfresh cilantro\b', r'\btomato paste\b', r'\bcanola oil\b', r'\bgreen pepper\b', r'\bfresh ginger\b',
                    r'\bcumin\b', r'\boregano\b', r'\bjuice of\b', r'\bground black pepper\b', r'\bketchup\b',
                    r'\bbalsamic vinegar\b', r'\blime juice\b', r'\bcilantro\b', r'\bground ginger\b', r'\bfresh basil\b',
                    r'\bginger\b', r'\bonion powder\b', r'\bdried thyme\b', r'\bdiced tomatoes\b', r'\bvinegar\b',
                    r'\bgreen bell pepper\b', r'\bbay leaf\b', r'\bdried basil\b', r'\bwhite sugar\b', r'\bred wine vinegar\b',
                    r'\bfresh ground pepper\b', r'\bsea salt\b', r'\bdry white wine\b', r'\bsalt & freshly ground black pepper\b',
                    r'\bwhole wheat flour\b', r'\blight brown sugar\b', r'\bsesame oil\b', r'\bthyme\b', r'\bcurry powder\b',
                ],
                'exclusions': [
                    'meat', 'pork', 'lamb', 'chicken', 'beef', 'duck', 'buffalo', 'poultry', 'cod', 'fish', 'sushi', 
                    'tuna', 'bass', 'fillet', 'ribs', 'trout', 'anchovy', 'barramundi', 'steak', 'basa', 'tenderloin', 
                    'bison', 'angus', 'salmon', 'snapper', 'liver', 'pollo', 'plaice', 'pickerel', 'ostrich', 'roughy', 
                    'opah', 'perch', 'pike', 'ahi', 'marlin', 'crab', 'mackerel', 'loin', 'lobster', 'leg', 'sausage', 
                    'frankfurt', 'lean', 'shark', 'whale', 'dolphin', 'clam', 'kidney', 'heart', 'brain', 'tongue', 
                    'arm roast', 'bear', 'rump', 'round roast', 'broil', 'caribou', 'deer', 'blade', 'chuck', 'elk', 
                    'ham', 'turkey', 'mortadella', 'kangaroo', 'kobe', 'mahi', 'alligator', 'crocodile', 'llama', 
                    'bangus', 'bacon', 'antelope', 'egg', 'dairy', 'milk', 'yogurt', 'butter', 'cream', 'cheese', 
                    'ice cream', 'curd', 'whey', 'casein', 'ghee', 'kefir', 'paneer', 'condensed milk', 'evaporated milk', 
                    'milk powder', 'honey'
                ]
            },
            # Additional specific vegan categories can be added here
        }

        # Function to compile regex and find matches
        def find_matches(category, ingredients):
            keywords_regex = re.compile('|'.join(category['keywords']), re.IGNORECASE)
            exclusions_regex = re.compile('|'.join(category.get('exclusions', [])), re.IGNORECASE) if category.get('exclusions') else None
            return [i for i in ingredients if keywords_regex.search(i) and (not exclusions_regex or not exclusions_regex.search(i))]

        # Aggregate all vegan ingredients
        vegan = []
        for category in vegan_categories.values():
            vegan.extend(find_matches(category, ingredients_list))

        # Remove duplicates and sort
        vegan = list(set(vegan))
        vegan.sort()

        return vegan
    

    dairy_ingredients = find_dairy_ingredients(ingredients_list)
    gluten_ingredients = find_gluten_ingredients(ingredients_list)
    nut_ingredients = find_nut_ingredients(ingredients_list)
    vegetarian_ingredients = find_vegetarian_ingredients(ingredients_list)
    vegan_ingredients = find_vegan_ingredients(ingredients_list)


    df['restrictions'] = np.empty((len(df), 0)).tolist()

    def categorize_dietary_restrictions(df, dairy_ingredients, gluten_ingredients, nut_ingredients, vegetarian_ingredients, vegan_ingredients):
        # Iterate over each recipe in the dataframe
        for index, row in df.iterrows():
            # Initialize an empty list to store restrictions for the current recipe
            current_restrictions = []

            # Check each ingredient in the recipe against all categories
            for ingredient in row['ingredients']:
                if ingredient in dairy_ingredients and 'Dairy' not in current_restrictions:
                    current_restrictions.append('Dairy')
                if ingredient in gluten_ingredients and 'Gluten' not in current_restrictions:
                    current_restrictions.append('Gluten')
                if ingredient in nut_ingredients and 'Nuts' not in current_restrictions:
                    current_restrictions.append('Nuts')
                if ingredient in vegetarian_ingredients and 'Vegetarian' not in current_restrictions:
                    current_restrictions.append('Vegetarian')
                if ingredient in vegan_ingredients and 'Vegan' not in current_restrictions:
                    current_restrictions.append('Vegan')

            # Update the restrictions for the recipe in the dataframe
            df.at[index, 'restrictions'] = current_restrictions

    # Call the function with the dataframe and the ingredient categories
    categorize_dietary_restrictions(df, dairy_ingredients, gluten_ingredients, nut_ingredients, vegetarian_ingredients, vegan_ingredients)

    # Filter the DataFrame to keep rows with more than 1 item in 'restrictions'

    df.to_csv("../data/Processed/df_recipes_final.csv", index=False)

    df_filtered = df[df['restrictions'].apply(lambda x: len(x) > 1)]

    df_filtered.to_csv("../data/Processed/df_recipes_final_filtered.csv", index=False)

    # Sort the DataFrame based on 'unique_value' of ingredients column alphabetically
    sorted_df_ingredients = df_ingredients.sort_values(by=['unique_value','count'], ascending=True,)
    # Export the sorted 'unique_value' of ingredients column to a CSV file
    sorted_df_ingredients.to_csv("../data/Processed/unique_values/ingredients_sorted_unique_values.csv", index=True)

    # Sort the DataFrame based on 'unique_value' of tags column alphabetically
    sorted_df_tags_unique = df_tags_unique.sort_values(by='count', ascending=True)
    # Export the sorted 'unique_value' of tags column to a CSV file
    sorted_df_tags_unique.to_csv("../data/Processed/unique_values/tags_sorted_unique_values.csv", index=True)
    df_tags_unique.to_csv("../data/Processed/unique_values/df_tags.csv")

    # Creating a nutrition DataFrame by extracting and formatting nutrition data.
    nutrition_df.to_csv("../data/Processed/df_streamlit/df_recipes_final_nutrition.csv")

    def split_dataframe_columns(df, columns_to_split):
        """
        Splits specified columns from the original DataFrame into separate DataFrames, each with 'recipe_id'.
        The specified columns and 'nutrition' column are dropped from the original DataFrame.

        Parameters:
        df (pandas.DataFrame): The original DataFrame.
        columns_to_split (list): List of column names to split into separate DataFrames.

        Returns:
        dict: A dictionary containing the modified original DataFrame and new DataFrames for each specified column.
        """
        new_dfs = {}

        # Create new DataFrames for each specified column
        for column in columns_to_split:
            new_dfs[f"df_{column}"] = df[['recipe_id', column]].copy()

        # Drop specified columns and 'nutrition' from the original DataFrame
        df = df.drop(columns=columns_to_split + ['nutrition'] + ["ingredient_group"]+ ["cooking_time"])

        # Add the modified original DataFrame to the dictionary
        new_dfs['original_df'] = df

        return new_dfs

    columns_to_extract = ['tags', 'steps', 'description']
    result_dfs = split_dataframe_columns(df_filtered, columns_to_extract)

    # Access the modified original DataFrame
    modified_df = result_dfs['original_df']

    # Access the new DataFrames
    df_tags = result_dfs['df_tags']
    df_steps = result_dfs['df_steps']
    df_description = result_dfs['df_description']

    modified_df.to_csv("../data/Processed/df_streamlit/df_recipes_final_filtered_dropped.csv", index=False)
    df_tags.to_csv("../data/Processed/df_streamlit/df_recipes_final_tags.csv", index=False)
    utils.split_and_save_df(df_steps, "../data/Processed/df_streamlit/df_recipes_final_steps", len(df_steps) // 2)    
    df_description.to_csv("../data/Processed/df_streamlit/df_recipes_final_description.csv", index=False)