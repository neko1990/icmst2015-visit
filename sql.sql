CREATE TABLE users(
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT NOT NULL,
    privilege INTEGER NOT NULL DEFAULT 0,
    studentid TEXT,
    college TEXT ,
    telephone TEXT,
    name TEXT,
    gender TEXT,
    ctime DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reg_log(
    rid INTEGER PRIMARY KEY AUTOINCREMENT,
    uid REFERENCES users(uid),
    email TEXT UNIQUE,
    studentid TEXT,
    college TEXT ,
    telephone TEXT,
    name TEXT,
    gender TEXT,
    ctime DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE articles (
    aid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE ,
    title TEXT NOT NULL UNIQUE,
    parent TEXT DEFAULT "NOPARENT",
    has_child_p INTEGER DEFAULT 0,
    content TEXT
);

CREATE TABLE sessions (
    session_id CHAR(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data text
);
