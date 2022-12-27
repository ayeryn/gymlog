from Report import MonthlyReport
import re


def get_input():
    """ Gather year and month from user

    When ALL mode is selected return 0 for month
    """
    year, month = 0, 0
    q = 'What year would you like to generated the report? (yyyy)\n'

    year = input(q)
    while not (re.fullmatch('\d{4}$', year)):
        year = input(q)

    q = 'What month? a for ALL months or mm\n'
    month = input(q)
    while not ((re.fullmatch('\d{2}$', month)) or month == 'a'):
        month = input(q)

    if month == 'a':
        month = 0

    return year, month


def main():

    year, month = get_input()

    # year, month = '2022', '12'

    report = MonthlyReport(month, year)
    report.print_report()


main()
