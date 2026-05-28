<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber } from 'sniic-design-system';
  // @ts-ignore
  import {
    percCPFEstados,
    percCNPJEstados,
    percCPFMunicipios,
    percCNPJMunicipios,
  } from '$lib/data/section2';

  const { Story } = defineMeta({
    title: 'Section 2/esferaBigNumbers',
    component: BigNumber,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**O perfil CPF/CNPJ muda conforme a esfera executora**

A composição entre pessoas físicas (CPF) e jurídicas (CNPJ) varia significativamente entre estados e municípios:

- **Estados**: ${percCPFEstados.toFixed(1)}% dos pagamentos foram para CPF e ${percCNPJEstados.toFixed(1)}% para CNPJ.
- **Municípios**: ${percCPFMunicipios.toFixed(1)}% dos pagamentos foram para CPF e ${percCNPJMunicipios.toFixed(1)}% para CNPJ.

Os estados concentram proporcionalmente mais entidades (CNPJ), enquanto os municípios têm base mais ampla de pessoas físicas — reflexo das políticas locais de fomento direto ao trabalhador cultural individual.

**Fonte**: \`aggregate_execution_by_person_type_state.csv\` e \`aggregate_execution_by_person_type_municipality.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="BigNumber — % CPF nos estados">
  {#snippet template()}
    <BigNumber value={percCPFEstados.toFixed(1)} suffix="%" fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — % CNPJ nos estados">
  {#snippet template()}
    <BigNumber value={percCNPJEstados.toFixed(1)} suffix="%" fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — % CPF nos municípios">
  {#snippet template()}
    <BigNumber value={percCPFMunicipios.toFixed(1)} suffix="%" fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — % CNPJ nos municípios">
  {#snippet template()}
    <BigNumber value={percCNPJMunicipios.toFixed(1)} suffix="%" fontSize={96} />
  {/snippet}
</Story>
