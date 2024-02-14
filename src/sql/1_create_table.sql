/*
�˱�������¼�û���Ϣ���û������޸���ϵ�绰���û����͵�¼����
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
�˱�������¼��Ѱζ����������Ϣ
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
�˱�������¼����Ʒ������Ӧ��Ϣ
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
��Ѱζ�����ɹ���ϸ��
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
�н�������ܱ�
*/
CREATE TABLE IF NOT EXISTS income (
	"month" CHAR(6) NOT NULL, --��Ӧ�ڳɹ���ϸ���еĴ������
	"city" VARCHAR(32) NOT NULL, --��Ӧ���û����е�ע�����
	"type" VARCHAR(32) NOT NULL, --��Ӧ���û����е���������
	"number" INT NOT NULL, 
	"money" NUMERIC NOT NULL
);