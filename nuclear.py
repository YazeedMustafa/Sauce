import requests
import os
import os.path
import urllib.request
from bs4 import BeautifulSoup
import shutil

imgAux = 'i.nhentai.net'
sauceAux = 'nhentai.net/g/'
titleAux = 'itemprop'
name = 'name'
forbidden = '\/:*?"<>|'
startPlace = os.getcwd()

def testVal(tt):
    i=0
    while i < len(tt):
        for b in forbidden:
            if b in tt[i]:
                tt = tt.replace(b,"")
        i += 1
    return tt


def crawl(url):
    source = requests.get(url)
    text = source.text
    soup = BeautifulSoup(text,"lxml")
    for link in soup.find_all('a',{'class':'gallerythumb'}):
        data = link.get('href')
        itemGet("https://nhentai.xxx"+data)
    os.chdir(startPlace)
    code = url.split("/")[-1]
    file_object = open('done.txt', 'a')
    file_object.write("\n"+str(code))
    file_object.close()

    
        

def itemGet(url):
    source = requests.get(url)
    text = source.text
    soup = BeautifulSoup(text,"lxml")
    for link in soup.find_all('img',{'class':'fit-horizontal'}):
        data = link.get('src')
        print(data)
        download_img(data)

def download_img(url):
    image_url = url
    filename = image_url.split("/")[-1]

    if len(filename) is 5:
        filename = ''.join(('00',filename))
    if len(filename) is 6:
        filename = ''.join(('0',filename))


    file_exists = os.path.exists(filename)
    if file_exists is True:
        print("[ALREADY GOT THIS IMAGE]"+filename)
        return

    r = requests.get(image_url, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True

        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')

def title(sauce):
    temp = 'https://nhentai.net/g/' + sauce
    source = requests.get(temp)
    plain_text = source.text

    
    soup = BeautifulSoup(plain_text,"lxml")

    for link in soup.findAll('meta'):
        nn = link.get("itemprop")
        if name in str(nn):
            cc = link.get("content")
            cc = testVal(cc)
            if not os.path.exists(os.getcwd()+"\\"+str(cc)):
                os.mkdir(os.getcwd()+"\\"+str(cc))
            os.chdir(os.getcwd()+"\\"+str(cc))
            crawl(temp)
            

#PRep the lists
a_file = open("nuke.txt", "r")
nukeList = []
for line in a_file:
  stripped_line = line.strip()
  line_list = stripped_line.split()
  nukeList.append(line_list)
a_file.close()


a_file = open("nukeEnd.txt", "r")
doneList = []
for line in a_file:
  stripped_line = line.strip()
  line_list = stripped_line.split()
  doneList.append(line_list)
a_file.close()



for row in nukeList:
    print("Downloading:> "+row[0])
    if row in doneList:
        print("ALREADY DONE:> "+row[0])
    else:
        title(row[0])
#title('395186')
