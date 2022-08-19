create database if not exists steam_bi;
use steam_bi;

create table if not exists user(
	user_pk int not null auto_increment,
	steam_id char(17) unique not null,
	display_name varchar(255),
	created_at timestamp default current_timestamp,
	primary key (user_pk)
);

create table if not exists game(
	game_pk int not null auto_increment,
	app_id int unique not null,
	name varchar(255) not null,
	created_at timestamp default current_timestamp,
	primary key (game_pk)
);

create table if not exists gameinuse(
	gameinuse_pk int not null auto_increment,
    user_fk int not null,
    game_fk int not null,
    playtime_forever_minutes int,
    playtime_2weeks_minutes int,
    created_at timestamp default current_timestamp,
    unique(user_fk, game_fK),
	primary	key (gameinuse_pk),
    foreign key (user_fk) references user(user_pk),
    foreign key(game_fk) references game(game_pk)
);

CREATE VIEW `view_gameinuse_v1` AS
SELECT gameinuse.gameinuse_pk
	  ,gameinuse.user_fk
	  ,user.display_name user
      ,gameinuse.game_fk
	  ,game.name AS game
      ,gameinuse.playtime_forever_minutes
      ,gameinuse.playtime_forever_minutes / 60 AS playtime_forever_hours
      ,gameinuse.playtime_forever_minutes / 60 / 24 AS playtime_forever_days
	  ,gameinuse.playtime_2weeks_minutes
      ,gameinuse.playtime_2weeks_minutes / 60 AS playtime_2weeks_hours
      ,gameinuse.playtime_2weeks_minutes / 60 / 24 AS playtime_2weeks_days
FROM gameinuse
JOIN user
	ON user.user_pk = gameinuse.user_fk
JOIN game
	ON game.game_pk = gameinuse.game_fk
;