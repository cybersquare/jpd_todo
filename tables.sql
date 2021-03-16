CREATE TABLE users(
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    name VARCHAR(100),
    gender VARCHAR(100),
    phone VARCHAR(10),
    dob DATE
);


CREATE TABLE todos(
    todo_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    content VARCHAR(200),
    user_id INT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);