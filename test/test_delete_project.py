import random

def test_delete_random_project(app):
    if len(app.project.get_projects_list()) == 0:
        app.project.add_project("Project for deletion")
    old_projects = app.project.get_projects_list()
    project_name = random.choice(old_projects)
    app.project.delete_project(project_name)
    old_projects.remove(project_name)
    new_projects = app.project.get_projects_list()
    assert sorted(old_projects) == sorted(new_projects)