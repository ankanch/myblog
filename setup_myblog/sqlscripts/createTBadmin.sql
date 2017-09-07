USE myblog;
CREATE TABLE admin(
        ID int(11) not null primary ,
        USERNAME  tinytext not null,
        PASSWORD  text not null,
        LOCKED  tinyint(1) not null,
        SESSIONS text not null
)