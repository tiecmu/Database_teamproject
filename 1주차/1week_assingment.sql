create database K_COVID19;
DROP TABLE K_COVID19;

use K_covid19;

-- table 삭제
drop table patientinfo;
drop table region;
drop table weather;
drop table caseinfo;

-- create table
CREATE TABLE caseinfo(
	case_id INT NOT NULL,
	province VARCHAR(50),
	city VARCHAR(50),
	infection_group TINYINT(1),
	infection_case VARCHAR(50),
	confirmed INT,
	latitude FLOAT,
	longitude FLOAT,
	PRIMARY KEY (case_id)
);

CREATE TABLE region(
	code int NOT NULL,
	province varchar(50),
	city varchar(50),
	latitude float,
	longitude float,
	elementary_school_count int,
	kindergarten_count int,
	academy_ratio float,
	elderly_population_ratio float,
	nursing_home_count int,
	PRIMARY KEY (code)
);

CREATE TABLE weather(
	region_code int NOT NULL,
	province varchar(50),
	wdate date NOT NULL,    
	avg_temp float,
	min_temp float,
	max_temp float,
	PRIMARY KEY (region_code, wdate)
);

CREATE TABLE patientinfo(
patient_id bigint NOT NULL,
sex varchar(10),
age varchar(10),
country varchar(50),
province varchar(50),
city varchar(50),
infection_case varchar(50),
infected_by bigint,
contact_number int,
symptom_onset_date date,
confirmed_date date,
released_date date,
deceased_date date,
state varchar(20),
PRIMARY KEY(patient_id)
);


-- foreign key (pasing을 이용해 데이터를 모두 넣고 사용해주세요. *넣지 않아도 상관 없음*)
ALTER TABLE caseinfo ADD CONSTRAINT
`fk_mgr_ssn_employee_ssn` FOREIGN KEY (infection_case) REFERENCES
patientinfo (infection_case) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE region ADD CONSTRAINT
`fk_mgr_ssn_employee_ssn` FOREIGN KEY (province) REFERENCES
patientinfo (province) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE weather ADD CONSTRAINT
`fk_mgr_ssn_employee_ssn` FOREIGN KEY (wdate) REFERENCES
patientinfo (confirmed_date) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE weather ADD CONSTRAINT
`fk_mgr_ssn_employee_ssn` FOREIGN KEY (infected_by) REFERENCES
patientinfo (patient_id) ON DELETE SET NULL ON UPDATE CASCADE;


-- table 확인
select * from patientinfo;
select * from region;
select * from caseinfo;
select * from weather;
select count(*) from patientinfo;
select count(*) from region;
select count(*) from caseinfo;
select count(*) from weather;
