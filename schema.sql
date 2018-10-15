drop table IF EXISTS register CASCADE;
drop table IF EXISTS tag CASCADE;
drop table IF EXISTS post CASCADE;
drop table IF EXISTS picture CASCADE;
drop table IF EXISTS review CASCADE;

create table register (
	id SERIAL PRIMARY KEY,
	email varchar(100),
    name varchar(20),
	user_id varchar(255),
    avator varchar(255) DEFAULT 'https://vignette.wikia.nocookie.net/pkmnshuffle/images/3/32/Psyduck.png/revision/latest?cb=20170407192426',
    description varchar(255),
    phone varchar(30),
    isDesigner boolean NOT NULL
);

create table tag(
	tag_id SERIAL PRIMARY KEY,
	register_id int references register,
	name varchar(255),
	type varchar(100)
);

create table post(
	post_id SERIAL PRIMARY KEY,
	publisher_id int references register,
	title varchar(255) NOT NULL,
	time varchar(255),
	content text,
	status int,
	dealer_id int references register,
	location varchar(255) NOT NULL,
	budget int,
	area text,
	tag_id int references tag,
);

create table review(
	review_id SERIAL PRIMARY KEY,
	company_id int references register,
	reviewer_id int references register,
	rate int NOT NULL,
	comment text
);

create table picture(
	picture_id SERIAL PRIMARY KEY,
	register_id int references register,
	post_id int references post,
	url text
);

insert into register (name, isdesigner) values ('test1', TRUE);
