import json
with open("inventory.json", "r") as file:
    data = json.load(file)
for item in data:
    item["status"] = "In Stock" if item["stock"] > 0 \
        else "Out of Stock"
with open("inventory_updated.json", "w") as file:
    json.dump(data, file, indent=4)

print("updated")
