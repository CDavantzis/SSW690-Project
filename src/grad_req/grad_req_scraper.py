import sys
import string


# usage grad_req_scraper.py <school_list.txt> <file to parse>


school_list = []

with open (sys.argv[1]) as f:
   school_list = f.read().splitlines() 

#print school_list[0]


for i, line in enumerate(open(sys.argv[2])):
    line.strip()
    line = filter(lambda x: x in string.printable, line)
    #if line == school_list[0]:
    print str(i) + ' : ' + repr(line)
