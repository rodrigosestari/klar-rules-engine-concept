import datetime

from business_rules.actions import rule_action, BaseActions
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable


# https://github.com/venmo/business-rules
class BuroDeCredito:
    def __init__(self, current_balance, credit_limit, start_date, maximum_amount_owed):
        self.current_balance = current_balance
        self.credit_limit = credit_limit
        self.start_date = start_date
        self.maximum_amount_owed = maximum_amount_owed
        self.initial_score = 0


class BuroDeCreditoVariables(BaseVariables):
    def __init__(self, buro):
        self.buro = buro

    @numeric_rule_variable
    def current_balance(self):
        return self.buro.current_balance

    @numeric_rule_variable
    def credit_limit(self):
        return self.buro.credit_limit

    @string_rule_variable()
    def start_date(self):
        return self.buro.start_date

    @numeric_rule_variable
    def maximum_amount_owed(self):
        return self.buro.maximum_amount_owed


class BuroDeCreditoActions(BaseActions):
    def __init__(self, buro):
        self.buro = buro

    @rule_action(params={'score_positive': FIELD_NUMERIC})
    def current_balance_less(self, score_positive):
        print("current_balance_less previus score_positive" + str(self.buro.initial_score))
        self.buro.initial_score += score_positive
        print("current_balance_less previus score_positive" + str(self.buro.initial_score))


rules = [
    # expiration_days < 5 AND current_inventory > 20
    {"conditions": {"any": [
        {"name": "current_balance",
         "operator": "less_than",
         "value": 100,
         },
        {"name": "current_balance",
         "operator": "greater_than",
         "value": 150,
         },
    ]},
        "actions": [
            {"name": "current_balance_less",
             "params": {"score_positive": 0.25},
             },
        ],
    }]

from business_rules import run_all

listOfBurros = [BuroDeCredito(120120, 1020, datetime.datetime.now(), 2120210)]
for product in listOfBurros:
    rule_was_triggered = run_all(rule_list=rules,
                                 defined_variables=BuroDeCreditoVariables(product),
                                 defined_actions=BuroDeCreditoActions(product),
                                 stop_on_first_trigger=True
                                 )
from business_rules import export_rule_data

json = export_rule_data(BuroDeCreditoVariables, BuroDeCreditoActions)
print(rule_was_triggered)
import json

json_string = json.dumps(rules)

# Writing JSON data
with open("rules.json", 'w') as f:
    json.dump(rules, f)
