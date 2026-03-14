export default defineEventHandler((event) => {
  const target = process.env.NUXT_API_BASE || 'http://localhost:8000'
  const path = event.path.replace(/^\/api/, '')
  return proxyRequest(event, `${target}${path}`)
})
