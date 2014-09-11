# -*- coding: utf-8 -*-

from .config import default_redmine_location
from .config import default_username
from .config import default_password
from .config import master_project

from redmine import Redmine
from redmine.exceptions import ResourceNotFoundError
from redmine.exceptions import ResourceAttrError
from redmine.exceptions import ValidationError

class RedmineConfig(object):

    def __init__(self, 
                 location=default_redmine_location,
                 username=default_username,
                 password=default_password,
                 apikey=None,
                 impersonate=None,
                ):
        if apikey != None and impersonate != None:
            self.redmine = Redmine(location, key=apikey, impersonate=impersonate)
        elif apikey != None and impersonate == None:
            self.redmine = Redmine(location, key=apikey)
        elif apikey == None and username != None and username != '' and password != None and password != '' and impersonate != None:
            self.redmine = Redmine(location, username=username, password=password, impersonate=impersonate)
        elif apikey == None and username != None and username != '' and password != None and password != '' and impersonate == None:
            self.redmine = Redmine(location, username=username, password=password)
        else:
            self.redmine = Redmine()

    def base_config(self):
            #master-Project
        master_project_id = 'webprojekte'
        self.master_project = redmine.project.get(master_project_id)

        custom_fields = redmine.custom_field.all()
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
        trackers = redmine.tracker.all()
        for tracker in trackers:
            if tracker.name == "Task":
                self.task_id = tracker.id

        self.base_projects = []
        all_projects = redmine.project.all()
        for project in all_projects:
            try:
                if project.parent != None and project.parent.id == self.master_project.id:
                    self.base_projects.append((project.id,u"{identifier}: {name}".format(identifier=project.identifier, name=project.name)))
            except ResourceNotFoundError, e:
                pass
            except ResourceAttrError, e:
                pass

redmine_config_object = RedmineConfig()

redmine = redmine_config_object.redmine
redmine_config = redmine_config_object.base_config()

class PyramidRedmineUtils(object):


    def setup_webproject(self,
                         project_name,
                         project_identifier,
                         project_parent_id,
                         project_description='',
                         project_homepage='',
                         project_status='',
                         project_lang='',
                         project_is_public=False,
                         project_inherit_members=True,
        ):
        try: 
            project = redmine.project.create(
                name=project_name, 
                identifier=project_identifier, 
                description=project_description,
                homepage=project_homepage,
                is_public=project_is_public, 
                inherit_members=project_inherit_members, 
                parent_id=int(project_parent_id),
                # Custom Fields
                custom_fields  = [
                    { 'id': redmine_config.cf_status_id, 'value' : project_status },
                    { 'id': redmine_config.cf_lang_id,   'value' : project_lang }
                ], 
                                                        
                )
            self.add_milestone_initialgespraech(project)
            self.add_milestone_playlanduenbergabe(project)
            self.add_milestone_onlinegang(project)
            self.add_milestone_initialgespraech(project)
            self.add_milestone_initialgespraech(project)
            self.add_milestone_pflege
            self.add_milestone_endoflive(project)

            return project


    def add_milestone_initialgespraech(self, project):            
        milestone = redmine.version.create(
            project_id=project.id,
            name=u"01. Initialgespräch",
            description=u"",
            )
        redmine.issue.create(
            project_id=project.id,
            subject="Termin Initialgespräch",
            tracker_id=redmine_config.task_id,
            description="""Termine für Kundengespräch""",
            fixed_version_id=milestone.id,
            )
        redmine.issue.create(
            project_id=project.id,
            subject="Strukturplan anfordern und analysieren",
            tracker_id=redmine_config.task_id,
            description="""Strukturplan zur Gesprächsvorbereitung""",
            fixed_version_id=milestone.id,
            )

    def add_milestone_playlanduenbergabe(self, project):  
        milestone = redmine.version.create(
            project_id=project.id,
            name=u"02. Playlandübergabe",
            description=u"",
            )
        redmine.issue.create(
            project_id=project.id,
            subject="Anpassung Playland",
            tracker_id=redmine_config.task_id,
            description="""

            """,
            fixed_version_id=milestone.id,
            )

    def add_milestone_onlinegang(self, project):
        milestone_onlinegang = redmine.version.create(
            project_id=project.id,
            name=u"03. Onlinegang",
            description=u"",
            )


    def add_milestone_pflege(self, project):
        milestone_pflege = redmine.version.create(
            project_id=project.id,
            name=u"04. Webseitenpflege",
            description=u"Eingehende Kundenanspassungswünsche und Support aka Maintenance.",
            )


    def add_milestone_qs(self, project):
        milestone_qs = redmine.version.create(
            project_id=project.id,
            name=u"05. QS / Relaunch",
            description=u"QS nach Onlinegang, bzw. Relaunch.",
            )


    def add_milestone_veranstaltungen(self, project):
        milestone_veranstaltungen = redmine.version.create(
            project_id=project.id,
            name=u"06. Veranstaltungen",
            description=u"Workshops, Thementage usw.",
            )


    def add_milestone_endoflive(self, project):
        milestone_endoflive = redmine.version.create(
            project_id=project.id,
            name=u"99. End of Lifecycle",
            description=u"",
            status='locked',
            )



        # Issues

        issue_kopfbild = redmine.issue.create(
            project_id=project.id,
            subject="Kopfbild erstellen",
            tracker_id=redmine_config.task_id,
            description="""

            """,
            fixed_version_id=milestone_initailgespraech.id,
            )
        issue_qs_vor_onlinegang = redmine.issue.create(
            project_id=project.id,
            subject="QS vor Onlinegang",
            tracker_id=redmine_config.task_id,
            description="""

            """,
            fixed_version_id=milestone_onlinegang.id,
            )
        issue_qs_nach_onlinegang = redmine.issue.create(
            project_id=project.id,
            subject="QS nach Onlinegang",
            tracker_id=redmine_config.task_id,
            description="""

            """,
            fixed_version_id=milestone_onlinegang.id,
            )