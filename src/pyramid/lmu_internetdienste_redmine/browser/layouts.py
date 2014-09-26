from pyramid.renderers import get_renderer
from pyramid.decorator import reify

from ..config import MAIN_MENU


class Layouts(object):

    @reify
    def global_template(self):
        renderer = get_renderer("templates/main_template.pt")
        return renderer.implementation().macros['layout']

    @reify
    def global_macros(self):
        renderer = get_renderer("templates/macros.pt")
        return renderer.implementation().macros

    @reify
    def site_menu(self):
        new_menu = MAIN_MENU[:]
        url = self.request.url
        for menu in new_menu:
            if menu['title'] == 'Home':
                menu['current'] = url.endswith('/')
            else:
                menu['current'] = url.endswith(menu['href'])
        return new_menu
