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
# age 의 중복되지 않은 값 생성
df = pd.DataFrame(data['age'])
df = df.drop_duplicates().dropna(axis=0) #NULL 값을 배제하였습니다.

age_unique = list(np.array(df['age'].tolist()))

print(age_unique)

# Using Hashing
# get confirmed_date from "K_COVID19.csv" and count
confirmed = data[['confirmed_date', 'age']]
cdate_dic = {}
for date_age in confirmed.values:  # 날짜 / 지역 별 확진된 사람 수
    data_age_tuple = tuple(date_age)
    if data_age_tuple in cdate_dic.keys():
        cdate_dic[data_age_tuple] = cdate_dic[data_age_tuple] + 1
    else:
        cdate_dic[data_age_tuple] = 1

deceased = data[['deceased_date', 'age']]
ddate_dic = {}
for date_age in deceased.values:  # 날짜 별 사망자 수
    data_age_tuple = tuple(date_age)
    if data_age_tuple in ddate_dic.keys():
        ddate_dic[data_age_tuple] = ddate_dic[data_age_tuple] + 1
    else:
        ddate_dic[data_age_tuple] = 1

# 중복된 case 제거를 위해 checking list & variable
date_age = []
total_confirmed = {}  # 총 확인된 감염자 수
total_deceased = {}  # 총 사망자

# 각 age 에 대한 확진자, 완치자, 사망자 수 초기화
for age in age_unique:
    total_confirmed[age] = 0
    total_deceased[age] = 0

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

        for age in age_unique:
            # composite key (date, age) 중복확인 및 null값 배제
            if (line[col_list['date']], age) in date_age or (line[col_list['date']] == "NULL" or age == "NULL"):
                continue
            else:
                date_age.append((line[col_list['date']], age))

            # make sql data & query
            sql_data = []
            # "NULL" -> None (String -> null)
            for idx in col_list.values():
                if line[idx] == "NULL":
                    line[idx] = None
                else:
                    line[idx] = line[idx].strip()

            sql_data.append(line[idx])
            sql_data.append(age)

            # append "total number from confirmed_date and age" to sql_date list
            if (line[col_list['date']], age) in cdate_dic.keys():
                total_confirmed[age] = total_confirmed[age] + cdate_dic[(line[col_list['date']], age)]
            sql_data.append(total_confirmed[age])

            # append "total number from deceased_date and age" to sql_date list
            if (line[col_list['date']], age) in ddate_dic.keys():
                total_deceased[age] = total_deceased[age] + ddate_dic[(line[col_list['date']], age)]
            sql_data.append(total_deceased[age])

            # Make query & execute
            query = """INSERT INTO `TimeAge`(date, age, confirmed, deceased) VALUES (%s,%s,%s,%s)"""
            sql_data = tuple(sql_data)

            # for debug
            try:
                cursor.execute(query, sql_data)
                print("[OK] Inserting [%s, %s] to TimeAge" % (line[col_list['date']], age))
            except (pymysql.Error, pymysql.Warning) as e:
                # print("[Error]  %s"%(pymysql.IntegrityError))
                if e.args[0] == 1062: continue
                print('[Error] %s | %s' % (line[col_list['date']], e))
                break

conn.commit()
cursor.close()
