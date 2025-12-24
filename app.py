from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'very-secret-key-123456789'

# Конфигурация базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///luxe_suede.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модели базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    thickness = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(200), default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(80))

# Создание таблиц
with app.app_context():
    db.create_all()

# Инициализация данных
def init_data():
    # Создаем администратора
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@luxe-suede.ru',
            password=generate_password_hash('123456'),
            role='admin'
        )
        db.session.add(admin)
        print("Администратор создан: admin / 123456")
    
    # Создаем тестового пользователя
    if not User.query.filter_by(username='user').first():
        user = User(
            username='user',
            email='user@example.com',
            password=generate_password_hash('user123'),
            role='user'
        )
        db.session.add(user)
        print("Пользователь создан: user / user123")
    
    # Создаем тестовые товары
    if Product.query.count() == 0:
        products = [
            Product(
                name='Натуральная замша итальянская',
                description='Высококачественная замша из Италии, мягкая и прочная',
                price=4500.0,
                category='Листы',
                color='Коричневый',
                thickness='1.2 мм',
                image='product1.jpg',
                created_by='admin'
            ),
            Product(
                name='Замша овечья премиум',
                description='Мягкая замша из овечьей кожи, идеальна для одежды',
                price=5200.0,
                category='Листы',
                color='Бежевый',
                thickness='0.8 мм',
                image='product2.jpg',
                created_by='admin'
            ),
            Product(
                name='Замша для обуви',
                description='Плотная замша для производства обуви',
                price=3800.0,
                category='Листы',
                color='Черный',
                thickness='1.5 мм',
                image='product3.jpg',
                created_by='admin'
            ),
            Product(
                name='Замша дикая',
                description='Натуральная замша с естественной текстурой',
                price=6100.0,
                category='Листы',
                color='Натуральный',
                thickness='1.0 мм',
                image='product4.jpg',
                created_by='admin'
            ),
            Product(
                name='Замша для мебели',
                description='Износостойкая замша для обивки мебели',
                price=4200.0,
                category='Рулоны',
                color='Серый',
                thickness='1.8 мм',
                image='product5.jpg',
                created_by='admin'
            ),
            Product(
                name='Замша для аксессуаров',
                description='Тонкая замша для сумок и кошельков',
                price=3300.0,
                category='Листы',
                color='Бордовый',
                thickness='0.6 мм',
                image='product6.jpg',
                created_by='admin'
            ),
            Product(
                name='Замша дубленая',
                description='Дубленая растительными экстрактами',
                price=4900.0,
                category='Листы',
                color='Темно-коричневый',
                thickness='1.3 мм',
                image='product7.jpg',
                created_by='admin'
            ),
            Product(
                name='Замша вощеная',
                description='Замша с восковым покрытием, водоотталкивающая',
                price=5700.0,
                category='Листы',
                color='Зеленый',
                thickness='1.4 мм',
                image='product8.jpg',
                created_by='admin'
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        print("Тестовые товары созданы")
    
    db.session.commit()

# Инициализация данных
with app.app_context():
    init_data()

# Декораторы
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('Доступ запрещен. Требуются права администратора', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

# Вспомогательная функция для работы с корзиной
def get_cart():
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']

def save_cart(cart):
    session['cart'] = cart
    session.modified = True

# Главная
@app.route('/')
def index():
    products = Product.query.limit(4).all()
    return render_template('index.html', products=products)

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Пароль должен содержать минимум 6 символов', 'danger')
            return render_template('register.html')
        
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role='user'
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Регистрация успешна! Теперь вы можете войти', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Ошибка при регистрации', 'danger')
    
    return render_template('register.html')

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Неверное имя пользователя или пароль', 'danger')
            return render_template('login.html')
        
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        session['email'] = user.email
        
        flash(f'Добро пожаловать, {username}!', 'success')
        return redirect(url_for('index'))
    
    return render_template('login.html')

# Выход
@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# Профиль - ИСПРАВЛЕНО
@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

# Каталог
@app.route('/products')
def all_products():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('products.html', products=products, categories=categories)

# Детали товара
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(3).all()
    
    return render_template('product_detail.html', product=product, related_products=related)

# Добавление в корзину
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Проверяем авторизацию
    if 'user_id' not in session:
        flash('Для добавления товаров в корзину необходимо войти в систему', 'warning')
        return redirect(url_for('login'))
    
    # Получаем товар
    product = Product.query.get(product_id)
    if not product:
        flash('Товар не найден', 'danger')
        return redirect(url_for('all_products'))
    
    # Получаем корзину
    cart = get_cart()
    
    # Добавляем товар
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
    
    # Сохраняем корзину
    save_cart(cart)
    
    flash(f'"{product.name}" добавлен в корзину!', 'success')
    
    # Возвращаемся на предыдущую страницу
    return redirect(request.referrer or url_for('all_products'))

# Просмотр корзины
@app.route('/cart')
@login_required
def view_cart():
    cart = get_cart()
    
    # Получаем товары из корзины
    cart_items = []
    total = 0
    
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = Product.query.get(product_id)
        
        if product:
            item_total = product.price * quantity
            total += item_total
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
    
    return render_template('cart.html', cart_items=cart_items, total=total)

# Обновление корзины
@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    cart = {}
    
    for key, value in request.form.items():
        if key.startswith('quantity_'):
            product_id = int(key.replace('quantity_', ''))
            quantity = int(value)
            
            if quantity > 0:
                cart[str(product_id)] = quantity
    
    save_cart(cart)
    flash('Корзина обновлена', 'success')
    return redirect(url_for('view_cart'))

# Удаление из корзины
@app.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart = get_cart()
    
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        save_cart(cart)
        flash('Товар удален из корзины', 'info')
    else:
        flash('Товар не найден в корзине', 'warning')
    
    return redirect(url_for('view_cart'))

# Оформление заказа
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = get_cart()
    
    if not cart:
        flash('Ваша корзина пуста', 'warning')
        return redirect(url_for('view_cart'))
    
    # Подсчет суммы
    cart_items = []
    total = 0
    
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = Product.query.get(product_id)
        
        if product:
            item_total = product.price * quantity
            total += item_total
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
    
    if request.method == 'POST':
        # Здесь должна быть логика оформления заказа
        flash('Заказ успешно оформлен!', 'success')
        
        # Очищаем корзину
        session.pop('cart', None)
        session.modified = True
        
        order_number = random.randint(100000, 999999)
        return render_template('order_confirmation.html', order_number=order_number)
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

# О нас
@app.route('/about')
def about():
    return render_template('about.html')

# Админ-панель
# Админ-панель
@app.route('/admin')
@admin_required
def admin_panel():
    total_products = Product.query.count()
    categories_list = db.session.query(Product.category).distinct().all()
    categories_list = [c[0] for c in categories_list]  # Преобразуем в список строк
    categories_count = len(categories_list)  # Количество категорий
    
    # Средняя цена
    total_price = db.session.query(db.func.sum(Product.price)).scalar() or 0
    avg_price = int(total_price / total_products) if total_products > 0 else 0
    
    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         categories=categories_list,  # Теперь передаем список
                         categories_count=categories_count,  # И количество отдельно
                         avg_price=avg_price)

# Управление товарами
# Управление товарами (админка)
@app.route('/admin/manage-products')
@admin_required
def manage_products():
    products = Product.query.all()
    return render_template('admin/manage_products.html', products=products)

# Добавление товара
@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    if request.method == 'POST':
        try:
            product = Product(
                name=request.form.get('name'),
                description=request.form.get('description'),
                price=float(request.form.get('price')),
                category=request.form.get('category'),
                color=request.form.get('color'),
                thickness=request.form.get('thickness'),
                image=request.form.get('image') or 'default.jpg',
                created_by=session['username']
            )
            
            db.session.add(product)
            db.session.commit()
            
            flash('Товар успешно добавлен', 'success')
            return redirect(url_for('manage_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении товара: {str(e)}', 'danger')
    
    return render_template('admin/add_product.html')

# Редактирование товара
@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            product.name = request.form.get('name')
            product.description = request.form.get('description')
            product.price = float(request.form.get('price'))
            product.category = request.form.get('category')
            product.color = request.form.get('color')
            product.thickness = request.form.get('thickness')
            product.image = request.form.get('image') or 'default.jpg'
            
            db.session.commit()
            
            flash('Товар успешно обновлен', 'success')
            return redirect(url_for('manage_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении товара: {str(e)}', 'danger')
    
    return render_template('admin/edit_product.html', product=product)

# Удаление товара
@app.route('/admin/products/delete/<int:product_id>')
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Товар успешно удален', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении товара: {str(e)}', 'danger')
    
    return redirect(url_for('manage_products'))

# Контекстный процессор
# Контекстный процессор
@app.context_processor
def inject_user():
    user_obj = None
    cart_count = 0
    is_admin = False
    
    if 'user_id' in session:
        user_obj = User.query.get(session['user_id'])
        
        # Проверяем роль пользователя
        if user_obj and user_obj.role == 'admin':
            is_admin = True
    
    if 'cart' in session:
        cart_count = len(session['cart'])
    
    return {
        'current_user': user_obj,
        'is_admin': is_admin,
        'cart_count': cart_count,
        'now': datetime.now()
    }
# Отладочные маршруты
@app.route('/debug/session')
def debug_session():
    return f"Session: {dict(session)}"

@app.route('/debug/cart')
def debug_cart():
    cart = get_cart()
    return f"Cart: {cart}"

@app.route('/debug/clear')
def debug_clear():
    session.clear()
    return "Session cleared"

if __name__ == '__main__':
    app.run(debug=True, port=5000)