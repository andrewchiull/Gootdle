# %%
import requests
r = requests.get('http://localhost:8000/data/')

print(r.content)