from flask import Flask, render_template
from flask_session import Session

from config import Config

def bad_request(e):
    return render_template('error/400.html', e=e), 400

def page_not_found(e):
    return render_template('error/404.html', e=e), 404

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    server_session = Session(app)

    # Register Pages for 400 and 404 Errors
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)

    # Main blueprint
    from src.main import bp as main_bp
    app.register_blueprint(main_bp)

    # API blueprint
    from src.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/')

    # Search blueprint
    from src.search import bp as search_bp
    app.register_blueprint(search_bp, url_prefix='/search')

    # Game blueprint
    from src.game import bp as game_bp
    app.register_blueprint(game_bp, url_prefix='/game/')

    # Wishlist blueprint
    from src.wishlist import bp as wishlist_bp
    app.register_blueprint(wishlist_bp, url_prefix='/wishlist')

    # Verify blueprint
    from src.verify import bp as verify_bp
    app.register_blueprint(verify_bp, url_prefix='/verify')

    # User blueprint
    from src.user import account_bp as account_bp
    from src.user import signup_bp as signup_bp
    from src.user import signin_bp as signin_bp
    from src.user import support_bp as support_bp

    app.register_blueprint(signup_bp, url_prefix='/signup')
    app.register_blueprint(signin_bp, url_prefix='/signin')
    app.register_blueprint(account_bp, url_prefix='/account')
    app.register_blueprint(support_bp, url_prefix='/support')

    return app