<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber } from 'sniic-design-system';
  // @ts-ignore
  import { specialTerritoryCount, specialTerritoryValue } from '$lib/data/section1';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);
  // @ts-ignore
  const formatNum = (v) => v.toLocaleString('pt-BR');

  const { Story } = defineMeta({
    title: 'Section 1/specialTerritoryBigNumbers',
    component: BigNumber,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Territórios especiais: Favelas, Quilombos e Territórios Indígenas**

**${formatNum(specialTerritoryCount)} agentes culturais** residentes em favelas, agrupamentos quilombolas e territórios indígenas foram contemplados pela Política Nacional Aldir Blanc, recebendo um total de **${formatBRL(specialTerritoryValue)}**.

Apesar do alcance, esses números evidenciam a **sub-representação sistemática** dessas populações no programa: a proporção de recursos destinada a esses territórios é significativamente menor do que o peso demográfico dessas comunidades na população brasileira.

**Fonte**: \`special_territory_w_ibge_by_brazil.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="BigNumber — agentes em territórios especiais">
  {#snippet template()}
    <BigNumber value={formatNum(specialTerritoryCount)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — valor para territórios especiais">
  {#snippet template()}
    <BigNumber value={formatBRL(specialTerritoryValue)} fontSize={72} />
  {/snippet}
</Story>
