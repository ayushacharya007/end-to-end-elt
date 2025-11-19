with user_source as (
        select * from {{ source('fake_source', 'users') }}
  ),
  user as (
      select
          {{ adapter.quote("valid_from") }},
        {{ adapter.quote("valid_to") }},
        {{ adapter.quote("email") }},
        {{ adapter.quote("plan_id") }},
        {{ adapter.quote("region") }},
        {{ adapter.quote("first_name") }},
        {{ adapter.quote("last_name") }},
        {{ adapter.quote("user_id") }},
        {{ adapter.quote("signup_date") }},
        {{ adapter.quote("referral_source") }}

      from user_source
  )
  select * from user
    