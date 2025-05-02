from flask import Flask, render_template, request
import string
import secrets
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

common_passwords = ["123456", "password", "qwerty", "admin", "user"]

def analyze_password_strength_manual(password):
    score = 0
    if len(password) >= 12: score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    if len(set(password)) >= 8: score += 1
    return score / 6

def analyze_password_strength(password):
    strength = analyze_password_strength_manual(password)
    if strength >= 0.75:
        return "قوية", "green"
    elif strength >= 0.5:
        return "متوسطة", "orange"
    else:
        return "ضعيفة", "red"

def is_common_password(password):
    return password in common_passwords

def estimate_brute_force_time(password):
    chars = string.ascii_letters + string.digits + string.punctuation
    total = len(chars) ** len(password) if password else 0
    speed = 10**9
    seconds = total / speed if total else 0
    if seconds < 1: return "أقل من ثانية"
    elif seconds < 60: return f"{seconds:.1f} ثانية"
    elif seconds < 3600: return f"{int(seconds//60)} دقيقة"
    elif seconds < 86400: return f"{int(seconds//3600)} ساعة"
    elif seconds < 31536000: return f"{int(seconds//86400)} يوم"
    else: return f"{int(seconds//31536000)} سنة"

def generate_suggestion(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    results = {}
    if request.method == 'POST':
        password = request.form['password']
        strength_text, color = analyze_password_strength(password)
        crack_time = estimate_brute_force_time(password)
        suggestion = generate_suggestion() if strength_text == "ضعيفة" else None
        results = {
            'password': password,
            'strength': strength_text,
            'color': color,
            'crack_time': crack_time,
            'is_common': is_common_password(password),
            'suggestion': suggestion
        }
    return render_template('index.html', results=results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
