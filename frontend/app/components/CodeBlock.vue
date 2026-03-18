<script setup lang="ts">
import DOMPurify from 'dompurify'
import { codeToHtml } from 'shiki'

const props = defineProps<{
  code: string
  lang?: string
}>()

const copied = ref(false)
const highlighted = ref('')

async function highlight() {
  const raw = await codeToHtml(props.code.trim(), {
    lang: props.lang ?? 'python',
    themes: {
      light: 'github-light',
      dark: 'github-dark'
    }
  })
  highlighted.value = DOMPurify.sanitize(raw)
}

watch(() => props.code, highlight, { immediate: true })

async function copy() {
  await navigator.clipboard.writeText(props.code.trim())
  copied.value = true
  setTimeout(() => {
    copied.value = false
  }, 2000)
}
</script>

<template>
  <div class="relative group rounded-lg overflow-hidden border border-gray-200 dark:border-gray-800">
    <button
      class="absolute top-2 right-2 p-1.5 rounded-md bg-gray-200/80 dark:bg-gray-700/80 text-gray-600 dark:text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-gray-300 dark:hover:bg-gray-600 cursor-pointer"
      @click="copy"
    >
      <UIcon
        :name="copied ? 'i-lucide-check' : 'i-lucide-copy'"
        class="size-4"
      />
    </button>
    <!-- eslint-disable vue/no-v-html -->
    <div
      class="code-block text-sm overflow-x-auto [&_pre]:p-4 [&_pre]:m-0"
      v-html="highlighted"
    />
    <!-- eslint-enable vue/no-v-html -->
  </div>
</template>

<style>
html.dark .code-block .shiki {
  background-color: var(--shiki-dark-bg) !important;
}

html.dark .code-block .shiki span {
  color: var(--shiki-dark) !important;
}
</style>
