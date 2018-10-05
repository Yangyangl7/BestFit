CREATE TABLE user(
	user_id SERIAL PRIMARY KEY,
	email varchar(100),
    name varchar(20),
    avator varchar(255),
    description varchar(255),
    phone varchar(30),
    isDesigner boolean NOT NULL
);

CREATE TABLE tag(
	tag_id SERIAL PRIMARY KEY,
	user_id int references user,
	name varchar(255),
	type varchar(100)
);

CREATE TABLE post(
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

CREATE TABLE review(
	review_id SERIAL PRIMARY KEY,
	company_id references user,
	reviewer_id references user,
	rate int NOT NULL,
	comment text
);

CREATE TABLE picture(
	picture_id SERIAL PRIMARY KEY,
	post_id int references post,
	url text
);