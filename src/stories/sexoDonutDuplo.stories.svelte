<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import SexoDonutDuplo from '$lib/components/SexoDonutDuplo.svelte';

  // Data from aggregate_contemplados_by_sexo_proportion.csv
  const outerFem  = 578195818;  // valor_contemplados_feminino
  const outerMasc = 676227421;  // valor_contemplados_masculino
  const innerFem  = 62943;      // quantidade_contemplados_feminino
  const innerMasc = 71650;      // quantidade_contemplados_masculino

  const { Story } = defineMeta({
    title: 'Section 3/sexoDonutDuplo',
    component: SexoDonutDuplo,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição por sexo: valor repassado e quantidade de agentes (PF)**

Donut duplo com dois anéis concêntricos:
- **Anel externo**: valor total repassado (R$ 1,25 bi), dividido entre feminino e masculino
- **Anel interno**: quantidade de agentes culturais (134.593), dividida entre feminino e masculino

Fonte: \`aggregate_contemplados_by_sexo_proportion.csv\` (cruzamento PNAB × Receita Federal, pessoas físicas).
          `,
        },
      },
    },
  });
</script>

<Story name="Valor repassado e quantidade por sexo">
  {#snippet template()}
    <div style="max-width: 420px; margin: 0 auto;">
      <SexoDonutDuplo
        {outerFem}
        {outerMasc}
        {innerFem}
        {innerMasc}
      />
    </div>
  {/snippet}
</Story>
