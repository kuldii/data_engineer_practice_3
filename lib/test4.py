from bs4 import BeautifulSoup
import json

output = []

for x in range(1,101):
    
    xmlFile = open("assets/data/4/zip_var_12/" + str(x) + ".xml", "r") 

    bs = BeautifulSoup(xmlFile, features="xml") 

    for productItem in bs.find_all('clothing'):
        dataProduct = dict()
        
        for test in productItem.find_all(True):
            if(str(test.text.strip()).isnumeric()):
                dataProduct[test.name.strip()] = int(test.text.strip())
            else:
                dataProduct[test.name.strip()] = test.text.strip()
        
        output.append(dataProduct)
        
totalValueReviews = 0
totalDataReviews = 0
dataStatistic = dict()
uniqueCategory = []
for rawData in output:
    totalValueReviews += rawData["reviews"]
    totalDataReviews += 1
    if(rawData["category"] not in uniqueCategory):
        uniqueCategory.append(rawData["category"])

outputCategory = []
for category in uniqueCategory:
    totalDataCategory = 0
    dataProduct = dict()
    for rawData in output:
        if(rawData["category"] == category):
            totalDataCategory += 1
    dataProduct["category"] = category
    dataProduct["totalData"] = totalDataCategory
    
    outputCategory.append(dataProduct)
    
  
dataStatistic["totalReviews"] = totalValueReviews
dataStatistic["meanReviews"] = totalValueReviews / totalDataReviews

output_sorted_by_id_asc = sorted(output, key=lambda k: k['id'], reverse=False)
output_sorted_by_reviews_desc = sorted(output, key=lambda k: k['reviews'], reverse=True)

if(len(output_sorted_by_reviews_desc) % 2 == 1):
    dataStatistic["median"] = int(output_sorted_by_reviews_desc[int(len(output_sorted_by_reviews_desc)/2)]["reviews"])
else:
    dataStatistic["median"] = float((int(output_sorted_by_reviews_desc[int(len(output_sorted_by_reviews_desc)/2)]["reviews"]) + int(output_sorted_by_reviews_desc[int(len(output_sorted_by_reviews_desc)/2)-1]["reviews"])) / 2)
    
dataStatistic["max"] = int(output_sorted_by_reviews_desc[0]["reviews"])
dataStatistic["min"] = int(output_sorted_by_reviews_desc[len(output_sorted_by_reviews_desc)-1]["reviews"])
dataStatistic["range"] = int(dataStatistic["max"]) - int(dataStatistic["min"])

with open("assets/output/4/output_sorted_by_id_asc.json", "w") as outfile:
    json.dump(output_sorted_by_id_asc, outfile, indent=4, ensure_ascii=False)
with open("assets/output/4/output_sorted_by_reviews_desc.json", "w") as outfile:
    json.dump(output_sorted_by_reviews_desc, outfile, indent=4, ensure_ascii=False)
with open("assets/output/4/output_category.json", "w") as outfile:
    json.dump(outputCategory, outfile, indent=4, ensure_ascii=False)
with open("assets/output/4/output_statistic.json", "w") as outfile:
    json.dump(dataStatistic, outfile, indent=4, ensure_ascii=False)