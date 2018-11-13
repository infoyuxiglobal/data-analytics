explain analyze
select 
	cfn.cust_id, csa.sales, cph.phone
from customer_sales            as  csa
inner join customer_phone      as cph
	on csa.cust_id = cph.cust_id 
inner join customer_first_name as cfn 
	on csa.cust_id = cfn.cust_id 

select * from  customer_phone
--
analyze customer_phone
--
select * from pg_stats where tablename like 'customer_%'