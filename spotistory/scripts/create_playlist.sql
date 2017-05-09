CREATE TABLE IF NOT EXISTS playlists
(
  week_id int,
  playlist_id text,
  UNIQUE(week_id) ON CONFLICT IGNORE
);