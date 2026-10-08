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
from typing import Dict, Optional

from django.utils.translation import gettext as _

from backend.flow.engine.bamboo.scene.common.builder import Builder
from backend.flow.plugins.components.collections.mysql.fake_log import FakeLogComponent


class MySQLFakeLogFlow(object):
    """
    日志测试专用流程，不执行远程命令，仅验证流程节点日志。
    """

    def __init__(self, root_id: str, data: Optional[Dict]):
        self.root_id = root_id
        self.data = data or {}

    def _build_kwargs(self, stage: str, log_count: int, sleep_seconds: float) -> Dict:
        return {
            "uid": self.data.get("uid"),
            "root_id": self.root_id,
            "stage": stage,
            "log_count": log_count,
            "sleep_seconds": sleep_seconds,
        }

    def fake_log_flow(self):
        params = self.data.get("params") or {}
        log_count = params.get("log_count", 10)
        sleep_seconds = params.get("sleep_seconds", 0.1)
        stages = params.get("stages") or [_("前置日志"), _("核心日志"), _("收尾日志")]
        parallel_stages = params.get("parallel_stages") or [_("并行日志-A"), _("并行日志-B")]

        pipeline = Builder(root_id=self.root_id, data=self.data)
        pipeline.add_act(
            act_name=_("日志测试-开始"),
            act_component_code=FakeLogComponent.code,
            kwargs=self._build_kwargs(stage=_("开始"), log_count=log_count, sleep_seconds=sleep_seconds),
        )
        for stage in stages:
            pipeline.add_act(
                act_name=_("日志测试-{}").format(stage),
                act_component_code=FakeLogComponent.code,
                kwargs=self._build_kwargs(stage=stage, log_count=log_count, sleep_seconds=sleep_seconds),
            )

        pipeline.add_parallel_acts(
            acts_list=[
                {
                    "act_name": _("日志测试-{}").format(stage),
                    "act_component_code": FakeLogComponent.code,
                    "kwargs": self._build_kwargs(stage=stage, log_count=log_count, sleep_seconds=sleep_seconds),
                }
                for stage in parallel_stages
            ]
        )
        pipeline.add_act(
            act_name=_("日志测试-结束"),
            act_component_code=FakeLogComponent.code,
            kwargs=self._build_kwargs(stage=_("结束"), log_count=log_count, sleep_seconds=sleep_seconds),
        )
        pipeline.run_pipeline()
