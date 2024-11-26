curl https://api.aiproxy.io/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-iiEY0IByanFKFqpERT27TwkauSK7GOrIgLKCIANsuiAiDGMI" \
  -d '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "你好，很高兴遇见你!"}],
     "temperature": 0.7,
     "session_id": "abcdef",
     "session_limit": 2
   }'