CREATE DATABASE myblog; 
CREATE USER 'myblog'@'localhost' IDENTIFIED BY '@PASSWORD@';
GRANT ALL PRIVILEGES ON myblog TO 'myblog'@'localhost';