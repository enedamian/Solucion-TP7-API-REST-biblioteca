from flask import Flask
from modelos.libros import inicializar_libros
from modelos.socios import inicializar_socios
from modelos.prestamos import inicializar_prestamos

from controladores.rutas_libros import libros_bp
from controladores.rutas_socios import socios_bp
from controladores.rutas_prestamos import prestamos_bp

app = Flask(__name__)

inicializar_libros()
inicializar_socios()
inicializar_prestamos()

# Register blueprint
app.register_blueprint(libros_bp)
app.register_blueprint(socios_bp)
app.register_blueprint(prestamos_bp)