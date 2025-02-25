from django.http import HttpResponse
from django.urls import path

from part.models import PartCategoryParameterTemplate, PartParameter

from plugin import InvenTreePlugin
from plugin.mixins import UrlsMixin, SettingsMixin

import sys

from .version import PLUGIN_VERSION
class TemplateFixPlugin(InvenTreePlugin, SettingsMixin, UrlsMixin):
    NAME = "TemplateFixPlugin"
    SLUG = "templatefix"
    TITLE = "Template Fix"
    AUTHOR = "Jordan Bush"
    PUBLISH_DATE = "2025-02-24:00:00"
    VERSION = PLUGIN_VERSION
    SETTINGS = {}

    def get_settings_content(self, request):
        print(sys.modules[TemplateFixPlugin.__module__])
        return """
        <h1>Template Fix Plugin</h1>
        <p>This plugin is designed to retroactively apply parameters to Parts that were added before a category template was created.</p>
        <strong>To use this plugin:</strong><p>Click the button below and allow the script to run. It may take a while.</p>
        <a class="btn btn-dark" onclick="window.open('/plugin/templatefix/fix/','name','width=1000px,height=800px')"">
         Attempt to apply templates
        </a>
        """

    def run_category(self, template, category):
        parts = category.parts.all()
        # For each part, check if it has parameters
        for part in parts:
            # Check if the part already has the specified parameter
            if not PartParameter.objects.filter(part=part, template=template.parameter_template).exists():
                print(f"Part: {part} does not have parameter: {template.parameter_template}")
                # If it doesn't, add the parameter
                PartParameter.create(
                    part=part,
                    template=template.parameter_template,
                    data=template.default_value,
                    save=True,
                )
                print(f"Added parameter: {template.parameter_template} to part: {part}")

    def fix_templates(self, request):
        print("Attempting to fix templates")
        # Pull down a list of all PartCategoryParameterTemplates
        templates = PartCategoryParameterTemplate.objects.all()
        # For each template, find any parts that meet the category
        for template in templates:
            print(f"Checking template: {template.parameter_template.name} - Default data {template.default_value}")
            parent_category = template.category
            # check for children categories
            categories = parent_category.get_descendants(include_self=True)
            for category in categories:
                self.run_category(template, category)

        return HttpResponse("Template Values applied - See server logs for more details.")

    def setup_urls(self):
        return [
            path('fix/', self.fix_templates, name='fix_templates'),
        ]
