class rulesBase(object):

    def __init__(self):
        self.rules = [
            {"conditions": {"all": [
                {"name": "expiration_days",
                 "operator": "less_than",
                 "value": 5,
                 },
                {"name": "current_inventory",
                 "operator": "greater_than",
                 "value": 20,
                 },
            ]},
                "actions": [
                    {"name": "put_on_sale",
                     "params": {"sale_percentage": 0.25},
                     },
                ],
            },

            {"actions": [
                {"name": "order_more",
                 "params": {"number_to_order": 40},
                 },
            ],
            }
        ]

    def return_rule(self):
        return self.rules
