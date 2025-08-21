<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS quiz_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    selected VARCHAR(255) NOT NULL,
    correct VARCHAR(255) NOT NULL,
    score INT NOT NULL
);

CREATE TABLE IF NOT EXISTS quiz_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    total INT NOT NULL,
    status VARCHAR(10) NOT NULL
);
=======
CREATE TABLE IF NOT EXISTS quiz_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    selected VARCHAR(255) NOT NULL,
    correct VARCHAR(255) NOT NULL,
    score INT NOT NULL
);

CREATE TABLE IF NOT EXISTS quiz_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    total INT NOT NULL,
    status VARCHAR(10) NOT NULL
);
>>>>>>> d295fd8 (quiz app initial commit)
