USE myblog;
CREATE TABLE articles(
        AID  int(10) unsigned not null primary auto_increment,
        ATITLE  text not null,
        ACONTENT  mediumtext not null,
        ACATEGORY  text not null,
        AKEYWORDS  text not null,
        AURL  tinytext not null,
        AREADINGS  int(10) unsigned not null,
        DATE  tinytext not null,
        DRAFT  tinyint(1),
        TRASH tinyint(1)
    )