# -*- coding: utf-8 -*-
import pymysql
import csv
import pandas as pd

# 처음에 딕셔너리에 데이터 날짜별로 다 모으고 나중에 딕셔너리 리스트로 바꾸고
# for문으로 나눠서 입력

# mysql server 연결, port 및 host 주의!
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='wotjd2979',
                       password='123456',
                       db='K_COVID19',
                       charset='utf8')

# Connection 으로부터 Cursor 생성
cursor = conn.cursor()

data = pd.read_csv('./K_COVID19.csv',na_values = ['?', '??', 'N/A', 'NA', 'nan', 'NaN', '-nan', '-NaN', 'null'])

df=data[['sex']]
df=df.drop_duplicates().dropna(how='any')
#or axis=0

sex_unique=df['sex'].tolist()
print(sex_unique)

# Using Hashing
# get confirmed_date from "K_COVID19.csv" and count
confirmed_date = data[['confirmed_date', 'sex']]  # confirmed_date 와  sex를 colum으로 가지는 dataFrame을 따로 만들어 주는 건가?
cdate_dic = {}
for date_sex in confirmed_date.values:
    date_sex_tuple=tuple(date_sex)
    if date_sex_tuple in cdate_dic.keys():
        cdate_dic[date_sex_tuple] = cdate_dic[date_sex_tuple]+1
    else:
        cdate_dic[date_sex_tuple]=1

# get deceased_date from "K_COVID19.csv" and count
deceased_date = data[['deceased_date', 'sex']]
ddate_dic = {}

for ddate_sex in deceased_date.values:
    ddate_sex_tuple=tuple(ddate_sex)
    if ddate_sex_tuple in ddate_dic.keys():
       ddate_dic[ddate_sex_tuple] = ddate_dic[ddate_sex_tuple]+1
    else:
        ddate_dic[ddate_sex_tuple]=1


# 중복된 case 제거를 위해 checking list & variable
date_gender = []
total_confirmed = {}
total_deceased = {}

for sex in sex_unique:
    total_confirmed[sex] = 0
    total_deceased[sex] = 0

with open("./addtional_Timeinfo.csv", 'r') as file:
    file_read = csv.reader(file)

    # Use column 1(date)
    # index = column - 1
    col_list = {
        'date': 0
    }

    for i, line in enumerate(file_read):

        # Skip first line
        if not i:
            continue

        for sex in sex_unique:
            # checking duplicate case_id & checking case_id == "NULL"
            if (line[col_list['date']], sex) in date_gender or (line[col_list['date']] == "NULL" or sex=="NULL"):
                continue
            else:
                date_gender.append((line[col_list['date']], sex))

            # make sql data & query
            sql_data = []
            # "NULL" -> None (String -> null)
            for idx in col_list.values():
                if line[idx] == "NULL":
                    line[idx] = None
                else:
                    line[idx] = line[idx].strip()

                sql_data.append(line[idx])
                sql_data.append(sex)

            # append "total number from confirmed_date" to sql_date list
            # 확진자수 누적

            if (line[col_list['date']],sex) in cdate_dic.keys():
                total_confirmed[sex] = total_confirmed[sex] + cdate_dic[(line[col_list['date']], sex)]
            sql_data.append(total_confirmed[sex])

            if (line[col_list['date']], sex) in ddate_dic.keys():
                total_deceased[sex] = total_deceased[sex] + ddate_dic[(line[col_list['date']], sex)]
            sql_data.append(total_deceased[sex])

            # Make query & execute

            query = """INSERT INTO `timegender`(date, sex, confirmed,  deceased) VALUES (%s,%s,%s,%s)"""
            sql_data = tuple(sql_data)
            print(sql_data)
            # for debug

            try:
                cursor.execute(query, sql_data)
                print("[OK] Inserting [%s] %s" % (
                    line[col_list['date']], sex))
            except (pymysql.Error, pymysql.Warning) as e:
                # print("[Error]  %s"%(pymysql.IntegrityError))
                if e.args[0] == 1062: continue
                print('[Error] %s | %s' % (line[col_list['date']], e))
                break

conn.commit()
cursor.close()