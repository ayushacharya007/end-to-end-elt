with dim_users as (
    select 
        {{ adapter.quote("user_id") }},
        concat({{ adapter.quote("first_name") }}, ' ', {{ adapter.quote("last_name") }}) as {{ adapter.quote("full_name") }},
        {{ adapter.quote("email") }},
        {{ adapter.quote("signup_date") }},
        {{ adapter.quote("referral_source") }},
        {{ adapter.quote("plan_id") }},
        {{ adapter.quote("region") }},
        {{ adapter.quote("valid_from") }},
        {{ adapter.quote("valid_to") }}

    from {{ ref('stg_users') }}
)

select * from dim_users