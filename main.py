# Syna Gogte

import requests
from bs4 import BeautifulSoup
import json


def fetch_menu_data():
    url = 'https://hospitality.usc.edu/residential-dining-menus/'
    response = requests.get(url)
    menu_data = []
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        menu_container = soup.find('div', class_='fw-accordion-custom meal-section')

        meal_container = menu_container.find_all('div', class_='hsp-accordian-container')

        for menu_item in meal_container:
            menu_meal = menu_item.find('h2', class_='fw-accordion-title ui-state-active')
            meal_title = menu_meal.find('span', class_='fw-accordion-title-inner').text.strip()
            meal_name = meal_title.split()[0]
            menu_item_data = {'date': meal_title.split()[4] + " " + meal_title.split()[5] + " " + meal_title.split()[6],
                              'meal': meal_name,
                              'locations': []}

            for item in menu_item.find_all('div', class_='col-sm-6 col-md-4'):
                item_loc = item.find('h3').text.strip()
                loc_data = {'loc': item_loc, 'items': []}

                menu_food = item.find_all('ul', class_='menu-item-list')

                if menu_food:
                    for food in menu_food:
                        item_cat = food.find_previous_sibling("h4").text.strip()
                        cat_data = {'category': item_cat, 'foods': []}

                        li_elements = food.find_all('li')

                        for li in li_elements:
                            text = ''.join([string for string in li.strings if string.parent.name != 'span']).strip()
                            food_data = {'food': text, 'allergen_data': []}

                            allergen_data = li.find('span', class_='fa-allergen-container').find_all('span')
                            for allergen in allergen_data:
                                food_data['allergen_data'].append(allergen.text)

                            cat_data['foods'].append(food_data)

                        loc_data['items'].append(cat_data)

                loc_file_name = f"{meal_name.lower()}_{item_loc.lower().replace('/', '_').replace(' ', '_')}_menu.json"
                with open(loc_file_name, "w") as json_file:
                    json.dump(loc_data, json_file)

                menu_item_data['locations'].append(loc_data)
            menu_data.append(menu_item_data)

    else:
        print(f"Error: {response.status_code}")

    return menu_data


# Call the function to fetch the menu data
data = fetch_menu_data()

with open("food.json", "w") as json_file:
    json.dump(data, json_file)

