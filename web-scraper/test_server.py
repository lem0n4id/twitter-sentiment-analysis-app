import requests
import pandas as pd

# item_id = 'aaa'
# print(requests.get(f'http://127.0.0.1:8000/items/{item_id}').json())
# print(requests.get('http://127.0.0.1:8000/items/?skip=0&limit=10').json())

response = requests.get('http://127.0.0.1:8000/news/?ticker=tsla').json()
df = pd.json_normalize(response)

print(df.head(2))
