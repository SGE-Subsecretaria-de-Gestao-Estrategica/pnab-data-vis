<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, TreemapChart, categorical8 } from 'sniic-design-system';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  // @ts-ignore
  import { racaCorBarData, racaCorGroupedData, racaCorTreemapData, racaCorTreemapValorData } from '$lib/data/section4';

  // @ts-ignore
  const formatN = (v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const racaLegend = racaCorTreemapData.children.map((d, i) => ({
    label: d.name,
    color: categorical8[i % categorical8.length],
  }));

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalByRaca',
    component: HorizontalBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Pardos e brancos dominam o emprego formal no setor cultural**

Entre os beneficiários com vínculo formal, **pardos** respondem por 44,9% e **brancos** por 30,3%. **Pretos/negros** representam apenas 9,6% — desproporcionalmente baixo em relação à presença na população geral.

O treemap torna visível a concentração: Parda e Branca juntas ocupam mais de três quartos do espaço.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras — Beneficiários com vínculo formal por raça/cor">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={racaCorGroupedData}
      seriesLabels={['PNAB', 'Brasil (RAIS 2024)']}
      colors={[categorical8[0], '#cb4034']}
      format={formatN}
      xLabel="% do total de trabalhadores formais"
      margin={{ top: 20, right: 60, bottom: 40, left: 120 }}
    />
  {/snippet}
</Story>

<Story name="Treemap — Proporção por raça/cor">
  {#snippet template()}
    <div style="display:flex; flex-direction:column; gap:12px;">
      <TreemapChart
        data={racaCorTreemapData}
        height={380}
        format={formatN}
        colors={categorical8}
      />
      <div style="display:flex; flex-wrap:wrap; gap:16px; padding:0 8px;">
        {#each racaLegend as item}
          <span style="display:flex; align-items:center; gap:6px; font-size:13px; font-family:system-ui, sans-serif;">
            <span style="display:inline-block; width:12px; height:12px; border-radius:2px; background:{item.color};"></span>
            {item.label}
          </span>
        {/each}
      </div>
    </div>
  {/snippet}
</Story>

<Story name="Treemap — Valor pago por raça/cor">
  {#snippet template()}
    <div style="display:flex; flex-direction:column; gap:12px;">
      <TreemapChart
        data={racaCorTreemapValorData}
        height={380}
        format={formatN}
        colors={categorical8}
      />
      <div style="display:flex; flex-wrap:wrap; gap:16px; padding:0 8px;">
        {#each racaLegend as item}
          <span style="display:flex; align-items:center; gap:6px; font-size:13px; font-family:system-ui, sans-serif;">
            <span style="display:inline-block; width:12px; height:12px; border-radius:2px; background:{item.color};"></span>
            {item.label}
          </span>
        {/each}
      </div>
    </div>
  {/snippet}
</Story>
