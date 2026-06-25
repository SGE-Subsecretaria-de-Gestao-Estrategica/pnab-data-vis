<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DivergingBarChart, colorPairs, colorScales } from 'sniic-design-system';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  // @ts-ignore
  import { sexoDivergingData, sexoComparisonStackedData, sexoComparisonStackedKeys, sexoComparisonStackedLabels } from '$lib/data/section4';

  // @ts-ignore
  const formatPctN = (v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalBySexo',
    component: DivergingBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Mulheres são mais afetadas pela informalidade**

Entre as mulheres beneficiárias, **60,1%** não possuem vínculo formal — proporção significativamente maior do que a observada entre os homens (**51,1%**). A informalidade atinge ambos os sexos, mas pesa estruturalmente mais sobre as trabalhadoras do setor cultural.
          `,
        },
      },
    },
  });
</script>

<Story name="Divergente — Sem vs. com vinculo formal por sexo">
  {#snippet template()}
    <DivergingBarChart
      data={sexoDivergingData}
      leftLabel="Sem vínculo formal"
      rightLabel="Com vínculo formal"
      referenceValue={50}
      referenceLabel="50%"
      colors={colorPairs.limeRed}
    />
  {/snippet}
</Story>

<Story name="Grafico 25 — Sexo PNAB vs RAIS">
  {#snippet template()}
    <HorizontalStackedBarChartCustom width={600}
      data={sexoComparisonStackedData}
      keys={[...sexoComparisonStackedKeys]}
      labels={sexoComparisonStackedLabels}
      colors={[colorScales.yellow[2], colorScales.blue[2]]}
      format={formatPctN}
      rowHeight={48}
      labelsAbove
    />
  {/snippet}
</Story>
