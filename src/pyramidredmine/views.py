# -*- coding: utf-8 -*-

import colander
import deform.widget

import ipdb

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from redmine import Redmine
from redmine.exceptions import ResourceNotFoundError
from redmine.exceptions import ResourceAttrError
from redmine.exceptions import ValidationError

redmine = Redmine('https://www.scm.verwaltung.uni-muenchen.de/spielwiese/', username='admin', password='admin')

class RedmineConfig(object):

    def __init__(self):
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

redmine_config = RedmineConfig()

class RedmineProjectView(object):

    def __init__(self, request):
        self.request = request


    @property
    def redmineproject_form(self):
        schema = RedmineProject()
        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.redmineproject_form.get_widget_resources()

    @view_config(route_name='projects_view', renderer='templates/projects_view.pt')
    def redmineproject_view(self):
        return dict(projects=redmine.project.all())   

    @view_config(route_name='project_add',
                 renderer='templates/project_add.pt')
    def project_add(self):
        form = self.redmineproject_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.redmineproject_form.validate(controls)
            except deform.ValidationFailure as e:
                # Form is NOT valid
                return dict(form=e.render())


            project = setup_webproject(project_name=appstruct['name'],
                             project_identifier=appstruct['identifier'],
                             project_parent_id=int(appstruct['parent']),
                             project_description=appstruct.get('description',''),
                             project_homepage=appstruct.get('homepage',''),
                             project_status=appstruct.get('status','') ,
                             project_lang=appstruct.get('lang',''),      
                )
           
            return HTTPFound(project.url)

        return dict(form=form)

    @view_config(route_name='project_view', renderer='templates/project_view.pt')
    def projectpage_view(self):
        id = self.request.matchdict['id']
        project = redmine.project.get(id)
        import ipdb; ipdb.set_trace()
        return dict(project=project)

    