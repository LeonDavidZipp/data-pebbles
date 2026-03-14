<script setup lang="ts">
useHead({
  meta: [{ name: 'viewport', content: 'width=device-width, initial-scale=1' }],
  link: [{ rel: 'icon', href: '/favicon.ico' }],
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
</script>

<template>
  <UApp>
    <div class="flex h-screen">
      <aside class="w-56 border-r border-default flex flex-col bg-elevated">
        <div class="p-4 border-b border-default">
          <NuxtLink
            to="/"
            class="text-lg font-semibold"
          >
            Data Pebbles
          </NuxtLink>
        </div>

        <nav class="flex-1 p-2 space-y-1">
          <NuxtLink
            v-for="layer in layers"
            :key="layer.to"
            :to="layer.to"
            class="flex items-center gap-2 px-3 py-2 rounded-md text-sm transition-colors"
            :class="
              activeLayer === layer.to
                ? 'bg-primary/10 text-primary font-medium'
                : 'text-muted hover:bg-elevated-muted'
            "
          >
            <UIcon
              :name="layer.icon"
              class="size-4"
            />
            {{ layer.label }}
          </NuxtLink>
        </nav>

        <div class="p-2 border-t border-default">
          <UColorModeButton class="w-full" />
        </div>
      </aside>

      <main class="flex-1 overflow-auto">
        <NuxtPage />
      </main>
    </div>
  </UApp>
</template>
