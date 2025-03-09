import './body.css'

export default function authorization() {
    return (
        <div className="authorization">
                <p className="auth1">Авторизация пользователя</p>
                
                <p className="auth1">Логин</p>
                <input className="auth1" id='login'></input>
                <p className="auth1">Пароль</p>
                <input className="auth1" id='password'></input>
                <p>
                    <button className="auth1">Войти</button>
                </p>
        </div>
    )
}

