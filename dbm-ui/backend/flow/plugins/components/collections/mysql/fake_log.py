# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import time

from django.utils.translation import gettext as _
from pipeline.component_framework.component import Component

from backend.flow.plugins.components.collections.common.base_service import BaseService


class FakeLogService(BaseService):
    """日志测试专用组件，不依赖外部执行对象。"""

    def _execute(self, data, parent_data, callback=None) -> bool:
        kwargs = data.get_one_of_inputs("kwargs") or {}
        stage = kwargs.get("stage", _("日志测试"))
        log_count = kwargs.get("log_count", 10)
        sleep_seconds = kwargs.get("sleep_seconds", 0.1)
        ticket_id = kwargs.get("uid")
        root_id = kwargs.get("root_id")

        self.log_info(
            _("[日志测试] 开始执行，ticket_id={}，root_id={}，stage={}，log_count={}").format(ticket_id, root_id, stage, log_count)
        )
        for index in range(1, log_count + 1):
            self.log_info(
                _("[日志测试] ticket_id={}，root_id={}，stage={}，step={}/{}").format(
                    ticket_id, root_id, stage, index, log_count
                )
            )
            if sleep_seconds:
                time.sleep(sleep_seconds)

        self.log_info(_("[日志测试] 执行完成，stage={}").format(stage))
        return True


class FakeLogComponent(Component):
    name = __name__
    code = "fake_log"
    bound_service = FakeLogService
