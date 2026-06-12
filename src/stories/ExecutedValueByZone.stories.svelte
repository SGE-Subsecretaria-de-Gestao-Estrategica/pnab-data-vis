<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart, colorScales } from 'sniic-design-system';
  // import { zoneData, zoneMunicipalityData } from '$lib/data/section1'; // CSVs faltantes: executed_value_zone_by_state/uf.csv

  const redBlue = [colorScales.red[2], colorScales.blue[2]];

  const stateFlags = Object.fromEntries(
    ['AC','AL','AM','AP','BA','CE','DF','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']
      .map((uf) => [uf, `/flags/states/${uf}.svg`])
  );

  const { Story } = defineMeta({
    title: 'Section 1/executedValueByZone',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Urbano vs rural: o campo ainda fica para trás**

Em todas as unidades federativas, o investimento **urbano é amplamente dominante**. Mesmo nos estados com perfil mais rural, a zona urbana concentra a esmagadora maioria dos recursos.

O gráfico ordena os estados pela **proporção de recursos rurais** — e mesmo os primeiros colocados dificilmente ultrapassam 15% de participação rural no total.

**Tocantins, Paraíba e Acre** aparecem com as maiores fatias rurais entre os estados. Já **Rondônia e Distrito Federal** têm as menores proporções.

Este padrão levanta questões estruturais sobre o alcance do programa em zonas rurais — especialmente em estados como Maranhão, Piauí e Pará, que têm grandes populações rurais mas investimentos fortemente concentrados nas cidades.
          `,
        },
      },
    },
  });
</script>

<!-- DISABLED: executed_value_zone_by_state/uf.csv faltantes
<Story name="Proporção Urbano/Rural por UF (Total UF)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={zoneData}
      keys={['valor_rural', 'valor_urbano']}
      categoryKey="label"
      labels={{ valor_urbano: 'Urbano', valor_rural: 'Rural' }}
      colors={redBlue}
      format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
      showTotalLabel={true}
    />
  {/snippet}
</Story>

<Story name="Proporção Urbano/Rural por UF (Municípios)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={zoneMunicipalityData}
      keys={['valor_rural', 'valor_urbano']}
      categoryKey="label"
      labels={{ valor_urbano: 'Urbano', valor_rural: 'Rural' }}
      colors={redBlue}
      format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
      showTotalLabel={true}
    />
  {/snippet}
</Story>

<Story name="Proporção Urbano/Rural por UF com Bandeiras (Total UF)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={zoneData}
      keys={['valor_rural', 'valor_urbano']}
      categoryKey="label"
      labels={{ valor_urbano: 'Urbano', valor_rural: 'Rural' }}
      colors={redBlue}
      format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
      showTotalLabel={true}
      icons={stateFlags}
      iconSize={20}
    />
  {/snippet}
</Story>

<Story name="Proporção Urbano/Rural por UF com Bandeiras (Municípios)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={zoneMunicipalityData}
      keys={['valor_rural', 'valor_urbano']}
      categoryKey="label"
      labels={{ valor_urbano: 'Urbano', valor_rural: 'Rural' }}
      colors={redBlue}
      format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
      showTotalLabel={true}
      icons={stateFlags}
      iconSize={20}
    />
  {/snippet}
</Story>
-->
