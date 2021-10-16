CREATE TABLE IF NOT EXISTS wantlists (
    username VARCHAR,
    release_id VARCHAR
);

CREATE TABLE IF NOT EXISTS listings (
    release_id VARCHAR,
    listing_id VARCHAR,
    title VARCHAR,
    url VARCHAR,
    media_condition VARCHAR,
    sleeve_condition VARCHAR,
    ships_from VARCHAR,
    price VARCHAR
);
