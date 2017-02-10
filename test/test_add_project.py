
def test_add_new_project(app):
    project_name = app.project.random_name()
    old_projects = app.project.get_projects_list()
    if project_name in old_projects:
        app.project.delete_project(project_name)
    app.project.add_project(project_name)
    old_projects.append(project_name)
    new_projects = app.project.get_projects_list()
    assert sorted(old_projects) == sorted(new_projects)
