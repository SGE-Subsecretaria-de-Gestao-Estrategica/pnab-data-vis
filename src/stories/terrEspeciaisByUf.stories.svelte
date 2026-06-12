<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart } from 'sniic-design-system';

  const COLORS = ['#F5C842', '#2B6CB0'];
  // @ts-ignore
  // import { terrEspeciaisData, TERR_KEYS, TERR_LABELS } from '$lib/data/section2'; // CSV faltante: territorios_especiais_por_municipio.csv

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);

  const { Story } = defineMeta({
    title: 'Section 1/terrEspeciaisByUf',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Valor destinado a territórios especiais por estado e esfera executora**

Cada barra representa um estado, mostrando o valor total (R$) destinado a agentes culturais em territórios especiais, dividido por esfera executora: repasses diretos da **UF**, execução pelo **governo estadual** e execução pelos **municípios**.

**Fonte**: \`territorios_especiais_por_uf.csv\`, \`territorios_especiais_por_estado.csv\`, \`territorios_especiais_por_municipio.csv\`.
          `,
        },
      },
    },
  });
</script>

<!-- DISABLED: territorios_especiais_por_municipio.csv faltante
<Story name="HorizontalStackedBarChart — valor em territórios especiais por UF e esfera">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={terrEspeciaisData}
      keys={[...TERR_KEYS]}
      labels={TERR_LABELS}
      colors={COLORS}
      format={formatBRL}
      showTotalLabel={true}
      rowHeight={36}
    />
  {/snippet}
</Story>
-->
