with payment_method_source as (
  select
    {{ adapter.quote("payment_method_id") }},
    lower({{ adapter.quote("method_name") }}) as method_name
  from {{ source('fake_source', 'payment_methods') }}
)
select * from payment_method_source