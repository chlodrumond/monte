import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.middleware.proxy_fix import ProxyFix

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "monte-academic-platform-secret")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/')
def index():
    """Homepage route"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Login page route"""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    """Handle login form submission"""
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Basic form validation
    if not email or not password:
        flash('Por favor, preencha todos os campos.', 'error')
        return render_template('login.html')
    
    # For demo purposes, just flash a success message
    # In a real application, you would validate credentials here
    flash(f'Login realizado com sucesso para {email}!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
