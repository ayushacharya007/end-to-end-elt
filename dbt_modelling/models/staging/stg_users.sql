with user_source as (
  select
    {{ adapter.quote("user_id") }},
    {{ adapter.quote("first_name") }},
    {{ adapter.quote("last_name") }},
    {{ adapter.quote("email") }},
    {{ adapter.quote("signup_date") }},
    {{ adapter.quote("region_id") }},
    {{ adapter.quote("plan_id") }},
    {{ adapter.quote("referral_source_id") }},
    {{ adapter.quote("valid_from") }},
    {{ adapter.quote("valid_to") }}
  from {{ source('fake_source', 'users') }}
)
select * from user_source
    