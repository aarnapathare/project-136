from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time 
import pandas as pd
import requests
import csv
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.cluster import KMeans 

starturl =  "hhttps://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

browser = webdriver.Chrome("/Users/aarnapathare/Desktop/coding/projects/project 127-128-129/chromedriver")
browser.get(starturl)

time.sleep(10)

stars_data = []

headers = ["name", "distance", "mass", "radius"]


def scrape():
    for i in range(1,5):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")
            
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
            
            if current_page_num <i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num >i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        
        for ul_tag in soup.find_all("ul", attrs={"class"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            
            hyperlink_li_tag = li_tags[0]

            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])

            stars_data.append(temp_list)

        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Page {i} scraping completed")

scrape()

new_stars_data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)

        soup = BeautifulSoup(page.text, "html.parser")

        star_table = soup.find_all("table")

        table_row = star_table[7].find_all("tr")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")

            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")

        new_stars_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)


for index,data in enumerate(stars_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink  {index+1} is completed")
print(new_stars_data[0:10])

final_stars_data  = []

for index, data in enumerate(stars_data):
    new_stars_data_element = new_stars_data[index]
    new_stars_data_element = [elem.replace("\n", "") for elem in new_stars_data_element]
    new_stars_data_element = new_stars_data_element[:7]
    final_stars_data.append(data+new_stars_data_element)

with open("final.csv", "w") as f:
    csvwriter = csv.writter(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_stars_data)


df = pd.read("data.csv")
print(df.shape)

del df["Brown Dwarf"]
del df["Constellation"]
del df["Right ascension"]
del df["Declination"]
del df["App Mag"]
del df["Spectral type"]


star_gravity = []
star_mass = []
star_radius = []
star_names = []

for index, name in enumerate(star_names):
     gravity = (float(star_mass[index])*5.972e+24)/(float(star_radius[index])*float(star_radius[index])*6371000*6371000)*6.674e-11
     star_gravity.append(gravity)

ax = plt.subplot()
ax.set_xlabel('star_radius')
ax.set_ylabel('star_mass')
ax.set_title('Star Radius and Mass')

X = df.iloc[:,[0,1]].values
print(X)

here = []
for i in range (1,10):
    kmeans = KMeans(n_clusters=i,init='k-means++', random_state=32)
    kmeans.fit(X)
    here.append(kmeans.inertia_)

star_distance = []
for index, distance in enumerate(star_distance):
    if distance < 100:
        star_distance.append(stars_data[index])
print(len(star_distance))

fig = go.Figure(go.Bar(x=["Star Name"], y=["Mass"]))
fig.show()

fig = go.Figure(go.Bar(x=["Star Name"], y=["Radius"]))
fig.show()

fig = go.Figure(go.Bar(x=["Star Name"], y=["Distance"]))
fig.show()

fig = go.Figure(go.Bar(x=["Star Name"], y=["Gravity"]))
fig.show()