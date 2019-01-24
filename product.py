import csv

from business_rules.actions import rule_action, BaseActions
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable


class Product:
    def __init__(self, sku, stock_item_id, title, category, sold_1_10, days_last_sold, last_sold_price, weight,
                 available, unit_cost, retail_price, inventory_went_positive, last_price_update,
                 days_ago_created, bc_id):
        self.sku = sku
        self.stock_item_id = stock_item_id
        self.title = title
        self.category = category
        self.sold_1_10 = sold_1_10
        self.days_last_sold = days_last_sold
        self.last_sold_price = last_sold_price
        self.weight = weight
        self.available = available
        self.unit_cost = unit_cost
        self.retail_price = retail_price
        self.inventory_went_positive = inventory_went_positive
        self.last_price_update = last_price_update
        self.days_ago_created = days_ago_created
        self.current_inventory = 24
        # self.days_last_sold = 5
        self.price = 10.00
        self.bc_id = bc_id


class ProductVariables(BaseVariables):
    def __init__(self, product):
        self.product = product

    @string_rule_variable
    def sku(self):
        return self.product.sku

    @string_rule_variable
    def bc_id(self):
        return self.product.bc_id

    @string_rule_variable
    def stock_item_id(self):
        return self.product.stock_item_id

    @string_rule_variable
    def title(self):
        return self.product.title

    @string_rule_variable
    def category(self):
        return self.product.category

    @numeric_rule_variable
    def sold_1_10(self):
        return self.product.sold_1_10

    @numeric_rule_variable
    def days_last_sold(self):
        return self.product.days_last_sold

    @numeric_rule_variable
    def last_sold_price(self):
        return self.product.last_sold_price

    @numeric_rule_variable
    def weight(self):
        return self.product.weight

    @numeric_rule_variable
    def available(self):
        return self.product.available

    @numeric_rule_variable
    def unit_cost(self):
        return self.product.unit_cost

    @numeric_rule_variable
    def retail_price(self):
        return self.product.retail_price

    @numeric_rule_variable
    def inventory_went_positive(self):
        return self.product.inventory_went_positive

    @numeric_rule_variable
    def last_price_update(self):
        return self.product.last_price_update

    @numeric_rule_variable
    def days_ago_created(self):
        return self.product.days_ago_created

    @numeric_rule_variable
    def current_inventory(self):
        return self.product.current_inventory

    @numeric_rule_variable
    def price(self):
        return self.product.price


class ProductActions(BaseActions):
    def __init__(self, product):
        self.product = product

    @rule_action(params={'sales_percentage': FIELD_NUMERIC})
    def price_change(self, sales_percentage):
        self.product.new_price = round(((1 + (sales_percentage / 100)) * self.product.retail_price), 2)
        if self.product.new_price > self.product.retail_price:
            self.product.change = 'UP'
        else:
            self.product.change = 'DOWN'
        print
        'Price went ' + self.product.change + ' from ' + str(self.product.retail_price) + ' to ' + str(
            self.product.new_price)
        output_file = open("C:/Users/George/Dropbox/price_output.csv", "ab")
        price_output = csv.writer(output_file)
        price_output.writerow([self.product.stock_item_id, self.product.bc_id, self.product.sku,
                               self.product.retail_price, self.product.new_price, self.product.change,
                               sales_percentage])
