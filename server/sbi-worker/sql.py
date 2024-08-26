insert_game = ("""
    INSERT INTO game (app_id, name) VALUES (%(app_id)s, %(name)s)
    ON DUPLICATE KEY UPDATE name=%(name)s
""")

insert_gameinuse = ("""
    INSERT INTO gameinuse (playtime_forever_minutes, playtime_2weeks_minutes, user_fk, game_fk) VALUES (%(playtime_forever_minutes)s, %(playtime_2weeks_minutes)s, (SELECT user_pk FROM user WHERE steam_id=%(steam_id)s), (SELECT game_pk FROM game WHERE app_id=%(app_id)s))
    ON DUPLICATE KEY UPDATE playtime_forever_minutes=%(playtime_forever_minutes)s, playtime_2weeks_minutes=%(playtime_2weeks_minutes)s
""")

insert_user = ("""
    INSERT INTO user (steam_id, display_name) VALUES (%(steam_id)s, %(display_name)s)
    ON DUPLICATE KEY UPDATE display_name=%(display_name)s
""")

query_game = "SELECT app_id from game"