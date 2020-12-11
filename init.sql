create table professors(
    username varchar(50) PRIMARY KEY NOT NULL,
    password varchar(50) NOT NULL
);
create table students(
    surname varchar(50) PRIMARY KEY NOT NULL
);
create table courses(
    title varchar(50) PRIMARY KEY NOT NULL,
    username varchar(50),
    FOREIGN KEY (username) REFERENCES professors(username)
);
create table requests(
    surname varchar(50) NOT NULL,
    title varchar(50) NOT NULL,
    FOREIGN KEY (surname) REFERENCES students(surname),
    FOREIGN KEY (title) REFERENCES courses(title),
    UNIQUE (surname, title)
);
create table courses_and_students(
    surname varchar(50) NOT NULL,
    title varchar(50) NOT NULL,
    FOREIGN KEY (surname) REFERENCES students(surname),
    FOREIGN KEY (title) REFERENCES courses(title),
    UNIQUE (surname, title)
);
