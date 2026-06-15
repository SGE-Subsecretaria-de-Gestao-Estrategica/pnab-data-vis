<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { TreemapChart, colorScales, categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { domicilioTreemapData, porteTreemapData5, percUrbanoCadunico, percPequenoPorteCadunico } from '$lib/data/section5';

  // @ts-ignore
  const formatNum = (v) => v.toLocaleString('pt-BR');
  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 5/cadunicoTreemaps',
    component: TreemapChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Situação de domicílio e porte municipal — CadÚnico**

- **${formatPct(percUrbanoCadunico)}** dos contemplados no CadÚnico vivem em área urbana e **${formatPct(100 - percUrbanoCadunico)}** em área rural.
- **${formatPct(percPequenoPorteCadunico)}** residem em municípios de pequeno porte (Pequeno I + Pequeno II), proporção maior do que a observada no conjunto geral de beneficiários.

**Fonte**: \`aggregate_cadunico_by_situacao_domicilio.csv\`, \`aggregate_cadunico_by_population_size.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Treemap — situação de domicílio (Urbana / Rural)">
  {#snippet template()}
    <TreemapChart
      data={domicilioTreemapData}
      height={260}
      format={formatNum}
      colors={[colorScales.orange[2], colorScales.teal[2]]}
    />
  {/snippet}
</Story>

<Story name="Treemap — porte municipal">
  {#snippet template()}
    <TreemapChart
      data={porteTreemapData5}
      height={260}
      format={formatNum}
      colors={categorical8}
    />
  {/snippet}
</Story>
