import requests
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(filenames='open-api.ini')
    secret_key = config['DEFAULT']['SECRET_KEY']
    query_param = config['DEFAULT']['QUERY']

    url = "http://www.kopis.or.kr/openApi/restful/pblprfr?service="+secret_key+query_param
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
