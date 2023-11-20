from bs4 import BeautifulSoup
import json

output = []

for x in range(1,501):
    dataJson = dict()
    xmlFile = open("assets/data/3/zip_var_12/" + str(x) + ".xml", "r") 

    bs = BeautifulSoup(xmlFile, features="xml") 

    dataJson["name"] = bs.find("name").text.strip()
    dataJson["constellation"] = bs.find("constellation").text.strip()
    dataJson["spectralClass"] = bs.find("spectral-class").text.strip()
    dataJson["radius"] = int(bs.find("radius").text.strip())
    dataJson["rotation"] = bs.find("rotation").text.strip()
    dataJson["age"] = bs.find("age").text.strip()
    dataJson["distance"] = bs.find("distance").text.strip()
    dataJson["absoluteMagnitude"] = bs.find("absolute-magnitude").text.strip()
    
    output.append(dataJson)
    
totalValueRadius = 0
totalDataRadius = 0
dataStatistic = dict()
uniqueConstellation = []
for rawData in output:
    totalValueRadius += rawData["radius"]
    totalDataRadius += 1
    if(rawData["constellation"] not in uniqueConstellation):
        uniqueConstellation.append(rawData["constellation"])
        
dataStatistic["totalRadius"] = totalValueRadius
dataStatistic["meanRadius"] = totalValueRadius / totalDataRadius
        
outputConstellation = []
for constellation in uniqueConstellation:
    totalDataConstellation = 0
    dataName = dict()
    for rawData in output:
        if(rawData["constellation"] == constellation):
            totalDataConstellation += 1
    dataName["constellation"] = constellation
    dataName["totalData"] = totalDataConstellation
    
    outputConstellation.append(dataName)
    
output_sorted_by_radius_asc = sorted(output, key=lambda k: k['radius'], reverse=False)
dataStatistic["min"] = int(output_sorted_by_radius_asc[0]["radius"])
dataStatistic["max"] = int(output_sorted_by_radius_asc[len(output_sorted_by_radius_asc)-1]["radius"])
dataStatistic["range"] = int(dataStatistic["max"]) - int(dataStatistic["min"])

if(len(output_sorted_by_radius_asc) % 2 == 1):
    dataStatistic["median"] = int(output_sorted_by_radius_asc[int(len(output_sorted_by_radius_asc)/2)]["radius"])
else:
    dataStatistic["median"] = float((int(output_sorted_by_radius_asc[int(len(output_sorted_by_radius_asc)/2)]["radius"]) + int(output_sorted_by_radius_asc[int(len(output_sorted_by_radius_asc)/2)-1]["radius"])) / 2)
    
output_sorted_by_age_desc = sorted(output, key=lambda k: k['age'], reverse=True)

with open("assets/output/3/output_sorted_by_radius_asc.json", "w") as outfile:
    json.dump(output_sorted_by_radius_asc, outfile, indent=4, ensure_ascii=False)
with open("assets/output/3/output_sorted_by_age_desc.json", "w") as outfile:
    json.dump(output_sorted_by_age_desc, outfile, indent=4, ensure_ascii=False)
with open("assets/output/3/output_constellation.json", "w") as outfile:
    json.dump(outputConstellation, outfile, indent=4, ensure_ascii=False)
with open("assets/output/3/output_statistic.json", "w") as outfile:
    json.dump(dataStatistic, outfile, indent=4, ensure_ascii=False)
