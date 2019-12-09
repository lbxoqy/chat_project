show databases;
create database chatproject charset=utf8;
use chatproject;
-- 创建user_table 
create table user_table(
	pid int primary key auto_increment ,
    account_id varchar(16) not null,
    nickname  varchar(32) not null,
    password  varchar(32) not null,
    sex enum('m','w') default 'm',
    img varchar(128),
    offline_message bool default false,
    answer1 varchar(32),
    answer2 varchar(32),
    answer3 varchar(32),
    online_status bool default false,
    unique(account_id)
);
create unique index account_index on user_table(account_id);
insert into user_table(pid,account_id,nickname,password,sex) values(100000,'admin','管理员','admin','m');
insert into user_table(pid,account_id,nickname,password,sex) values(100001,'admin1','管理员','admin','m');
insert into user_table(pid,account_id,nickname,password,sex) values(100002,'admin2','管理员','admin','m');
insert into user_table(pid,account_id,nickname,password,sex) values(100003,'admin3','管理员','admin','m');
insert into user_table(pid,account_id,nickname,password,sex) values(100004,'admin4','管理员','admin','m');
insert into user_table(pid,account_id,nickname,password,sex) values(100005,'admin5','管理员','admin','m');
insert into user_table(account_id,nickname,password) values('admin6','管理员','admin');

select * from user_table;
update user_table set online_status=0 where account_id='admin4';

-- 创建好友表
create table user_friend_table (
	u_id int,
    f_id int,
    constraint u_f_fk foreign key(u_id) references user_table(pid) on delete cascade on update cascade,
    constraint f_u_fk foreign key(f_id) references user_table(pid) on delete cascade on update cascade,
    unique(u_id,f_id)
);
insert into user_friend_table values(100000,100001);
insert into user_friend_table values(100000,100002);
insert into user_friend_table values(100000,100003);
insert into user_friend_table values(100000,100004);
insert into user_friend_table values(100000,100005);
insert into user_friend_table values(100001,100000);

select * from user_friend_table;


-- 创建user_offline_message_table用户离线表
create table  user_offline_message_table(
	u_id int,
    message varchar(256),
    img blob,
    constraint u_m_fk foreign key(u_id) references user_table(pid) on delete cascade on update cascade
);
insert into user_offline_message_table(u_id,message) values(100001,"hello");
select * from user_offline_message_table;

-- 创建群聊表
create table group_table(
	group_id int primary key auto_increment,
    group_name varchar(16) not null
);

insert into group_table(group_id,group_name) values (200000,'我的群聊');
select * from group_table;

-- 创建群聊和用户表
create table group_user(
	group_id int,
    u_id int,
    constraint u_g_fk foreign key(u_id) references user_table(pid) on delete cascade on update cascade,
    constraint g_g_fk foreign key(group_id) references group_table(group_id) on delete cascade on update cascade,
    unique(group_id,u_id)
);

insert into group_user values(200000,100000);
select * from group_user;
