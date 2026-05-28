<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart } from 'sniic-design-system';
  // @ts-ignore
  import { ufByRegionGroups, ageGroupKeys, ageGroupLabels } from '$lib/data/section4';

  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;
  // @ts-ignore
  const formatPctN = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalByRegionCorr',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Correlação região — UF: informalidade no setor cultural**

Cada região recebe uma família de cores própria (tons mais claros = sem vínculo formal; tons mais escuros = com vínculo formal).

O **Nordeste** lidera a informalidade com quase 60% de beneficiários sem vínculo. Dentro da região, Piauí (66,9%), Pernambuco e Paraíba concentram os maiores índices. No outro extremo, **Amapá, Acre e Rondônia**, no Norte, apresentam a maior proporção de trabalhadores formais.
          `,
        },
      },
    },
  });
</script>

<Story name="Comparativo por região — informalidade com cores regionais">
  {#snippet template()}
    <div style="display: flex; flex-direction: column; gap: 0.75rem; padding: 1rem;">
      {#each ufByRegionGroups as { regiao, colors, avgInformal }}
        <div style="display: grid; grid-template-columns: 9rem 1fr 12rem; align-items: center; gap: 0.75rem;">
          <span style="font-size: 0.9rem; font-weight: 600; text-align: right;">{regiao}</span>
          <div style="display: flex; height: 28px; border-radius: 4px; overflow: hidden;">
            <div style="width: {avgInformal}%; background: {colors[0]};"></div>
            <div style="width: {100 - avgInformal}%; background: {colors[1]};"></div>
          </div>
          <span style="font-size: 0.78rem; opacity: 0.65;">{formatPctN(avgInformal)} sem vínculo</span>
        </div>
      {/each}
    </div>
  {/snippet}
</Story>

<Story name="Por UF agrupado por região — barras empilhadas com cores regionais">
  {#snippet template()}
    <div style="display: flex; flex-direction: column; gap: 2rem; padding: 1rem;">
      {#each ufByRegionGroups as { regiao, colors, avgInformal, data }}
        <div>
          <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
            <span style="display: inline-block; width: 12px; height: 12px; border-radius: 3px; background: {colors[1]};"></span>
            <strong>{regiao}</strong>
            <span style="font-size: 0.8rem; opacity: 0.6; margin-left: auto;">média: {formatPctN(avgInformal)} sem vínculo</span>
          </div>
          <HorizontalStackedBarChart
            {data}
            keys={[...ageGroupKeys]}
            labels={ageGroupLabels}
            {colors}
            format={formatPct}
            showTotalLabel={false}
          />
        </div>
      {/each}
    </div>
  {/snippet}
</Story>
