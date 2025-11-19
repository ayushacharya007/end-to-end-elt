with plan_source as (
        select * from {{ source('fake_source', 'plans') }}
  ),
  plan as (
      select
          {{ adapter.quote("monthly_fee") }},
        {{ adapter.quote("features") }},
        {{ adapter.quote("plan_id") }},
        {{ adapter.quote("max_users") }},
        {{ adapter.quote("plan_name") }}

      from plan_source
  )
  select * from plan
    