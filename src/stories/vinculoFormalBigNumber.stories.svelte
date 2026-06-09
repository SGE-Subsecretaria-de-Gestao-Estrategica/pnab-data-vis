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
    <BigNumber value={percComVinculo.toFixed(1)} suffix="%" fontSize={96} label="com vínculo formal de trabalho" />
  {/snippet}
</Story>
