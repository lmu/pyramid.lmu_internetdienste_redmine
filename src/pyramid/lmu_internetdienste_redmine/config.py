# -*- coding: utf-8 -*-

from redmine import Redmine
from redmine.exceptions import AuthError
from redmine.exceptions import ResourceNotFoundError
from redmine.exceptions import ResourceAttrError
from redmine.exceptions import ValidationError

<<<<<<< HEAD
default_redmine_location='https://www.scm.verwaltung.uni-muenchen.de/spielwiese/' # NOQA
#default_redmine_location = 'http://localhost/spielwiese/'
=======
import logging

# Debugging Modules
import ipdb

#default_redmine_location='https://www.scm.verwaltung.uni-muenchen.de/spielwiese/' # NOQA
default_redmine_location = 'http://localhost/spielwiese/'
>>>>>>> 39c2834b5b488b8742598a525b3ec259283e435e
default_username = 'admin'
default_password = 'admin'

MAIN_MENU = [
    {'href': '', 'title': 'Home'},
]






master_webproject = 'webprojekte'
#master_webproject = 'webauftritte'

logger = logging.getLogger('pyramid.lmu_internetdienste_redmine')


class RedmineConfig(object):

    def __init__(self,
                 location=default_redmine_location,
                 username=default_username,
                 password=default_password,
                 apikey=None,
                 impersonate=None):

        if apikey is not None and impersonate is not None:
            self.redmine = Redmine(
                location,
                key=apikey,
                impersonate=impersonate)
        elif apikey is not None and impersonate is None:
            self.redmine = Redmine(location, key=apikey)
        elif apikey is None and \
                username is not None and \
                username != '' and \
                password is not None and \
                password != '' and \
                impersonate is not None:
            self.redmine = Redmine(
                location,
                username=username,
                password=password,
                impersonate=impersonate)
        elif apikey is None and \
                username is not None and \
                username != '' and \
                password is not None and \
                password != '' and \
                impersonate is None:

            self.redmine = Redmine(
                location,
                username=username,
                password=password,
                requests={'verify': False})
        else:
            self.redmine = Redmine()

    def base_config(self):
        self.master_project = self.redmine.project.get(master_webproject)

        self.ticket_statuss = [(state['id'],state['name']) for state in self.redmine.issue_status.all()]

        custom_fields = self.redmine.custom_field.all()
        #projects custom fields
        self.cf_lang_id = None
        self.cf_status_id = None

        self.project_statuss = [('online', 'online'), ('offline', 'offline')]
        self.langs = [('de', 'de'), ('en', 'en')]

        for cf in custom_fields:
            if cf.name == "Sprache":
                self.cf_lang_id = cf.id
                self.langs = [(lang['value'], lang['value']) for lang in cf.possible_values ]
            elif cf.name == "Status" and cf.customized_type == "project":
                self.cf_status_id = cf.id
                self.project_statuss = [(lang['value'], lang['value']) for lang in cf.possible_values ]

        self.task_id = 1
        trackers = self.redmine.tracker.all()
        for tracker in trackers:
            if tracker.name == "Task":
                self.task_id = tracker.id

        self.fiona_base_projects = []
        self.all_projects = []
        all_projects = self.redmine.project.all()
        for project in all_projects:
            self.all_projects.append(
                (project.id, u"{identifier}: {name}".format(
                    identifier=project.identifier,
                    name=project.name)))
            try:
                if project.parent is not None and \
                        project.parent.id == self.master_project.id:
                    self.fiona_base_projects.append(
                        (project.id, u"{identifier}: {name}".format(
                            identifier=project.identifier,
                            name=project.name)))
            except ResourceNotFoundError as e:
                logger.debug(e)
            except ResourceAttrError as e:
                logger.debug(e)
        return self


__redmine_config_object = RedmineConfig()

__redmine = __redmine_config_object.redmine
__redmine_config = __redmine_config_object.base_config()
