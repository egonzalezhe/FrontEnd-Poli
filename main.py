# ARCHIVO: server.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'techflow_secret_key_2024'

# Configuración de la base de datos
def init_db():
    """Inicializa la base de datos con las tablas necesarias"""
    conn = sqlite3.connect('techflow.db')
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de servicios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio DECIMAL(10,2) NOT NULL,
            stock INTEGER DEFAULT 0,
            promocion BOOLEAN DEFAULT 0,
            icono TEXT DEFAULT '🔧',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertar usuario admin por defecto
    try:
        password_hash = hashlib.md5('admin123'.encode()).hexdigest()
        cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', 
                      ('admin', password_hash))
    except:
        pass  # Usuario ya existe
    
    # Insertar servicios de ejemplo
    servicios_ejemplo = [
        ('Desarrollo Web', 'Sitios web modernos y responsivos con las últimas tecnologías', 2500000, 15, 1, '💻'),
        ('Apps Móviles', 'Aplicaciones nativas para iOS y Android', 4500000, 8, 0, '📱'),
        ('Cloud Computing', 'Migración y gestión de servicios en la nube', 3200000, 12, 1, '☁️'),
        ('Ciberseguridad', 'Auditorías de seguridad y protección de datos', 2800000, 6, 0, '🔐'),
        ('Inteligencia Artificial', 'Soluciones de IA y Machine Learning personalizadas', 6500000, 4, 1, '🤖'),
        ('UI/UX Design', 'Diseño de interfaces centradas en el usuario', 1800000, 20, 0, '🎨'),
        ('Business Intelligence', 'Análisis de datos y reportes empresariales', 3800000, 10, 0, '📊'),
        ('Mantenimiento IT', 'Soporte técnico especializado 24/7', 1200000, 25, 0, '🔧'),
        ('E-commerce', 'Tiendas online completas y optimizadas', 3500000, 7, 1, '🌐'),
        ('Consultoría Digital', 'Estrategias de transformación digital', 2200000, 18, 0, '📈')
    ]
    
    for servicio in servicios_ejemplo:
        try:
            cursor.execute('''INSERT INTO servicios 
                             (nombre, descripcion, precio, stock, promocion, icono) 
                             VALUES (?, ?, ?, ?, ?, ?)''', servicio)
        except:
            pass  # Servicio ya existe
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Obtiene conexión a la base de datos"""
    conn = sqlite3.connect('techflow.db')
    conn.row_factory = sqlite3.Row
    return conn

# RUTAS PRINCIPALES (MOCKUPS)

@app.route('/')
def home():
    """MOCKUP 1: Página principal/home"""
    return '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechFlow Solutions - Home</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .header { background: rgba(255,255,255,0.95); padding: 1rem 2rem; position: fixed; width: 100%; top: 0; z-index: 1000; }
        .navbar { display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; }
        .logo { font-size: 1.8rem; font-weight: bold; color: #667eea; }
        .nav-links { display: flex; gap: 2rem; list-style: none; }
        .nav-links a { text-decoration: none; color: #333; font-weight: 500; }
        .nav-links a:hover { color: #667eea; }
        .hero { text-align: center; padding: 8rem 2rem 4rem; color: white; }
        .hero h1 { font-size: 3.5rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .hero p { font-size: 1.3rem; max-width: 600px; margin: 0 auto; }
        .slider { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; margin: 2rem auto; max-width: 800px; padding: 2rem; text-align: center; color: white; }
        .company-info { background: rgba(255,255,255,0.95); margin: 3rem 2rem; padding: 3rem; border-radius: 15px; text-align: center; }
        .stats { display: flex; justify-content: center; gap: 3rem; margin-top: 2rem; }
        .stat h3 { font-size: 2rem; color: #667eea; }
        .footer { background: rgba(0,0,0,0.8); color: white; padding: 2rem; text-align: center; margin-top: 3rem; }
    </style>
</head>
<body>
    <header class="header">
        <nav class="navbar">
            <div class="logo">TechFlow Solutions</div>
            <ul class="nav-links">
                <li><a href="/">Inicio</a></li>
                <li><a href="/servicios">Servicios</a></li>
                <li><a href="/login">Admin</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="hero">
            <h1>TechFlow Solutions</h1>
            <p>Transformamos ideas en soluciones tecnológicas innovadoras que impulsan el crecimiento de tu negocio</p>
        </section>

        <section class="slider">
            <h3>🚀 Innovación Tecnológica</h3>
            <p>Desarrollamos software personalizado con las últimas tecnologías</p>
        </section>

        <section class="company-info">
            <h2>¿Quiénes Somos?</h2>
            <p>Somos una empresa líder en servicios tecnológicos con más de 10 años de experiencia. 
            Nos especializamos en desarrollo de software, consultoría IT y soluciones digitales.</p>
            
            <div class="stats">
                <div class="stat"><h3>500+</h3><p>Proyectos</p></div>
                <div class="stat"><h3>50+</h3><p>Clientes</p></div>
                <div class="stat"><h3>24/7</h3><p>Soporte</p></div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <p>&copy; 2024 TechFlow Solutions. Todos los derechos reservados.</p>
        <p>📧 info@techflowsolutions.com | 📱 +57 300 123 4567</p>
    </footer>
</body>
</html>
    '''

@app.route('/servicios')
def servicios():
    """MOCKUP 2: Lista de servicios"""
    conn = get_db_connection()
    servicios = conn.execute('SELECT * FROM servicios ORDER BY id').fetchall()
    conn.close()
    
    servicios_html = ''
    for servicio in servicios:
        servicios_html += f'''
        <div class="service-card" onclick="location.href='/detalle/{servicio['id']}'">
            <div class="service-icon">{servicio['icono']}</div>
            <h3>{servicio['nombre']}</h3>
            <p>{servicio['descripcion'][:50]}...</p>
            <div class="price">${servicio['precio']:,.0f}</div>
        </div>
        '''
    
    return f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechFlow Solutions - Servicios</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .header {{ background: rgba(255,255,255,0.95); padding: 1rem 2rem; position: fixed; width: 100%; top: 0; z-index: 1000; }}
        .navbar {{ display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; }}
        .logo {{ font-size: 1.8rem; font-weight: bold; color: #667eea; }}
        .nav-links {{ display: flex; gap: 2rem; list-style: none; }}
        .nav-links a {{ text-decoration: none; color: #333; font-weight: 500; }}
        .nav-links a:hover {{ color: #667eea; }}
        .hero {{ text-align: center; padding: 8rem 2rem 4rem; color: white; }}
        .hero h1 {{ font-size: 3rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .services-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; padding: 2rem; max-width: 1200px; margin: 0 auto; }}
        .service-card {{ background: rgba(255,255,255,0.95); border-radius: 15px; padding: 2rem; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: transform 0.3s ease; cursor: pointer; }}
        .service-card:hover {{ transform: translateY(-5px); }}
        .service-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
        .service-card h3 {{ margin-bottom: 1rem; color: #333; }}
        .price {{ font-size: 1.5rem; font-weight: bold; color: #667eea; }}
    </style>
</head>
<body>
    <header class="header">
        <nav class="navbar">
            <div class="logo">TechFlow Solutions</div>
            <ul class="nav-links">
                <li><a href="/">Inicio</a></li>
                <li><a href="/servicios">Servicios</a></li>
                <li><a href="/login">Admin</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="hero">
            <h1>Nuestros Servicios</h1>
            <p>Soluciones tecnológicas completas para tu empresa</p>
        </section>

        <section class="services-grid">
            {servicios_html}
        </section>
    </main>
</body>
</html>
    '''

@app.route('/detalle/<int:servicio_id>')
def detalle_servicio(servicio_id):
    """MOCKUP 3: Detalle de servicio"""
    conn = get_db_connection()
    servicio = conn.execute('SELECT * FROM servicios WHERE id = ?', (servicio_id,)).fetchone()
    conn.close()
    
    if not servicio:
        return redirect(url_for('servicios'))
    
    promocion_badge = f'<span class="promotion-badge">¡En Promoción! 20% OFF</span>' if servicio['promocion'] else ''
    
    return f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechFlow Solutions - {servicio['nombre']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .header {{ background: rgba(255,255,255,0.95); padding: 1rem 2rem; position: fixed; width: 100%; top: 0; z-index: 1000; }}
        .navbar {{ display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; }}
        .logo {{ font-size: 1.8rem; font-weight: bold; color: #667eea; }}
        .nav-links {{ display: flex; gap: 2rem; list-style: none; }}
        .nav-links a {{ text-decoration: none; color: #333; font-weight: 500; }}
        .detail-container {{ max-width: 1000px; margin: 8rem auto 2rem; padding: 0 2rem; }}
        .detail-header {{ background: rgba(255,255,255,0.95); border-radius: 15px; padding: 3rem; margin-bottom: 2rem; display: flex; align-items: center; gap: 2rem; }}
        .detail-icon {{ font-size: 4rem; background: #667eea; color: white; width: 120px; height: 120px; border-radius: 15px; display: flex; align-items: center; justify-content: center; }}
        .price {{ font-size: 1.5rem; font-weight: bold; color: #667eea; }}
        .promotion-badge {{ background: #ff4757; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; margin-top: 1rem; display: inline-block; }}
        .detail-content {{ background: rgba(255,255,255,0.95); border-radius: 15px; padding: 3rem; }}
        .info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }}
        .info-item {{ background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; }}
        .btn {{ padding: 1rem 2rem; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; margin: 0.5rem; }}
        .btn-primary {{ background: #667eea; color: white; }}
        .btn-secondary {{ background: #6c757d; color: white; }}
    </style>
</head>
<body>
    <header class="header">
        <nav class="navbar">
            <div class="logo">TechFlow Solutions</div>
            <ul class="nav-links">
                <li><a href="/">Inicio</a></li>
                <li><a href="/servicios">Servicios</a></li>
                <li><a href="/login">Admin</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <div class="detail-container">
            <div class="detail-header">
                <div class="detail-icon">{servicio['icono']}</div>
                <div>
                    <h1>{servicio['nombre']}</h1>
                    <div class="price">${servicio['precio']:,.0f}</div>
                    {promocion_badge}
                </div>
            </div>

            <div class="detail-content">
                <h3>Descripción del Servicio</h3>
                <p>{servicio['descripcion']}</p>

                <div class="info-grid">
                    <div class="info-item">
                        <strong>Servicios Disponibles:</strong><br>
                        {servicio['stock']} proyectos
                    </div>
                    <div class="info-item">
                        <strong>Tiempo de Entrega:</strong><br>
                        4-6 semanas
                    </div>
                    <div class="info-item">
                        <strong>Garantía:</strong><br>
                        12 meses
                    </div>
                    <div class="info-item">
                        <strong>Soporte:</strong><br>
                        Incluido 6 meses
                    </div>
                </div>

                <div style="margin-top: 2rem;">
                    <button class="btn btn-primary">Solicitar Cotización</button>
                    <button class="btn btn-secondary" onclick="window.history.back()">Volver</button>
                </div>
            </div>
        </div>
    </main>
</body>
</html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    """MOCKUP 4: Login de administrador"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', 
                           (username, password_hash)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('admin'))
        else:
            error = 'Credenciales incorrectas'
    else:
        error = None
    
    error_msg = f'<div style="color: red; text-align: center; margin-bottom: 1rem;">{error}</div>' if error else ''
    
    return f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechFlow Solutions - Login Admin</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
        .login-container {{ background: rgba(255,255,255,0.95); border-radius: 15px; padding: 3rem; width: 400px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
        .login-container h2 {{ color: #333; margin-bottom: 2rem; }}
        .form-group {{ margin-bottom: 1.5rem; text-align: left; }}
        .form-group label {{ display: block; margin-bottom: 0.5rem; font-weight: 500; }}
        .form-group input {{ width: 100%; padding: 1rem; border: 2px solid #ddd; border-radius: 8px; font-size: 1rem; }}
        .form-group input:focus {{ outline: none; border-color: #667eea; }}
        .btn {{ width: 100%; padding: 1rem; background: #667eea; color: white; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; }}
        .btn:hover {{ background: #5a6fd8; }}
        .demo-info {{ background: #e7f3ff; padding: 1rem; border-radius: 8px; margin-top: 1rem; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="login-container">
        <h2>🔐 Acceso Administrativo</h2>
        {error_msg}
        
        <form method="POST">
            <div class="form-group">
                <label for="username">👤 Usuario:</label>
                <input type="text" id="username" name="username" required>
            </div>

            <div class="form-group">
                <label for="password">🔑 Contraseña:</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn">Iniciar Sesión</button>
        </form>

        <div class="demo-info">
            <strong>Credenciales de prueba:</strong><br>
            Usuario: <strong>admin</strong><br>
            Contraseña: <strong>admin123</strong>
        </div>

        <div style="margin-top: 1rem;">
            <a href="/" style="color: #667eea; text-decoration: none;">← Volver al inicio</a>
        </div>
    </div>
</body>
</html>
    '''

@app.route('/admin')
def admin():
    """MOCKUP 5: Panel de administración (CRUD)"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    servicios = conn.execute('SELECT * FROM servicios ORDER BY id').fetchall()
    conn.close()
    
    servicios_rows = ''
    for servicio in servicios:
        promocion_badge = '<span style="background: #d4edda; color: #155724; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">Sí</span>' if servicio['promocion'] else '<span style="background: #f8d7da; color: #721c24; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">No</span>'
        
        servicios_rows += f'''
        <tr>
            <td>{servicio['id']}</td>
            <td>{servicio['icono']}</td>
            <td>{servicio['nombre']}</td>
            <td>${servicio['precio']:,.0f}</td>
            <td>{servicio['stock']}</td>
            <td>{promocion_badge}</td>
            <td>
                <a href="/admin/editar/{servicio['id']}" style="background: #17a2b8; color: white; padding: 0.5rem; border-radius: 5px; text-decoration: none; margin: 2px;">✏️</a>
                <a href="/admin/eliminar/{servicio['id']}" onclick="return confirm('¿Eliminar este servicio?')" style="background: #dc3545; color: white; padding: 0.5rem; border-radius: 5px; text-decoration: none; margin: 2px;">🗑️</a>
            </td>
        </tr>
        '''
    
    return f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechFlow Solutions - Panel Admin</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding-top: 80px; }}
        .header {{ background: rgba(255,255,255,0.95); padding: 1rem 2rem; position: fixed; width: 100%; top: 0; z-index: 1000; }}
        .navbar {{ display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; }}
        .logo {{ font-size: 1.8rem; font-weight: bold; color: #667eea; }}
        .nav-links {{ display: flex; gap: 2rem; list-style: none; }}
        .nav-links a {{ text-decoration: none; color: #333; font-weight: 500; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 2rem; }}
        .admin-header {{ background: rgba(255,255,255,0.95); border-radius: 15px; padding: 2rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; }}
        .crud-section {{ background: rgba(255,255,255,0.95); border-radius: 15px; padding: 2rem; }}
        .crud-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }}
        .admin-table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }}
        .admin-table th, .admin-table td {{ padding: 1rem; text-align: left; border-bottom: 1px solid #ddd; }}
        .admin-table th {{ background: #f8f9fa; font-weight: 600; }}
        .admin-table tr:hover {{ background: #f8f9fa; }}
        .btn {{ padding: 1rem 2rem; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; text-decoration: none; display: inline-block; }}
        .btn-success {{ background: #28a745; color: white; }}
        .btn-secondary {{ background: #6c757d; color: white; }}
        .stat-badge {{ background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; margin-left: 1rem; }}
    </style>
</head>
<body>
    <header class="header">
        <nav class="navbar">
            <div class="logo">TechFlow Solutions</div>
            <ul class="nav-links">
                <li><a href="/">Inicio</a></li>
                <li><a href="/servicios">Servicios</a></li>
                <li><a href="/logout">Cerrar Sesión</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <div class="container">
            <div class="admin-header">
                <h1>🛠️ Panel de Administración</h1>
                <div>
                    <span class="stat-badge">Admin: {session['username']}</span>
                </div>
            </div>

            <section class="crud-section">
                <div class="crud-header">
                    <h2>Gestión de Servicios</h2>
                    <a href="/admin/agregar" class="btn btn-success">➕ Nuevo Servicio</a>
                </div>

                <div style="overflow-x: auto;">
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Icono</th>
                                <th>Nombre</th>
                                <th>Precio</th>
                                <th>Stock</th>
                                <th>Promoción</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {servicios_rows}
                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    </main>
</body>
</html>
    '''

# RUTAS CRUD ADICIONALES

@app.route('/admin/agregar', methods=['GET', 'POST'])
def agregar_servicio():
    """Agregar nuevo servicio"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        promocion = 1 if 'promocion' in request.form else 0
        icono = request.form['icono']
        
        conn = get_db_connection()
        conn.execute('''INSERT INTO servicios (nombre, descripcion, precio, stock, promocion, icono) 
                       VALUES (?, ?, ?, ?, ?, ?)''', 
                    (nombre, descripcion, precio, stock, promocion, icono))
        conn.commit()
        conn.close()
        
        return redirect(url_for('admin'))
    
    return '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agregar Servicio</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 2rem; }
        .container { max-width: 600px; margin: 0 auto; background: rgba(255,255,255,0.95); border-radius: 15px; padding: 3rem; }
        .form-group { margin-bottom: 1.5rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
        .form-group input, .form-group textarea { width: 100%; padding: 1rem; border: 2px solid #ddd; border-radius: 8px; font-size: 1rem; }
        .form-group input:focus, .form-group textarea:focus { outline: none; border-color: #667eea; }
        .btn { padding: 1rem 2rem; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; margin-right: 1rem; }
        .btn-primary { background: #667eea; color: white; }
        .btn-secondary { background: #6c757d; color: white; text-decoration: none; display: inline-block; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>➕ Agregar Nuevo Servicio</h2>
        
        <form method="POST">
            <div class="form-group">
                <label>Nombre del Servicio:</label>
                <input type="text" name="nombre" required>
            </div>
            
            <div class="form-group">
                <label>Icono (emoji):</label>
                <input type="text" name="icono" maxlength="2" value="🔧">
            </div>
            
            <div class="form-group">
                <label>Precio:</label>
                <input type="number" name="precio" required>
            </div>
            
            <div class="form-group">
                <label>Stock:</label>
                <input type="number" name="stock" required>
            </div>
            
            <div class="form-group">
                <label>Descripción:</label>
                <textarea name="descripcion" rows="3"></textarea>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" name="promocion"> En promoción
                </label>
            </div>
            
            <button type="submit" class="btn btn-primary">💾 Guardar</button>
            <a href="/admin" class="btn btn-secondary">❌ Cancelar</a>
        </form>
    </div>
</body>
</html>
    '''

@app.route('/admin/eliminar/<int:servicio_id>')
def eliminar_servicio(servicio_id):
    """Eliminar servicio"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM servicios WHERE id = ?', (servicio_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('home'))

# API JSON para datos
@app.route('/api/servicios')
def api_servicios():
    """API REST para obtener servicios en JSON"""
    conn = get_db_connection()
    servicios = conn.execute('SELECT * FROM servicios').fetchall()
    conn.close()
    
    servicios_list = []
    for servicio in servicios:
        servicios_list.append({
            'id': servicio['id'],
            'nombre': servicio['nombre'],
            'descripcion': servicio['descripcion'],
            'precio': servicio['precio'],
            'stock': servicio['stock'],
            'promocion': bool(servicio['promocion']),
            'icono': servicio['icono']
        })
    
    return jsonify(servicios_list)

if __name__ == '__main__':
    # Inicializar base de datos
    init_db()
    print("✅ Base de datos inicializada")
    print("🚀 Servidor iniciando en http://localhost:5000")
    print("📝 Credenciales: admin / admin123")
    
    # Ejecutar servidor
    app.run(debug=True, host='0.0.0.0', port=5000)