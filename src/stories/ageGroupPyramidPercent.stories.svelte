<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import DonutChartWithLegend from '$lib/components/DonutChartWithLegend.svelte';
  // @ts-ignore
  import { sexoDonutByAgeGroup } from '$lib/data/section3';

  const sexColors = [colorScales.blue[2], colorScales.yellow[2]];

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 3/sexDonutByAgeGroup',
    component: DonutChartWithLegend,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuicao percentual por sexo em cada faixa etaria**

Cada donut mostra a proporcao de homens e mulheres dentro de uma faixa etaria. Nas faixas mais jovens, os homens predominam; a partir dos 55 anos, as mulheres passam a ser maioria.

*Nota: a variavel sexo refere-se ao sexo biologico registrado na base da Receita Federal.*

**Fonte**: \`aggregate_valor_quantity_by_age_group_sexo_wide.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Donut — 15-24 anos">
  {#snippet template()}
    <DonutChartWithLegend
      data={sexoDonutByAgeGroup[0].donutData}
      colors={sexColors}
      centerLabel={sexoDonutByAgeGroup[0].faixa}
      centerValue={sexoDonutByAgeGroup[0].total.toLocaleString('pt-BR')}
      format={formatPct}
      height={360}
    />
  {/snippet}
</Story>

<Story name="Donut — 25-54 anos">
  {#snippet template()}
    <DonutChartWithLegend
      data={sexoDonutByAgeGroup[1].donutData}
      colors={sexColors}
      centerLabel={sexoDonutByAgeGroup[1].faixa}
      centerValue={sexoDonutByAgeGroup[1].total.toLocaleString('pt-BR')}
      format={formatPct}
      height={360}
    />
  {/snippet}
</Story>

<Story name="Donut — 55-64 anos">
  {#snippet template()}
    <DonutChartWithLegend
      data={sexoDonutByAgeGroup[2].donutData}
      colors={sexColors}
      centerLabel={sexoDonutByAgeGroup[2].faixa}
      centerValue={sexoDonutByAgeGroup[2].total.toLocaleString('pt-BR')}
      format={formatPct}
      height={360}
    />
  {/snippet}
</Story>

<Story name="Donut — 65+ anos">
  {#snippet template()}
    <DonutChartWithLegend
      data={sexoDonutByAgeGroup[3].donutData}
      colors={sexColors}
      centerLabel={sexoDonutByAgeGroup[3].faixa}
      centerValue={sexoDonutByAgeGroup[3].total.toLocaleString('pt-BR')}
      format={formatPct}
      height={360}
    />
  {/snippet}
</Story>
