from selenium import webdriver 
import re
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time

#https://sites.google.com/chromium.ord/driver/

# Define a method to get user input for the number of teams
from bs4 import BeautifulSoup
all_event_titles = []
all_event_lines = []
all_event_odds = []
# Create a set from the teams for efficient membership testing
teams = []
exact_teams = []  # List for teams with exact names
teams_set = set(teams)
exact_teams_set = set(exact_teams)

event_titles = []
event_lines = []
event_odds = []
def driver_loop(sport):
    global event_titles, event_lines, event_odds, teams  # Declare the variables as global

    print(sport)
    sport_string = "https://bovada.lv/sports/" + sport.lower()
    print (sport_string)
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(sport_string)
    print(driver.title)
    # Wait for elements with the class "event-title" to be present
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event-title")))


    # Get the page source after the page is loaded
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    # Find all elements with the class name "event-title"
    event_titles = soup.find_all(class_="competitor-name")
    event_lines = soup.find_all(class_="market-line bet-handicap")
    event_odds = soup.find_all(class_="bet-price")
    # num_odds = len(event_odds)
    # print(num_odds)
    # num_titles = len(event_titles)
    # print(num_titles)
    time.sleep(2)

    driver.quit()
odds = ""
odds_list = []

def odds_calculator(odd):
    odd += ""
    if '-' in odd:
        # Remove the negative sign and convert to int
        if '(' in odd:
            modified_odd = odd[3:-2]
            odd += ""
            print(modified_odd)
            numeric_value = int(modified_odd)
        else:
            numeric_value = int(odd[2:])
        # Apply the formula for negative odds
        decimal_odds = (100 / numeric_value) + 1
    elif '+' in odd:
        if '(' in odd:
            modified_odd = odd[3:-2]
            odd += ""
            print(modified_odd)
            numeric_value = int(modified_odd)
        else:
            numeric_value = int(odd[2:])
        decimal_odds = (numeric_value / 100) + 1
    else:
        # Handle the case where odd does not start with '+' or '-'
        return
    # Append the result to odds_list
    odds_list.append(decimal_odds)
# odds_calculator("-150")
# odds_calculator("+150")
# print(odds_list)
def decimal_to_american(decimal):
    total_decimal = 1
    final_parlay_odds = 1
    for item in decimal:
        total_decimal *= item
    
    if total_decimal < 2.00:
        final_parlay_odds = str(int((-100) / (total_decimal - 1)))
    else: 
        final_parlay_odds = "+" + str(int((total_decimal - 1) * 100))
    return final_parlay_odds


def get_num_teams():
    while True:
        num_teams = input("Enter the number of teams you would like to look up: ")
        try:
            # Attempt to convert the input to an integer
            int_teams = int(num_teams)
            return int_teams  # Return the valid integer
        except ValueError:
            # Handle the case where the input is not a valid integer
            print("Invalid input. Please enter a valid integer.")

def get_num_sports():
    while True:
        num_sports = input("Enter the number of sports you would like to look up: ")
        try:
            # Attempt to convert the input to an integer
            int_sports = int(num_sports)
            return int_sports  # Return the valid integer
        except ValueError:
            # Handle the case where the input is not a valid integer
            print("Invalid input. Please enter a valid integer.")

diff_sports = []
count_teams = 0
int_sports = get_num_sports()
if int_sports > 0: 
    while count_teams < int_sports:
        sport_name = input(f"Enter sport #{count_teams + 1}: ")
        diff_sports.append(sport_name)
        count_teams += 1

    # Now, the diff_sports list will contain the names of different sports entered by the user.
    print("Different sports entered:")
    for sport in diff_sports:
        print(sport)
        
#int_teams = get_num_teams()



spread_teams = [] 
moneyline_teams = []
spread_set = set(spread_teams)
moneyline_set = set(moneyline_teams)
count = 0 
counter = 0
while counter < int_sports:
    print(diff_sports[counter])
    
    int_teams = get_num_teams()

    while count < int_teams:

        team  = input("Enter the name of one team you would like to look up or enter exit to quit: ")
        pattern = re.compile(r'^[a-zA-Z0-9#\(\) ]+\.?$')  # Allow letters, numbers, '#', '(', ')', and an optional period at the end
        if team.lower() == 'exit':
            break
        # Check if the user input matches the pattern
        if pattern.match(team):
            
            # Check if the input ends with a period
            if team.endswith('.'):
                while True:
                    spread_or_moneyline = input("Spread? Enter 'y' for Yes and 'n' for No: ")

                  # Remove the period and add to exact_teams
                    if spread_or_moneyline.lower() == ("y"):
                        #print("I made it here")
                        exact_teams.append(team.lower()[:-1])
                        spread_teams.append(team.lower()[:-1])
                        break
                    elif spread_or_moneyline.lower() == ("n"):
                        exact_teams.append(team.lower()[:-1])
                        moneyline_teams.append(team.lower()[:-1])
                        break
                    else: 
                        print("Invalid input, Please only input 'y' or 'n'")
                

            else:
                while True:
                    spread_or_moneyline = input("Spread? Enter 'y' for Yes and 'n' for No: ")

                    teams.append(team)
                    if spread_or_moneyline.lower() == ("y"):
                        #print("I made it here")
                        spread_teams.append(team.lower())
                        teams.append(team)
                        break

                    elif spread_or_moneyline.lower() == "n":
                        teams.append(team)
                        moneyline_teams.append(team.lower())
                        break
                    else: 
                        print("Invalid input, Please only input 'y' or 'n'")
            count += 1
        else:
            print("Input contains characters other than letters or an incorrect period format.")
    driver_loop(diff_sports[counter])
    all_event_titles.extend(event_titles)
    all_event_lines.extend(event_lines)
    all_event_odds.extend(event_odds)
    counter += 1
    #driver_loop(diff_sports[counter])

    count = 0


for team in teams:
    #print(team + " no")
    teams_set.add(team)


for team in exact_teams:
    #print(team + " Yes")
    exact_teams_set.add(team)

for team in spread_teams:
    #print(team + " Spread")
    spread_set.add(team)


for team in moneyline_teams:
    #print(team + " Moneyline")
    moneyline_set.add(team)




import datetime

# Get the current date and time
current_datetime = datetime.datetime.now()

# Print the current date
print("Date:", current_datetime.date())
num_odds = len(all_event_odds)
print(num_odds)

current_odds_index = 0
count = 1
for all_event_title, all_event_line in zip(all_event_titles, all_event_lines):
    # Extract and print the team and spread
    
    team = all_event_title.text
    spread = all_event_line.text
    #print(all_event_title.text)
    # Extract and print the spread odds (current_odds_index) and moneyline odds (current_odds_index + 1)
    spread_odds = all_event_odds[current_odds_index].text
    current_odds_index += 2
    moneyline_odds = all_event_odds[current_odds_index].text

    # Increment the current_odds_index by 2 to skip over the over/under odds
    current_odds_index -= 1
    if team.lower() in exact_teams_set:
        #print("Exact")
        if team.lower() in spread_set:
            odds_calculator(spread_odds)
            print(f"Exact Team: {team}, Spread: {spread}, Spread Odds: {spread_odds}")
        elif team.lower() in moneyline_set:
            odds_calculator(moneyline_odds)
            print(f"Exact Team: {team}, Moneyline Odds: {moneyline_odds}")


       # print(f"Exact Team: {team}, Spread: {spread}, Spread Odds: {spread_odds}, Moneyline Odds: {moneyline_odds}")

              
    elif any(partial_team.lower() in team.lower() for partial_team in teams_set):
       # print("Not Exact")
        #print(team.lower())
        if any(partial_team.lower() in team.lower() for partial_team in spread_set):
            odds_calculator(spread_odds)
            print(f"Team: {team}, Spread: {spread}, Spread Odds: {spread_odds}")
        else: #if team.lower() in moneyline_set:
            odds_calculator(moneyline_odds)
            print(f"Team: {team}, Moneyline Odds: {moneyline_odds}")
        #print(f"{team}: Spread: {spread}, Spread Odds: {spread_odds}, Moneyline Odds: {moneyline_odds}")
    
     # Check if the boolean variable is True and the counter is even
    if count % 2 == 0:
    # Do something when both conditions are met
        # print("Both conditions are met.")
         if (num_odds - 1 < current_odds_index + 4):
             break
         else:
             current_odds_index += 4
         
    count += 1
parlay = decimal_to_american(odds_list)
print("Total Parlay Odds: " + parlay)

        

