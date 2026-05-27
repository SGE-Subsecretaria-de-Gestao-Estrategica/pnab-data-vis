import type { Preview } from '@storybook/sveltekit'
import '../node_modules/sniic-design-system/dist/sniic.css'

const preview: Preview = {
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