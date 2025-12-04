with regions_source as (
	select * from {{ source('fake_source', 'regions') }}
),
regions as (
	select
		{{ adapter.quote("region_id") }},
		{{ adapter.quote("region_name") }}
	from regions_source
)
select * from regions