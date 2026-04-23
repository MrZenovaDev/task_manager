import re 

text=" title=do priority=high due=2029/23/22"
format_pattern=r"title=(\w) priority=(\w) due=(\d{4}/\d{2}/\d{2})" 
match=re.search(format_pattern,text)
if match:
    print(1)