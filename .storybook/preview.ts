import type { Preview } from '@storybook/sveltekit'
import '../node_modules/sniic-design-system/dist/sniic.css'
// @ts-ignore
import SvgExportDecoratorNamed from '../src/lib/components/SvgExportDecoratorNamed.svelte'

function makeFilename(title: string, name: string): string {
  const group = title.includes('/') ? title.split('/')[1] : title.replace(/\s+/g, '')
  const slug = name
    .replace(/[–—]/g, '-')
    .replace(/[^\w\s\-áéíóúàèìòùâêîôûãõçÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÇ]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
  return `${group}--${slug}.svg`
}

const preview: Preview = {
  decorators: [
    // @ts-ignore
    (story: unknown, context: { title: string; name: string }) => ({
      Component: SvgExportDecoratorNamed,
      props: { filename: makeFilename(context.title, context.name) },
    }),
  ],
  parameters: {
    options: {
      storySort: {
        order: ['Section 1', 'Section 2', 'Section 3', 'Section 4'],
      },
    },
    controls: {
      matchers: {
       color: /(background|color)$/i,
       date: /Date$/i,
      },
    },

    a11y: {
      // 'todo' - show a11y violations in the test UI only
      // 'error' - fail CI on a11y violations
      // 'off' - skip a11y checks entirely
      test: 'todo'
    }
  },
};

export default preview;