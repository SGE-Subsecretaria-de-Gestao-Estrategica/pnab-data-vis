<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber } from 'sniic-design-system';
  // @ts-ignore
  import { percComVinculo } from '$lib/data/section4';

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalBigNumber',
    component: BigNumber,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Vínculo formal de trabalho entre beneficiários do PNAB**

**${percComVinculo.toFixed(1)}%** das pessoas físicas que acessaram recursos da Política Nacional Aldir Blanc possuem registro de vínculo formal de trabalho.

**Fonte**: cruzamento da base de contemplados do PNAB com a RAIS (Relação Anual de Informações Sociais).
          `,
        },
      },
    },
  });
</script>

<Story name="BigNumber — % com vínculo formal de trabalho">
  {#snippet template()}
    <div style="display: flex; flex-direction: column; align-items: center; gap: 0.75rem; max-width: 320px; font-family: 'Space Grotesk', system-ui, sans-serif;">
      <BigNumber value={percComVinculo.toFixed(1)} suffix="%" fontSize={96} />
      <p style="margin: 0; font-size: 1rem; line-height: 1.5; text-align: center; opacity: 0.75;">
        das pessoas físicas que acessaram recursos da Política Nacional Aldir Blanc possuem registro de vínculo formal de trabalho
      </p>
    </div>
  {/snippet}
</Story>
