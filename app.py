from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barrio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), nullable=False)
    forma_entrada = db.Column(db.String(50), nullable=False)
    patente = db.Column(db.String(10), nullable=True)
    ingresante = db.Column(db.String(50), nullable=False)
    propiedad_de = db.Column(db.String(100), nullable=True)
    fecha_hora_ingreso = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_hora_salida = db.Column(db.DateTime, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    password = request.form['password']
    if password == 'GuardiaLaDelia':
        session['logged_in'] = True
        return redirect(url_for('mostrar_ingresos'))
    else:
        flash('Contraseña incorrecta')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/ingresos', methods=['GET'])
def mostrar_ingresos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('ingresos.html')

@app.route('/ingresos', methods=['POST'])
def procesar_ingresos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    nombre_apellido = request.form['nombre_apellido']
    dni = request.form['dni']
    forma_entrada = request.form['forma_entrada']
    patente = request.form['patente'] if forma_entrada == 'Vehículo' else None
    ingresante = request.form['ingresante']
    propiedad_de = request.form['propiedad_de'] if ingresante in ['Visita', 'Servicio'] else None

    # Definir la zona horaria de Argentina
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    
    # Obtener la hora actual en UTC
    now_utc = datetime.now(pytz.utc)
    
    # Convertir la hora actual a la zona horaria de Argentina
    now_argentina = now_utc.astimezone(argentina_tz)

    nuevo_usuario = Usuario(
        nombre_apellido=nombre_apellido,
        dni=dni,
        forma_entrada=forma_entrada,
        patente=patente,
        ingresante=ingresante,
        propiedad_de=propiedad_de,
        fecha_hora_ingreso=now_argentina  # Usar la hora de Argentina
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    flash('Ingreso registrado con éxito')
    return redirect(url_for('mostrar_ingresos'))

@app.route('/salidas', methods=['GET'])
def mostrar_salidas():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('salidas.html')

@app.route('/salidas', methods=['POST'])
def procesar_salidas():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    tipo_salida = request.form['tipo_salida']
    
    # Definir la zona horaria de Argentina
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    
    # Obtener la hora actual en UTC
    now_utc = datetime.now(pytz.utc)
    
    # Convertir la hora actual a la zona horaria de Argentina
    now_argentina = now_utc.astimezone(argentina_tz)

    if tipo_salida == 'dni':
        dni = request.form['dni']
        usuario = Usuario.query.filter_by(dni=dni).order_by(Usuario.fecha_hora_ingreso.desc()).first()
        
        if usuario:
            usuario.fecha_hora_salida = now_argentina  # Usar la hora de Argentina
            db.session.commit()
            flash('Salida registrada con éxito')
        else:
            flash('Usuario no encontrado')
    elif tipo_salida == 'patente':
        patente = request.form['patente']
        usuarios = Usuario.query.filter_by(patente=patente, fecha_hora_salida=None).all()

        if usuarios:
            for usuario in usuarios:
                usuario.fecha_hora_salida = now_argentina  # Usar la hora de Argentina
            db.session.commit()
            flash('Salida registrada con éxito')
        else:
            flash('No se encontraron usuarios con esa patente o ya registraron salida')

    return redirect(url_for('mostrar_salidas'))

@app.route('/consultas', methods=['GET'])
def mostrar_consultas():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('consultas.html')

def obtener_ultimo_ingreso(dni_patente):
    usuario = Usuario.query.filter(
        (Usuario.dni == dni_patente) | (Usuario.patente == dni_patente)
    ).order_by(Usuario.fecha_hora_ingreso.desc()).first()
    return usuario

def obtener_ultimo_salida(dni_patente):
    usuario = Usuario.query.filter(
        (Usuario.dni == dni_patente) | (Usuario.patente == dni_patente)
    ).order_by(Usuario.fecha_hora_salida.desc()).first()
    return usuario

def obtener_ingresos_casa(propiedad, fecha):
    start_of_day = datetime.combine(fecha, datetime.min.time())
    end_of_day = datetime.combine(fecha, datetime.max.time())

    usuarios = Usuario.query.filter(
        Usuario.propiedad_de == propiedad,
        Usuario.fecha_hora_ingreso >= start_of_day,
        Usuario.fecha_hora_ingreso <= end_of_day
    ).all()
    
    return usuarios

@app.route('/consultas', methods=['POST'])
def procesar_consultas():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    resultado = None

    if request.method == 'POST':
        consulta = request.form['consulta']
        dni_patente = request.form.get('dni_patente', None)
        propiedad = request.form.get('propiedad', None)
        fecha_str = request.form.get('fecha', None)

        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        
        if consulta == 'ultimo_ingreso':
            usuario = obtener_ultimo_ingreso(dni_patente)
            if usuario:
                fecha_ingreso = usuario.fecha_hora_ingreso.astimezone(argentina_tz).strftime('%Y-%m-%d %H:%M:%S')
                resultado = f"Último ingreso de {usuario.nombre_apellido} con DNI {usuario.dni} fue el {fecha_ingreso}"
            else:
                resultado = "No se encontró el ingreso"

        elif consulta == 'ultimo_salida':
            usuario = obtener_ultimo_salida(dni_patente)
            if usuario:
                fecha_salida = usuario.fecha_hora_salida.astimezone(argentina_tz).strftime('%Y-%m-%d %H:%M:%S') if usuario.fecha_hora_salida else "No registrada"
                resultado = f"Última salida de {usuario.nombre_apellido} con DNI {usuario.dni} fue el {fecha_salida}"
            else:
                resultado = "No se encontró la salida"

        elif consulta == 'ingresos_casa' and propiedad and fecha_str:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            usuarios = obtener_ingresos_casa(propiedad, fecha)
            if usuarios:
                resultado = f"Ingresos a la casa de {propiedad} desde {fecha_str}:\n" + "\n".join(
                    [f"{usuario.nombre_apellido} (DNI: {usuario.dni}) ingresó el {usuario.fecha_hora_ingreso.astimezone(argentina_tz).strftime('%Y-%m-%d %H:%M:%S')}" for usuario in usuarios]
                )
            else:
                resultado = "No se encontraron ingresos para esa propiedad y fecha"

    return render_template('consultas.html', resultado=resultado)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('term')
    usuarios = Usuario.query.filter(Usuario.nombre_apellido.ilike(f'%{search}%')).all()
    suggestions = [{'label': usuario.nombre_apellido, 'dni': usuario.dni, 'forma_entrada': usuario.forma_entrada, 'patente': usuario.patente, 'ingresante': usuario.ingresante, 'propiedad_de': usuario.propiedad_de} for usuario in usuarios]
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
