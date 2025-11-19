with plan_source as (
        select * from {{ source('fake_source', 'plans') }}
  )

  select * from plan_source