import requests

sample = "anotherPinky.wsq"
file = "anotherLeftPinky.wsq"
response = requests.get("127.0.0.1:7777/scan/?sample="+sample+"&file="+file)
print(response)