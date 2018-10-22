drop table if exists customer; 

CREATE TABLE customer (
        cust_id BIGINT,
        first_name VARCHAR(15),
        last_name VARCHAR(20),
        city VARCHAR(27),
        state VARCHAR(20),
        tier INT,
		phone BIGINT,
        sales REAL
);

CREATE TABLE credit_score (
        cust_id BIGINT,
        credit_score INT
);
CREATE TABLE bod (
        cust_id BIGINT,
        bod VARCHAR(10)
);

copy customer  FROM 'C:\_DATA\DW5\customer.csv' DELIMITER ';' CSV HEADER;
;

copy credit_score  FROM 'C:\_DATA\DW5\credit_score.csv' DELIMITER ';' CSV HEADER;
;

copy bod  FROM 'C:\_DATA\DW5\bod.csv' DELIMITER ';' CSV HEADER;
;

alter table customer add primary key (cust_id);

drop table if exists customer10k;

create table customer10k  as
select * from customer where cust_id % 100 = 1 
;
alter table customer10k add primary key (cust_id);


drop table if exists customer30k;

create table customer30k  as
select * from customer where cust_id % 100 < 3
;

alter table customer10k add primary key (cust_id);
;
