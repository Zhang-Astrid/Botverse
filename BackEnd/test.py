import requests

BASE_URL = "http://127.0.0.1:8080"  # Flask 应用的地址

# 测试注册用户
def test_register(username, password):
    url = f"{BASE_URL}/user_sys/register"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    print("Register Response:", response.status_code, response.json())
    return response

# 测试登录用户
def test_login(username, password):
    url = f"{BASE_URL}/user_sys/login"
    data = {
        "username": username,
        "password": password
    }
    session = requests.Session()  # 使用会话以保存 cookies
    response = session.post(url, json=data)
    print("Login Response:", response.status_code, response.json())
    return session, response

# 测试获取用户信息
def test_get_user_info(session):
    url = f"{BASE_URL}/user_sys/user"
    response = session.get(url)
    print("User Info Response:", response.status_code, response.json())
    return response

if __name__ == "__main__":
    # 测试用的用户名和密码
    username = "testuser"
    password = "secure_password"

    # Step 1: 测试注册
    register_response = test_register(username, password)

    # Step 2: 测试登录
    session, login_response = test_login(username, password)

    # Step 3: 测试获取用户信息
    if login_response.status_code == 200:  # 如果登录成功
        test_get_user_info(session)
