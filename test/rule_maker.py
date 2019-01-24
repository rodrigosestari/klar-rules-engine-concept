import csv

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

#list = read_csv()
#list = ['rule',"CONDITION", "days_last_sold", "greater_than", 4,"CONDITION", "created", "less_than", 5, 'action', 'increase_price', 'sales_percentage', 0.1, 'rule',"CONDITION", "days_last_sold", "greater_than", 4,"CONDITION", "created", "less_than", 5, 'action', 'increase_price', 'sales_percentage', 0.1]
#rules = []

def make_conditions(list):
    conditions = []
    outer_list = list
    k=0
    while k < len(outer_list):
        if list[k].upper() == "CONDITION":
            condition = {"name": list[k+1], "operator": list[k+2], "value": int(list[k+3])}
            k+= 4
            conditions.append(condition)
    return conditions

def make_actions(list):
    actions = []
    m=0
    while m < len(list):
        if list[m].upper() == 'ACTION':
            action = {'name':list[m+1], 'params': {list[m+2]:float(list[m+3])}}
            m+=4
            actions.append(action)
    return actions

def make_rules():
    rules = []
    list = read_csv()
    i=0
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
            rules.append({'conditions':{'all':make_conditions(conditions)}, 'actions':make_actions(actions)})
    print(rules)
    return rules

