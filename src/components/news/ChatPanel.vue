<template>
  <div class="chat-panel">
    <div class="chat-panel__header">
      <div class="chat-panel__brand">
        <span class="chat-panel__d">D</span>
        <span class="chat-panel__title">Daniellife 會計丹尼</span>
      </div>
      <span class="chat-panel__model">使用模型：&#123;ChatGPT 4.0&#125;</span>
    </div>

    <div class="chat-panel__messages" ref="messagesEl">
      <div v-for="(msg, i) in messages" :key="i" class="chat-msg" :class="`chat-msg--${msg.role}`">
        <div class="chat-msg__bubble">{{ msg.content }}</div>
      </div>
      <div v-if="!messages.length" class="chat-panel__hint">
        詢問任何財經問題<br>例如：「幫我解釋 Fed 升息對台股的影響」
      </div>
    </div>

    <div class="chat-panel__input-row">
      <input v-model="chatInput" class="chat-panel__input" type="text" placeholder="輸入……" @keyup.enter="sendChat" />
      <button class="chat-panel__send" @click="sendChat" aria-label="送出">▶</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import type { ChatMessage } from '@/types/market'

const messages  = ref<ChatMessage[]>([])
const chatInput = ref('')
const messagesEl = ref<HTMLElement | null>(null)

async function sendChat() {
  const text = chatInput.value.trim()
  if (!text) return
  chatInput.value = ''
  messages.value.push({ role: 'user', content: text })
  // TODO: call GitHub Models API (GPT-4o) here
  await nextTick()
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  setTimeout(() => {
    messages.value.push({ role: 'assistant', content: '（AI 回覆功能尚未串接，敬請期待）' })
    nextTick(() => { if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight })
  }, 600)
}
</script>

<style scoped>
.chat-panel { flex-shrink: 0; width: 360px; border: 1px solid var(--color-ink-4); border-radius: var(--radius-md); display: flex; flex-direction: column; height: 620px; overflow: hidden; position: sticky; top: var(--space-6); }

.chat-panel__header { padding: var(--space-3) var(--space-4); border-bottom: 1px solid var(--color-ink-4); display: flex; align-items: center; justify-content: space-between; background: var(--color-white); flex-shrink: 0; }
.chat-panel__brand { display: flex; align-items: center; gap: var(--space-2); }
.chat-panel__d { width: 26px; height: 26px; border-radius: 50%; background: var(--color-primary); display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: var(--color-ink-1); line-height: 1; flex-shrink: 0; }
.chat-panel__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); }
.chat-panel__model { font-size: 11px; color: var(--color-ink-3); font-family: var(--font-body); }

.chat-panel__messages { flex: 1; overflow-y: auto; padding: var(--space-4); display: flex; flex-direction: column; gap: var(--space-3); }
.chat-panel__hint { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-3); text-align: center; padding-top: var(--space-6); line-height: 1.9; }

.chat-msg { display: flex; }
.chat-msg--user      { justify-content: flex-end; }
.chat-msg--assistant { justify-content: flex-start; }
.chat-msg__bubble { max-width: 82%; padding: var(--space-2) var(--space-3); border-radius: var(--radius-md); font-family: var(--font-cjk); font-size: 13px; line-height: 1.7; }
.chat-msg--user .chat-msg__bubble      { background: rgba(232, 193, 58, 0.28); color: var(--color-ink-1); border-bottom-right-radius: 4px; }
.chat-msg--assistant .chat-msg__bubble { background: rgba(232, 193, 58, 0.13); color: var(--color-ink-1); border-bottom-left-radius: 4px; }

.chat-panel__input-row { border-top: 1px solid var(--color-ink-4); padding: var(--space-3); display: flex; gap: var(--space-2); flex-shrink: 0; }
.chat-panel__input { flex: 1; padding: var(--space-2) var(--space-3); border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-1); outline: none; transition: border-color 0.2s; }
.chat-panel__input:focus { border-color: var(--color-primary); }
.chat-panel__input::placeholder { color: var(--color-ink-3); }
.chat-panel__send { width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; background: var(--color-primary); border: none; border-radius: var(--radius-sm); font-size: 15px; color: var(--color-ink-1); cursor: pointer; transition: opacity 0.2s; flex-shrink: 0; }
.chat-panel__send:hover { opacity: 0.82; }

@media (max-width: 960px) { .chat-panel { width: 100%; position: static; height: 480px; } }
</style>
