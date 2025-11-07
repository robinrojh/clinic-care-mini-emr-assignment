CREATE TABLE users (
    email VARCHAR(255) PRIMARY KEY,
    last_name VARCHAR(255),
    first_name VARCHAR(255),
    hashed_pw VARCHAR(1000)
);

CREATE TABLE notes (
    note_id BIGINT PRIMARY KEY,
    email VARCHAR(255),
    title VARCHAR(255),
    content TEXT,

    created_at timestamp default current_timestamp

    FOREIGN KEY (email) REFERENCES users(email)
);

CREATE TABLE codes (
    chapter_code CHAR(1),
    category_code CHAR(2),
    subcategory_code CHAR(1) DEFAULT '-', -- '-' for subcategory code represents no subcategory.
    title TEXT,
    description TEXT,

    PRIMARY KEY (chapter_code, category_code, subcategory_code)
);

CREATE TABLE notes_codes (
    note_id INT,
    chapter_code CHAR(1),
    category_code CHAR(2),
    subcategory_code CHAR(1) DEFAULT '-', -- '-' for subcategory code represents no subcategory.

    PRIMARY KEY (note_id, chapter_code, category_code, subcategory_code),
    FOREIGN KEY (note_id) REFERENCES notes(note_id),
    FOREIGN KEY (chapter_code, category_code, subcategory_code) REFERENCES codes(chapter_code, category_code, subcategory_code)
);