# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 UnitedStack Inc.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


def get_test_lookup_value(**kw):
    lookup_values = {
        'id': kw.get('id', 3),
        'match': kw.get('match', 'fqdn=abc.ustack.com'),
        'value': kw.get('value', 'abcde'),
        'lookup_key_id': kw.get('lookup_key_id', 2018),
        'created_at': None,
        'updated_at': None,
    }
    return lookup_values
