import threading
import requests
import json

def getAccessToken(consumer_key, consumer_secret):
    URL = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"
    PARAMS = {
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret
    }

    response = requests.get(URL, params=PARAMS)

    if response.status_code == 200:
        return response.json()['result']['accessToken']
    else:
        return None

def getGeoLevel1Code(ACCESS_TOKEN, path):
    result = {}

    URL = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json"
    PARAMS = {
        "accessToken": ACCESS_TOKEN
    }
    
    response = requests.get(URL, params=PARAMS)

    if response.status_code == 200:
        datalist = response.json()['result']

        threads = []
        for item in datalist:
            print(item['addr_name'] + ' 처리중...')
            result[item['addr_name']] = {}
            t = threading.Thread(target=getGeoLevel2Code(ACCESS_TOKEN, item['cd'], result[item['addr_name']]))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        print('JSON 파일을 작성중입니다.')
        fileWrite(path, result)
        print('JSON 파일 생성 완료!')
        return result
    else:
        return None

def getGeoLevel2Code(ACCESS_TOKEN, cd, result_dict):
    URL = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json"
    PARAMS = {
        "accessToken": ACCESS_TOKEN,
        "cd": cd
    }
    
    response = requests.get(URL, params=PARAMS)

    if response.status_code == 200:
        datalist = response.json()['result']

        threads = []
        for item in datalist:
            result_dict[item['addr_name']] = {}
            t = threading.Thread(target=getGeoLevel3Code, args=(ACCESS_TOKEN, item['cd'], result_dict[item['addr_name']]))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
    else:
        return None

def getGeoLevel3Code(ACCESS_TOKEN, cd, result_dict):
    if len(cd) > 5:
        return
    
    URL = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json"
    PARAMS = {
        "accessToken": ACCESS_TOKEN,
        "cd": cd
    }
    
    response = requests.get(URL, params=PARAMS)
    if response.status_code == 200:
        datalist = response.json()['result']
        
        threads = []
        for item in datalist:
            result_dict[item['addr_name']] = {}
            t = threading.Thread(target=transCoord, args=(ACCESS_TOKEN, item['x_coor'], item['y_coor'], result_dict, item['addr_name']))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
    else:
        return None

def transCoord(ACCESS_TOKEN, x_coor, y_coor, result_dict, addr_name):
    URL = "https://sgisapi.kostat.go.kr/OpenAPI3/transformation/transcoord.json"
    PARAMS = {
        "accessToken": ACCESS_TOKEN,
        "src": "5179",
        "dst": "4326",
        "posX": x_coor,
        "posY": y_coor
    }
    
    response = requests.get(URL, params=PARAMS)

    if response.status_code == 200:
        result = response.json()['result']
        result_dict[addr_name] = {
            "x": result['posX'],
            "y": result['posY']
        }
    else:
        return None

def fileWrite(path, data):
    open(path, 'w').close()
    with open(path, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def mappingToGeo(consumer_key, consumer_secret, path):
    print('각 시/군/구의 UTM-K (GRS80) 좌표 데이터를 WGS84 좌표 데이터로 변환하여 JSON으로 저장합니다.')
    ACCESS_TOKEN = getAccessToken(consumer_key, consumer_secret)

    if ACCESS_TOKEN is not None:
        print('Access Token을 정상적으로 발급 하였습니다.')
        print('작업을 시작합니다.')
        getGeoLevel1Code(ACCESS_TOKEN, path)
        print('작업을 종료합니다.')
    else:
        print('Access Token을 발급할 수 없습니다.')

if __name__ == "__main__":
    consumer_key = "" # 통계청에서 발급받은 consumer_key
    consumer_secret = "" # 통계청에서 발급받은 consumer_secret
    path = "./MappingGeo.json"
    mappingToGeo(consumer_key, consumer_secret, path)