<script setup>
import { inject, nextTick, onMounted, ref } from 'vue'

const mobile = inject('mobile')
const axios = inject('axios')

const sss_url = `${import.meta.env.VITE_HTTP_URL}/sss-copilot`

const sss_data = ref({ exists: false })

onMounted(async () => {
  const { data } = await axios.get(sss_url)
  sss_data.value = data
})

function import_sss({ event }) {
  sss_data.value = JSON.parse(event.target.response)
}

const token = inject('token')

const maa_code_input = ref(false)
const maa_code = ref('')
const loading = ref(false)
const code = ref(null)

function start_input() {
  maa_code.value = ''
  maa_code_input.value = true
  nextTick(() => code.value.focus())
}

async function download_maa_copilot() {
  loading.value = true
  const number = maa_code.value.replace('maa://', '')
  const { data } = await axios.get(`https://prts.maa.plus/copilot/get/${number}`, {
    transformRequest: [
      (data, headers) => {
        delete headers.token
        return JSON.stringify(data)
      }
    ]
  })
  const form_data = new FormData()
  form_data.append('copilot', new Blob([data.data.content], { type: 'application/json' }))
  const response = await axios.post(sss_url, form_data)
  sss_data.value = response.data
  maa_code_input.value = false
  loading.value = false
}
</script>

<template>
  <n-form
    :label-placement="mobile ? 'top' : 'left'"
    :show-feedback="false"
    label-width="72"
    label-align="left"
  >
    <n-form-item label="导入作业">
      <div class="sss-container">
        <template v-if="maa_code_input">
          <n-input
            ref="code"
            v-model:value="maa_code"
            type="text"
            placeholder="maa://114514"
            :disabled="loading"
          />
          <n-button @click="download_maa_copilot" :loading="loading" :disabled="loading">
            下载
          </n-button>
          <n-button @click="maa_code_input = false">取消</n-button>
        </template>
        <template v-else>
          <n-button style="flex-grow: 1" @click="start_input">输入“神秘代码”</n-button>
          <n-upload
            style="width: auto; flex-grow: 1"
            trigger-style="width: 100%"
            :action="sss_url"
            :headers="{ token: token }"
            :show-file-list="false"
            name="copilot"
            @finish="import_sss"
          >
            <n-button style="width: 100%">选择作业文件</n-button>
          </n-upload>
        </template>
      </div>
    </n-form-item>
    <n-form-item label="作业信息">
      <n-flex vertical>
        <div class="wrapper" v-if="sss_data.exists">
          <div class="title">{{ sss_data.title }}</div>
          <div>{{ sss_data.details }}</div>
        </div>
        <div v-else>未选择作业</div>
        <n-flex v-for="o in sss_data.operators" align="center">
          <n-avatar :src="`avatar/${o.name}.webp`" />
          <div>{{ o.name }}（{{ o.skill }}技能）</div>
        </n-flex>
      </n-flex>
    </n-form-item>
  </n-form>
</template>

<style scoped>
.sss-container {
  display: flex;
  width: 100%;
  gap: 8px;
}

.wrapper {
  white-space: pre-wrap;
  user-select: text;
}

.title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 6px;
}
</style>
