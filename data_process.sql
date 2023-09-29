-- 筛选出2006-2023年的数据
create table amount as
select "Country Code", "Country Name", "Fiscal Year" as "Year", "Transaction Type Name" as "Assistance Name", sum("Current Dollar Amount") as "Amount"
from us_foreign_aid_complete
where "Fiscal Year" between 2006 and 2023
group by "Country Code", "Country Name", "Fiscal Year", "Transaction Type Name"
order by "Country Code", "Fiscal Year", "Transaction Type Name";