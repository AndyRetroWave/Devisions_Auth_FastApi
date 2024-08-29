AUTH_HTML = {
    'welcome':
    """
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



    'register': """
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
        <form action="/auth/register" method="post">
            <div class="form-group">
                <label for="username">Имя</label>
                <input type="text" id="given_name" name="given_name" required>
            </div>
            <div class="form-group">
                <label for="username">Фамилия</label>
                <input type="text" id="family_name" name="family_name" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="password">Пароль</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" href="/auth/register" class="btn">Регистрация</button>
        </form>
        <div style="margin-top: 20px;">
            <a href="/register/google" class="google-btn">
                <img src="https://img.icons8.com/?size=100&id=17950&format=png&color=000000" alt="Google" class="google-icon">
                Регистрация через Google
            </a>
        </div>
    </div>
</body>
</html>

"""


}
