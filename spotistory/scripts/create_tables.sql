CREATE TABLE IF NOT EXISTS genre
(
  id TEXT PRIMARY KEY ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS artist
(
  id TEXT PRIMARY KEY ON CONFLICT IGNORE,
  uri TEXT NOT NULL,
  title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS artist_genre
(
  artist_id TEXT NOT NULL,
  genre_id TEXT NOT NULL,
  FOREIGN KEY(artist_id) REFERENCES artist(id),
  FOREIGN KEY(genre_id) REFERENCES genre(id),
  UNIQUE(artist_id, genre_id) ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS track
(
  id TEXT PRIMARY KEY ON CONFLICT IGNORE,
  uri TEXT NOT NULL,
  duration INTEGER,
  artist_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  FOREIGN KEY(artist_id) REFERENCES artist(id)
);

CREATE TABLE IF NOT EXISTS user
(
  display_name TEXT NOT NULL,
  id TEXT PRIMARY KEY ON CONFLICT IGNORE,
  uri TEXT NOT NULL,
  followers INTEGER
);

CREATE TABLE IF NOT EXISTS history
(
  track_id TEXT NOT NULL,
  played_at DATETIME,
  user_id TEXT,
  UNIQUE(track_id, played_at, user_id) ON CONFLICT IGNORE,
  FOREIGN KEY(track_id) REFERENCES track(id),
  FOREIGN KEY (user_id) REFERENCES user(id)
);
