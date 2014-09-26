# -*- coding: utf-8 -*-

import csv
import datetime

from redmine import Redmine
from redmine.exceptions import AuthError
from redmine.exceptions import ResourceNotFoundError
#from redmine.exceptions import ResourceAttrError
from redmine.exceptions import ValidationError

from .config import __redmine
#from .config import default_username
#from .config import default_password

from .config import logger
from .config import __redmine_config as redmine_config

import ipdb


def auth_user(username,
              password,
              redmine=__redmine,
              url=None,
              verify_ssl_certs=False):
    user = None
    try:
        if url is not None:
            user = Redmine(
                url,
                username=username,
                password=password,
                requests={'verify': False} if not verify_ssl_certs else {},
            ).auth()
        else:
            user = Redmine(
                redmine.url,
                username=username,
                password=password,
                requests={'verify': False} if not verify_ssl_certs else {},
            ).auth()
    except AuthError:
        raise Exception('Invalid login or password provided')
    return user


def get_all_contacts(project_id=0, redmine=__redmine):
    _all_contacts = []
    if project_id == 0:
        _all_contacts = redmine.contact.all()
    elif project_id > 0:
        _all_contacts = redmine.contact.all(project_id=project_id)
    all_contacts = {}
    for contact in _all_contacts:
        fields = contact.custom_fields
        ck = 'keine_'+contact.last_name.lower()
        for field in fields:
            if field.name == 'Campus-Kennung':
                ck = field.value.strip().lower()
        logger.debug("add {user} to all_contacts".format(user=ck))
        all_contacts[ck] = contact


def setup_webproject(project_name,
                     project_identifier,
                     project_parent_id,
                     project_description='',
                     project_homepage='',
                     project_status='',
                     project_lang='',
                     project_is_public=False,
                     project_inherit_members=True,
                     redmine=__redmine):
    project = None
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
            custom_fields=[
                {'id': redmine_config.cf_status_id, 'value': project_status},
                {'id': redmine_config.cf_lang_id, 'value': project_lang}
            ])
    except:
        logger.error("Project already seems to exist")
        pass
    return project


def add_milestone_initialgespraech(self, project, redmine=__redmine):
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
        subject=u"Strukturplan anfordern und analysieren",
        tracker_id=redmine_config.task_id,
        description=u"""
Strukturplan zur Gesprächsvorbereitung
""",
        fixed_version_id=milestone.id,
    )


def add_milestone_playlanduenbergabe(project, redmine=__redmine):
    milestone = redmine.version.create(
        project_id=project.id,
        name=u"02. Playlandübergabe",
        description=u"""
""",
    )

    redmine.issue.create(
        project_id=project.id,
        subject=u"Anpassung Playland",
        tracker_id=redmine_config.task_id,
        description=u"""

        """,
        fixed_version_id=milestone.id,
    )


def add_milestone_onlinegang(project, redmine=__redmine):
    milestone_onlinegang = redmine.version.create(
        project_id=project.id,
        name=u"03. Onlinegang",
        description=u"""
""",
    )

    redmine.issue.create(
        project_id=project.id,
        subject=u""
    )


def add_milestone_pflege(self, project):
    milestone_pflege = redmine.version.create(
        project_id=project.id,
        name=u"04. Webseitenpflege",
        description=u"""
Eingehende Kundenanspassungswünsche und Support aka Maintenance.
""",
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


def update_redmine_projects_with_fiona_dump(csv_file,
                                            redmine=__redmine):

    cf_lang_id = redmine_config.cf_lang_id
    cf_status_id = redmine_config.cf_status_id

    reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')

    #Fiona-Name;Fiona-Pfad;Playland-Titel;Erstellungsdatum;Status;URL;Sprache;Fionagruppe; # NOQA

    project = 0
    rmaster_project = redmine_config.master_project

    for row in reader:

        fiona_id = row.get('Fiona-Name')

        logger.info("Write Project: " + fiona_id)

        path = row.get('Fiona-Pfad')
        fiona_title = row.get('Playland-Titel')
        url = row.get('URL')
        # Custom Fields
        status = row.get('Status')
        lang = row.get('Sprache')

        path_list = path.split('/')
        try:
            try:
                myproject = redmine.project.get(fiona_id)
                redmine.project.update(myproject.id,
                                       name=fiona_title,
                                       homepage=url,
                                       is_public=False,
                                       inherit_members=True,
                                       # Custom Fields
                                       custom_fields=[
                                           {'id': cf_status_id,
                                            'value': row.get('Status', '')},
                                           {'id': cf_lang_id,
                                            'value': row.get('Sprache', '')}
                                       ])
            except ResourceNotFoundError, e:
                if len(path_list) == 2:
                    project = redmine.project.create(name=fiona_title,
                                                     identifier=fiona_id,
                                                     homepage=url,
                                                     is_public=False,
                                                     inherit_members=True,
                                                     parent_id=rmaster_project.id,
                                                     # Custom Fields
                                                     custom_fields=[
                                                         {'id': cf_status_id,
                                                          'value' : row.get('Status', '')},
                                                         {'id': cf_lang_id,
                                                          'value' : row.get('Sprache', '')}
                                                     ],
                                                    )
                elif len(path_list) == 3:
                    parent_project = redmine.project.get(path_list[1])
                    redmine.project.create(name=fiona_title,
                                           identifier=fiona_id,
                                           homepage=url,
                                           is_public=False,
                                           inherit_members=True,
                                           parent_id=parent_project.id,
                                           # Custom Fields
                                           custom_fields=[
                                               {'id': cf_status_id,
                                                'value' : row.get('Status', '')},
                                               {'id': cf_lang_id,
                                                'value' : row.get('Sprache', '')}
                                           ])

        except ValidationError, e:
            logger.error(
                "Error on {id} with error: {message}",
                id=fiona_id,
                message=e.message)

    # Update Projects withj Contact information
    csv_file.reset()
    reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')

    ipdb.set_trace()

    all_contacts = get_all_contacts()
    error_store = {}

    #Fiona-Name;Fiona-Pfad;Playland-Titel;Erstellungsdatum;Status;URL;Sprache;Fionagruppe; # NOQA

    project = 0
    for row in reader:
        #import ipdb; ipdb.set_trace()
        fiona_id = row.get('Fiona-Name')
        user_data = row.get('Fionagruppe')

        logger.info("update Project: " + fiona_id)

        if user_data is not None:
            try:
                project = redmine.project.get(fiona_id)
                content = """
h1. Fionagruppen


"""

                groups = user_data.split('#')

                for group in groups:
                    if group != '':
                        group_data = group.split(':')
                        group_name = group_data[0]
                        user_ids = group_data[1].split(' ')

                        content += "\n\nh2. " + group_name + "\n\n"
                        for user in user_ids:
                            #contact = redmine.contact.get()
                            if user != '':
                                contact = all_contacts.get(user.lower())

                                if contact is not None:

                                    content += "* {{contact(%s)}}: %s \n" % (contact.id, user)
                                else:
                                    content += "* " + user + "\n"
                                    error_message = error_store.get(user, {})
                                    e_webauftritt = error_message.get('Webauftritt', [])
                                    e_webauftritt.append(project.identifier)
                                    e_group = error_message.get('Group', [])
                                    e_group.append(group_name)

                                    error_store[user] = {'Webauftritt': e_webauftritt, 'Group': e_group}

                try:
                    page = redmine.wiki_page.get(
                        'Fionagruppen',
                        project_id=project.id)
                    redmine.wiki_page.update('Fionagruppen',
                                             project_id=project.id,
                                             title='Fionagruppen',
                                             text=content)
                except ResourceNotFoundError, e:
                    redmine.wiki_page.create(project_id=project.id,
                                             title='Fionagruppen',
                                             text=content)

            except ValidationError, e:
                logger.error(
                    "Error on {id} with error: {message}",
                    id=fiona_id,
                    message=e.message)
            except ResourceNotFoundError, e:
                pass
    if error_store:
        error_message = """Folgende User sind unbekannt:

|_.Campus-Kennung |_.Fionagruppen |_.Projekte |
"""
        for message in error_store:
            error_message += '| {ck} | {groups} | {projects} |\n'.format(
                ck=message,
                groups=', '.join(set(error_store[message]['Group'])),
                projects=', '.join(set(error_store[message]['Webauftritt'])))

        redmine.issue.create(
            project_id=rmaster_project.id,
            subject="Unbekannte Nutzer bei Import " +
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            description=error_message
        )
