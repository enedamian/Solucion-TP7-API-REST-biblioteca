from flask import Flask
# cargo las funciones para incializar los modelos
from modelos.libros import inicializar_libros
from modelos.socios import inicializar_socios
from modelos.prestamos import inicializar_prestamos

# cargo los blueprints
from controladores.rutas_libros import libros_bp
from controladores.rutas_socios import socios_bp
from controladores.rutas_prestamos import prestamos_bp

app = Flask(__name__)

# Inicializo los modelos
inicializar_libros()
inicializar_socios()
inicializar_prestamos()

# Registro los blueprints en la aplicación
app.register_blueprint(libros_bp)
app.register_blueprint(socios_bp)
app.register_blueprint(prestamos_bp)

if __name__ == '__main__':
    app.run(debug=True)