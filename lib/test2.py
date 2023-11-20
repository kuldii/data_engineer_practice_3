from bs4 import BeautifulSoup
import json

output = []

for x in range(1,65):
    
    HTMLFile = open("assets/data/2/zip_var_12/" + str(x) + ".html", "r") 
    dataWeb = HTMLFile.read() 

    bs = BeautifulSoup(dataWeb, 'html.parser') 

    for productItem in bs.find_all('div', attrs="product-item"):
        dataProduct = dict()
        
        dataProduct["dataId"] = productItem.find('a')['data-id']
        dataProduct["image"] = productItem.find('img')['src']
        dataProduct["productName"] = str(productItem.find('span').text).replace("\n", "").strip()
        dataProduct["price"] = int(str(productItem.find('price').text).replace(" ", "").replace("₽", ""))
        dataProduct["bonus"] = int(str(productItem.find('strong').text).split("начислим ")[1].replace("бонусов", "").replace(" ", ""))
        innerContent = productItem.find('ul')
        itemList = innerContent.find_all('li')
        
        spesification = dict()
        
        for item in itemList:
            spesification[item.attrs["type"]] = str(item.text).replace("\n", "").strip()
        
        dataProduct["spesification"] = spesification
        
        output.append(dataProduct)

totalValueBonus = 0
totalDataBonus = 0
dataStatistic = dict()
uniqueProduct = []
for rawData in output:
    totalValueBonus += rawData["bonus"]
    totalDataBonus += 1
    if(rawData["productName"] not in uniqueProduct):
        uniqueProduct.append(rawData["productName"])

outputProduct = []
for productName in uniqueProduct:
    totalDataProduct = 0
    dataProduct = dict()
    for rawData in output:
        if(rawData["productName"] == productName):
            totalDataProduct += 1
    dataProduct["productName"] = productName
    dataProduct["totalData"] = totalDataProduct
    
    outputProduct.append(dataProduct)
    
  
dataStatistic["totalBonus"] = totalValueBonus
dataStatistic["meanBonus"] = totalValueBonus / totalDataBonus

output_sorted_by_id_asc = sorted(output, key=lambda k: k['dataId'], reverse=False)

if(len(output_sorted_by_id_asc) % 2 == 1):
    dataStatistic["median"] = int(output_sorted_by_id_asc[int(len(output_sorted_by_id_asc)/2)]["bonus"])
else:
    dataStatistic["median"] = float((int(output_sorted_by_id_asc[int(len(output_sorted_by_id_asc)/2)]["bonus"]) + int(output_sorted_by_id_asc[int(len(output_sorted_by_id_asc)/2)-1]["bonus"])) / 2)
    
output_sorted_by_bonus_desc = sorted(output, key=lambda k: k['bonus'], reverse=True)

dataStatistic["max"] = int(output_sorted_by_bonus_desc[0]["bonus"])
dataStatistic["min"] = int(output_sorted_by_bonus_desc[len(output_sorted_by_bonus_desc)-1]["bonus"])
dataStatistic["range"] = int(dataStatistic["max"]) - int(dataStatistic["min"])

with open("assets/output/2/output_sorted_by_id_asc.json", "w") as outfile:
    json.dump(output_sorted_by_id_asc, outfile, indent=4, ensure_ascii=False)
with open("assets/output/2/output_sorted_by_bonus_desc.json", "w") as outfile:
    json.dump(output_sorted_by_bonus_desc, outfile, indent=4, ensure_ascii=False)
with open("assets/output/2/output_product.json", "w") as outfile:
    json.dump(outputProduct, outfile, indent=4, ensure_ascii=False)
with open("assets/output/2/output_statistic.json", "w") as outfile:
    json.dump(dataStatistic, outfile, indent=4, ensure_ascii=False)