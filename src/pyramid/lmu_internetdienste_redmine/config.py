# -*- coding: utf-8 -*-

import logging

from redmine import Redmine
from redmine.exceptions import AuthError
from redmine.exceptions import ResourceNotFoundError
from redmine.exceptions import ResourceAttrError
from redmine.exceptions import ValidationError

#default_redmine_location='https://www.scm.verwaltung.uni-muenchen.de/spielwiese/' # NOQA
default_redmine_location = 'http://localhost/spielwiese/'
default_username = 'admin'
default_password = 'admin'

MAIN_MENU = [
    {'href': '', 'title': 'Home'},
]






#master_webproject = 'webprojekte'
master_webproject = 'webauftritte'

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
                password=password)
        else:
            self.redmine = Redmine()

    def base_config(self):
        self.master_project = self.redmine.project.get(master_webproject)

        custom_fields = self.redmine.custom_field.all()
        #projects custom fields
        self.cf_lang_id = None
        self.cf_status_id = None

        self.statuss = [('online', 'online'), ('offline', 'offline')]
        self.langs = [('de', 'de'), ('en', 'en')]

        for cf in custom_fields:
            if cf.name == "Sprache":
                self.cf_lang_id = cf.id
                self.langs = [(lang['value'], lang['value']) for lang in cf.possible_values ]
            elif cf.name == "Status" and cf.customized_type == "project":
                self.cf_status_id = cf.id
                self.statuss = [(lang['value'], lang['value']) for lang in cf.possible_values ]

        self.task_id = 1
        trackers = self.redmine.tracker.all()
        for tracker in trackers:
            if tracker.name == "Task":
                self.task_id = tracker.id

        self.fiona_base_projects = []
        all_projects = self.redmine.project.all()
        for project in all_projects:
            try:
                if project.parent is not None and \
                        project.parent.id == self.master_project.id:
                    self.fiona_base_projects.append(
                        (project.id, u"{identifier}: {name}".format(
                            identifier=project.identifier,
                            name=project.name)))
            except ResourceNotFoundError as e:
                logger.error(e)
            except ResourceAttrError as e:
                logger.error(e)
        return self


__redmine_config_object = RedmineConfig()

__redmine = __redmine_config_object.redmine
__redmine_config = __redmine_config_object.base_config()
