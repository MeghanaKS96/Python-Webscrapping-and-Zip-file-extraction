import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import zipfile
import io
from io import BytesIO
from datetime import datetime as dt

ctx ='44'
stationid=''
for i in range(5-len(str(ctx))):
    stationid = stationid +'0'
stationid = stationid + str(ctx)
type='recent'
zip_file_url = ''

if(type=='historical'):
    url=zip_file_url+'historical/'
elif (type=='recent'):
    url=zip_file_url+'recent/'

filename = ''+stationid
req = requests.get(url)
my_dict = re.findall('(?<=<a href=")[^"]*', str(req.content))
for x in my_dict:
 if(filename in x ):
     new_url = url + x

print(str(new_url))

req1 = requests.get(new_url)
z = zipfile.ZipFile(io.BytesIO(req1.content))
for file in z.filelist:
    if file.filename.startswith(''):
        targetfile= file.filename
csv_file = z.open(targetfile)
dataq = pd.read_csv(csv_file,delimiter= ';',header=1)
for index, row in dataq.iterrows():
    converted_date = str(row[1])
    years = converted_date[0:4]
    months = converted_date[4:6]
    days = converted_date[6:8]
    hours = converted_date[8:10]
    minutes = converted_date[10:12]

    date_time = years + '-' + months + '-' + days +  ' ' + hours
    date_time_obj = dt.strptime(date_time, '%Y-%m-%d %H')
    intervalmin = 60
    print(date_time_obj,row[0],row[2],row[3],row[4],intervalmin)