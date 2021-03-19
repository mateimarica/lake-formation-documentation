import json

# Convert JSON input to Python dictionary
results = json.loads(input())

for row in results['ResultSet']['Rows']:
	for column in row['Data']:
		print(column['VarCharValue'] + "\t", end="")
	
	# Goes to next line
	print()