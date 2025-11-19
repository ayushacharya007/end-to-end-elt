with subscription_source as (
        select * from {{ source('fake_source', 'subscriptions') }}
  )

  select * from subscription_source
    