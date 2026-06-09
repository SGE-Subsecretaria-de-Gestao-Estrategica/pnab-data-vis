<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  // @ts-ignore
  import {
    pncvOuOutrosData,
    pncvOuOutrosKeys,
    pncvOuOutrosLabels,
  } from '$lib/data/section6';

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 6/pncvOuOutros',
    component: HorizontalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**PNCV vs. Outros — Participação do valor por faixa de repasse municipal**

Compara a participação percentual do valor estimado entre a **Política Nacional de Cultura Viva (PNCV)** e demais despesas ("Outros"), segmentada por faixa de repasse:

- **Brasil** — visão agregada nacional
- **Município recebeu mais de 360 mil reais** — municípios de maior porte de repasse
- **Município recebeu até 360 mil reais** — municípios de menor porte de repasse

**Fonte**: \`capitulo_6_grafico_pncv_ou_outros__2026-06-03_17-52.csv\`
          `,
        },
      },
    },
  });
</script>

<Story name="HorizontalStackedBarChart — PNCV vs Outros por faixa de repasse (teal e blue)">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={pncvOuOutrosData}
      keys={[...pncvOuOutrosKeys]}
      labels={pncvOuOutrosLabels}
      colors={[colorScales.teal[2], colorScales.blue[2]]}
      format={formatPct}
      showTotalLabel={false}
      marginLeft={220}
    />
  {/snippet}
</Story>

<Story name="HorizontalStackedBarChart — PNCV vs Outros por faixa de repasse (orange e blue)">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={pncvOuOutrosData}
      keys={[...pncvOuOutrosKeys]}
      labels={pncvOuOutrosLabels}
      colors={[colorScales.orange[2], colorScales.blue[2]]}
      format={formatPct}
      showTotalLabel={false}
      marginLeft={220}
    />
  {/snippet}
</Story>
