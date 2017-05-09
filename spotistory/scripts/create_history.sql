CREATE TABLE IF NOT EXISTS history
(
  music_id text,
  uri text,
  played_at int,
  to_add bool,
  week_id int,
  UNIQUE(music_id, played_at) ON CONFLICT IGNORE
);

