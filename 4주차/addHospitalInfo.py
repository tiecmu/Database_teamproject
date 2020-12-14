# -*- coding: utf-8 -*-
import pymysql
import csv
import math, numbers
import pandas as pd


class GeoUtil:
    """
    Geographical Utils
    """

    @staticmethod
    def degree2radius(degree):
        return degree * (math.pi / 180)

    @staticmethod
    def get_euclidean_distance(x1, y1, x2, y2, round_decimal_digits=5):
        """
        유클리안 Formula 이용하여 (x1,y1)과 (x2,y2) 점의 거리를 반환
        """
        if x1 is None or y1 is None or x2 is None or y2 is None:
            return None
        assert isinstance(x1, numbers.Number) and -180 <= x1 and x1 <= 180
        assert isinstance(y1, numbers.Number) and -90 <= y1 and y1 <= 90
        assert isinstance(x2, numbers.Number) and -180 <= x2 and x2 <= 180
        assert isinstance(y2, numbers.Number) and -90 <= y2 and y2 <= 90

        dLon = abs(x2 - x1)  # 경도 차이
        if dLon >= 180:  # 반대편으로 갈 수 있는 경우
            dLon -= 360  # 반대편 각을 구한다
        dLat = y2 - y1  # 위도 차이
        return round(math.sqrt(pow(dLon, 2) + pow(dLat, 2)), round_decimal_digits)


# mysql server 연결, port 및 host 주의!
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='wotjd2979',
                       password='123456',
                       db='K_COVID19',
                       charset='utf8')

# Connection 으로부터 Cursor 생성
cursor = conn.cursor(pymysql.cursors.DictCursor)

# Region.csv 에서 데이터를 읽어옮
data_region = pd.read_csv('Region.csv')
data_hospital = pd.read_csv('Hospital.csv')

try:
    sql = '''ALTER TABLE patientinfo ADD hospital_id bigint'''
    cursor.execute(sql)
except:
    print("이미 컬럼이 추가되었습니다.")


# # 중복된 case 제거를 위해 checking list & variable


now = {}  # 현재 수용인원 dictionary 만들기 & 중복된 case 제거를 위해 checking list & variable
for index, row in data_hospital.iterrows():
    # checking duplicate hospital_id & checking hospital_id == "NULL and calculating distance"
    if (row['Hospital_id'] in now.keys()) or (row['Hospital_id'] == "NULL"):
        continue
    else:
        now[row['Hospital_id']] = row['now']

sql = '''Select patient_id, province, city from patientinfo'''
cursor.execute(sql)

patients = cursor.fetchall()
for patient in patients:
    region = ''  # patient의 위도 경도를 위한 위치
    if str(patient['city']) == "etc" or patient['city'] == None:
        region = data_region[data_region['province'] == patient['province']]
        region = region.head(1)  # 대푯값 추출
    else:  # 다른 province 더라도 같은 이름의 city가 존재할 수 있으므로 데이터 에러 가능성 배제
        region = data_region[
            (data_region['city'] == patient['city']) & (data_region['province'] == patient['province'])]

    distance = {}
    for index, row in data_hospital.iterrows():
        # checking duplicate hospital_id & checking hospital_id == "NULL and calculating distance"
        # 중복된 case 제거를 위해 checking list & variable
        if (row['Hospital_id'] in distance.keys()) or (row['Hospital_id'] == "NULL"):
            continue
        else:  # hospital 과 patient의 거리
            try:
                distance[row['Hospital_id']] \
                    = GeoUtil.get_euclidean_distance(float(region['longitude']),
                                                     float(region['latitude']),
                                                     float(row['Hospital_longitude']),
                                                     float(row['Hospital_latitude']))
            except:  # region의 city와 patient의 city의 명칭이 다른 경우 예외처리
                continue

    # 거리순으르 오름차순으로 정렬
    sorted_distance = sorted(distance.items(), key=(lambda x: x[1]))

    # 수용인언이 가득차지 않으면서 가까운 병원 선택
    for hospital_id, distance in sorted_distance:
        selected_hospital = data_hospital[data_hospital['Hospital_id'] == hospital_id]

        if int(selected_hospital['capacity']) > now[hospital_id]:
            now[hospital_id] += 1
            sql = '''UPDATE patientinfo set hospital_id=''' + str(hospital_id) + ''' where patient_id=''' \
                  + str(patient['patient_id'])
            try:
                cursor.execute(sql)
                print("[OK] Inserting [%s] to patient : %s" % (hospital_id, patient['patient_id']))
            except (pymysql.Error, pymysql.Warning) as e:
                # print("[Error]  %s"%(pymysql.IntegrityError))
                if e.args[0] == 1062: continue
                print('[Error] %s | %s' % (hospital_id, e))
                break
            break;
# sql로 입력
hospital = []
with open("./Hospital.csv", 'r', encoding='utf8') as file:
    file_read = csv.reader(file)

    # Use column (1)Hospital_id (2)Hospital_name (3)Hospital_province (4)Hospital_city
    # (5)Hospital_latitude (6)Hospital_longitude (7)capacity (8)now
    # index = column - 1
    col_list = {
        'Hospital_id': 0,
        'Hospital_name': 1,
        'Hospital_province': 2,
        'Hospital_city': 3,
        'Hospital_latitude': 4,
        'Hospital_longitude': 5,
        'capacity': 6
    }

    for i, line in enumerate(file_read):

        # Skip first line
        if not i:
            continue

        # checking duplicate case_id & checking case_id == "NULL"
        if (line[col_list['Hospital_id']] in hospital) or (line[col_list['Hospital_id']] == "NULL"):
            continue
        else:
            hospital.append(line[col_list['Hospital_id']])

        # make sql data & query
        sql_data = []
        #"NULL" -> None (String -> null)
        for idx in col_list.values():
            if line[idx] == "NULL":
                line[idx] = None
            else:
                line[idx] = line[idx].strip()

            sql_data.append(line[idx])

        sql_data.append(now[int(line[col_list['Hospital_id']])])

        # Make query & execute
        query = """INSERT INTO `Hospital`(Hospital_id, Hospital_name, Hospital_province, Hospital_city,
        Hospital_latitude, Hospital_longitude, capacity, now) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
        sql_data = tuple(sql_data)

        # for debug
        try:
            cursor.execute(query, sql_data)
            print("[OK] Inserting [%s] to Hospital" % (line[col_list['Hospital_name']]))
        except (pymysql.Error, pymysql.Warning) as e:
            # print("[Error]  %s"%(pymysql.IntegrityError))
            if e.args[0] == 1062: continue
            print('[Error] %s | %s' % (line[col_list['Hospital_name']], e))
            break

conn.commit()
cursor.close()
