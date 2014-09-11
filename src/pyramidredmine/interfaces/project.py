# -*- coding: utf-8 -*-

from zope.interface import Interface

import colander
import deform.widget

class IRedmineProject(colander.MappingSchema, Interface):
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
            values=redmine_config.base_projects
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
            values=redmine_config.statuss,
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
            size=5,
            ),
        missing=colander.drop,
        )
