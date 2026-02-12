CREATE TABLE IF NOT EXISTS watttime_forecasts
(
    region       String,
    signal_type  String,
    units        String,
    generated_at DateTime64(3, 'UTC'),
    point_time   DateTime64(3, 'UTC'),
    value        Float64
)
ENGINE = MergeTree
ORDER BY (region, signal_type, generated_at, point_time);
