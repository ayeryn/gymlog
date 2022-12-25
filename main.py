from Report import Report
# import Class
# import re


def main():
    # q = 'What month would you like to generated the report? (yyyymm)\n'
    # request = input(q)
    # while not (request.isnumeric() and len(request) == 6) :
    #     request = input(q)
        
    # year = request[:4]
    # month = request[4:]

    year = '2022'
    month = '12'

    report = Report(month, year)
    report.process_jnl()
    report.generate_report()
    report.print_report()

main()