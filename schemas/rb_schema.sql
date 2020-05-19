create table artist
(
    artist_id     int auto_increment primary key,
    name          varchar(128) null,
    bio           text         null,
    profile_image varchar(128) null,
    instagram_id  varchar(128) null
);

create table location
(
    location_id  int auto_increment
        primary key,
    name         varchar(128) null,
    map_url      varchar(256) null,
    instagram_id varchar(128) null,
    description  text         null
);

create table event
(
    event_id    int auto_increment primary key,
    title       varchar(512)                null,
    price       int default 0               null,
    pay_type    enum ('ticket', 'entrance') null,
    youtube_id  varchar(64)                 null,
    description text                        null,
    start_at    datetime                    null,
    end_at      datetime                    null,
    location_id int                         null,
    constraint FK_event__location_location_id
        foreign key (location_id) references location (location_id)
            on update cascade on delete cascade
);

create table program_types
(
    type_id int auto_increment primary key,
    name    varchar(32)          not null,
    disable tinyint(1) default 0 not null,
    constraint UNQ_program_types_name
        unique (name)
);

create table rel_artist_event
(
    relation_id int auto_increment primary key,
    artist_id   int null,
    event_id    int null,
    constraint FK_artist_id__location_location_id
        foreign key (artist_id) references artist (artist_id)
            on update cascade on delete cascade,
    constraint FK_event_id__event_location_id
        foreign key (event_id) references event (event_id)
            on update cascade on delete cascade
);

create table rel_artist_program_type
(
    relation_id int auto_increment primary key,
    type_id     int not null,
    artist_id   int not null,
    constraint FK_rel_artist_program_type_artist_id__artist_artist_id
        foreign key (artist_id) references artist (artist_id)
            on update cascade on delete cascade,
    constraint FK_rel_artist_program_type_type_id__program_type_type_id
        foreign key (type_id) references program_types (type_id)
            on update cascade on delete cascade
);
