<!--
 * TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
 *
 * Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
 *
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License athttps://opensource.org/licenses/MIT
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
 * the specific language governing permissions and limitations under the License.
-->

<template>
  <BkFormItem
    :label="t('脚本来源')"
    required>
    <BkRadioGroup
      v-model="importMode"
      class="mb-8"
      @change="handleImportModeChange">
      <BkRadioButton
        label="manual"
        style="width: 140px">
        {{ t('手动输入') }}
      </BkRadioButton>
      <BkRadioButton
        label="file"
        style="width: 140px">
        {{ t('脚本文件') }}
      </BkRadioButton>
    </BkRadioGroup>
    <KeepAlive>
      <Component
        :is="renderCom"
        ref="fileRef"
        v-model="modelValue"
        v-bind="attrs"
        :is-show="isShow"
        @change="handleContentChange"
        @grammar-check="handleGrammarCheck" />
    </KeepAlive>
  </BkFormItem>
</template>
<script setup lang="ts">
  import { useI18n } from 'vue-i18n';

  import type { Mongodb } from '@services/model/ticket/ticket';

  import { useTicketDetail } from '@hooks';

  import { useSqlImport } from '@stores';

  import { DBTypes, TicketTypes } from '@common/const';

  import type SqlFile from '@views/db-manage/common/model/sql-file/SqlFile';

  import LocalFile from './local-file/Index.vue';
  import ManualInput from './manual-input/Index.vue';

  interface Expose {
    getFileData: () => Record<string, SqlFile>;
    getValue: () => {
      mode: string;
      scripts: {
        content: string;
        name: string;
      }[];
    };
    setInit: (cacheData: Record<string, SqlFile>) => void;
  }

  const modelValue = defineModel<string[]>({
    default: () => [],
  });
  const importMode = defineModel<'manual' | 'file'>('importMode', {
    required: true,
  });

  const { t } = useI18n();

  const comMap = {
    file: LocalFile,
    manual: ManualInput,
  };

  const attrs = useAttrs();
  const { updateDbType, updateUploadFilePath } = useSqlImport();

  updateDbType(DBTypes.SQLSERVER); // TODO DELETE

  useTicketDetail<Mongodb.ExecScriptApply>(TicketTypes.MONGODB_EXEC_SCRIPT_APPLY, {
    onSuccess(ticketDetail) {
      updateUploadFilePath(ticketDetail.details.path);
    },
  });

  const fileRef = ref<InstanceType<typeof LocalFile>>();
  const isShow = ref(true);

  const renderCom = computed(() => comMap[importMode.value]);

  // 文件来源改变时需要重置文件列表和语法检测
  const handleImportModeChange = () => {
    modelValue.value = [];
  };

  // 内容变更处理
  const handleContentChange = (value: string[]) => {
    modelValue.value = value;
  };

  // 语法检测状态
  const handleGrammarCheck = (_doCheck: boolean, _result: boolean | string) => {
    // 保留语法检测状态，可后续扩展使用
  };

  defineExpose<Expose>({
    getFileData() {
      return fileRef.value!.getFileData();
    },
    getValue() {
      return {
        mode: importMode.value,
        scripts: fileRef.value!.getValue(),
      };
    },
    setInit(cacheData: Record<string, SqlFile>) {
      fileRef.value!.setInit(cacheData);
    },
  });
</script>
