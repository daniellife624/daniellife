<template>
  <Teleport to="body">
    <div v-if="continent" class="modal-backdrop" @click.self="$emit('close')">
      <div
        class="modal add-modal"
        :style="{ '--accent': accentBg, '--accent-text': accentText }"
      >
        <button class="modal__close" @click="$emit('close')">×</button>

        <div class="add-modal__header">
          <span class="add-modal__pre">地區（自動帶入）：</span>
          <span class="add-modal__cont">{{ CONT_ZH[continent.key] || continent.label }}</span>
        </div>

        <div class="add-modal__fields">
          <div class="add-modal__row">
            <div class="add-modal__icon">人</div>
            <input class="add-modal__input" placeholder="和誰一起去？" v-model="form.companions" />
          </div>
          <div class="add-modal__row">
            <div class="add-modal__icon">事</div>
            <input class="add-modal__input" placeholder="做了什麼有趣的事情？" v-model="form.activities" />
          </div>
          <div class="add-modal__row">
            <div class="add-modal__icon">時</div>
            <input class="add-modal__input" placeholder="詳細的時間點？（e.g. 2024-03-15）" v-model="form.visitedAt" />
          </div>
          <div class="add-modal__row add-modal__row--col">
            <div class="add-modal__row add-modal__row--inner">
              <div class="add-modal__icon">地</div>
              <select class="add-modal__select" v-model="form.country" @change="form.city = ''">
                <option value="" disabled>選擇國家</option>
                <option v-for="c in countryList" :key="c.name" :value="c.name">{{ c.name }}</option>
                <option value="__other__">其他（手動輸入）</option>
              </select>
            </div>
            <input
              v-if="form.country === '__other__'"
              class="add-modal__input add-modal__input--indent"
              placeholder="請輸入國家名稱"
              v-model="form.customCountry"
            />
            <div class="add-modal__row add-modal__row--inner" v-if="form.country && form.country !== '__other__'">
              <div class="add-modal__icon add-modal__icon--sm">城</div>
              <select class="add-modal__select" v-model="form.city">
                <option value="" disabled>選擇城市</option>
                <option v-for="city in cityList" :key="city" :value="city">{{ city }}</option>
                <option value="__other__">其他（手動輸入）</option>
              </select>
            </div>
            <input
              v-if="form.country !== '__other__' && form.city === '__other__'"
              class="add-modal__input add-modal__input--indent"
              placeholder="請輸入城市名稱"
              v-model="form.customCity"
            />
          </div>
          <div class="add-modal__row">
            <div class="add-modal__icon">物</div>
            <input class="add-modal__input" placeholder="有沒有買什麼東西？" v-model="form.purchases" />
          </div>
        </div>

        <div class="add-modal__photos">
          <div
            v-for="(photo, i) in photoPreviews"
            :key="i"
            class="add-modal__photo-slot"
            @click="triggerPhoto(i)"
          >
            <img v-if="photo" :src="photo" class="add-modal__photo-img" alt="旅行照片" />
            <span v-else class="add-modal__photo-add">+</span>
          </div>
        </div>
        <input ref="photoInputEl" type="file" accept="image/*" style="display:none" @change="onPhotoChange" />

        <p v-if="submitError" class="add-modal__error">{{ submitError }}</p>
        <button class="add-modal__submit" :disabled="submitting" @click="submit">
          {{ submitting ? '新增中…' : '新增旅行日記' }}
        </button>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { createTravelEntry, uploadTravelPhoto } from '@/api/activities'
import { CONTINENT_COUNTRIES } from '@/data/travelData'
import type { Continent } from '@/types/activities'

const props = defineProps<{
  continent: Continent | null
  accentBg: string
  accentText: string
}>()

const emit = defineEmits<{
  close: []
  submitted: []
}>()

const CONT_ZH: Record<string, string> = {
  Europe: '歐洲', Asia: '亞洲', Africa: '非洲',
  Australia: '澳洲', Americas: '美洲',
}

const form = reactive({
  companions: '', activities: '', visitedAt: '',
  country: '', customCountry: '',
  city: '', customCity: '',
  purchases: '',
})
const photoPreviews = ref<(string | null)[]>([null, null, null, null])
const photoFiles    = ref<(File | null)[]>([null, null, null, null])
const submitting    = ref(false)
const submitError   = ref('')
let currentSlot     = 0
const photoInputEl  = ref<HTMLInputElement | null>(null)

const countryList = computed(() =>
  props.continent ? (CONTINENT_COUNTRIES[props.continent.key] ?? []) : []
)

const cityList = computed(() => {
  const found = countryList.value.find((c) => c.name === form.country)
  return found?.cities ?? []
})

watch(() => props.continent, (val) => {
  if (!val) return
  Object.assign(form, {
    companions: '', activities: '', visitedAt: '',
    country: '', customCountry: '',
    city: '', customCity: '',
    purchases: '',
  })
  photoPreviews.value = [null, null, null, null]
  photoFiles.value    = [null, null, null, null]
  submitError.value   = ''
})

function triggerPhoto(i: number) {
  currentSlot = i
  photoInputEl.value?.click()
}

function onPhotoChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  photoPreviews.value[currentSlot] = URL.createObjectURL(file)
  photoFiles.value[currentSlot] = file
  ;(e.target as HTMLInputElement).value = ''
}

async function submit() {
  if (!props.continent) return
  const country = form.country === '__other__' ? form.customCountry.trim() : form.country
  const city    = form.city    === '__other__' ? form.customCity.trim()    : form.city
  if (!country) { submitError.value = '請選擇或輸入國家'; return }
  if (!city)    { submitError.value = '請選擇或輸入城市'; return }
  if (!form.visitedAt.trim()) { submitError.value = '請填入造訪時間'; return }

  submitting.value  = true
  submitError.value = ''
  try {
    const entry = await createTravelEntry({
      country, city,
      continent: props.continent.key,
      visitedAt: form.visitedAt.trim(),
      companions: form.companions || undefined,
      activities: form.activities || undefined,
      purchases:  form.purchases  || undefined,
      journal: '',
      photos: [],
    })
    for (const file of photoFiles.value) {
      if (file) await uploadTravelPhoto(entry.id, file)
    }
    emit('submitted')
    emit('close')
  } catch (err) {
    submitError.value = err instanceof Error ? err.message : '新增失敗，請再試一次'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--color-white);
  border-radius: var(--radius-md);
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
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

.add-modal {
  max-width: 500px;
  width: 92vw;
  max-height: 90vh;
  overflow-y: auto;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
}

.add-modal__header {
  font-family: var(--font-cjk);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-ink-1);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  padding-right: var(--space-5);
  margin-bottom: 2px;
}

.add-modal__pre { font-weight: 400; }
.add-modal__cont { color: var(--accent, #3b82f6); }

.add-modal__fields { display: flex; flex-direction: column; gap: var(--space-2); }

.add-modal__row { display: flex; align-items: center; gap: var(--space-2); }
.add-modal__row--col { flex-direction: column; align-items: stretch; gap: var(--space-2); }
.add-modal__row--inner { display: flex; align-items: center; gap: var(--space-2); }

.add-modal__icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--accent, #3b82f6);
  color: var(--accent-text, #fff);
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.add-modal__icon--sm {
  width: 24px;
  height: 24px;
  font-size: 12px;
}

.add-modal__input {
  flex: 1;
  border: none;
  border-bottom: 1px solid var(--color-ink-4);
  outline: none;
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-1);
  padding: 5px 2px;
  background: transparent;
  transition: border-color 0.2s;
}

.add-modal__input:focus { border-bottom-color: var(--accent, #3b82f6); }
.add-modal__input::placeholder { color: var(--color-ink-3); }
.add-modal__input--indent { margin-left: 40px; }

.add-modal__select {
  flex: 1;
  border: none;
  border-bottom: 1px solid var(--color-ink-4);
  outline: none;
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-1);
  padding: 5px 2px;
  background: transparent;
  cursor: pointer;
  transition: border-color 0.2s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23999' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 4px center;
  padding-right: 20px;
}

.add-modal__select:focus { border-bottom-color: var(--accent, #3b82f6); }

.add-modal__photos {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2);
}

.add-modal__photo-slot {
  height: 100px;
  border: 2px dashed var(--color-ink-4);
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  transition: border-color 0.2s;
}

.add-modal__photo-slot:hover { border-color: var(--accent, #3b82f6); }
.add-modal__photo-add { font-size: 28px; color: var(--color-ink-4); line-height: 1; }
.add-modal__photo-img { width: 100%; height: 100%; object-fit: cover; }

.add-modal__error {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: #dc2626;
  text-align: center;
}

.add-modal__submit {
  width: 100%;
  padding: var(--space-3) 0;
  background: var(--accent, #3b82f6);
  color: var(--accent-text, #fff);
  font-family: var(--font-cjk);
  font-size: 15px;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: opacity 0.2s;
}

.add-modal__submit:hover:not(:disabled) { opacity: 0.88; }
.add-modal__submit:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
