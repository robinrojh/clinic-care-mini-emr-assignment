CREATE TABLE users (
    user_id INT PRIMARY KEY,
    last_name VARCHAR(255),
    first_name VARCHAR(255)
)

CREATE TABLE notes (
    note_id INT PRIMARY KEY,
    user_id INT,
    title VARCHAR(255),
    content TEXT

    FOREIGN KEY (user_id) REFERENCES users(user_id)
)

CREATE TABLE codes (
    chapter_code CHAR(1),
    category_code INT,
    subcategory_code INT DEFAULT -1,
    has_dagger BOOLEAN DEFAULT FALSE,
    has_asterisk BOOLEAN DEFAULT FALSE,
    description TEXT,

    PRIMARY KEY (chapter_code, category_code, subcategory_code, has_dagger, has_asterisk)
)

CREATE TABLE notes_codes (
    note_id INT PRIMARY KEY,
    chapter_code CHAR(1),
    category_code INT,
    subcategory_code INT DEFAULT -1,
    has_dagger BOOLEAN DEFAULT FALSE,
    has_asterisk BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (note_id, chapter_code, category_code, subcategory_code, has_dagger, has_asterisk)
    FOREIGN KEY (note_id) REFERENCES notes(note_id)
    FOREIGN KEY (chapter_code, category_code, subcategory_code, has_dagger, has_asterisk) REFERENCES codes(chapter_code, category_code, subcategory_code, has_dagger, has_asterisk)
)