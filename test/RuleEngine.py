import csv

from business_rules import run_all
from business_rules.actions import *
from business_rules.operators import *
from business_rules.variables import *


def read_csv():
    rules = []
    f = open('rules.csv')
    csvFile = csv.reader(f)
    for row in csvFile:
        count = 0
        while count < len(row):
            rules.append(row[count].strip())
            count += 1
    rules = filter(None, rules)
    for item in rules:
        if item.lower() == 'parameter':
            rules.remove(item)
    return rules

def make_conditions(list):
    conditions = []
    outer_list = list
    k = 0
    while k < len(outer_list):
        if list[k].upper() == "CONDITION":
            condition = {"name": list[k + 1], "operator": list[k + 2], "value": int(list[k + 3])}
            k += 4
            conditions.append(condition)
    return conditions


def make_actions(list):
    actions = []
    m = 0
    while m < len(list):
        if list[m].upper() == 'ACTION':
            action = {'name': list[m + 1], 'params': {list[m + 2]: float(list[m + 3])}}
            m += 4
            actions.append(action)
    return actions


def make_rules():
    rules = []
    list = read_csv()
    i = 0
    next_rule = 0
    while len(list) != 0:
        if list[i].upper() == 'RULE':
            list.pop(i)
            if 'rule' not in list:
                action = list.index('action')
                conditions = list[0:action]
                actions = list[action:]
                list = []
            else:
                next_rule = list.index('rule')
                action = list.index('action')
                conditions = list[0:action]
                actions = list[action:next_rule]
                list = list[next_rule:]
            rules.append({'conditions': {'all': make_conditions(conditions)}, 'actions': make_actions(actions)})
    print(rules)
    return rules


class TestA:
    def __init__(self):
        self.current_inventory = 24
        self.days_last_sold = 5
        self.price = 10.00


class ProductVariables(BaseVariables):
    def __init__(self, product):
        self.product = product

    @numeric_rule_variable
    def current_inventory(self):
        return self.product.current_inventory

    @numeric_rule_variable
    def days_last_sold(self):
        return self.product.days_last_sold


class ProductActions(BaseActions):
    def __init__(self, product):
        self.product = product

    @rule_action(params={'sales_percentage': FIELD_NUMERIC})
    def increase_price(self, sales_percentage):
        self.product.new_price = (1.0 + sales_percentage) * self.product.price
        print('Price went up from ' + str(self.product.price) + ' to ' + str(self.product.new_price))


rules_old = [
    {"conditions": {
        "all": [
            {
                "operator": "greater_than",
                "name": "days_last_sold",
                "value": 4,
            }
        ]},
        "actions": [
            {"name": "increase_price",
             "params": {"sales_percentage": 0.1},
             }
        ]
    }
]

rules = make_rules()

p = TestA()
print(p.current_inventory)
print(p.days_last_sold)
print(type(p.days_last_sold))

product = ProductVariables(p)
print(product.current_inventory())
print(product.days_last_sold())
print(type(product.days_last_sold()))

run_all(rule_list=rules,
        defined_variables=ProductVariables(p),
        defined_actions=ProductActions(p),
        stop_on_first_trigger=True
        )
