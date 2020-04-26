
# Let's now tell docker to execute a command (bash) in the some-mysql container and make it interactive so that we can run commands inside the some-mysql container in another process (i.e. don't stop the mysql process within the docker container)
docker exec -it some-mysql bash

# Now we are inside the mysql container in a separate process. Let's run the mysql client app so that we can execute SQL queries
mysql -uroot -p

# Let's now display all of the databases inside the MySQL instance
show databases;

# Let's select the demo database we created on initialization
use demo;

# We are now in the database. We can now create tables and run query commands. To verify that we have no tables, let's view all of the tables;
show tables;

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

# need to run this to initialize the default folder.
INSERT INTO folders (title) VALUES ("root");
