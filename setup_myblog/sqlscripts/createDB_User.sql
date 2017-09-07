CREATE DATABASE myblog; 
CREATE USER 'myblog'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON myblog TO 'myblog'@'localhost';