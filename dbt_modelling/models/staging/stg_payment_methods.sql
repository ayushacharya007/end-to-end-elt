with payment_methods_source as (
  select * from {{ source('fake_source', 'payment_methods') }}
),
payment_methods as (
  select
    {{ adapter.quote("payment_method_id") }},
    {{ adapter.quote("method_name") }}
  from payment_methods_source
)
select * from payment_methods