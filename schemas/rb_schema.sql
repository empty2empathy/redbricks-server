create database redbricks;

create table artist
(
    artist_id     int primary key auto_increment,
    name          varchar(128),
    bio           text,
    profile_image varchar(128),
    instagram_id  varchar(128)
);

create table event
(
    event_id    int primary key auto_increment,
    title       varchar(512),
    price       int(11) default 0,
    youtube_id  varchar(64),
    description text,
    start_at    datetime,
    end_at      datetime,
    location_id int,
    constraint FK_event__location_location_id
        foreign key (location_id) references location (location_id)
            on update cascade on delete cascade
);

create table rel_artist_event
(
    relation_id int primary key auto_increment,
    artist_id   int,
    event_id    int,
    constraint FK_event__location_location_id
        foreign key (artist_id) references artist (artist_id)
            on update cascade on delete cascade,
    constraint FK_event__location_location_id
        foreign key (event_id) references event (event_id)
            on update cascade on delete cascade
);

create table location
(
    location_id  int primary key auto_increment,
    name         varchar(128),
    map_url      varchar(256),
    instagram_id varchar(128),
    description  text
);