from flask import Flask, render_template

from config import Config

def bad_request(e):
    return render_template('error/400.html', e=e), 400

def page_not_found(e):
    return render_template('error/404.html', e=e), 404

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register Pages for 400 and 404 Errors
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)

    # Hain blueprint
    from src.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Search blueprint
    from src.search import bp as search_bp
    app.register_blueprint(search_bp, url_prefix='/search')

    # Game blueprint
    from src.game import bp as game_bp
    app.register_blueprint(game_bp, url_prefix='/game/')

    # User blueprint
    from src.user import user_bp as user_bp
    from src.user import signup_bp as signup_bp
    from src.user import signin_bp as signin_bp

    app.register_blueprint(signup_bp, url_prefix='/signup/')
    app.register_blueprint(signin_bp, url_prefix='/signin/')
    app.register_blueprint(user_bp, url_prefix='/user/')
    

    return app