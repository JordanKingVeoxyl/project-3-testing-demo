"""
Import section
"""
import sys
import gspread
from google.oauth2.service_account import Credentials
from termcolor import colored

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_ireland')

def greeting 
    """
    Function to ask the user to input their name and then greets them.
    """
    print(' Hello! Welcome to Love Ireland. Here at Love Ireland we would love to hear')
    print(' about your experiences with the top most loved counties in Ireland.')
    print(' We would also love to offer you a personalised tour guide plan for')
    print(' the counties that you havent got to visit yet!')
    name = input('First of all, we would love to know your name. Please enter your name: ') 
    print('Hello', name, '! Lets get started.')

def county_and_score(county_name, score)
    """
    Function to return a list of the top 3 popular counties in Ireland & their scores together.
    """
    print(' Below you shall find a list of available counties,')
    print(' along with their user scores.\n')

    for county_name, score in zip(county_name, score):
        print(colored(
            (f' County title: {county_name}\n User score: {score} / 5 stars\n'),
            'cyan'))

    print(' Enter "1" if you would like to learn how to explore a new county.')
    print(' Enter "2" if you would like to submit a score for a county you')
    print(' have already tried.\n')


# This function is based on the 'Love Sandwiches' walk through.
def county_titles():
    """
    Function to return a list of the available county titles to choose from.
    """
    counties = SHEET.worksheet('scores')
    county_names = []
    for ind in range(1, 4):
        county_name = counties.col_values(ind)
        county_names.append(county_name[0])

    return county_names


def index_titles():
    """
    Function to index popular counties
    """
    county_names = county_titles()
    index = 1
    for county_name in county_names:
        print(colored((f' {index}. {county_name}'), 'cyan'))
        index += 1


# This function is based on the 'Love Sandwiches' walk through.
def get_user_score():
    """
    Function to get all of the user scores, and return data as a list of data.
    """
    scores = SHEET.worksheet('scores')
    columns = []
    for ind in range(1, 4):
        column = scores.col_values(ind)
        columns.append(column[1:])

    return columns


def calculate_average_score(data):
    """
    A mathmatical function that takes the data generated in the get_user_score(): function
    And returns an average of all the scores inputted.
    """
    average_score = []
    for column in data:
        score_count = 0
        score_total = 0

        for num in column:
            if num:
                score_count += 1
                score_total += int(num)

        average = score_total / score_count
        average_score.append(round(average, 2))

    return average_score


def rate_or_retrieve():
    """
    A function to determine which option the user would like to proceed with.
    They may either rate a county they have previously explored,
    Or get information/tour guide of a new county to explore to be able to review
    at a later stage.
    """
    option = input(" Make your selection, 1 county or 2 score:\n ")
    if option == '1':
        retrieve_county()
    elif option == '2':
        submit_score()
    else:
        print(colored(
            ('\n Invalid choice. You may only choose 1 or 2\n'), 'red'))
        return rate_or_retrieve()


def retrieve_county():
    """
    A function to display popular county names once more,
    and allow the user to select a county to retrieve.
    """
    print('\n Select the county you would like to retrieve information on.')
    print(' Choose the county based on its numberical value.\n')

    index_titles()

    selection = input('\n Please select a county to retrieve information about:\n ')

    if selection == '1':
        travel_guide_list('dublin')
    elif selection == '2':
        travel_guide_list('cork')
    elif selection == '3':
        travel_guide_list('galway')
    else:
        print(colored(('\n Invalid choice.'), 'red'))
        print(colored(
            (' You may only choose one of the listed options.\n'), 'red'))
        return retrieve_county()

    print(colored(('\n Happy exploring!'), 'magenta'))
    quit_repeat()


def travel_guide_list(county):
    """
    Function to return a locations list & full guide instructions.
    """
    travel_guide = SHEET.worksheet(county)

    all_rows = []
    for ind in range(1, 5):
        all_col = travel_guide.col_values(ind)
        all_rows.append(all_col[1:])

    location = all_rows[0]
    closes_at = all_rows[1]
    recommended_time_to_spend_at = all_rows[2]
    guide_instructions = all_rows[3]

    print(colored(('\n Locations list:\n'), 'magenta'))
    for (location, closes_at, recommended_time_to_spend_at) in zip(location, closes_at, recommended_time_to_spend_at):
        print(colored((f' {location} - {closes_at}{recommended_time_to_spend_at}'), 'cyan'))

    print(colored(('\n Guide Instructions:\n'), 'magenta'))
    for guide_instruction in guide_instructions:
        print(colored((guide_instruction), 'cyan'))


def submit_score():
    """
    Function to display county names once more,
    and allow the user to select a title to rate.
    """
    print('\n Select the county you would like to rate.')
    print(' Choose the county by the numberical value.')
    print(' Enter a score between 1-5. Whole numbers ONLY.')
    print(' 1 being the worst, 5 the best.\n')

    index_titles()

    selection = input('\n Please select a county to submit a score for:\n ')
    update_score = SHEET.worksheet('scores')

    if selection == '1':
        input_score = user_scores()
        update_score.append_row([input_score[0], '', ''])
    elif selection == '2':
        input_score = user_scores()
        update_score.append_row(['', input_score[0], ''])
    elif selection == '3':
        input_score = user_scores()
        update_score.append_row(['', '', input_score[0]])
    else:
        print(colored(('\n Invalid choice.'), 'red'))
        print(colored(
            (' You may only choose one of the listed options.\n'), 'red'))
        return submit_score()

    print('\n Thank you for your review!')
    quit_repeat()


def user_scores():
    """
    Accepts the user input to determine if the score is valid.
    To be used within the 'submit_score' function.
    """
    score = []
    while True:
        try:
            star_score = int(input(' Submit your score: \n '))
            break
        except ValueError:
            print(colored(
                (' \nYou must enter a number between 1 and 5'), 'red'))
            continue
    if star_score <= 5:
        score.append(star_score)
        return score
    else:
        print(colored((' \nYou must enter a number between 1 and 5'), 'red'))
        user_scores()

    return score


def quit_repeat():
    """
    Function to allow the user to either quit the program,
    or restart it and select '1' or '2' again.
    """
    print('\n Enter: "R" to restart the application.')
    print('\n Enter: "Q" to quit the application.\n')
    option = input(" Enter your selection:\n ").upper()
    if option == 'R':
        main()
    elif option == 'Q':
        sys.exit('\n Thank you for your participation & slán!')
    else:
        print(colored((' \nInvalid choice. Enter: R or Q only please.\n'), 'red'))
        return quit_repeat()


def main():
    """
    Call all program functions.
    """
    user_scores = get_user_score():
    average_score = calculate_average_score(user_scores)
    county_name = county_titles()
    county_and_score(county_name, average_score)
    rate_or_retrieve()


print(colored(("\n Welcome to Love Ireland. Let's begin!"), 'green'))
print(colored((" Welcome to Love Ireland. Let's begin!"), 'white'))
print(colored((" Welcome to Love Ireland. Let's begin!\n"), 'light_red'))
main()