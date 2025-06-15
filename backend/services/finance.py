# пока простая логика на память

class FinanceService:
    def __init__(self):
        self.data = {}

    def add_expense(self, user_id, amount, category):
        self.data.setdefault(user_id, []).append((amount, category))

    def get_expenses(self, user_id):
        return self.data.get(user_id, [])
