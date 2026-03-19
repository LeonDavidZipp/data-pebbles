export function useCopyId() {
  const copiedId = ref<string | null>(null)
  let timeout: ReturnType<typeof setTimeout> | null = null

  function copyId(key: string, value: string | number) {
    navigator.clipboard.writeText(String(value))
    copiedId.value = key
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(
      () => { copiedId.value = null }, 1500
    )
  }

  return { copiedId, copyId }
}
