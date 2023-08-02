# %%

last_version = '3.1.10'

def version():
    return last_version

# 주민등록번호 입력시 - 제거
def get_raw_value(data):
    return data[0:6] + data[7:]

# 주민등록번호 입력시 년도만 추출
def get_year(data):
    return data[:2]    

# 주민등록번호 입력시 월/일만 추출
def get_birtlh(data):
    return data[2:6]

def get_gender(data):
    if data[7] == '1' or data[7] == '3':
        return "남자"
    else:
        return "여자"
    

if __name__ == "__main__":
    print(__name__)
    print(get_raw_value("800101-1234567"))
    print(get_year("800101-1234567"))
    print(get_birtlh("800101-1234567"))
    print(get_gender("800101-1234567"))
    

# %%
