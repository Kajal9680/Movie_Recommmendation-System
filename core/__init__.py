from flask import Flask
from config import Config
from core.database.db_config import init_db
from core.utils.data_loader import load_data, preprocess
from core.machine_learning.content_model import build_content_model
import core.machine_learning.model_state as state

def create_app():
    app = Flask(__name__, 
                template_folder='frontend/templates', 
                static_folder='frontend/static')
    app.config.from_object(Config)
    
    # Initialize Database
    init_db()
    
    # Load and Preprocess Data
    state.movies_df = preprocess(load_data())
    state.nn_model, state.tfidf_matrix = build_content_model(state.movies_df)
    
    # Register Blueprints
    from core.backend.auth_routes import auth_bp
    from core.backend.movie_routes import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    return app
