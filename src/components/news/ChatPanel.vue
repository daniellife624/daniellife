<template>
  <div class="chat-panel">
    <div class="chat-panel__header">
      <div class="chat-panel__brand">
        <span class="chat-panel__d">D</span>
        <span class="chat-panel__title">會計丹尼</span>
      </div>
      <div class="chat-panel__model-wrap">
        <span class="chat-panel__provider">{{ providerLabel }}</span>
        <select v-if="availableModels.length > 1" v-model="selectedModel" class="chat-panel__model-select">
          <option v-for="m in availableModels" :key="m" :value="m">{{ m }}</option>
        </select>
        <span v-else class="chat-panel__model-name">{{ selectedModel }}</span>
      </div>
    </div>

    <div class="chat-panel__messages" ref="messagesEl">
      <div v-if="!messages.length" class="chat-panel__hint">
        詢問任何財經問題<br>例如：「幫我解釋 Fed 升息對台股的影響」
      </div>
      <div v-for="(msg, i) in messages" :key="i" class="chat-msg" :class="`chat-msg--${msg.role}`">
        <div class="chat-msg__bubble">{{ msg.content }}</div>
      </div>
      <div v-if="loading" class="chat-msg chat-msg--assistant">
        <div class="chat-msg__bubble chat-msg__bubble--typing">
          <span></span><span></span><span></span>
        </div>
      </div>
    </div>

    <div class="chat-panel__input-row">
      <input
        v-model="chatInput"
        class="chat-panel__input"
        type="text"
        placeholder="輸入……"
        :disabled="loading"
        @keyup.enter="sendChat"
      />
      <button class="chat-panel__send" :disabled="loading" @click="sendChat" aria-label="送出">▶</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { getChatConfig, sendChatMessage } from '@/api/market'
import type { ChatMessage } from '@/types/market'

const PROVIDER_LABELS: Record<string, string> = {
  gemini: 'Google Gemini',
  groq:   'Groq',
  github: 'GitHub Models',
}

const messages      = ref<ChatMessage[]>([])
const chatInput     = ref('')
const loading       = ref(false)
const messagesEl    = ref<HTMLElement | null>(null)
const availableModels = ref<string[]>([])
const selectedModel   = ref('')
const currentProvider = ref('')

const providerLabel = computed(() => PROVIDER_LABELS[currentProvider.value] ?? currentProvider.value)

function scrollToBottom() {
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}

async function sendChat() {
  const text = chatInput.value.trim()
  if (!text || loading.value) return
  chatInput.value = ''
  messages.value.push({ role: 'user', content: text })
  loading.value = true
  await nextTick()
  scrollToBottom()
  try {
    const reply = await sendChatMessage(messages.value, selectedModel.value || undefined)
    messages.value.push({ role: 'assistant', content: reply })
  } catch {
    messages.value.push({ role: 'assistant', content: '抱歉，AI 功能暫時無法使用，請稍後再試。' })
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

onMounted(async () => {
  try {
    const cfg = await getChatConfig()
    currentProvider.value = cfg.provider
    availableModels.value = cfg.models
    selectedModel.value   = cfg.default
  } catch {
    currentProvider.value = 'github'
    selectedModel.value   = 'gpt-4o'
  }
})
</script>

<style scoped>
.chat-panel { flex-shrink: 0; width: 360px; border: 1px solid var(--color-ink-4); border-radius: var(--radius-md); display: flex; flex-direction: column; height: 620px; overflow: hidden; position: sticky; top: var(--space-6); }

.chat-panel__header { padding: var(--space-3) var(--space-4); border-bottom: 1px solid var(--color-ink-4); display: flex; align-items: center; justify-content: space-between; background: var(--color-white); flex-shrink: 0; gap: var(--space-2); }
.chat-panel__brand { display: flex; align-items: center; gap: var(--space-2); min-width: 0; }
.chat-panel__d { width: 26px; height: 26px; border-radius: 50%; background: var(--color-primary); display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: var(--color-ink-1); line-height: 1; flex-shrink: 0; }
.chat-panel__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.chat-panel__model-wrap { display: flex; flex-direction: column; align-items: flex-end; gap: 2px; flex-shrink: 0; }
.chat-panel__provider { font-size: 10px; color: var(--color-ink-3); font-family: var(--font-body); white-space: nowrap; }
.chat-panel__model-name { font-size: 11px; color: var(--color-ink-3); font-family: var(--font-body); }
.chat-panel__model-select { font-size: 11px; color: var(--color-ink-2); font-family: var(--font-body); border: 1px solid var(--color-ink-4); border-radius: 4px; padding: 1px 4px; background: var(--color-white); cursor: pointer; outline: none; max-width: 160px; }
.chat-panel__model-select:focus { border-color: var(--color-primary); }

.chat-panel__messages { flex: 1; overflow-y: auto; padding: var(--space-4); display: flex; flex-direction: column; gap: var(--space-3); }
.chat-panel__hint { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-3); text-align: center; padding-top: var(--space-6); line-height: 1.9; }

.chat-msg { display: flex; }
.chat-msg--user      { justify-content: flex-end; }
.chat-msg--assistant { justify-content: flex-start; }
.chat-msg__bubble { max-width: 82%; padding: var(--space-2) var(--space-3); border-radius: var(--radius-md); font-family: var(--font-cjk); font-size: 13px; line-height: 1.7; white-space: pre-wrap; }
.chat-msg--user .chat-msg__bubble      { background: rgba(232, 193, 58, 0.28); color: var(--color-ink-1); border-bottom-right-radius: 4px; }
.chat-msg--assistant .chat-msg__bubble { background: rgba(232, 193, 58, 0.13); color: var(--color-ink-1); border-bottom-left-radius: 4px; }

.chat-msg__bubble--typing { display: flex; align-items: center; gap: 4px; padding: var(--space-3) var(--space-3); }
.chat-msg__bubble--typing span { width: 7px; height: 7px; border-radius: 50%; background: var(--color-ink-3); animation: blink 1.2s infinite; }
.chat-msg__bubble--typing span:nth-child(2) { animation-delay: 0.2s; }
.chat-panel__bubble--typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%, 80%, 100% { opacity: 0.2; } 40% { opacity: 1; } }

.chat-panel__input-row { border-top: 1px solid var(--color-ink-4); padding: var(--space-3); display: flex; gap: var(--space-2); flex-shrink: 0; }
.chat-panel__input { flex: 1; padding: var(--space-2) var(--space-3); border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-1); outline: none; transition: border-color 0.2s; }
.chat-panel__input:focus { border-color: var(--color-primary); }
.chat-panel__input::placeholder { color: var(--color-ink-3); }
.chat-panel__input:disabled { background: var(--color-primary-bg); }
.chat-panel__send { width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; background: var(--color-primary); border: none; border-radius: var(--radius-sm); font-size: 15px; color: var(--color-ink-1); cursor: pointer; transition: opacity 0.2s; flex-shrink: 0; }
.chat-panel__send:hover:not(:disabled) { opacity: 0.82; }
.chat-panel__send:disabled { opacity: 0.4; cursor: default; }

@media (max-width: 960px) { .chat-panel { width: 100%; position: static; height: 480px; } }
</style>
