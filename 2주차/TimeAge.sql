-- table 삭제
drop table timeage;

-- create table
create table timeage(
	date DATE,
	age VARCHAR(10),
	confirmed INT,
	deceased INT
);

-- foreign key (pasing을 이용해 데이터를 모두 넣고 사용해주세요. *넣지 않아도 상관 없음*)
ALTER TABLE timeage ADD CONSTRAINT
`fk_tp_province_p_province` FOREIGN KEY (age) REFERENCES
patientinfo (age) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE timeage ADD CONSTRAINT
`fk_tp_date_t_date` FOREIGN KEY (date) REFERENCES
timeinfo (date) ON DELETE SET NULL ON UPDATE CASCADE;


-- table 확인
select * from timeage;
select count(*) from timeage;
