
class SessionHelper:

    def __init__(self, app):
        self.app = app


    def login(self, username, password):
        wd = self.app.wd
        self.app.open_app_page()
        wd.find_element_by_id("username").click()
        wd.find_element_by_id("username").clear()
        wd.find_element_by_id("username").send_keys(username)
        wd.find_element_by_id("password").click()
        wd.find_element_by_id("password").clear()
        wd.find_element_by_id("password").send_keys(password)
        wd.find_element_by_xpath("//input[@type='submit']").click()


    def logout(self):
        wd = self.app.wd
        wd.find_element_by_css_selector("span.user-info").click()
        wd.find_element_by_css_selector("i.ace-icon.fa-sign-out").click()


    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()


    def is_logged_in(self):
        wd = self.app.wd
        return not wd.current_url.endswith("/login_page.php")


    def is_logged_in_as(self, username):
        return self.get_logged_username() == username


    def get_logged_username(self):
        wd = self.app.wd
        return wd.find_element_by_xpath("//span[@class='user-info']").text


    def ensure_login(self, username, password):
        self.app.open_app_page()
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        else:
            self.login(username, password)