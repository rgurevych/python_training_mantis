
def test_signup_new_account(app):
    username = "testuser123"
    password = "testpass"
    app.james.ensure_user_exists(username, password)