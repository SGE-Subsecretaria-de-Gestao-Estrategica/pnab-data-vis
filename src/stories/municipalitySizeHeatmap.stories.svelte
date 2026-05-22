<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HeatMap, colorScales } from 'sniic-design-system';
  import { heatmapData, heatmapBuckets } from '$lib/data/section1';

  const { Story } = defineMeta({
    title: 'Section 1/municipalitySizeHeatmap',
    component: HeatMap,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Onde estão os municípios beneficiados? O cruzamento entre estado e porte**

Este mapa de calor cruza dois eixos: os **estados** (ordenados pelo valor total executado, do maior ao menor) e as **faixas de porte municipal** (de menos de 2 mil a mais de 10 milhões de habitantes).

Cada célula mostra quantos entes foram contemplados naquela combinação — e a intensidade da cor indica a concentração.

Alguns padrões chamam atenção:
- **MG** tem uma célula muito escura na faixa 10–50k hab, indicando grande número de municípios pequenos atendidos.
- **PE e PB** também mostram forte concentração em municípios de pequeno porte.
- **SP** se destaca nas faixas maiores (200k–1M hab), refletindo sua estrutura urbana.
- **RS** apresenta um padrão incomum, com concentração na faixa 50–200k e ausência na faixa 10–50k.

O mapa evidencia que o perfil de beneficiários varia enormemente entre estados — e que não existe um "município típico" do PNAB.
          `,
        },
      },
    },
  });
</script>

<Story name="Heatmap — Estados por faixa de porte dos municipios">
  {#snippet template()}
    <HeatMap
      data={heatmapData}
      height={820}
      colorRange={colorScales.blue}
      xLabel="Faixa de porte populacional"
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
      xLabel="Faixa de porte populacional"
      yLabel="Estado (UF)"
      format={(v) => String(v)}
      showValues={false}
      showLegend={true}
      cellRadius={2}
      cellGap={3}
    />
  {/snippet}
</Story>
