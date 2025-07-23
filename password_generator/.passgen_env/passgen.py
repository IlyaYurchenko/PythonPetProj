from flask import Flask, render_template, request, redirect, url_for, flash
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    length = request.form.get('length', type=int)
    if not length or length < 8 or length > 16:
        flash('Password length must be between 8 and 16 characters.', 'error')
        return redirect(url_for('index'))
    
    characters = string.ascii_letters + string.digits
    passwd = ''.join(random.choice(characters) for _ in range(length))
    flash(f'Generated Password: {passwd}', 'success')
    return redirect(url_for('index'))

@app.route('/PasswdCheck', methods=['POST'])
def check_password():
    password = request.form.get('password')
    if not password:
        flash('Please enter a password to check.', 'error')
        return redirect(url_for('index'))

    if len(password) < 8 or len(password) > 16:
        flash('Password must be between 8 and 16 characters.', 'error')
        return redirect(url_for('index'))

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    if has_upper and has_lower and has_digit:
        flash('Password is strong.', 'success')
    else:
        flash('Password must contain at least one uppercase letter, one lowercase letter, and one digit.', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)