with feature_source as (
  select
    {{ adapter.quote("feature_id") }},
    lower({{ adapter.quote("feature_name") }}) as feature_name,
    {{ adapter.quote("plan_id") }}
  from {{ source('fake_source', 'features') }}
)
select * from feature_source
