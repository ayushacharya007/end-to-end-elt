with user_source as (
        select * from {{ source('fake_source', 'users') }}
  )

  select * from user_source
    