import re
from datetime import datetime
import json

todays_date = datetime.today().strftime('%Y-%m-%d')

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

report = {}
report[todays_date] = {}

policy = {
    'p=none': 0,
    'p=quarantine': 0,
    'p=reject': 0,
    'p= none': 0,
    'p= quarantine': 0,
    'p= reject': 0
}

companyv2 = {
    'dmarcanalyzer': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'dmarcian': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'proofpoint': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'cloudflare': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'agari': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'ondmarc': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'easydmarc': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'powerdmarc': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'uri': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'vali': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'ondmarc': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'netcraft': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'emailauth': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'postmarkapp': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'barracudanetworks': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'dmarcly': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'everest': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'dmarcinput': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        },
    'self': {
        'total': 0, 
        'p=none': 0,
        'p=quarantine': 0,
        'p=reject': 0,
        'p= none': 0,
        'p= quarantine': 0,
        'p= reject': 0
        }
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
    'dmarcly': 0,
    'everest': 0,
    'dmarcinput': 0
}

with open('april_cloudflare_results.txt') as file:
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

            for x in policy:
                if re.search(r'\b' + x + r'\b', dmarc_record):
                    policy[x] +=1  
                    found_company = 0
                    for y in companyv2:
                        if y in dmarc_record:
                            companyv2[y]['total'] += 1
                            companyv2[y][x] += 1
                            found_company += 1
                    if 'ag.au.dmarcian' in dmarc_record:
                        if 'p=none' in dmarc_record:
                            f = open("list.txt", "a")
                            f.write(f'{domain},{dmarc_record}\n')
                            f.close()
                            #print(f'{domain},{dmarc_record}')
                    if found_company == 0:
                        if domain[7:] in dmarc_record:
                            companyv2['self']['total'] += 1  
                            companyv2['self'][x] += 1
                    break
            
            if not re.search(re.escape(pattern1), dmarc_record):
                nop += 1
            
            if not re.search(re.escape('rua'), dmarc_record):
                no_rua += 1                
            '''
            found_company = 0
            for x in company:
                if x in dmarc_record:
                    companyv2[x]['total'] += 1
                    found_company += 1
            if found_company == 0:
                if domain[7:] in dmarc_record:
                    companyv2['self']['total'] += 1  '''                  
        else:
            pass
        
pnone = policy['p= none'] + policy['p=none']
pquarantine = policy['p= quarantine'] + policy['p=quarantine']
preject = policy['p= reject'] + policy['p=reject']

total_records = pnone + pquarantine + preject



for x, y in company.items():
    report[todays_date][x] = y

#print(json.dumps(report))
'''
# function to add to JSON
def write_json(new_data, filename='1mdomain.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["global_data"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
 
    # python object to be appended
y = report
     
write_json(y) 
'''
print('--------')
#print(companyv2)

for x, y in companyv2.items():
    y["p=none"] = y["p=none"] + y["p= none"]
    del y["p= none"]
    y["p=quarantine"] = y["p=quarantine"] + y["p= quarantine"]
    del y["p= quarantine"]
    y["p=reject"] = y["p=reject"] + y["p= reject"]
    del y["p= reject"]

print(companyv2)


