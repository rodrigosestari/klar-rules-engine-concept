from business_rules import run_all
from product import ProductVariables, ProductActions,Product
from rule import rulesBase

rules = rulesBase().return_rule()

for product in Products.objects.all():
    run_all(rule_list=rules,
            defined_variables=ProductVariables(product),
            defined_actions=ProductActions(product),
            stop_on_first_trigger=True
            )
