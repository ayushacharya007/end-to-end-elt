with subscription_source as (
  select
    {{ adapter.quote("subscription_id") }},
    {{ adapter.quote("user_id") }},
    {{ adapter.quote("plan_id") }},
    {{ adapter.quote("payment_method_id") }},
    {{ adapter.quote("start_date") }},
    {{ adapter.quote("end_date") }},
    {{ adapter.quote("status") }},
    {{ adapter.quote("valid_from") }},
    {{ adapter.quote("valid_to") }}
  from {{ source('fake_source', 'subscriptions') }}
)
select * from subscription_source
    