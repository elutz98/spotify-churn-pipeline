-- Step 1: Identify churned users
-- A user has churned if they ever hit the Cancellation Confirmation page
WITH churn_flags AS (
  SELECT
    userId,
    MAX(CASE WHEN page = 'Cancellation Confirmation' THEN 1 ELSE 0 END) AS has_churned
  FROM `spotify-churn-pipeline.sparkify_churn.raw_events`
  WHERE userId IS NOT NULL  -- filter out logged-out sessions with blank userId
  GROUP BY userId
),

-- Step 2: Clean timestamps and get one row per relevant event
events_clean AS (
  SELECT
    userId,
    page,
    length,
    TIMESTAMP_MILLIS(CAST(ts AS INT64)) AS event_time
  FROM `spotify-churn-pipeline.sparkify_churn.raw_events`
  WHERE userId IS NOT NULL
),

-- Step 3: Aggregate into user-level engagement features
user_features AS (
  SELECT
    userId,

    -- Total listening hours: sum song lengths (seconds) / 3600
    SUM(CASE WHEN page = 'NextSong' THEN length ELSE 0 END) / 3600.0 AS total_listening_hours,

    -- Skip rate: proportion of song plays that were "skipped"
    -- We approximate a skip as a NextSong event where the user didn't listen to the full song
    -- Simpler proxy: ratio of Thumbs Down events to total NextSong events
    SAFE_DIVIDE(
      COUNTIF(page = 'Thumbs Down'),
      COUNTIF(page = 'NextSong')
    ) AS average_skip_rate,

    -- Active days in the last 30 days of the dataset's time window
    COUNT(DISTINCT
      CASE
        WHEN event_time >= (
          SELECT TIMESTAMP_SUB(MAX(event_time), INTERVAL 30 DAY)
          FROM events_clean
        )
        THEN DATE(event_time)
      END
    ) AS active_days_in_last_30,

    -- Total events, useful as a general engagement signal
    COUNT(*) AS total_events

  FROM events_clean
  GROUP BY userId
)

-- Final: join features with churn label
SELECT
  f.userId,
  f.total_listening_hours,
  f.average_skip_rate,
  f.active_days_in_last_30,
  f.total_events,
  c.has_churned
FROM user_features f
JOIN churn_flags c
  ON f.userId = c.userId
ORDER BY f.userId;