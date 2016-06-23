import json

fdata = open('sample.json').read()

data = json.loads( fdata )

print(data)