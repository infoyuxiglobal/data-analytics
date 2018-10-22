drop table if exists customer_part;

CREATE TABLE customer_part (
        cust_id BIGINT,
        first_name VARCHAR(15),
        last_name VARCHAR(20),
        city VARCHAR(27),
        state VARCHAR(20),
        tier INT,
		phone BIGINT,
        sales REAL
) partition by range (tier)
;

-- This is the template for creating each of the partitions
create table customer_part_$LL_$UL partition of customer_part 
for values from ($LL) to ($UL$); -- the upper limit (after "to") is **NOT** included in the partition!

-- Now populate the table with data
copy customer_part  FROM 'C:\_DATA\DW5\customer.csv' DELIMITER ';' CSV HEADER;
;