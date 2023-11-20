from bs4 import BeautifulSoup
import json
import requests 


openFile = open("assets/data/5/source.json")
source = json.load(openFile)

allProducts = []
outputCategory = []

for url in source:
    dataStatisticCategory = dict()
    category = url.split("https://www.designs4cnc.in/product-category/")[1].replace("/", "")
    
    req = requests.get(url)
    bs = BeautifulSoup(req.content, "lxml")
    
    rawTotalProduct = bs.find("p", attrs={"class": "woocommerce-result-count"})
    
    totalProduct = 0
    if(rawTotalProduct.text.__contains__("of")):
        totalProduct = rawTotalProduct.text.split(" of ")[1].replace("results", "").strip()
    else:
        totalProduct = rawTotalProduct.text.split("all")[1].replace("results", "").strip()
        
    innerContent = bs.find("ul", attrs={"class": "products"})

    for dataContent in innerContent.find_all("li", attrs={"class": "product"}):
        product = dict()
        product["category"] = category
        product["link"] = dataContent.a["href"]
        product["productName"] = dataContent.h3.text.strip()
        product["currency"] = dataContent.find("span", attrs={"class": "woocommerce-Price-currencySymbol"}).text
        product["price"] = float(dataContent.find("bdi").text.replace(product["currency"], "").replace(",",""))
        
        allProducts.append(product)
    
    dataStatisticCategory["category"] = category
    dataStatisticCategory["totalProduct"] = totalProduct
    outputCategory.append(dataStatisticCategory)
    
# print(outputCategory)
# print(allProducts)

totalValuePrice = 0
totalDataPrice = 0
dataStatistic = dict()
uniqueCategory = []
for rawData in allProducts:
    totalValuePrice += rawData["price"]
    totalDataPrice += 1
    
dataStatistic["totalPrice"] = totalValuePrice
dataStatistic["meanPrice"] = totalValuePrice / totalDataPrice

output_sorted_by_category_asc = sorted(allProducts, key=lambda k: k['category'], reverse=False)
output_sorted_by_price_desc = sorted(allProducts, key=lambda k: k['price'], reverse=True)

if(len(output_sorted_by_price_desc) % 2 == 1):
    dataStatistic["median"] = int(output_sorted_by_price_desc[int(len(output_sorted_by_price_desc)/2)]["price"])
else:
    dataStatistic["median"] = float((int(output_sorted_by_price_desc[int(len(output_sorted_by_price_desc)/2)]["price"]) + int(output_sorted_by_price_desc[int(len(output_sorted_by_price_desc)/2)-1]["price"])) / 2)
    
dataStatistic["max"] = int(output_sorted_by_price_desc[0]["price"])
dataStatistic["min"] = int(output_sorted_by_price_desc[len(output_sorted_by_price_desc)-1]["price"])
dataStatistic["range"] = int(dataStatistic["max"]) - int(dataStatistic["min"])


with open("assets/output/5/output_sorted_by_category_asc.json", "w") as outfile:
    json.dump(output_sorted_by_category_asc, outfile, indent=4, ensure_ascii=False)
with open("assets/output/5/output_sorted_by_price_desc.json", "w") as outfile:
    json.dump(output_sorted_by_price_desc, outfile, indent=4, ensure_ascii=False)
with open("assets/output/5/output_category.json", "w") as outfile:
    json.dump(outputCategory, outfile, indent=4, ensure_ascii=False)
with open("assets/output/5/output_statistic.json", "w") as outfile:
    json.dump(dataStatistic, outfile, indent=4, ensure_ascii=False)