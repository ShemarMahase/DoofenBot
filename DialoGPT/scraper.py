import requests
from bs4 import BeautifulSoup
import re
import string
import pandas as pd

target_characters = {'Doofenshmirtz'}
with open("doof_script.txt", "w") as f:
  f.write("")

def scrape(page_url):
    preq = requests.get(page_url)
    psoup = BeautifulSoup(preq.text, 'html.parser')
    pcontent = psoup.find("div", class_="mw-parser-output")

    for elem in pcontent.find_all(["p","div","li"]):
        text = elem.get_text(strip=True)

        if not text:
            continue

        if re.match(r"^\[.*\]$", text) or re.match(r"^\(.*\)$", text):
                continue
        matches = re.findall(r"([A-Za-z\s]+):([^:]+)", text)
        for name, line in matches:
            name = name.strip()
            line = line.strip()
            if name and line:
                line = re.sub(r"\(.*?\)", "", line)
                line = re.sub(r"([.!?])([A-Za-z])", r"\1 \2", line)
                line = re.sub(r"([A-Za-z\s]+):([A-Za-z\s]+)", r"\1: \2", line)
                line = re.sub(r"\s{2,}", " ", line).strip()
                
                with open("doof_script.txt", "a", encoding="utf-8") as f:
                    f.write(name+": "+line + "\n\n") 

base_url = "https://phineasandferb.fandom.com/wiki/Category:Transcripts?from="
exclude = {'X','Y','Z'}
for char in string.ascii_uppercase:
        if char in exclude:
            continue
        print("Looking through "+ char + " links")
        url = base_url+char
        # url = "https://phineasandferb.fandom.com/wiki/Category:Transcripts"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')

        content = soup.find('div', class_= 'category-page__members')

        if content:
            links = content.find_all('a')
            for link in links:
                href = link.get('href')
                if href and href.startswith('/wiki/'):
                    full_url = f"https://phineasandferb.fandom.com{href}"
                    scrape(full_url)

        else:
            print("couldnt find transcript")

print("done scraping. exiting\n")

pattern = r'([a-zA-Z|\s]+): (.+)'
data = {
    "name": [],
    "line": [],
}

with open("doof_script.txt", 'rt',encoding="utf-8") as file:
  for line in file.readlines():
    match = re.findall(pattern, line)
    if match:
      name, line = match[0]
      data['name'].append(name)
      data['line'].append(line)

df = pd.DataFrame(data)
df.to_csv("P_and_F_extract.csv", index=False)