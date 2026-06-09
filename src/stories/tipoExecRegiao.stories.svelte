<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import {
    tipoExecRegiaoData,
    tipoExecRegiaoKeys,
    tipoExecRegiaoLabels,
  } from '$lib/data/section6';

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 6/tipoExecRegiao',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Tipo de Execução por Região — Fomento Cultural**

Participação percentual do valor estimado por tipo de execução (**Ação Cultural**, **Bolsa** e **Premiação**) dentro do Fomento Cultural, segmentada por região do Brasil e visão nacional.

**Fonte**: \`capitulo_6_grafico_tipo_exec_regiao__2026-06-03_18-36.csv\`
          `,
        },
      },
    },
  });
</script>

<Story name="HorizontalStackedBarChart — tipo de execucao por regiao">
  {#snippet template()}
    <div style="padding-left: 220px;">
      <HorizontalStackedBarChart
        data={tipoExecRegiaoData}
        keys={[...tipoExecRegiaoKeys]}
        labels={tipoExecRegiaoLabels}
        colors={[colorScales.blue[2], colorScales.teal[2], colorScales.orange[2]]}
        format={formatPct}
        showTotalLabel={false}
      />
    </div>
  {/snippet}
</Story>
