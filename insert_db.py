import pymysql
import configparser


def db_insert(musical_dict):

    preprocessing(musical_dict)

    config = configparser.ConfigParser()
    config.read(filenames='open-api.ini')
    host = config['DATABASE']['HOST']
    user = config['DATABASE']['USER']
    password = config['DATABASE']['PASSWORD']
    db = config['DATABASE']['DB']
    conn = pymysql.connect(
        host=host, user=user, password=password, db=db
    )
    cursor = conn.cursor()

    for key, musical in musical_dict.items():
        data = [musical['musical_id'], musical['begin_date'], musical['end_date'], musical['casting'],
                musical['genre'], musical['musical_status'], musical['name'], musical['place_name'],
                musical['poster_url'], musical['running_time']]
        query = "INSERT INTO musical (id,begin_date,end_date,casting," \
                "genre,musical_status,name,place_name,poster_url,running_time) " \
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            cursor.execute(query, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f'예외가 발생했습니다. 예외 메세지 : {e}')

    conn.close()


def preprocessing(musical_dict):
    for musical in musical_dict.values():
        if musical['casting'] == ' ':
            musical['casting'] = None
