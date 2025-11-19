with usage_source as (
        select * from {{ source('fake_source', 'usages') }}
  )

  select * from usage_source
    