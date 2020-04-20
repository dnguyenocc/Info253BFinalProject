CREATE TABLE documents (
    id int NOT NULL AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    content VARCHAR(2000),
    PRIMARY KEY (id)
);


CREATE TABLE folders (
    id int NOT NULL AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE contains (
    id int NOT NULL AUTO_INCREMENT,
    document_id int,
    folder_id int, 
    FOREIGN KEY (document_id) REFERENCES documents(id),
    FOREIGN KEY (folder_id) REFERENCES folders(id),
    PRIMARY KEY (id)
);


