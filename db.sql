/* MySQL 数据库 */
/* 创建用户 'py'，host 为 'localhost'，密码为 'py_passwd'，该用户对数据库 shorturl 下所有表拥有所有权限 */
grant all on shorturl.* to 'root'@'localhost' identified by 'root';

create database shorturl DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

use shorturl;

create table short_url (
  id int auto_increment primary key,
	long_url varchar(512) null,
	short_url varchar(50) null,
	url_type CHAR(1) null,
	create_time timestamp default CURRENT_TIMESTAMP null
)engine=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;



# ALTER SCHEMA `shorturl`  DEFAULT CHARACTER SET utf8  DEFAULT COLLATE utf8_bin ;