# Copyright 2017 BlueCat Networks (USA) Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# By: BlueCat Networks
# Date: 05-12-17
# Gateway Version: 17.10.1
# Description: Example Gateway workflows

from wtforms import SubmitField
from bluecat.wtform_fields import Configuration, View, Zone, CustomStringField, CustomSearchButtonField, \
    FilteredSelectField, PlainHTML
from bluecat.wtform_extensions import GatewayForm
from bluecat.server_endpoints import get_text_records_endpoint


class GenericFormTemplate(GatewayForm):
    # When updating the form, remember to make the corresponding changes to the workflow pages
    workflow_name = 'delete_text_record_example'
    workflow_permission = 'delete_text_record_example_page'
    configuration = Configuration(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        label='Configuration',
        required=True,
        coerce=int,
        validators=[],
        is_disabled_on_start=False,
        on_complete=['call_view'],
        enable_on_complete=['view']
    )

    view = View(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        label='View',
        required=True,
        one_off=True,
        on_complete=[],
        enable_on_complete=['parent_zone']
    )

    parent_zone = Zone(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        label='Zone',
        required=True,
        start_initialized=True,
        inputs={'zone': 'parent_zone', 'configuration': 'configuration', 'view': 'view'},
        enable_on_complete=['text_record', 'search']
    )

    text_record = CustomStringField(
        label='Text Record',
        required=True
    )

    search = CustomSearchButtonField(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        default='Search',
        inputs={
            'configuration': 'configuration',
            'view': 'view',
            'parent_zone': 'parent_zone',
            'name': 'text_record'
        },
        server_side_method=get_text_records_endpoint,
        message_field='search_message',
        on_click=['populate_txt_list'],
        enable_on_complete=['txt_filter', 'txt_list']
    )

    plain_0 = PlainHTML('<div id="search_message"></div>')

    txt_filter = CustomStringField(
        label='Filter',
        is_disabled_on_error=True
    )

    txt_list = FilteredSelectField(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        filter_field='txt_filter',
        choices=[(0, '')],
        coerce=int,
        is_disabled_on_error=True,
        enable_on_complete=['submit']
    )

    submit = SubmitField(
        label='Delete',
        render_kw={'disabled': True}
    )
