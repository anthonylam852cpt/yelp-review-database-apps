import json


def cleanStr4SQL(s):
    return s.replace("'","''").replace("\n"," ")

def getAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getAttributes(value)
        else:
            L.append((attribute,value))
    return L

def parseBusinessData():
    print("Parsing businesses...")
    #read the JSON file
    with open('.//yelp_business.JSON','r') as f:
        outfile =  open('.//yelp_categories2.sql', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business = data['business_id'] #business id

            # process business categories
            for category in data['categories']:
                category_str = "('" + business + "','" + cleanStr4SQL(category) + "'),"
                outfile.write(category_str + '\n')

            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()


parseBusinessData()