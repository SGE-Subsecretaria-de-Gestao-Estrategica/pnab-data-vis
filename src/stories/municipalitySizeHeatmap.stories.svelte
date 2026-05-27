<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HeatMap, colorScales, SvgExportDecorator } from 'sniic-design-system';
  import { heatmapData, heatmapBuckets } from '$lib/data/section1';

  const { Story } = defineMeta({
    title: 'Section 1/municipalityValueHeatmap',
    component: HeatMap,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Onde estão os municípios beneficiados? O cruzamento entre estado e faixa de valor pago**

Este mapa de calor cruza dois eixos: os **estados** (ordenados pelo valor total executado, do maior ao menor) e as **faixas de valor pago por município** (de até R$2 mil a mais de R$10 milhões).

Cada célula mostra quantos municípios foram contemplados naquela combinação — e a intensidade da cor indica a concentração.

Alguns padrões chamam atenção:
- A massa dos municípios se concentra nas faixas **R$2–10k** e **R$10–50k**, típicas de pequenas cidades.
- **MG** e **BA** dominam as faixas intermediárias pelo volume de municípios atendidos.
- Repasses acima de **R$500 mil** ficam restritos a estados com maior base urbana, como **SP** e **RJ**.
- Estados menores tendem a apresentar distribuição mais estreita, concentrada em poucas faixas de valor.

O mapa evidencia que o perfil de distribuição de valores varia enormemente entre estados — e que não existe um valor típico do PNAB.
          `,
        },
      },
    },
  });
</script>

<Story name="Heatmap — Estados por faixa de valor pago">
  {#snippet template()}
    <HeatMap
      data={heatmapData}
      height={820}
      colorRange={colorScales.blue}
      xLabel="Faixa de valor pago"
      yLabel="Estado (UF)"
      format={(v) => v > 0 ? String(v) : ''}
      showValues={true}
      showLegend={true}
      cellRadius={2}
      cellGap={3}
    />
  {/snippet}
</Story>

<Story name="Heatmap — Teal (sem valores)">
  {#snippet template()}
    <HeatMap
      data={heatmapData}
      height={820}
      colorRange={colorScales.teal}
      xLabel="Faixa de valor pago"
      yLabel="Estado (UF)"
      format={(v) => String(v)}
      showValues={false}
      showLegend={true}
      cellRadius={2}
      cellGap={3}
    />
  {/snippet}
</Story>
