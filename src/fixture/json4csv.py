import csv, json

app_name = 'f1app'
models = ['employee', 'country', 'dependent', 'agent', 'dependemp']
fj = open(app_name + '.json', 'w')
output = []
for model in models:
    with open(model + '.csv') as csvfile:
        csvfile = csv.DictReader(csvfile)
#        x = 0
        for each in csvfile:
            print(each)

#            x += 1
            row = {}
            row = {'model': app_name+'.' + model, 'fields': (each)}
#            row = {'model': app_name+'.' + model, 'pk': x, 'fields': (each)}
            output.append(row)

json.dump(output, fj, indent=4, sort_keys=False, ensure_ascii=False)
