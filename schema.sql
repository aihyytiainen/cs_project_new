CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT,
	password TEXT,
	groupA BOOLEAN,
	groupB BOOLEAN,
	groupC BOOLEAN,
	groupD BOOLEAN,
	admin BOOLEAN
);
CREATE TABLE polls (
	id SERIAL PRIMARY KEY,
	topic TEXT,
	created_at TIMESTAMP,
	created_by TEXT
	visible BOOLEAN
);

CREATE TABLE choices (
	id SERIAL PRIMARY KEY,
	poll_id INTEGER REFERENCES polls,
	choice TEXT
);

CREATE TABLE answers (
	id SERIAL PRIMARY KEY,
	choice_id INTEGER REFERENCES choices,
	sent_at TIMESTAMP
);

CREATE TABLE votedpolls (
	id SERIAL PRIMARY KEY,
	poll_id INTEGER REFERENCES polls,
	username TEXT REFERENCES users
);
