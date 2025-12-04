with payment_method_source as (
  select
    {{ adapter.quote("payment_method_id") }},
    {{ adapter.quote("method_name") }}
  from {{ source('fake_source', 'payment_methods') }}
)
select * from payment_method_source