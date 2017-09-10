CREATE DATABASE myblog character set UTF8mb4 collate utf8mb4_bin; 
CREATE USER 'myblogx'@'%' IDENTIFIED BY '@PASSWORD@';
GRANT UPDATE,SELECT,DELETE,INSERT ON myblog.* TO 'myblogx'@'%';