
def test_signup_new_account(app):
    username = app.james.random_username()
    email = username + "@localhost"
    password = "testpass"
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)
    assert app.soap.login_possible(username, password)
    #app.session.login(username, password)
    #assert app.session.is_logged_in_as(username)
    #app.session.logout()