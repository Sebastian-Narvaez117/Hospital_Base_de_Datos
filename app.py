from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializamos SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    # Configuración de la base de datos para conectar con Hospital
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sliferyra@localhost/Hospital'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evitar advertencias
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'una_clave_secreta_muy_segura'

    # Inicializar la base de datos con la app
    db.init_app(app)

    with app.app_context():
        # Importar rutas y registrar blueprints
        from routes.route import router
        from routes.route2 import router2
        app.register_blueprint(router)
        app.register_blueprint(router2)

        # Crear las tablas si no existen
        #db.create_all()

    return app
