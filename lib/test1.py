from bs4 import BeautifulSoup
import json

output = []

for x in range(1,1000):
    HTMLFile = open("assets/data/1/zip_var_12/" + str(x) + ".html", "r") 
    dataWeb = HTMLFile.read() 

    bs = BeautifulSoup(dataWeb, 'html.parser') 

    dataJson = dict()

    dataTitle = bs.find('h1', attrs="title").text.replace("\n","").strip().split(":")
    dataJson["building"] = dataTitle[1].replace("   ","").replace("  ","")

    dataAddress = bs.find('p', attrs="address-p").text.replace("\n","").strip().split("Индекс:")
    dataJson["index"] = dataAddress[1].replace("   ","").replace("  ","")
    dataJson["street"] = dataAddress[0].split(":")[1].replace("   ","").replace("  ","")

    dataImg = bs.find('img')
    dataJson["image"] = dataImg['src']

    for tag in bs.find_all('span'):
        allDataSpan = str(tag.text).strip().split("\n")
        for dataSpan in allDataSpan:
            dataSplit = dataSpan.split(":")
            if(len(dataSplit) == 1):
                if(dataSplit[0].__contains__("Построено в")):
                    dataJson["year"] = dataSplit[0]
            else:
                keySpan = dataSplit[0]
                valueSpan = dataSplit[1].replace(" ","")
                if(keySpan == "Город"):
                    dataJson["city"] = valueSpan
                elif(keySpan == "Этажи"):
                    dataJson["floor"] = valueSpan
                elif(keySpan == "Парковка"):
                    dataJson["parking"] = valueSpan
                elif(keySpan == "Рейтинг"):
                    dataJson["rating"] = valueSpan
                elif(keySpan == "Просмотры"):
                    dataJson["views"] = valueSpan
                else:
                    dataJson["other"] = valueSpan
                    
                
    output.append(dataJson)

totalValueViews = 0
totalDataViews = 0
dataStatistic = dict()
uniqueCity = []
for rawData in output:
    totalValueViews += int(rawData["views"])
    totalDataViews += 1
    if(rawData["city"] not in uniqueCity):
        uniqueCity.append(rawData["city"])

outputCity = []
for city in uniqueCity:
    totalDataCity = 0
    dataCity = dict()
    for rawData in output:
        if(rawData["city"] == city):
            totalDataCity += 1
    dataCity["city"] = city
    dataCity["totalData"] = totalDataCity
    
    outputCity.append(dataCity)
    
  

dataStatistic["totalViews"] = totalValueViews
dataStatistic["meanViews"] = totalValueViews / totalDataViews

output_sorted_by_views_asc = sorted(output, key=lambda k: k['views'], reverse=False)

dataStatistic["min"] = int(output_sorted_by_views_asc[0]["views"])
dataStatistic["max"] = int(output_sorted_by_views_asc[len(output_sorted_by_views_asc)-1]["views"])
if(len(output_sorted_by_views_asc) % 2 == 1):
    dataStatistic["median"] = int(output_sorted_by_views_asc[int(len(output_sorted_by_views_asc)/2)]["views"])
else:
    dataStatistic["median"] = float((int(output_sorted_by_views_asc[int(len(output_sorted_by_views_asc)/2)]["views"]) + int(output_sorted_by_views_asc[int(len(output_sorted_by_views_asc)/2)-1]["views"])) / 2)
    
dataStatistic["range"] = int(dataStatistic["max"]) - int(dataStatistic["min"])

output_sorted_by_rating_desc = sorted(output, key=lambda k: k['rating'], reverse=True)

with open("assets/output/1/output_sorted_by_views_asc.json", "w") as outfile:
    json.dump(output_sorted_by_views_asc, outfile, indent=4, ensure_ascii=False)
with open("assets/output/1/output_sorted_by_rating_desc.json", "w") as outfile:
    json.dump(output_sorted_by_rating_desc, outfile, indent=4, ensure_ascii=False)
with open("assets/output/1/output_city.json", "w") as outfile:
    json.dump(outputCity, outfile, indent=4, ensure_ascii=False)
with open("assets/output/1/output_statistic.json", "w") as outfile:
    json.dump(dataStatistic, outfile, indent=4, ensure_ascii=False)