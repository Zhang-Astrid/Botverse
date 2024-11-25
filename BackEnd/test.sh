#注册

# curl -X POST http://127.0.0.1:8080/register \
#     -H "Content-Type: application/json" \
#     -d '{"username": "testuser", "password": "testpassword"}'

# 登录
# curl -X POST http://127.0.0.1:8080/login \
#     -H "Content-Type: application/json" \
#     -d '{"username": "testuser", "password": "testpassword"}' \
#     -c cookies.txt

# 查看用户信息
curl -X GET http://127.0.0.1:8080/user \
    -H "Content-Type: application/json" \
    -b cookies.txt
