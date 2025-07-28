import json
with open("products.json", "r") as file:
    data = json.load(file)
for product in data:
    product["price"] = round(product["price"] * 1.10, 2)
with open("products_updated.json", "w") as file:
    json.dump(data, file, indent=4)
print("updated")
