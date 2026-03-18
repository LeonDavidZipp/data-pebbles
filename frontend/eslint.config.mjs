// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt(
  {
    ignores: ['app/utils/api/**']
  },
  {
    rules: {
      '@stylistic/operator-linebreak': ['error', 'after']
    }
  }
)
