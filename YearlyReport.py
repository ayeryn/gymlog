from Report import MonthlyReport
# import calendar


class YearlyReport(MonthlyReport):

    def __init__(self, year):
        self.year = year
        self.title = 'Yearly Report ' + str(year)

        # Initialize attrs
        self.attendance = {}
        self.classes = set()
        self.class_tally = {}
        self.report_str = ''
        self.total_classes = 0
        self.num_of_weeks = 0
        self.cal = []
        self.files = []
