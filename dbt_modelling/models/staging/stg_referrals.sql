with referral_source as (
  select
    {{ adapter.quote("referral_source_id") }},
    {{ adapter.quote("source_name") }}
  from {{ source('fake_source', 'referrals') }}
)
select * from referral_source