## 기상청 일자별 데이터 수집

#%%
# 1. 모듈 연결하기
import requests
import pandas as pd
import json


# %%
# 2. 기본정보 설정
url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
params ={'serviceKey' : 'eOKsALPibWs6uSftLkNmhrSuUg8sIKjXB/4rYd9RiJh5GfG/Sx3PzFFs0xfaeXStSnkzQabrT+a/djvB+RKa2A==', 
         'pageNo' : '1', 
         'numOfRows' : '10', 
         'dataType' : 'XML', 
         'dataCd' : 'ASOS', 
         'dateCd' : 'DAY', 
         'startDt' : '20100101', 
         'endDt' : '20100601', 
         'stnIds' : '108' }

#%%
# 3. 데이터 요청하기

response = requests.get(url, params=params)

if response.status_code == 200:
    print('Success!')
else:
    exit(response.status_code)

# %%

# 4. json데이터를 딕셔너리로 변환(파싱)
weather = json.loads(response.content)
weather['response']['body']['totalCount']


# %%
# 5. 전체 데이터를 이용한 데이터 재요청하기
params['numOfRows'] = weather['response']['body']['totalCount']
response = requests.get(url, params=params)
# %%
