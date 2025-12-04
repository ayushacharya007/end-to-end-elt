with plan_source as (
  select
    {{ adapter.quote("plan_id") }},
    {{ adapter.quote("plan_name") }},
    {{ adapter.quote("monthly_fee") }},
    {{ adapter.quote("max_users") }},
    {{ adapter.quote("api_limit") }},
    {{ adapter.quote("storage_limit_mb") }},
    {{ adapter.quote("project_limit") }}
  from {{ source('fake_source', 'plans') }}
)
select * from plan_source
  