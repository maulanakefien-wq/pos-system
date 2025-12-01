#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# POS System - Flask Web Application
from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'pos-system-secret-2025-egypt'

# In-Memory Database
DATA = {
    'users': {
        'admin': {'password': 'admin123', 'name': 'المسؤول', 'role': 'admin'},
        'seller': {'password': '123456', 'name': 'عامل', 'role': 'seller'}
    },
    'products': {},
    'customers': {},
    'invoices': {}
}

LOGIN_HTML = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول - نظام نقاط البيع</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-container { background: white; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); padding: 40px; width: 100%; max-width: 400px; }
        .login-header { text-align: center; margin-bottom: 30px; }
        .login-header h1 { color: #667eea; font-weight: bold; font-size: 28px; }
        .form-control { border-radius: 8px; border: 2px solid #ddd; padding: 12px; margin-bottom: 15px; }
        .form-control:focus { border-color: #667eea; box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25); }
        .btn-login { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; color: white; padding: 12px; width: 100%; cursor: pointer; border-radius: 8px; }
        .error { color: #dc3545; margin-bottom: 15px; text-align: center; }
        .demo-info { background: #e7f3ff; border-left: 4px solid #2196F3; padding: 15px; margin-top: 20px; font-size: 13px; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>🛍️ نظام نقاط البيع</h1>
            <p style="color: #666;">نسخة ويب متقدمة</p>
        </div>
        {% if error %}
        <div class="error">❌ {{ error }}</div>
        {% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="اسم المستخدم" class="form-control" required>
            <input type="password" name="password" placeholder="كلمة المرور" class="form-control" required>
            <button type="submit" class="btn-login">دخول</button>
        </form>
        <div class="demo-info">
            <strong>📌 بيانات التجربة:</strong><br>
            👤 admin / 🔐 admin123<br>
            👤 seller / 🔐 123456
        </div>
    </div>
</body>
</html>'''

DASHBOARD_HTML = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f5f7fa; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .stat-number { font-size: 32px; font-weight: bold; color: #667eea; }
        .btn-primary { background: #667eea; border: none; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark">
        <div class="container-fluid">
            <span class="navbar-brand">🛍️ نظام نقاط البيع</span>
            <div>
                <span style="color: white; margin-right: 20px;">👤 {{ username }}</span>
                <a href="/logout" class="btn btn-sm btn-light">خروج</a>
            </div>
        </div>
    </nav>
    <div class="container mt-5">
        <div class="row"><div class="col-md-3"><div class="card"><div class="card-body text-center"><div class="stat-number">0</div><p>الفواتير</p></div></div></div><div class="col-md-3"><div class="card"><div class="card-body text-center"><div class="stat-number">0</div><p>الأصناف</p></div></div></div><div class="col-md-3"><div class="card"><div class="card-body text-center"><div class="stat-number">0</div><p>العملاء</p></div></div></div><div class="col-md-3"><div class="card"><div class="card-body text-center"><div class="stat-number">0</div><p>الأرباح</p></div></div></div></div>
        <div class="alert alert-success mt-4">✅ <strong>البرنامج يعمل بنجاح!</strong> هذا إصدار نسخة العمل الأولية</div>
    </div>
</body>
</html>'''

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in DATA['users'] and DATA['users'][username]['password'] == password:
            session['user'] = username
            session['name'] = DATA['users'][username]['name']
            return redirect(url_for('dashboard'))
        else:
            error = 'اسم المستخدم أو كلمة المرور غير صحيحة'
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string(DASHBOARD_HTML, username=session.get('name'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(error):
    return '<h1>❌ الصفحة غير موجودة</h1><a href="/">العودة</a>', 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
