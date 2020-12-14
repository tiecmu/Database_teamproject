-- remove hospital table
drop table Hospital;

-- create hospital table
create table Hospital (
	Hospital_id bigint not null,
	Hospital_name varchar(100),
	Hospital_province varchar(50),
    Hospital_city varchar(50),
	Hospital_latitude float,
	Hospital_longitude float,
	capacity int,
    now int,
    PRIMARY KEY(Hospital_id)
);

-- foreign key (pasing을 이용해 데이터를 모두 넣고 사용해주세요. *넣지 않아도 상관 없음*)
ALTER TABLE patientinfo ADD CONSTRAINT
`fk_p.Hospital_id_H.Hospital_id` FOREIGN KEY (hospital_id) REFERENCES
Hospital (Hospital_id) ON DELETE SET NULL ON UPDATE CASCADE;

-- table 확인
select * from Hospital;
select count(*) from Hospital;