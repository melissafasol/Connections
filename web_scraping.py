import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

all_data = []

nums = list(range(1, 334))
for idx in nums:
    print(idx)
    url = f'https://connections.swellgarfo.com/nyt/{idx}'
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        print("Success!")
    else:
        print("An error has occurred.")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
    data = json.loads(script_tag.string)

    # Extract the part of the JSON that contains answers and words
    answers_data = data['props']['pageProps']['answers']

    # Create dictionary from the answers data
    answers_dict = {item['description']: item['words'] for item in answers_data}

    all_data.append(answers_dict)

print(all_data)

rows = []
for category_dict in all_data:
    for category, words in category_dict.items():
        for word in words:
            rows.append({"category": category, "word": word})

df = pd.DataFrame(rows)
print(df)
df.to_csv('/Users/melissafasol/Desktop/Connections/data/all_data.csv')
