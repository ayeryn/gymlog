import calendar
import os

class Report:

    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.cal = calendar.month(int(self.year), int(self.month))
        self.name = os.getcwd() + '/' + self.year + self.month + '.csv'
        self.title = 'Monthly Report {}/{}'.format(self.year, self.month)
    
    def print_attrs(self):
        msg = 'month = {}\nyear = {}\n'.format(self.month, self.year)
        msg += 'cal = {}\nname = {}\n'.format(self.cal, self.name)
        print(msg)
        
