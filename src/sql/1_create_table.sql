/*
此表用来记录用户信息，用户可以修改联系电话、用户简介和登录密码
*/
CREATE TABLE IF NOT EXISTS myuser (
	"id" SERIAL PRIMARY KEY,
	"username" VARCHAR(32) NOT NULL,
	"password" VARCHAR(64) NOT NULL,
	"is_admin" BOOL NOT NULL DEFAULT FALSE,
	"name" VARCHAR(32) NOT NULL,
	"id_type" VARCHAR(16) NOT NULL,
	"id_number" VARCHAR(32) NOT NULL,
	"phone_number" CHAR(11) NOT NULL,
	"is_vip" BOOL NOT NULL DEFAULT FALSE,
	"description" VARCHAR(255),
	"city" VARCHAR(32) NOT NULL, 
	"reg_time" timestamp NOT NULL,
	"mod_time" timestamp NOT NULL
);


/*
此表用来记录“寻味道”请求信息
*/
CREATE TABLE IF NOT EXISTS search (
	"id" SERIAL PRIMARY KEY,
	"user_id" INT references myuser("id"),
	"flavor_type" VARCHAR(32) NOT NULL,
	"req_name" VARCHAR(32) NOT NULL,
	"req_description" VARCHAR(255),
	"price" NUMERIC NOT NULL,
	"end_time" date NOT NULL,
	"photo" BYTEA,
	"crea_time" timestamp NOT NULL,
	"mod_time" timestamp NOT NULL,
	"state" SMALLINT NOT NULL
);

/*
此表用来记录“请品鉴”响应信息
*/
CREATE TABLE IF NOT EXISTS taste (
	"id" SERIAL PRIMARY KEY,
	"req_id" INT references search("id"),
	"user_id" INT references myuser("id"),
	"description" VARCHAR(255),
	"crea_time" timestamp NOT NULL,
	"mod_time" timestamp NOT NULL,
	"state" SMALLINT NOT NULL
);

/*
“寻味道”成功明细表
*/
CREATE TABLE IF NOT EXISTS success (
	"req_id" INT references search("id"),
	"user1_id" INT references myuser("id"),
	"user2_id" INT references myuser("id"),
	"finish_time" date NOT NULL,
	"fee1" NUMERIC NOT NULL,
	"fee2" NUMERIC NOT NULL
);

/*
中介收益汇总表
*/
CREATE TABLE IF NOT EXISTS income (
	"month" CHAR(6) NOT NULL, --对应于成功明细表中的达成日期
	"city" VARCHAR(32) NOT NULL, --对应于用户表中的注册城市
	"type" VARCHAR(32) NOT NULL, --对应于用户表中的请求类型
	"number" INT NOT NULL, 
	"money" NUMERIC NOT NULL
);