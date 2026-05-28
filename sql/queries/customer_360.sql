SELECT
    u.user_id,
    u.country,
    u.industry,
    u.company_size,

    s.plan_type,
    s.monthly_revenue,
    s.is_churned,

    COUNT(DISTINCT ue.event_id) AS total_usage_events,

    AVG(ue.session_duration) AS avg_session_duration,

    COUNT(DISTINCT st.ticket_id) AS total_tickets,

    AVG(st.resolution_time_hours) AS avg_resolution_time,

    AVG(st.satisfaction_score) AS avg_satisfaction,

    COUNT(DISTINCT me.engagement_id) AS total_campaign_engagements,

    AVG(me.email_opened) AS email_open_rate,

    AVG(me.clicked) AS click_rate

FROM users u

JOIN subscriptions s
ON u.user_id = s.user_id

LEFT JOIN usage_events ue
ON u.user_id = ue.user_id

LEFT JOIN support_tickets st
ON u.user_id = st.user_id

LEFT JOIN marketing_engagement me
ON u.user_id = me.user_id

GROUP BY
    u.user_id,
    u.country,
    u.industry,
    u.company_size,
    s.plan_type,
    s.monthly_revenue,
    s.is_churned;