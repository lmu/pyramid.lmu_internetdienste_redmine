# -*- coding: utf-8 -*-

import colander
import deform.widget

#from zope.interface import Interface

#from pyramid.url import resource_url

from ..config import __redmine_config as redmine_config


class IRedmineWebProject(colander.MappingSchema):
    name = colander.SchemaNode(
        colander.String(),
        title="Projekt Titel:",
        missing=colander.required,
    )

    identifier = colander.SchemaNode(
        colander.String(),
        title="Projekt Name (Fiona Name):",
        missing=colander.required,
    )

    description = colander.SchemaNode(
        colander.String(),
        title="Beschreibung des Projekts:",
        required=False,
        widget=deform.widget.TextAreaWidget(),
        missing=colander.drop,
    )

    parent = colander.SchemaNode(
        colander.String(),
        title="Unterprojekt von:",
        widget=deform.widget.SelectWidget(
            values=redmine_config.fiona_base_projects
        )
    )

    homepage = colander.SchemaNode(
        colander.String(),
        title="Ziel Domain:",
        missing=colander.drop,
    )

    status = colander.SchemaNode(
        colander.String(),
        title="Status des Webauftritts:",
        default="offline",
        widget=deform.widget.RadioChoiceWidget(
            values=redmine_config.project_statuss,
        ),
        missing=colander.drop,
    )

    lang = colander.SchemaNode(
        colander.List(),
        title="Sprache des Webauftritts:",
        widget=deform.widget.SelectWidget(
            values=redmine_config.langs,
            multiple=True,
            default='de',
            size=2,
        ),
        missing=colander.drop,
    )


class ITicketSchema(colander.MappingSchema):

    activate = colander.SchemaNode(
        colander.Boolean(),
        title='Activate Ticket',
        default=True,
    )

    status = colander.SchemaNode(
        colander.List(),
        title="Start Status",
        widget=deform.widget.SelectWidget(
            values=redmine_config.ticket_statuss,
            multiple=False,
            default='1',
        ),
        missing=colander.drop,
    )


class IRedmineMilestoneProject(colander.MappingSchema):

    project = colander.SchemaNode(
        colander.String(),
        title="Projekt:",
        widget=deform.widget.SelectWidget(
            values=redmine_config.all_projects,
            multiple=True,
            readonly=False,
        )
    )

    milestone_01_playlandphase = colander.SchemaNode(
        colander.Boolean(),
        title='Füge Meilenstein "01. Playlandphase" hinzu',
        default=True,
    )

    milestone_02_onlinegang = colander.SchemaNode(
        colander.Boolean(),
        title='Füge Meilenstein "02. Onlinegang" hinzu',
        default=True,
    )

    milestone_03_webseitenpflege = colander.SchemaNode(
        colander.Boolean(),
        title='Füge Meilenstein "03. Webseitenpflege" hinzu',
        default=True,
    )

    milestone_04_relaunch = colander.SchemaNode(
        colander.Boolean(),
        title='Füge Meilenstein "04. Relaunch" hinzu',
        default=False,
    )

    milestone_99_eol = colander.SchemaNode(
        colander.Boolean(),
        title='Füge Meilenstein "99. End of Life Cycle" hinzu',
        default=False,
    )


class MemoryTmpStore(dict):
    """ Instances of this class implement the
    :class:`deform.interfaces.FileUploadTempStore` interface"""
    def preview_url(self, uid):
        return None

tmpstore = MemoryTmpStore()


class IRedmineFionaUpdateProjects(colander.MappingSchema):
    csv_file = colander.SchemaNode(
        deform.FileData(),
        title="Upload eines Fiona Projekt Dumps",
        description="""Bitte laden Sie einen Projekt Dump aus Fiona hoch,
diese Datei enthält eine Comma Separated Value Set von Fiona Name, Pfad, ...;
Die erste Zeile enthält die Zeilenüberschriften.""",
        widget=deform.widget.FileUploadWidget(tmpstore)
    )
