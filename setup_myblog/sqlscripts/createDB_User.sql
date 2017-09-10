CREATE DATABASE myblog; 
CREATE USER 'myblogx'@'localhost' IDENTIFIED BY '@PASSWORD@';
GRANT UPDATE,SELECT,DELETE,INSERT ON myblog.* TO 'myblogx'@'localhost';