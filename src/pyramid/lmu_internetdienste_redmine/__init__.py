from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Use Template Engine Chameleon
    config.include('pyramid_chameleon')

    # Add Routes
    config.add_route('home', '/')
    config.add_route('projects_view', '/projects')
    config.add_route('project_view', '/project/{id}')
    config.add_route('project_add', '/project_add')
    config.add_route('project_add_milestones', '/project_add_milestones/{id}')
    config.add_route('project_change_identifier', '/project_change_identifier/{id}')
    config.add_route('update_fiona_projects', '/update_fiona_projects')

    # Add Static Resources
    config.add_static_view(
        'static',
        'static',
        cache_max_age=3600)
    config.add_static_view(
        'deform_static',
        'deform:static/',
        #cache_max_age=3600
    )

    # Scan subfolder
    config.scan('.browser')

    return config.make_wsgi_app()
