from datetime import timedelta
from backend.routes.auth import create_access_token

# Create a test token
test_token = create_access_token(
    user_id="test_user_123",
    email="test@example.com",
    expires_minutes=60  # valid for 1 hour
)

print(test_token)
