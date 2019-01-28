import datetime
import json

from business_rules import export_rule_data
from business_rules import run_all
from business_rules.actions import rule_action, BaseActions
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable


class Credit:
    def __init__(self, current_balance, credit_limit, start_date, maximum_amount_owed):
        self.current_balance = current_balance
        self.credit_limit = credit_limit
        self.start_date = start_date
        self.maximum_amount_owed = maximum_amount_owed
        self.initial_score = 0


class CreditVariables(BaseVariables):
    def __init__(self, credit):
        self.credit = credit

    @numeric_rule_variable
    def current_balance(self):
        return self.credit.current_balance

    @numeric_rule_variable
    def credit_limit(self):
        return self.credit.credit_limit

    @string_rule_variable()
    def start_date(self):
        return self.credit.start_date

    @numeric_rule_variable
    def maximum_amount_owed(self):
        return self.credit.maximum_amount_owed


class CreditActions(BaseActions):
    def __init__(self, credit):
        self.credit = credit

    @rule_action(params={'score_positive': FIELD_NUMERIC})
    def current_balance_less(self, score_positive):
        print("current_balance_less previus score_positive" + str(self.credit.initial_score))
        self.credit.initial_score += score_positive
        print("current_balance_less previus score_positive" + str(self.credit.initial_score))


with open("rules.json") as data_file:
    rules = json.loads(data_file.read())

listOfCredits = [Credit(120120, 1020, datetime.datetime.now(), 2120210)]
for product in listOfCredits:
    rule_was_triggered = run_all(rule_list=rules,
                                 defined_variables=CreditVariables(product),
                                 defined_actions=CreditActions(product),
                                 stop_on_first_trigger=True
                                 )

json = export_rule_data(CreditVariables, CreditActions)
print(json)
