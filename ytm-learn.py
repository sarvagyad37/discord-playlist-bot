import re
tempname = ['PVRIS - Thank You (feat. Raye)']
tempname = re.sub(r'\([^()]*\)', '', tempname[0])
print(type(tempname))