<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, colorScales, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import { specialTerritoryBarData } from '$lib/data/section2';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);

  const { Story } = defineMeta({
    title: 'Section 2/specialTerritoryByType',
    component: HorizontalBarChart,
    tags: ['autodocs'],
    decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Valor total destinado por tipo de território especial**

Dos recursos que chegaram a territórios especiais, as **favelas e comunidades urbanas** concentram a maior fatia, muito acima dos demais tipos. Agrupamentos quilombolas e indígenas, que reúnem populações historicamente mais marginalizadas, receberam volumes muito menores em termos absolutos.

**Fonte**: \`values_by_special_territory_uf.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="HorizontalBarChart — valor por tipo de território especial (teal)">
  {#snippet template()}
    <HorizontalBarChart
      data={specialTerritoryBarData}
      color={colorScales.teal[2]}
      format={formatBRL}
      xLabel="Valor total (R$)"
      margin={{ top: 20, right: 80, bottom: 40, left: 280 }}
    />
  {/snippet}
</Story>

<Story name="HorizontalBarChart — valor por tipo de território especial (blue)">
  {#snippet template()}
    <HorizontalBarChart
      data={specialTerritoryBarData}
      color={colorScales.blue[2]}
      format={formatBRL}
      xLabel="Valor total (R$)"
      margin={{ top: 20, right: 80, bottom: 40, left: 280 }}
    />
  {/snippet}
</Story>
