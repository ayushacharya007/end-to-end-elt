with referral_source as (
  select * from {{ source('fake_source', 'referral_sources') }}
),
referrals as (
  select
    {{ adapter.quote("referral_source_id") }},
    {{ adapter.quote("referral_source_name") }},
    {{ adapter.quote("valid_from") }},
    {{ adapter.quote("valid_to") }}

  from referral_source
)
select * from referrals