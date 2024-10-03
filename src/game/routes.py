import pickle
import time

import redis

from flask import render_template, redirect, url_for
from src.game import bp

from src.utils.GameDetails import GameDetails

@bp.route('/<steam_app_id>')
def game(steam_app_id):
    # Redirect user to home page if steam_app_id is invalid
    if not steam_app_id.isdigit():
        return redirect(url_for('main.index'))

    start = time.perf_counter()
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    if (game_cache := redis_conn.get(steam_app_id)) is not None:
        print("Using game cache...")
        game_details = pickle.loads(game_cache)
        end = time.perf_counter()
        print(f"Total Time: {end - start:0.4f} seconds")
    else:
        game_details = GameDetails(steam_app_id)

        # Store game_details in cache
        game_cache = pickle.dumps(game_details)
        redis_conn.set(steam_app_id, game_cache)
        HOUR_SECONDS = 3600
        redis_conn.expire(steam_app_id, HOUR_SECONDS)
    return render_template('game/game_page.html', game=game_details)
