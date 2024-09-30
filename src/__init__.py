from flask import Flask

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Hain blueprint
    from src.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Search blueprint
    from src.search import bp as search_bp
    app.register_blueprint(search_bp, url_prefix='/search')

    # Game blueprint
    from src.game import bp as game_bp
    app.register_blueprint(game_bp, url_prefix='/game/')

    return app