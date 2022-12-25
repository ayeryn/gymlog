import calendar
import os

class Report:

    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.cal = calendar.month(int(self.year), int(self.month))
        self.name = os.getcwd() + '/' + self.year + self.month + '.csv'
        self.title = 'Monthly Report {}/{}'.format(self.year, self.month)

        # Initialize data structures 
        self.attendance = {}
    
    def print_attrs(self):
        msg = 'month = {}\nyear = {}\n'.format(self.month, self.year)
        msg += 'cal = {}\nname = {}\n'.format(self.cal, self.name)
        print(msg)
        
    def process_jnl(self):
        """Return a dict of class:attendance

        Read monthly workout journal to dictionary
        """

        with open(self.name, 'r') as f:
            for line in f:
                temp = line.split(',')
                self.attendance[temp[0]] = temp[1].title()

    def print_attendance(self):
        for k, v in self.attendance.items():
            print('{:>2}: {}'.format(k, v))
        