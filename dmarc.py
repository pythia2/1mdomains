import re
from datetime import datetime
import json

line_count = 0
record_count = 0
reporting_to_self = 0
no_rua = 0
nop = 0
pattern1 = "p="
agari = 0

p_none = 0
p_quarantine = 0
p_reject = 0

policy = {
    'p=none': 0,
    'p=quarantine': 0,
    'p=reject': 0,
    'p= none': 0,
    'p= quarantine': 0,
    'p= reject': 0
}

company = {
    'dmarcanalyzer': 0,
    'dmarcian': 0,
    'proofpoint': 0,
    'cloudflare': 0,
    'agari': 0,
    'ondmarc': 0,
    'easydmarc': 0,
    'powerdmarc': 0,
    'uri': 0,
    'vali': 0,
    'ondmarc': 0,
    'netcraft': 0,
    'emailauth': 0,
    'postmarkapp': 0,
    'barracudanetworks': 0,
    'dmarcly': 0
}

todays_date = datetime.today().strftime('%Y-%m-%d')


with open('1000000-results.txt') as file:
    for line in file:
        line_count += 1
        # Define a regular expression pattern to match the desired parts
        pattern = re.compile(r'(\S+)\s+\d+\s+IN\s+TXT\s+"(.*)"')

        # Use the pattern to match the groups in the input string
        match = pattern.match(line)

        if match:
            # Extract the matched groups
            domain = match.group(1).rstrip('.')  # Remove trailing period
            dmarc_record = match.group(2)
            record_count += 1
            # Print the results
            #print(f"Domain: {domain}")
            #print(f"DMARC Record: {dmarc_record}")
            for x in policy:
                if re.search(r'\b' + x + r'\b', dmarc_record):
                    policy[x] +=1  
                    break
            
            if not re.search(re.escape(pattern1), dmarc_record):
                nop += 1
            
            if not re.search(re.escape('rua'), dmarc_record):
                no_rua += 1                

            found_company = 0
            for x in company:
                if x in dmarc_record:
                    company[x] += 1
                    found_company += 1
            if found_company == 0:
                if domain[7:] in dmarc_record:
                    reporting_to_self += 1
                    print(f'{domain[7:]}: {dmarc_record}')

                    
        else:
            pass
        
#print(f'Record count: {record_count}, Line Count: {line_count}')
#for x, y in company.items():
#create a ditionary with the data you have then output to JSON
    #print(f'{x}: {y}')

pnone = policy['p= none'] + policy['p=none']
pquarantine = policy['p= quarantine'] + policy['p=quarantine']
preject = policy['p= reject'] + policy['p=reject']

total_records = pnone + pquarantine + preject

#print(policy)
#print(nop)
#print(no_rua)
#print(company)

report = {}
report[todays_date] = {}
report[todays_date]['Total Records'] = total_records
report[todays_date]['p=none'] = pnone
report[todays_date]['p=quarantine'] = pquarantine
report[todays_date]['p=reject'] = preject
report[todays_date]['No RUA'] = no_rua
report[todays_date]['Reporting to self'] = reporting_to_self

for x, y in company.items():
    report[todays_date][x] = y


'''
    '2024-03-12':{
        'Total Records': total_records,
        'p=none': pnone,
        'p=quarantine': pquarantine,
        'p=reject': preject,
        'dmarcanalyzer': 7061,
        'dmarcian': 9005,
        'proofpoint': 10720,
        'cloudflare': 10220,
        'agari': 2562,
        'ondmarc': 2218,
        'easydmarc': 3670,
        'powerdmarc': 1270,
        'uri': 4009,
        'vali': 11517,
        'netcraft': 163,
        'emailauth': 103
    }
}
'''
print(json.dumps(report))

'''import json
data = {"year": 2020, "sales": 12345678, "currency": "€"}
# creating a JSON string
json_string = json.dumps(data)
# storing it in a file
with open("data.json", "w") as json_file:
    json.dump(data, json_file)'''
'''{
  '2023-11-28': [
      'country': { 'key': 'value' },
      'other country': {'key': 'value'}
   ]
}'''