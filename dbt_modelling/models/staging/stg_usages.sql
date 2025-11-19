with user_source as (
        select * from {{ source('fake_source', 'usages') }}
  ),
  usage as (
      select
          {{ adapter.quote("user_id") }},
        {{ adapter.quote("plan_id") }},
        {{ adapter.quote("storage_used_mb") }},
        {{ adapter.quote("active_minutes") }},
        {{ adapter.quote("usage_id") }},
        {{ adapter.quote("actions_performed") }},
        {{ adapter.quote("usage_date") }},
        {{ adapter.quote("api_calls") }}

      from user_source
  )
  select * from usage
    