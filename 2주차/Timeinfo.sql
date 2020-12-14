-- table 삭제
drop table timeinfo;

create table timeinfo(
	date DATE NOT NULL,
	test INT,
	negative INT,
	confirmed INT,
	released INT,
	deceased INT,
	PRIMARY KEY(date)
);

-- table 확인
select * from timeinfo;
select count(*) from timeinfo;

