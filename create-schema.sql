
PRAGMA foreign_keys=OFF;
DROP TABLE IF EXISTS users;
PRAGMA foreign_keys=ON;


CREATE TABLE users (
    user_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    PRIMARY KEY (user_id)
);
