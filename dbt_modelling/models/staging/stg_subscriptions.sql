with subscription_source as (
        select * from {{ source('fake_source', 'subscriptions') }}
  ),
  subscription as (
      select
          {{ adapter.quote("valid_from") }},
        {{ adapter.quote("valid_to") }},
        {{ adapter.quote("subscription_id") }},
        {{ adapter.quote("payment_method") }},
        {{ adapter.quote("plan_id") }},
        {{ adapter.quote("start_date") }},
        {{ adapter.quote("user_id") }},
        {{ adapter.quote("end_date") }},
        {{ adapter.quote("status") }}

      from subscription_source
  )
  select * from subscription
    