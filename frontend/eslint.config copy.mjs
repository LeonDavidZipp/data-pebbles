// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt()
  .append({
    ignores: ['app/utils/api/**']
  })
  .override('nuxt/stylistic', {
    rules: {
      '@stylistic/arrow-parens': ['error', 'always'],
      '@stylistic/operator-linebreak': 'off',
      '@stylistic/indent-binary-ops': 'off',
      '@stylistic/quote-props': 'off',
      '@stylistic/member-delimiter-style': 'off'
    }
  })
  .override('nuxt/vue/rules', {
    rules: {
      'vue/multi-word-component-names': 'off',
      'vue/singleline-html-element-content-newline': 'off',
      'vue/max-attributes-per-line': 'off',
      'vue/html-self-closing': 'off',
      'vue/html-closing-bracket-newline': 'off',
      'vue/html-indent': 'off',
      'vue/attributes-order': 'off',
      'vue/operator-linebreak': 'off'
    }
  })
