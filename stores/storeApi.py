import requests
import json

def fetch(*args,**kwargs):
    base_url = 'https://fakestoreapi.com/'
    # base_url = 'https://api.storerestapi.com/'
    
    path = 'products/categories'
    url = base_url+path
    limit=''
    params = {
        'limit':limit
    }
    response =requests.get(url)
    res = response.json()
    print(res)
    i=11
    with open('userst.py','a+') as Stored:
        # pass
        for x in  res["data"]:
                # print(x["id"], end="\n")
            p = str(x)
            e = '\n\n'
            Stored.write(f"user{i} = {p}{e}")
            i+=1
    
    # x = json.loads(res)
    # print(x)
    # print(response["id"])                                                                                                         
fetch()