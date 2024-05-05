import json
import csv

# Load JSON data
with open('topologia.json', 'r') as json_file:
    data = json.load(json_file)

# Flatten JSON data into a list of lists
csv_data = []
for node, node_data in data.items():
    csv_row = [node]
    resource = node_data['FPGA']
    csv_row.append(resource)
        #csv_row.extend(resource.values()) 
    
    link = node_data['Links']
    csv_row.append(link)
    csv_data.append(csv_row)

# Write flattened data to CSV file
with open('data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Define headers for the CSV file
    headers = ["Node", "Destination", "Latency", "Throughput"]
    writer.writerow(headers)

    # Write flattened data
    writer.writerows(csv_data)
