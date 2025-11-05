CREATE TABLE users (
    user_id INT PRIMARY KEY,
    last_name VARCHAR(255),
    first_name VARCHAR(255)
);

CREATE TABLE notes (
    note_id INT PRIMARY KEY,
    user_id INT,
    title VARCHAR(255),
    content TEXT,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
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