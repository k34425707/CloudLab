/*
登入sql 後 run  
source /Users/1subtraction/Downloads/sql/sqlScript/setup.sql
*/
DROP DATABASE lab;
CREATE DATABASE lab;
USE lab;
/*
建立一個  table user 
Id:學號

Name:名字
uPassword:預設a加學號
Privilege:權限
我設想
0是普通學生
1是助教
*/
CREATE TABLE user
(
    uId VARCHAR(11) NOT NULL,
    uPassword VARCHAR(20),
    uName VARCHAR(5),
    uPrivilege INT(1),
    PRIMARY KEY (uId)
                    
);
