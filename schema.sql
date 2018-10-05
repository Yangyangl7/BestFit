create table register (
	id SERIAL PRIMARY KEY,
	email varchar(100),
    name varchar(20),
    avator varchar(255),
    description varchar(255),
    phone varchar(30),
    isDesigner boolean NOT NULL
);

create table tag(
	tag_id SERIAL PRIMARY KEY,
	register_id int references user,
	name varchar(255),
	type varchar(100)
);

create table post(
	post_id SERIAL PRIMARY KEY,
	publisher_id int references user,
	content text,
	status int,
	dealer_id int references user,
	location varchar(255) NOT NULL,
	budget int,
	area text,
	tag_id int references tag
);

create table review(
	review_id SERIAL PRIMARY KEY,
	company_id references user,
	reviewer_id references user,
	rate int NOT NULL,
	comment text
);

create table picture(
	picture_id SERIAL PRIMARY KEY,
	register_id int references user,
	post_id int references post,
	url text
);

insert into register (name, isdesigner) values ('test1', TRUE);