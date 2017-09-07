USE myblog;
CREATE TABLE categories(
        CID  int(11) not null primary auto_increment,
        CNAME  text not null,
        CACOUNT  int(10) unsigned not null,
        CURL tinytext not null
)