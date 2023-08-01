import requests
import configparser
import xml.etree.ElementTree as ET
import musical_list_api as ml


def build_query_param(param_dict):
    query = ""
    for key, val in param_dict.items():
        query += ("&" + key + "=" + str(val))
    return query


def api_request(secret_key,query):
    url = "http://www.kopis.or.kr/openApi/restful/pblprfr?service="+secret_key+query
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(filenames='open-api.ini')
    secret_key = config['DEFAULT']['SECRET_KEY']

    stdate = 20230801
    eddate = 20230901
    cpage = 0
    rows = 100
    shcate = "GGGA"
    param_dict = {
        'stdate': stdate,
        'eddate': eddate,
        'cpage': cpage,
        'rows': rows,
        'shcate': shcate
    }

    musical_dict = {}

    # 공연 목록 api call 후 파싱
    while True:
        param_dict['cpage'] += 1
        query = build_query_param(param_dict)
        http_response_text = api_request(secret_key, query)
        root = ET.fromstring(http_response_text)
        if root.find('db') is None:
            break
        ml.get_musical_from_xml(musical_dict,root)

    for key, val in musical_dict.items():
        print(f'key = {key}, values = {val}')


