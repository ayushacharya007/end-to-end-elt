with usage_source as (
  select
    {{ adapter.quote("usage_id") }},
    {{ adapter.quote("user_id") }},
    {{ adapter.quote("subscription_id") }},
    {{ adapter.quote("usage_date") }},
    {{ adapter.quote("actions_performed") }},
    {{ adapter.quote("api_calls") }},
    {{ adapter.quote("storage_used_mb") }},
    {{ adapter.quote("active_minutes") }}
  from {{ source('fake_source', 'usages') }}
)
select * from usage_source  