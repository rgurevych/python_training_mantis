import string
import random
import re

class ProjectHelper:

    def __init__(self, app):
        self.app = app

    projects_cache = None

    def open_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("/manage_proj_page.php"):
            #the number of elements in menu depends on existance of projects, therefore the try-except is used
            try:
                wd.find_element_by_xpath("//div[@class='nav-wrap']/ul/li[7]/a/i").click()
            except Exception:
                wd.find_element_by_xpath("//div[@class='nav-wrap']/ul/li[6]/a/i").click()
            wd.find_element_by_xpath("//div[2]/div[2]/div[2]/div/ul/li[3]/a").click()


    def add_project(self, project_name):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_css_selector('input.btn').click()
        wd.find_element_by_id('project-name').click()
        wd.find_element_by_id('project-name').clear()
        wd.find_element_by_id('project-name').send_keys(project_name)
        wd.find_element_by_css_selector('input.btn').click()
        wd.find_element_by_css_selector('a.btn').click()
        self.projects_cache = None


    def delete_project(self, project_name):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_link_text(project_name).click()
        wd.find_element_by_xpath("//form[@id='project-delete-form']/fieldset/input[3]").click()
        wd.find_element_by_css_selector('input.btn').click()
        self.projects_cache = None


    def get_projects_list(self):
        if self.projects_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.projects_cache = []
            for element in wd.find_elements_by_xpath("//tbody/tr/td/a"):
                text = element.text
                self.projects_cache.append(text)
        return self.projects_cache


    def random_name(self):
        sym = string.ascii_letters + string.digits + " "*10
        return re.sub('\s+', ' ', ("".join([random.choice(sym) for i in range(random.randrange(20))]).rstrip()))