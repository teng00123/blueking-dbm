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
# 此单据用于测试流程日志，不依赖远程执行对象

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from backend.flow.engine.controller.mysql import MySQLController
from backend.ticket import builders
from backend.ticket.builders.mysql.base import BaseMySQLTicketFlowBuilder
from backend.ticket.constants import TicketType


class MySQLFakeLogParamsSerializer(serializers.Serializer):
    log_count = serializers.IntegerField(
        help_text=_("单节点日志条数"), required=False, default=10, min_value=1, max_value=20000
    )
    sleep_seconds = serializers.FloatField(
        help_text=_("每条日志间隔秒数"), required=False, default=0.1, min_value=0, max_value=5
    )
    stages = serializers.ListField(
        help_text=_("串行日志阶段"),
        child=serializers.CharField(),
        required=False,
        default=list,
        allow_empty=True,
    )
    parallel_stages = serializers.ListField(
        help_text=_("并行日志阶段"),
        child=serializers.CharField(),
        required=False,
        default=list,
        allow_empty=True,
    )


class MySQLFakeLogDetailSerializer(serializers.Serializer):
    params = MySQLFakeLogParamsSerializer(help_text=_("日志测试参数"), required=False, default=dict)


class MySQLFakeLogFlowParamBuilder(builders.FlowParamBuilder):
    """日志测试单据参数"""

    controller = MySQLController.mysql_fake_log_scene


@builders.BuilderFactory.register(TicketType.FAKE_LOG_TICKET)
class MySQLFakeLogFlowBuilder(BaseMySQLTicketFlowBuilder):
    serializer = MySQLFakeLogDetailSerializer
    inner_flow_builder = MySQLFakeLogFlowParamBuilder
    inner_flow_name = "Fake Log Test"

    @property
    def need_itsm(self):
        return False

    @property
    def need_manual_confirm(self):
        return False
