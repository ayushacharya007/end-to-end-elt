with referral_source as (
  select
    {{ adapter.quote("referral_source_id") }},
    lower({{ adapter.quote("source_name") }}) as source_name
  from {{ source('fake_source', 'referrals') }}
)
select * from referral_source