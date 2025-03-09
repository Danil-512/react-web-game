import './body.css'

export default function authorization() {
    return (
        <div class="authorization">
                <p class="auth1">Авторизация пользователя</p>
                
                <p class="auth1">Логин</p>
                <input class="auth1" id='login'></input>
                <p class="auth1">Пароль</p>
                <input class="auth1" id='password'></input>
                <p>
                    <button class="auth1">Войти</button>
                </p>
        </div>
    )
}

