#-*- coding: utf-8 -*-
#  Copyright (c) 2010 Franz Allan Valencia See
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from console import console
from roomter import roomter
from sub_process import sub_process
from tools import tools
from strip_ogg import strip_ogg
from switch_stream_Worker import switch_stream_Worker

__version__ = '0.1'

class test_tool(console,roomter,sub_process,tools,strip_ogg,switch_stream_Worker):
	"""audio自动化测试库"""
	ROBOT_LIBRARY_SCOPE = 'GLOBAL'
