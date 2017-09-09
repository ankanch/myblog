USE myblog;
CREATE TABLE admin(
    ID int(11) primary key not null auto_increment ,
    USERNAME  text not null,
    PASSWORD  text not null,
    LOCKED  tinyint(1) not null,
    SESSIONS text not null
)