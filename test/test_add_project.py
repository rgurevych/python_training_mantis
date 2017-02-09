import time

def test_add_new_project(app):
    project_name = app.project.random_name()
    old_projects = app.project.get_projects_list()
    app.project.add_project(project_name)
    old_projects.append(project_name)
    new_projects = app.project.get_projects_list()
    assert sorted(old_projects) == sorted(new_projects)
