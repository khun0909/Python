# 1. 모듈 연결하기
import requests
import pandas as pd
import json
from datetime import date, datetime, timedelta   # 날짜/시간 관련 모듈
import tqdm   # 진행바 모듈

# 지점명을 이용한 지점코드 찾기
def loc_code_sch(loc_name):
    loc_code = pd.read_csv('./기상청위치코드.csv', encoding='utf-8')
    loc_code=loc_code[loc_code['지점명']==loc_name]['지점'].values[0]
    #print(loc_code)
    
    return str(loc_code)


# Weather API 함수 생성
def weather_api(startDt, endDt, stnIds, numOfRows=10):
    
    # 기상청 API 호출을 위한 기본 정보 설정
    url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    params ={'serviceKey' : '개인키 입력', 
            'pageNo' : '1', 
            'numOfRows' : numOfRows, 
            'dataType' : 'JSON', 
            'dataCd' : 'ASOS', 
            'dateCd' : 'DAY', 
            'startDt' : startDt, # 20210101
            'endDt' : endDt, 
            'stnIds' : stnIds }
    
    # 기상청 데이터 조회
    response = requests.get(url, params=params)  # API 호출
    if response.status_code != 200:        # 정상적으로 호출되지 않은 경우
        exit('API 호출 에러: ' + response.status_code)
        
    try:
        weather_res = json.loads(response.content)       # 결과를 json 형태(딕셔너리형)로 변환
    except:
        print(weather_res.content)
        exit()
        
    return weather_res   # 결과 반환

def weather_ext(startDT, endDT, stnIds):
    # 데이터 추출
    weather_df=pd.DataFrame()   # 최초 데이터프레임 생성
    cnt = 0                     # 데이터 추출 횟수 카운트
    today = date.today().strftime("%Y%m%d")      # 오늘 날짜 =>텍스트로 변환

    for i in tqdm.tqdm(range(int(startDT[:4]), int(endDT[:4])+1)):
        if cnt !=0:     # 최초 데이터프레임 생성 후 2번째부터는 시작일과 종료일 변경
            startDTs = date(i, 1, 1).strftime("%Y%m%d")   # 시작일
        else:
            startDTs = startDT
        
        if i != int(endDT[:4]):     # 마지막 년도는 종료일로 설정
            endDTs = date(i, 12, 31).strftime("%Y%m%d")   # 종료일
        else:
            endDTs = endDT
        
        if int(endDTs) >= int(today):     # 오늘 날짜보다 종료일이 크면
            endDTs = int(date.today().strftime("%Y%m%d")) - 1   # 20230808-1 = 20230807
            endDTs = str(endDTs)  # 종료일 당일 전날로 변경후 텍스트로 변환
        
        weather_res = weather_api(startDTs, endDTs, stnIds)   # 함수 호출(최초)
        
        
        try:  # 지역이 없는 경우 에러 발생
            numOfRows = weather_res['response']['body']['totalCount']
        except:     
            continue  # 지역이 없는 경우 다음 년도로 넘어감
        
        weather_res = weather_api(startDTs, endDTs, stnIds, numOfRows)   # 함수 호출(전체 조회 데이터)
        df1 = pd.DataFrame(weather_res['response']['body']['items']['item'])  # 데이터프레임 생성
        weather_df = pd.concat([weather_df, df1], ignore_index=True)          # 데이터프레임 병합
        cnt += 1    # 데이터 추출 횟수 카운트
        
    return weather_df   # 결과 반환
        
        
        
if __name__ == '__main__': # 현재 파일 내부에서만 실행되는 코드
    
    # 사용자로부터 데이터 입력 받기
    startDT = input('시작일(yyyymmdd): ')  # 시작일(20150601)
    endDT = input('종료일(yyyymmdd): ')    # 종료일(20230808)

    # 지역명으로 지점코드 조회
    loc_name= input('지역을 입력하세요: ')
    stnIds= loc_code_sch(loc_name)    
    
    weather_df = weather_ext(startDT, endDT, stnIds)   # 함수 호출
    
    weather_df.info()
