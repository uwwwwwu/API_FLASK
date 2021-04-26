# -*- coding: utf-8 -*- 

from xml.etree import ElementTree as ET
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
import numpy as np
import datetime
import requests
import copy
import time

app = Flask(__name__, static_url_path='')

req_url = 'http://openapi.work.go.kr/opi/opi/opia/wantedApi.do'
s_parameters = {
    'authKey':'WNKMBKIW3GCNURZ1ABGNL2VR1HJ',
    'callTp':'L',
    'returnType':'XML',
    'startPage':1,
    'display':100,
    'career':'N',
    'education':'04',
    'region':'11000'
}

s_f_parameters = {
    'authKey':'WNKMBKIW3GCNURZ1ABGNL2VR1HJ',
    'callTp':'L',
    'returnType':'XML',
    'startPage':1,
    'display':100,
    'career':'N',
    'education':'05',
    'region':'11000'
}

s_req = requests.get(req_url, params=s_parameters)
s_f_req = requests.get(req_url, params=s_f_parameters)
s_content = s_req.text
s_f_content = s_f_req.text
s_root = ET.fromstring(s_content)
s_f_root = ET.fromstring(s_f_content)
s_wanted = s_root.findall('.//wanted')
s_f_wanted = s_f_root.findall('.//wanted')

s_data = []
s_f_data = []

#서울(2-3)
for s_want in s_wanted:
    company = s_want.find('company').text
    if company[0:5].count('(') and len(company) > 9:
            company = company[0:8]+ ".."
    elif company[0:8].count(' ') and len(company) > 9:
            company = company[0:8]+ ".."
    elif len(company) > 8:
        company = company[0:7]+ ".."
    title = s_want.find('title').text
    if len(title) > 12:
        title = title[0:11]+ ".."
    career = s_want.find('career').text + ' / ' + '대졸(2~3년)'
    closeDt = s_want.find('closeDt').text
    s_data.append([company+datetime.datetime.now().strftime("%H:%M:%S"), title, career, closeDt])

#서울(4)
for s_f_want in s_f_wanted:
    company = s_f_want.find('company').text
    if company[0:5].count('(') and len(company) > 9:
            company = company[0:8]+ ".."
    elif company[0:8].count(' ') and len(company) > 9:
            company = company[0:8]+ ".."
    elif len(company) > 8:
        company = company[0:7]+ ".."
    title = s_f_want.find('title').text
    if len(title) > 12:
        title = title[0:11]+ ".."
    career = s_f_want.find('career').text + ' / ' + '대졸(4년)'
    closeDt = s_f_want.find('closeDt').text
    s_f_data.append([company, title, career, closeDt])
        

        

# '충북세종','충남세종대전','경기','인천','경남부산울산','경북대구','전남광주','전북','강원','제주'
etc=['43000||36110','44000||36110||30000','41000','28000','48000||26000||31000','47000||27000','46000||29000','45000','42000','50000']
#배열선언-2년제
etc_parameters = [0 for i in range(10)]
etc_req = [0 for i in range(10)]
etc_content = [0 for i in range(10)]
etc_root = [0 for i in range(10)]
etc_wanted = [0 for i in range(10)]
etc_data=[[] for _ in range(10)]
stack_data = []

#배열선언-4년제
etc_f_parameters = [0 for i in range(10)]
etc_f_req = [0 for i in range(10)]
etc_f_content = [0 for i in range(10)]
etc_f_root = [0 for i in range(10)]
etc_f_wanted = [0 for i in range(10)]
etc_f_data=[[] for _ in range(10)]
stack_f_data = []

for i in range(10):
    etc_parameters[i] = {
        'authKey':'WNKMBKIW3GCNURZ1ABGNL2VR1HJ',
        'callTp':'L',
        'returnType':'XML',
        'startPage':1,
        'display':100,
        'career':'N',
        'education':'04',
        'region': etc[i]
    }
        
    etc_f_parameters[i] = {
        'authKey':'WNKMBKIW3GCNURZ1ABGNL2VR1HJ',
        'callTp':'L',
        'returnType':'XML',
        'startPage':1,
        'display':100,
        'career':'N',
        'education':'05',
        'region': etc[i]
    }


    etc_req[i] = requests.get(req_url, params=etc_parameters[i])
    etc_f_req[i] = requests.get(req_url, params=etc_f_parameters[i])
    etc_content[i] = etc_req[i].text
    etc_f_content[i] = etc_f_req[i].text
    etc_root[i] = ET.fromstring(etc_content[i])
    etc_f_root[i] = ET.fromstring(etc_f_content[i])
    etc_wanted[i] = etc_root[i].findall('.//wanted')
    etc_f_wanted[i] = etc_f_root[i].findall('.//wanted')

    #지역별 크롤링 -2년제
    for etc_want in etc_wanted[i]:
        company = etc_want.find('company').text
        if company[0:5].count('(') and len(company) > 9:
                company = company[0:8]+ ".."
        elif company[0:8].count(' ') and len(company) > 9:
                company = company[0:8]+ ".."
        elif len(company) > 8:
            company = company[0:7]+ ".."

        title = etc_want.find('title').text
        if len(title) > 12:
            title = title[0:11]+ ".."
        career = etc_want.find('career').text + ' / '  + '대졸(2~3년)'
        closeDt = etc_want.find('closeDt').text
        stack_data.append([company, title, career, closeDt])

    #지역별 크롤링 -4년제
    for etc_f_want in etc_f_wanted[i]:
        company = etc_f_want.find('company').text
        if company[0:5].count('(') and len(company) > 9:
                company = company[0:8]+ ".."
        elif company[0:8].count(' ') and len(company) > 9:
                company = company[0:8]+ ".."
        elif len(company) > 8:
            company = company[0:7]+ ".."

        title = etc_f_want.find('title').text
        if len(title) > 12:
            title = title[0:11]+ ".."
        career = etc_f_want.find('career').text + ' / '  + '대졸(4년)'
        closeDt = etc_f_want.find('closeDt').text
        stack_f_data.append([company, title, career, closeDt])    

    etc_data[i] = stack_data
    stack_data = []

    etc_f_data[i] = stack_f_data
    stack_f_data = []





############################################
# s_data = 서울 (2-3),  s_f_data = 서울(4)
#'충북세종' CB
#'충남세종대전' CN 
#'경기' GG
#'인천' INC
#'경남부산울산' GN
#'경북대구' GB
#'전남광주' JN
#'전북' JB
#'강원' GW
#'제주' JJ
###########################################

@app.route('/CB') 
def indexCB():
    return render_template('hoon.html',s_data=s_data, len_s=len(s_data), etc_data=etc_data[0], len_etc=len(etc_data[0]), local_code=43000) 

@app.route('/CB-F') 
def indexCBF():
    return render_template('hoon.html',s_data=s_f_data, len_s=len(s_f_data), etc_data=etc_f_data[0], len_etc=len(etc_f_data[0]), local_code=43000) 

@app.route('/CN') 
def indexCN():
    return render_template('hoon.html',s_data=s_data, len_s=len(s_data), etc_data=etc_data[1], len_etc=len(etc_data[1]), local_code=44000) 

@app.route('/CN-F') 
def indexCNF():
    return render_template('hoon.html',s_data=s_f_data, len_s=len(s_f_data), etc_data=etc_f_data[1], len_etc=len(etc_f_data[1]), local_code=44000) 

@app.route('/GG') 
def indexGG():
    return render_template('hoon.html',s_data=s_data, len_s=len(s_data), etc_data=etc_data[2], len_etc=len(etc_data[2]), local_code=41000) 

@app.route('/GG-F') 
def indexGGF():
    return render_template('hoon.html',s_data=s_f_data, len_s=len(s_f_data), etc_data=etc_f_data[2], len_etc=len(etc_f_data[2]), local_code=41000) 

@app.route('/INC') 
def indexINC():
    return render_template('hoon.html',s_data=s_data, len_s=len(s_data), etc_data=etc_data[3], len_etc=len(etc_data[3]), local_code=28000) 

@app.route('/INC-F') 
def indexINCF():
    return render_template('hoon.html',s_data=s_f_data, len_s=len(s_f_data), etc_data=etc_f_data[3], len_etc=len(etc_f_data[3]), local_code=28000) 

@app.route('/GN') 
def indexGN():
    return render_template('hoon.html',s_data=s_data, len_s=len(s_data), etc_data=etc_data[4], len_etc=len(etc_data[4]), local_code=48000) 

@app.route('/GN-F') 
def indexGNF():
    return render_template('hoon.html',s_data=s_f_data, len_s=len(s_f_data), etc_data=etc_f_data[4], len_etc=len(etc_f_data[4]), local_code=48000) 

@app.route('/GB') 
def indexGB():
    return render_template('hoon.html',s_data=s_data, len_s=len(s_data), etc_data=etc_data[5], len_etc=len(etc_data[5]), local_code=47000) 

@app.route('/GB-F') 
def indexGBF():
    return render_template('hoon.html',s_data=s_f_data, len_s=len(s_f_data), etc_data=etc_f_data[5], len_etc=len(etc_f_data[5]), local_code=47000) 

@app.route('/JN') 
def indexJN():
    return render_template('hoon.html',s_data=s_data, len_s=len(s_data), etc_data=etc_data[6], len_etc=len(etc_data[6]), local_code=46000) 

@app.route('/JN-F') 
def indexJNF():
    return render_template('hoon.html',s_data=s_f_data, len_s=len(s_f_data), etc_data=etc_f_data[6], len_etc=len(etc_f_data[6]), local_code=46000)

@app.route('/JB') 
def indexJB():
    return render_template('hoon.html',s_data=s_data, len_s=len(s_data), etc_data=etc_data[7], len_etc=len(etc_data[7]), local_code=45000) 

@app.route('/JB-F') 
def indexJBF():
    return render_template('hoon.html',s_data=s_f_data, len_s=len(s_f_data), etc_data=etc_f_data[7], len_etc=len(etc_f_data[7]), local_code=45000) 

@app.route('/GW') 
def indexGW():
    return render_template('hoon.html',s_data=s_data, len_s=len(s_data), etc_data=etc_data[8], len_etc=len(etc_data[8]), local_code=42000) 

@app.route('/GW-F') 
def indexGWF():
    return render_template('hoon.html',s_data=s_f_data, len_s=len(s_f_data), etc_data=etc_f_data[8], len_etc=len(etc_f_data[8]), local_code=42000) 

@app.route('/JJ') 
def indexJJ():
    return render_template('hoon.html',s_data=s_data, len_s=len(s_data), etc_data=etc_data[9], len_etc=len(etc_data[9]), local_code=50000) 

@app.route('/JJ-F') 
def indexJJF():
    return render_template('hoon.html',s_data=s_f_data, len_s=len(s_f_data), etc_data=etc_f_data[9], len_etc=len(etc_f_data[9]), local_code=50000) 



if __name__ == '__main__': 
    app.run(debug=True)


