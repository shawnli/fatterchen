#!/usr/bin/env python
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
import sys

from setuptools import setup

version = sys.version_info
PY2 = version[0] == 2
PY3 = version[0] == 3

if PY2 and version[:2] < (2, 6):
    raise Exception('pyodps supports python 2.6+ (including python 3+).')

requirements = []
with open('requirements.txt') as f:
    requirements.extend(f.read().splitlines())


long_description = None
if os.path.exists('README.md'):
    with open('README.md') as f:
        long_description = f.read()

setup(name='AliX',
      version='0.0.1',
      long_description=long_description,
      license='Apache License 2.0',
      install_requires=requirements,
      )
