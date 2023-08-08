#%%
import weather_api as wtapi

# 사용자로부터 데이터 입력 받기
startDT = input('시작일(yyyymmdd): ')  # 시작일(20150601)
endDT = input('종료일(yyyymmdd): ')    # 종료일(20230808)

# 지역명으로 지점코드 조회
loc_name= input('지역을 입력하세요: ')

stnIds= wtapi.loc_code_sch(loc_name) 
weather_df = wtapi.weather_ext(startDT, endDT, stnIds)   # 함수 호출
    
weather_df.info()
