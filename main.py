#Make options like Scrape and Rewrite, analyze user profiles individually by url from names already in database from initial scrape, Sort alphabetically, plug into AI and detect facial similarities. create groups based on school. Maybe sort by facial similarities as a challenge?
#NeuralNet DataFeed - feed into AI :))))))))))))))))))))))))))

from selenium import webdriver
import time
from dotenv import load_dotenv
import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    with open('data.html', 'r') as filehandle:
        content = filehandle.read()
    return render_template('index.html', content=content)

if __name__ == "__main__":
    app.run(debug=True)

driver = webdriver.Firefox()
driver.get('https://northvilleschools.schoology.com/')
temp = driver.find_element_by_id("edit-mail")
temp.send_keys(os.getenv("USERNAME"))
temp = driver.find_element_by_id("edit-pass")
temp.send_keys(os.getenv("PASSWORD"))
temp.submit()

indexes = []
scrapedNames = []

with open('lll.txt', 'r') as filehandle:
    filecontents = filehandle.readlines()
    for line in filecontents:
        comboFromFile = line[:-1]
        indexes.append(comboFromFile)

time.sleep(3)

start = 0

with open('savestate.txt', 'r') as filehandle:
    savestate = filehandle.read()
    if (savestate != ''):
        start = savestate.split('<>')
        start[2] = start[2].split(',')
        for i in start[2]:
            scrapedNames.append(i)

started = False
started2 = False

for i in indexes:
    if (start != 0):
        if (i != start[0]):
            if (started == False):
                continue
    started = True
    x = 1
    for x in range(500):
        if (start != 0):
            if (x != int(start[1])):
                if (started2 == False):
                    continue
        started2 = True
        driver.get('https://northvilleschools.schoology.com/search/user?page=' + str(x) + '&s=' + i)
        time.sleep(2)
        try:
            driver.find_elements_by_xpath("//div[@class='results-counter empty']")[0]
            break
        except:
            names = driver.find_elements_by_xpath("//a[@class='sExtlink-processed']")
            index = 0
            tempindex1 = ''
            tempindex2 = ''
            tempindex3 = ''
            for n in names:
                index+=1
                if (index == 1):
                    tempindex1 = n.get_attribute('innerHTML').split('"')[5]
                elif (index == 2):
                    tempindex2 = n.get_attribute('innerHTML')
                else:
                    tempindex3 = n.get_attribute('innerHTML')
                    if (tempindex2 not in scrapedNames):
                        scrapedNames.append(tempindex2)
                        with open('data.html', 'a') as filehandle:
                            filehandle.write('<img>' + tempindex1 + '</img><span>' + tempindex2 + '</span><span>' + tempindex3 + '</span><br><br>')
                        tempindex1 = ''
                        tempindex2 = ''
                        tempindex3 = ''
                        index = 0
        with open('savestate.txt', 'w') as filehandle:
            filehandle.write(i + '<>' + str(x) + '<>' + ','.join(scrapedNames))