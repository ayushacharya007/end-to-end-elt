with region_source as (
	select
		{{ adapter.quote("region_id") }},
		lower({{ adapter.quote("region_name") }}) as region_name
	from {{ source('fake_source', 'regions') }}
)
select * from region_source