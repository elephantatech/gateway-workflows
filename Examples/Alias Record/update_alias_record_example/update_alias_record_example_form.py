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
from bluecat.wtform_fields import Configuration, View, Zone, CustomStringField, AliasRecord, get_alias_records_endpoint
from bluecat.wtform_extensions import GatewayForm


class GenericFormTemplate(GatewayForm):
    # When updating the form, remember to make the corresponding changes to the workflow pages
    workflow_name = 'update_alias_record_example'
    workflow_permission = 'update_alias_record_example_page'
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
        on_complete=['call_zone', 'call_linked_record_zone'],
        enable_on_complete=['zone']
    )

    zone = Zone(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        label='Zone',
        required=True,
        enable_on_complete=['alias_record']
    )

    alias_record = AliasRecord(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        label='Alias Record',
        required=True,
        inputs={'configuration': 'configuration', 'view': 'view', 'zone': 'zone', 'alias_record': 'alias_record'},
        server_outputs={'alias_record_name': 'alias_name', 'linked_record_zone': 'linked_record_zone',
                        'linked_record_name': 'linked_record'},
        server_side_output_method=get_alias_records_endpoint,
        on_complete=['server_output_alias_record'],
        enable_on_complete=['alias_name', 'linked_record_zone', 'linked_record', 'submit']
    )

    alias_name = CustomStringField(
        label='New Alias Name',
        required=True
    )

    linked_record_zone = Zone(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        label='Linked Record Zone',
        required=True,
        inputs={'configuration': 'configuration', 'view': 'view', 'zone': 'linked_record_zone'},
        clear_below_on_change=False
    )

    linked_record = CustomStringField(
        label='Linked Record',
        required=True
    )

    submit = SubmitField(label='Update')
