AUTH_HTML = {
    "welcome": """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login or Register</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: #fff;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            .container h1 {
                margin-bottom: 20px;
                color: #333;
            }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                margin: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                color: #fff;
                background-color: #007BFF;
                text-decoration: none;
                transition: background-color 0.3s;
            }
            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Добро пожаловать!</h1>
            <a href="/auth/register" class="btn">Регистрация</a>
            <a href="/auth/login" class="btn">Вход</a>
        </div>
    </body>
    </html>
    """,
    "register_good": """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Register</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: #fff;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 300px;
            }
            .container h1 {
                margin-bottom: 20px;
                color: #333;
            }
            .form-group {
                margin-bottom: 15px;
                text-align: left;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
                color: #333;
            }
            .form-group input {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 16px;
            }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                margin-top: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                color: #fff;
                background-color: #007BFF;
                text-decoration: none;
                transition: background-color 0.3s;
                cursor: pointer;
            }
            .btn:hover {
                background-color: #0056b3;
            }
            .google-btn {
                display: inline-block;
                padding: 10px 20px;
                margin-top: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 16px;
                color: #333;
                background-color: #fff;
                text-decoration: none;
                transition: background-color 0.3s;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .google-btn:hover {
                background-color: #f8f8f8;
            }
            .google-icon {
                width: 20px;
                height: 20px;
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Регистрация</h1>
            <form action="/auth/register" method="post" onsubmit="return checkPasswordStrength()">
                <div class="form-group">
                    <label for="given_name">Имя</label>
                    <input type="text" id="given_name" name="given_name" required>
                </div>
                <div class="form-group">
                    <label for="family_name">Фамилия</label>
                    <input type="text" id="family_name" name="family_name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required onblur="checkEmailAvailability()">
                    <div class="email-availability" id="email-availability"></div>
                </div>
                <div class="form-group">
                    <label for="password">Пароль</label>
                    <input type="password" id="password" name="password" required oninput="checkPasswordStrength()">
                    <div class="password-strength" id="password-strength"></div>
                </div>
                <button type="submit" class="btn">Регистрация</button>
            </form>
            <div style="margin-top: 20px;">
                <a href="/auth/register/google" class="google-btn">
                    <img src="https://img.icons8.com/?size=100&id=17950&format=png&color=000000" alt="Google" class="google-icon">
                    Регистрация через Google
                </a>
            </div>
        </div>
        <script>
        function checkEmailAvailability() {
            const email = document.getElementById('email').value;
            const emailAvailability = document.getElementById('email-availability');
            // Очистка предыдущего сообщения
            emailAvailability.textContent = '';
            // Проверка email по стандарту с использованием регулярного выражения
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                emailAvailability.textContent = 'Неверный формат email';
                emailAvailability.style.color = 'red';
                return;
            }
            // Отправка AJAX-запроса на сервер
            fetch('/auth/check-email?email_check=' + encodeURIComponent(email), {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    emailAvailability.textContent = 'Такой пользователь уже существует';
                    emailAvailability.style.color = 'red';
                } else {
                    emailAvailability.textContent = 'Email доступен';
                    emailAvailability.style.color = 'green';
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                emailAvailability.textContent = 'Произошла ошибка при проверке email';
                emailAvailability.style.color = 'red';
                });
            };

            function checkPasswordStrength() {
                const password = document.getElementById('password').value;
                const passwordStrength = document.getElementById('password-strength');
                if (password.length < 8) {
                    passwordStrength.textContent = 'Пароль должен содержать не менее 8 символов';
                    passwordStrength.style.color = 'red';
                    return false;
                } else if (!/[a-z]/.test(password) || !/[A-Z]/.test(password) || !/[0-9]/.test(password) || !/[^a-zA-Z0-9]/.test(password)) {
                    passwordStrength.textContent = 'Пароль должен содержать хотя бы одну строчную букву, одну заглавную букву, одну цифру и один специальный символ';
                    passwordStrength.style.color = 'red';
                    return false;
                } else {
                    passwordStrength.textContent = 'Пароль достаточно сильный';
                    passwordStrength.style.color = 'green';
                    return true;
                }
            }
        </script>
    </body>
</html>

""",
    "welcome_register": """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Добро пожаловать в нашу социальную сеть!</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: #fff;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            h1 {
                color: #333;
            }
            p {
                color: #666;
                line-height: 1.6;
            }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                margin-top: 20px;
                background-color: #007BFF;
                color: #fff;
                text-decoration: none;
                border-radius: 5px;
            }
            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Добро пожаловать в нашу социальную сеть!</h1>
            <p>Вы успешно зарегистрировались и теперь являетесь частью нашего сообщества. Мы рады видеть вас здесь!</p>
            <p>Чтобы начать, вы можете:</p>
            <a href="/profile" class="btn">Перейти к своему профилю</a>
            <a href="/friends" class="btn">Найти друзей</a>
            <a href="/settings" class="btn">Настроить аккаунт</a>
            <p>Если у вас возникнут вопросы, не стесняйтесь обращаться в нашу <a href="/support">службу поддержки</a>.</p>
        </div>
    </body>
    </html>
""",
    "login": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            text-align: center;
        }
        .login-container h2 {
            margin-bottom: 20px;
        }
        .login-container input[type="email"],
        .login-container input[type="password"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 3px;
        }
        .login-container input[type="submit"] {
            width: 100%;
            padding: 10px;
            background-color: #28a745;
            border: none;
            border-radius: 3px;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
        }
        .login-container input[type="submit"]:hover {
            background-color: #218838;
        }
        .error-message {
            color: red;
            margin-top: 10px;
        }
        .google-btn:hover {
            background-color: #f8f8f8;
        }
        .google-icon {
            width: 20px;
            height: 20px;
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login</h2>
        <form id="loginForm" action="/auth/login" method="post">
            <input type="email" id="email" name="email" placeholder="Email" required>
            <input type="password" id="password" name="password" placeholder="Password" required>
            <input type="submit" value="Login">
        </form>
        <div style="margin-top: 20px;">
            <a href="/auth/login/google" class="google-btn">
                <img src="https://img.icons8.com/?size=100&id=17950&format=png&color=000000" alt="Google" class="google-icon">
                Зайти через Google
            </a>
        </div>
        <div id="errorMessage" class="error-message"></div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(event) {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                # body: JSON.stringify({ email, password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.access_token && data.refresh_token) {
                    // Store tokens in localStorage or sessionStorage
                    localStorage.setItem('access_token', data.access_token);
                    localStorage.setItem('refresh_token', data.refresh_token);
                    // Redirect to another page on success
                    window.location.href = '/dashboard';
                } else {
                    document.getElementById('errorMessage').innerText = data.message || 'Login failed';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('errorMessage').innerText = 'An error occurred. Please try again later.';
            });
        });
    </script>
</body>
</html>
""",
}
