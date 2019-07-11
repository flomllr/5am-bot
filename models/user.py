class User(object):

    def __init__(self, full_name, weekly_awakenings, total_awakenings, average, median, missed_weeks, paid, debt):
        self.full_name = full_name
        self.weekly_awakenings = weekly_awakenings
        self.total_awakenings = total_awakenings
        self.average = average
        self.median = median
        self.missed_weeks = missed_weeks
        self.paid = paid
        self.debt = debt

    def json(self):
        return {
            'full_name': self.full_name,
            'weekly_awakenings': self.weekly_awakenings,
            'total_awakenings': self.total_awakenings,
            'average': self.average,
            'median': self.median,
            'missed_weeks': self.missed_weeks,
            'paid': self.paid,
            'debt': self.debt
        }