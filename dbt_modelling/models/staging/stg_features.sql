with feature_source as (
  select * from {{ source('fake_source', 'features') }}
),
features as (
  select
    {{ adapter.quote("feature_id") }},
    {{ adapter.quote("feature_name") }},
    {{ adapter.quote("plan_id") }}
  from feature_source
)
select * from features
