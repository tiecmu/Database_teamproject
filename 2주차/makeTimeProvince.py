# -*- coding: utf-8 -*-
import pymysql
import csv
import pandas as pd
import numpy as np

# mysql server 연결, port 및 host 주의!
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='wotjd2979',
                       password='123456',
                       db='K_COVID19',
                       charset='utf8')

# Connection 으로부터 Cursor 생성
cursor = conn.cursor()

data = pd.read_csv('K_COVID19.csv')

# 데이터프레임 사용
# province 의 중복되지 않은 값 생성
df = pd.DataFrame(data['province'])
df = df.drop_duplicates().dropna(axis=1)

province_unique = df['province'].tolist()

print(province_unique)
# # Using Hashing
# # get confirmed_date from "K_COVID19.csv" and count
confirmed = data[['confirmed_date', 'province']]
cdate_dic = {}
for date_province in confirmed.values:  # 날짜 / 지역 별 확진된 사람 수
    data_province_tuple = tuple(date_province)
    if data_province_tuple in cdate_dic.keys():
        cdate_dic[data_province_tuple] = cdate_dic[data_province_tuple] + 1
    else:
        cdate_dic[data_province_tuple] = 1

# get released_date from "K_COVID19.csv" and count
released = data[['released_date', 'province']]
rdate_dic = {}
for date_province in released.values:  # 날짜 별 완치된 사람 수
    data_province_tuple = tuple(date_province)
    if data_province_tuple in rdate_dic.keys():
        rdate_dic[data_province_tuple] = rdate_dic[data_province_tuple] + 1
    else:
        rdate_dic[data_province_tuple] = 1

# get deceased_date from "K_COVID19.csv" and count
deceased = data[['deceased_date', 'province']]
ddate_dic = {}
for date_province in deceased.values:  # 날짜 별 사망자 수
    data_province_tuple = tuple(date_province)
    if data_province_tuple in ddate_dic.keys():
        ddate_dic[data_province_tuple] = ddate_dic[data_province_tuple] + 1
    else:
        ddate_dic[data_province_tuple] = 1

# 중복된 case 제거를 위해 checking list & variable
date_province = []
total_confirmed = {}  # 총 확인된 감염자 수
total_released = {}  # 총 완치된
total_deceased = {}  # 총 사망자

# 각 province 에 대한 확진자, 완치자, 사망자 수 초기화
for province in province_unique:
    total_confirmed[province] = 0
    total_released[province] = 0
    total_deceased[province] = 0

with open("./addtional_Timeinfo.csv", 'r') as file:
    file_time_read = csv.reader(file)

    # Use column 1(date)
    # index = column - 1
    col_list = {
        'date': 0}

    for i, line in enumerate(file_time_read):

        # Skip first line
        if not i:
            continue

        for province in province_unique:
            # composite key (date, province) 중복확인 및 null값 배제
            if (line[col_list['date']], province) in date_province or (line[col_list['date']] == "NULL" or province == "NULL"):
                continue
            else:
                date_province.append((line[col_list['date']], province))

            # make sql data & query
            sql_data = []
            # "NULL" -> None (String -> null)
            for idx in col_list.values():
                if line[idx] == "NULL":
                    line[idx] = None
                else:
                    line[idx] = line[idx].strip()

            sql_data.append(line[idx])
            sql_data.append(province)

            # append "total number from confirmed_date and province" to sql_date list
            if (line[col_list['date']], province) in cdate_dic.keys():
                total_confirmed[province] = total_confirmed[province] + cdate_dic[(line[col_list['date']], province)]
            sql_data.append(total_confirmed[province])

            # append "total number from released_date and province" to sql_date list
            if (line[col_list['date']], province) in rdate_dic.keys():
                total_released[province] = total_released[province] + rdate_dic[(line[col_list['date']], province)]
            sql_data.append(total_released[province])

            # append "total number from deceased_date and province" to sql_date list
            if (line[col_list['date']], province) in ddate_dic.keys():
                total_deceased[province] = total_deceased[province] + ddate_dic[(line[col_list['date']], province)]
            sql_data.append(total_deceased[province])

            # Make query & execute
            query = """INSERT INTO `TimeProvince`(date, province, confirmed, released, deceased) VALUES (%s,%s,%s,%s,%s)"""
            sql_data = tuple(sql_data)

            # for debug
            try:
                cursor.execute(query, sql_data)
                print("[OK] Inserting [%s, %s] to TimeProvince" % (line[col_list['date']], province))
            except (pymysql.Error, pymysql.Warning) as e:
                # print("[Error]  %s"%(pymysql.IntegrityError))
                if e.args[0] == 1062: continue
                print('[Error] %s | %s' % (line[col_list['date']], e))
                break

conn.commit()
cursor.close()
