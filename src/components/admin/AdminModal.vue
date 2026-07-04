<template>
  <Teleport to="body">
    <div v-if="open" class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal">
        <button class="modal__close" @click="$emit('close')">×</button>
        <h3 class="modal__title">
          {{ mode === 'add' ? '新增' : '編輯' }}：{{ sectionLabel }}
        </h3>

        <div class="modal__fields">
          <label v-for="field in fields" :key="field.key" class="modal__label">
            {{ field.label }}
            <template v-if="field.type === 'textarea'">
              <textarea
                v-model="localFormData[field.key]"
                class="modal__textarea"
                rows="3"
                :maxlength="field.maxLength"
              ></textarea>
              <span v-if="field.maxLength" class="modal__char-count">
                {{ (localFormData[field.key] ?? '').length }} / {{ field.maxLength }}
              </span>
            </template>
            <div v-else-if="field.options && field.multi" class="modal__radio-group">
              <button
                v-for="opt in field.options"
                :key="opt"
                type="button"
                class="modal__radio-btn"
                :class="{ 'modal__radio-btn--active': multiValues(field.key).includes(opt) }"
                @click="toggleMultiOption(field.key, opt)"
              >{{ opt }}</button>
            </div>
            <div v-else-if="field.options" class="modal__radio-group">
              <button
                v-for="opt in field.options"
                :key="opt"
                type="button"
                class="modal__radio-btn"
                :class="{ 'modal__radio-btn--active': localFormData[field.key] === opt }"
                @click="localFormData[field.key] = opt"
              >{{ opt }}</button>
            </div>
            <input
              v-else
              v-model="localFormData[field.key]"
              class="modal__input"
              :type="field.type ?? 'text'"
              :placeholder="field.placeholder ?? field.label"
            />
          </label>
        </div>

        <!-- 照片管理（activities / travel — 多張；edit 模式） -->
        <template v-if="mode === 'edit' && (current === 'activities' || current === 'travel')">
          <div class="modal__pm-title">照片管理</div>
          <div class="modal__pm-grid">
            <div v-for="url in editingPhotos" :key="url" class="modal__pm-item">
              <img :src="mediaUrl(url)" class="modal__pm-thumb" alt="照片" />
              <button class="modal__pm-del" :disabled="photoUploading" @click="$emit('delete-multi', url)">×</button>
            </div>
            <label class="modal__pm-add" :class="{ 'modal__pm-add--loading': photoUploading }">
              <span>{{ photoUploading ? '…' : '+' }}</span>
              <input type="file" accept="image/*" style="display:none" :disabled="photoUploading" @change="(e) => $emit('upload-multi', e)" />
            </label>
          </div>
        </template>

        <!-- 照片管理（social — 單張；edit 模式） -->
        <template v-if="mode === 'edit' && current === 'social'">
          <div class="modal__pm-title">照片（單張）</div>
          <div class="modal__pm-single">
            <img v-if="editingPhotoUrl" :src="mediaUrl(editingPhotoUrl)" class="modal__pm-single-img" alt="活動照片" />
            <div v-else class="modal__pm-single-placeholder">尚無照片</div>
            <div class="modal__pm-single-actions">
              <label class="modal__pm-upload-btn" :class="{ 'modal__pm-upload-btn--loading': photoUploading }">
                {{ photoUploading ? '上傳中…' : editingPhotoUrl ? '更換照片' : '上傳照片' }}
                <input type="file" accept="image/*" style="display:none" :disabled="photoUploading" @change="(e) => $emit('upload-single-edit', e)" />
              </label>
              <button v-if="editingPhotoUrl" class="modal__pm-del-btn" :disabled="photoUploading" @click="$emit('delete-single-edit')">刪除照片</button>
            </div>
          </div>
        </template>

        <!-- 照片管理（internships — 單張；edit 模式） -->
        <template v-if="mode === 'edit' && current === 'internships'">
          <div class="modal__pm-title">照片（單張）</div>
          <div class="modal__pm-single">
            <img v-if="editingPhotoUrl" :src="mediaUrl(editingPhotoUrl)" class="modal__pm-single-img" alt="實習照片" />
            <div v-else class="modal__pm-single-placeholder">尚無照片</div>
            <div class="modal__pm-single-actions">
              <label class="modal__pm-upload-btn" :class="{ 'modal__pm-upload-btn--loading': photoUploading }">
                {{ photoUploading ? '上傳中…' : editingPhotoUrl ? '更換照片' : '上傳照片' }}
                <input type="file" accept="image/*" style="display:none" :disabled="photoUploading" @change="(e) => $emit('upload-single-edit', e)" />
              </label>
              <button v-if="editingPhotoUrl" class="modal__pm-del-btn" :disabled="photoUploading" @click="$emit('delete-single-edit')">刪除照片</button>
            </div>
          </div>
        </template>

        <!-- 新增模式：多張照片選取（activities / travel） -->
        <template v-if="mode === 'add' && (current === 'activities' || current === 'travel')">
          <div class="modal__pm-title">照片（可選，最多 4 張）</div>
          <div class="modal__pm-grid">
            <div
              v-for="(preview, i) in pendingPhotoPreview"
              :key="i"
              class="modal__pm-add modal__pm-slot"
              @click="triggerPendingPhoto(i)"
            >
              <img v-if="preview" :src="preview" class="modal__pm-thumb" />
              <span v-else>+</span>
            </div>
          </div>
          <input ref="pendingPhotoInputEl" type="file" accept="image/*" style="display:none" @change="onPendingPhotoChange" />
        </template>

        <!-- 新增模式：單張照片選取（social / internships） -->
        <template v-if="mode === 'add' && (current === 'social' || current === 'internships')">
          <div class="modal__pm-title">照片（可選）</div>
          <div class="modal__pm-single">
            <img v-if="pendingSinglePreview" :src="pendingSinglePreview" class="modal__pm-single-img" />
            <div v-else class="modal__pm-single-placeholder">尚無照片</div>
            <label class="modal__pm-upload-btn">
              {{ pendingSinglePreview ? '更換照片' : '選擇照片' }}
              <input type="file" accept="image/*" style="display:none" @change="onPendingSingleChange" />
            </label>
          </div>
        </template>

        <p v-if="saveError" class="modal__error">{{ saveError }}</p>
        <div class="modal__actions">
          <button class="modal__btn modal__btn--cancel" @click="$emit('close')">取消</button>
          <button class="modal__btn modal__btn--save" :disabled="saving" @click="handleSave">
            {{ saving ? '儲存中…' : '儲存' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { mediaUrl } from '@/api/client'

export type FieldDef = { key: string; label: string; type?: string; placeholder?: string; options?: string[]; multi?: boolean; maxLength?: number }

const props = defineProps<{
  open: boolean
  mode: 'add' | 'edit'
  sectionLabel: string
  fields: FieldDef[]
  initialFormData: Record<string, string>
  current: string
  saving: boolean
  saveError: string
  editingPhotos: string[]
  editingPhotoUrl: string
  photoUploading: boolean
}>()

const emit = defineEmits<{
  close: []
  save: [data: { formData: Record<string, string>; pendingMultiFiles: (File | null)[]; pendingSingleFile: File | null }]
  'upload-multi': [e: Event]
  'delete-multi': [url: string]
  'upload-single-edit': [e: Event]
  'delete-single-edit': []
}>()

// Local form state — initialized from initialFormData each time the modal opens
const localFormData = ref<Record<string, string>>({})

// Pending photos for add mode
const pendingPhotoFiles    = ref<(File | null)[]>([null, null, null, null])
const pendingPhotoPreview  = ref<(string | null)[]>([null, null, null, null])
const pendingSingleFile    = ref<File | null>(null)
const pendingSinglePreview = ref<string>('')
let   pendingPhotoSlot     = 0
const pendingPhotoInputEl  = ref<HTMLInputElement | null>(null)

watch(() => props.open, (newOpen) => {
  if (!newOpen) return
  localFormData.value = { ...props.initialFormData }
  pendingPhotoFiles.value    = [null, null, null, null]
  pendingPhotoPreview.value  = [null, null, null, null]
  pendingSingleFile.value    = null
  pendingSinglePreview.value = ''
})

function multiValues(key: string): string[] {
  return (localFormData.value[key] ?? '').split(',').map((v) => v.trim()).filter(Boolean)
}

function toggleMultiOption(key: string, opt: string) {
  const current = multiValues(key)
  const idx = current.indexOf(opt)
  if (idx >= 0) current.splice(idx, 1)
  else current.push(opt)
  localFormData.value[key] = current.join(',')
}

function triggerPendingPhoto(slot: number) {
  pendingPhotoSlot = slot
  pendingPhotoInputEl.value?.click()
}

function onPendingPhotoChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  ;(e.target as HTMLInputElement).value = ''
  pendingPhotoFiles.value[pendingPhotoSlot] = file
  const reader = new FileReader()
  reader.onload = (ev) => { pendingPhotoPreview.value[pendingPhotoSlot] = ev.target?.result as string }
  reader.readAsDataURL(file)
}

function onPendingSingleChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  ;(e.target as HTMLInputElement).value = ''
  pendingSingleFile.value = file
  const reader = new FileReader()
  reader.onload = (ev) => { pendingSinglePreview.value = ev.target?.result as string }
  reader.readAsDataURL(file)
}

function handleSave() {
  emit('save', {
    formData: localFormData.value,
    pendingMultiFiles: pendingPhotoFiles.value,
    pendingSingleFile: pendingSingleFile.value,
  })
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--color-white);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  width: 560px;
  max-width: 92vw;
  max-height: 88vh;
  overflow-y: auto;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.modal__close {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  font-size: 20px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-ink-3);
}

.modal__title {
  font-family: var(--font-cjk);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.modal__fields { display: flex; flex-direction: column; gap: var(--space-3); }

.modal__label {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  font-family: var(--font-cjk);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-ink-2);
}

.modal__char-count {
  align-self: flex-end;
  font-size: 11px;
  font-weight: 400;
  color: var(--color-ink-3);
}

.modal__input,
.modal__textarea {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
  box-sizing: border-box;
}
.modal__input:focus,
.modal__textarea:focus { border-color: var(--color-primary); }
.modal__textarea { resize: vertical; }

.modal__error {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: #dc2626;
  background: #fef2f2;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
}

/* ── Photo manager ── */
.modal__pm-title {
  font-family: var(--font-cjk);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-ink-2);
  margin: var(--space-4) 0 var(--space-2);
  border-top: 1px solid var(--color-ink-4);
  padding-top: var(--space-3);
}

.modal__pm-grid { display: flex; flex-wrap: wrap; gap: var(--space-2); }

.modal__pm-item {
  position: relative;
  width: 80px;
  height: 80px;
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.modal__pm-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.modal__pm-del {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: none;
  background: rgba(0,0,0,.55);
  color: #fff;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal__pm-add {
  width: 80px;
  height: 80px;
  border: 2px dashed var(--color-ink-4);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: var(--color-ink-3);
  cursor: pointer;
  transition: border-color 0.2s;
}
.modal__pm-add:hover { border-color: var(--color-primary); }
.modal__pm-add--loading { opacity: 0.5; cursor: default; }

.modal__pm-single { display: flex; gap: var(--space-3); align-items: flex-start; }

.modal__pm-single-img {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  display: block;
}

.modal__pm-single-placeholder {
  width: 120px;
  height: 90px;
  background: #f5efea;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: var(--color-ink-3);
  font-family: var(--font-cjk);
}

.modal__pm-single-actions { display: flex; flex-direction: column; gap: var(--space-2); }

.modal__pm-upload-btn {
  padding: var(--space-1) var(--space-3);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
  color: var(--color-primary);
  font-family: var(--font-cjk);
  font-size: 13px;
  cursor: pointer;
  background: transparent;
  display: inline-block;
}
.modal__pm-upload-btn:hover { background: var(--color-primary); color: #fff; }
.modal__pm-upload-btn--loading { opacity: 0.5; cursor: default; }

.modal__pm-del-btn {
  padding: var(--space-1) var(--space-3);
  border: 1px solid #dc2626;
  border-radius: var(--radius-sm);
  color: #dc2626;
  font-family: var(--font-cjk);
  font-size: 13px;
  cursor: pointer;
  background: transparent;
}
.modal__pm-del-btn:hover { background: #dc2626; color: #fff; }

.modal__radio-group { display: flex; gap: 0; border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); overflow: hidden; width: fit-content; }
.modal__radio-btn { padding: var(--space-2) var(--space-5); background: var(--color-white); border: none; font-family: var(--font-cjk); font-size: 14px; color: var(--color-ink-2); cursor: pointer; transition: background 0.15s, color 0.15s; }
.modal__radio-btn + .modal__radio-btn { border-left: 1px solid var(--color-ink-4); }
.modal__radio-btn--active { background: var(--color-primary); color: var(--color-ink-1); font-weight: 700; }

.modal__actions { display: flex; gap: var(--space-2); justify-content: flex-end; }

.modal__btn {
  padding: var(--space-2) var(--space-5);
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.modal__btn:disabled { opacity: 0.6; cursor: not-allowed; }
.modal__btn:not(:disabled):hover { opacity: 0.82; }
.modal__btn--cancel { background: var(--color-ink-4); color: var(--color-ink-1); }
.modal__btn--save   { background: var(--color-primary); color: var(--color-ink-1); }
</style>
