<script setup lang="ts">
useHead({
  meta: [{ name: 'viewport', content: 'width=device-width, initial-scale=1' }],
  link: [{ rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
  htmlAttrs: {
    lang: 'en'
  }
})

useSeoMeta({
  title: 'Data Pebbles',
  description: 'Medallion architecture data lake manager'
})

const route = useRoute()

const layers = [
  { label: 'Bronze', icon: 'i-lucide-hard-drive', to: '/bronze' },
  { label: 'Silver', icon: 'i-lucide-database', to: '/silver' },
  { label: 'Gold', icon: 'i-lucide-crown', to: '/gold' }
]

const activeLayer = computed(() => {
  const path = route.path
  if (path.startsWith('/silver')) return '/silver'
  if (path.startsWith('/gold')) return '/gold'
  return '/bronze'
})

const mlflowPort = 5001
</script>

<template>
  <UApp>
    <div class="flex h-screen bg-gray-50 dark:bg-gray-950">
      <!-- Sidebar -->
      <aside class="w-60 bg-gray-900 dark:bg-gray-950 text-white flex flex-col border-r border-gray-800">
        <div class="px-5 py-4 flex items-center gap-2.5">
          <div class="size-8 rounded-lg overflow-hidden flex items-center justify-center">
            <img
              src="/favicon.svg"
              alt="Data Pebbles"
              class="size-8"
            >
          </div>
          <NuxtLink
            to="/"
            class="text-base font-semibold tracking-tight text-white"
          >
            Data Pebbles
          </NuxtLink>
        </div>

        <div class="px-3 mt-2 mb-1">
          <span class="px-2 text-[11px] font-semibold uppercase tracking-wider text-gray-500">
            Layers
          </span>
        </div>

        <nav class="flex-1 px-3 space-y-0.5">
          <NuxtLink
            v-for="layer in layers"
            :key="layer.to"
            :to="layer.to"
            class="flex items-center gap-2.5 px-3 py-2 rounded-md text-sm transition-colors"
            :class="
              activeLayer === layer.to
                ? 'bg-white/10 text-white font-medium'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            "
          >
            <UIcon
              :name="layer.icon"
              class="size-4"
            />
            {{ layer.label }}
          </NuxtLink>

          <div class="pt-4 pb-1">
            <span class="px-2 text-[11px] font-semibold uppercase tracking-wider text-gray-500">
              Tools
            </span>
          </div>

          <a
            :href="`http://localhost:${mlflowPort}`"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center gap-2.5 px-3 py-2 rounded-md text-sm transition-colors text-gray-400 hover:text-white hover:bg-white/5"
          >
            <UIcon
              name="i-lucide-flask-conical"
              class="size-4"
            />
            MLflow
            <UIcon
              name="i-lucide-external-link"
              class="size-3 ml-auto opacity-50"
            />
          </a>

          <NuxtLink
            to="/sdk"
            class="flex items-center gap-2.5 px-3 py-2 rounded-md text-sm transition-colors"
            :class="
              route.path.startsWith('/sdk')
                ? 'bg-white/10 text-white font-medium'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            "
          >
            <UIcon
              name="i-lucide-book-open"
              class="size-4"
            />
            SDK
          </NuxtLink>
        </nav>

        <div class="px-3 pb-3 mt-auto border-t border-gray-800 pt-3">
          <UColorModeButton
            variant="ghost"
            class="w-full text-gray-400 hover:text-white"
          />
        </div>
      </aside>

      <!-- Main content -->
      <main class="flex-1 overflow-auto">
        <NuxtPage />
      </main>
    </div>
  </UApp>
</template>
