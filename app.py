from flask import Flask
from modelos.libros import inicializar_libros

from controladores.rutas_libros import libros_bp

app = Flask(__name__)

inicializar_libros()

# Register blueprint
app.register_blueprint(libros_bp)