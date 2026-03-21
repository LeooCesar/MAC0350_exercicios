CREATE TABLE artist (
    artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE band_member (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    artist_id INTEGER NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
);

CREATE TABLE album (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    artist_id INTEGER NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
);

CREATE TABLE song (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    FOREIGN KEY (album_id) REFERENCES album(album_id)
);

CREATE TABLE album_review (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 10), 
    comment TEXT,
    album_id INTEGER NOT NULL,
    FOREIGN KEY (album_id) REFERENCES album(album_id)
);

CREATE TABLE song_review (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 10),
    comment TEXT,
    song_id INTEGER NOT NULL,
    FOREIGN KEY (song_id) REFERENCES song(song_id)
);