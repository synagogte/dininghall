import requests
from bs4 import BeautifulSoup
import json


def fetch_menu_data():
    # print("input a date")
    # month, day, year = input().split()
    # print(month + " " + day + " " + year)
    url = 'https://hospitality.usc.edu/residential-dining-menus/'
    # url = 'https://hospitality.usc.edu/residential-dining-menus/?menu_date=' + month + '+' + day + '%2C+' + year
    # print(url)
    # full url including a date:
    # https://hospitality.usc.edu/residential-dining-menus/?menu_date=August+27%2C+2023
    response = requests.get(url)
    menu_data = []
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Locate the menu container element
        menu_container = soup.find('div', class_='fw-accordion-custom meal-section')
        # print("container: " + str(menu_container))
        # Find all menu items within the container
        meal_container = menu_container.find_all('div', class_='hsp-accordian-container')
        print("meal container: " + str(meal_container))
        for menu_item in menu_container:
            menu_meal = menu_item.find('h2', class_='fw-accordion-title ui-state-active')
            meal_title = menu_meal.find('span', class_='fw-accordion-title-inner').text.strip()
            # print("date: " + meal_title.split()[4] + meal_title.split()[5] + meal_title.split()[6])
            print(meal_title.split()[4] + " " + meal_title.split()[5] + " " + meal_title.split()[6])
            print(meal_title.split()[0])
            menu = menu_item.find_all('div', class_='col-sm-6 col-md-4')
            # print("menu: " + str(menu))
            # Process the menu items as needed
            menu_data.append({'date': meal_title.split()[4] + " " + meal_title.split()[5] + " " + meal_title.split()[6]})
            menu_data.append({'meal': meal_title.split()[0]})
            for item in menu:
                item_loc = item.find('h3').text.strip()
                # menu_data.append({'loc': item_loc, 'food': item_description})
                print("loc:" + str(item_loc))
                menu_data.append({'loc': item_loc})
                menu_food = item.find_all('ul', class_='menu-item-list')  # how many places in the dining hall
                if menu_food:
                    for food in menu_food:
                        item_cat = food.find_previous_sibling("h4").text.strip()
                        print("category:" + item_cat)
                        menu_data.append({'category': item_cat})
                        li_elements = food.find_all('li')

                        for li in li_elements:
                            text = ''.join([string for string in li.strings if string.parent.name != 'span']).strip()
                            print("food:" + text)
                            menu_data.append({'food': text})
                            skip = li.find('span', class_='fa-allergen-container')
                            allergen_data = skip.find_all('span')
                            for allergen in allergen_data:
                                print(allergen.text, end=' | ')
                                menu_data.append({'allergen data': allergen.text})
                            print()

            print("")

    else:
        # Handle error if the website couldn't be accessed
        print(f"Error: {response.status_code}")

    return menu_data


# Call the function to fetch the menu data
data = fetch_menu_data()
with open("data.json", "w") as json_file:
    json.dump(data, json_file)
