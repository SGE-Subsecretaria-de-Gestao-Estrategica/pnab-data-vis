<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber, DivergingBarChart, HorizontalStackedBarChart, colorPairs, colorScales } from 'sniic-design-system';
  import {
    specialData,
    percRecursoEspecial,
    percPopulacaoEspecial,
    specialDivergingData,
    specialStackedData,
  } from '$lib/data/section1';

  // Individual territory values (Favela, Quilombola, Indígena)
  const favela    = specialData.find((d) => d.territorio === 'Favela e Comunidade Urbana');
  const quilombola = specialData.find((d) => d.territorio === 'Agrupamento quilombola');
  const indigena  = specialData.find((d) => d.territorio === 'Agrupamento indígena');

  const { Story } = defineMeta({
    title: 'Section 1/specialTerritory',
    component: BigNumber,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**A pergunta mais difícil: o programa chegou a quem mais precisa?**

Favelas, quilombos e territórios indígenas concentram algumas das populações mais vulneráveis do Brasil. O PNAB alcançou esses territórios?

Os dados revelam uma **lacuna de equidade** significativa. **9,53%** da população brasileira vive em territórios especiais (favelas e comunidades urbanas, quilombos e terras indígenas) — mas apenas **5,29%** dos recursos chegaram até eles.

O descompasso é maior nas favelas: **8% da população**, mas apenas **4,85% dos recursos**. Quilombos e territórios indígenas, juntos, somam menos de 1,5% da população e receberam menos de 0,5% do total investido.

O gráfico divergente mostra essa assimetria de forma direta: em todos os territórios especiais, a barra de população (o que a comunidade representa) é maior do que a barra de recursos (o que ela recebeu) — o que significa que todos estão, sistematicamente, **sub-representados** no programa.
          `,
        },
      },
    },
  });
</script>

<!-- ===== Option 1: BigNumber ===== -->

<Story name="BigNumber - % recursos em territórios especiais">
  {#snippet template()}
    <BigNumber
      value={percRecursoEspecial}
      suffix="%"
      fontSize={96}
    />
  {/snippet}
</Story>

<Story name="BigNumber - % população em territórios especiais">
  {#snippet template()}
    <BigNumber
      value={percPopulacaoEspecial}
      suffix="%"
      fontSize={96}
    />
  {/snippet}
</Story>

<Story name="BigNumber - Favela: % recursos">
  {#snippet template()}
    <BigNumber
      value={favela?.perc_recurso.toFixed(2) ?? ''}
      suffix="%"
      fontSize={96}
    />
  {/snippet}
</Story>

<Story name="BigNumber - Favela: % população">
  {#snippet template()}
    <BigNumber
      value={favela?.perc_populacao.toFixed(1) ?? ''}
      suffix="%"
      fontSize={96}
    />
  {/snippet}
</Story>

<!-- ===== Option 2: DivergingBarChart (equity gap) ===== -->

<Story name="DivergingBarChart - Lacuna de equidade (blueTeal)">
  {#snippet template()}
    <div style="overflow: hidden;">
      <div style="margin-left: -80px; width: calc(100% + 80px);">
        <DivergingBarChart
          data={specialDivergingData}
          leftLabel="% população no território"
          rightLabel="% do total de recursos"
          referenceValue={50}
          referenceLabel="Equidade"
          colors={colorPairs.blueTeal}
        />
      </div>
    </div>
  {/snippet}
</Story>

<Story name="DivergingBarChart - Lacuna de equidade (blueOrange)">
  {#snippet template()}
    <div style="overflow: hidden;">
      <div style="margin-left: -80px; width: calc(100% + 80px);">
        <DivergingBarChart
          data={specialDivergingData}
          leftLabel="% população no território"
          rightLabel="% do total de recursos"
          referenceValue={50}
          referenceLabel="Equidade"
          colors={colorPairs.blueOrange}
        />
      </div>
    </div>
  {/snippet}
</Story>

<Story name="DivergingBarChart - Lacuna de equidade (purpleYellow)">
  {#snippet template()}
    <div style="overflow: hidden;">
      <div style="margin-left: -80px; width: calc(100% + 80px);">
        <DivergingBarChart
          data={specialDivergingData}
          leftLabel="% população no território"
          rightLabel="% do total de recursos"
          referenceValue={50}
          referenceLabel="Equidade"
          colors={colorPairs.purpleYellow}
        />
      </div>
    </div>
  {/snippet}
</Story>

<!-- ===== Option 3: HorizontalStackedBarChart (Estado vs Município) ===== -->

<Story name="HorizontalStackedBarChart - Estado vs Município (valor absoluto)">
  {#snippet template()}
    <div style="padding-left: 100px;">
      <HorizontalStackedBarChart
        data={specialStackedData}
        keys={['valor_estado', 'valor_municipio']}
        categoryKey="shortLabel"
        labels={{ valor_estado: 'Governo Estadual', valor_municipio: 'Governo Municipal' }}
        colors={[colorScales.blue[2], colorScales.red[2]]}
        format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
        showTotalLabel={true}
      />
    </div>
  {/snippet}
</Story>

<Story name="HorizontalStackedBarChart - Estado vs Município (teal/orange)">
  {#snippet template()}
    <div style="padding-left: 100px;">
      <HorizontalStackedBarChart
        data={specialStackedData}
        keys={['valor_estado', 'valor_municipio']}
        categoryKey="shortLabel"
        labels={{ valor_estado: 'Governo Estadual', valor_municipio: 'Governo Municipal' }}
        colors={[colorScales.teal[2], colorScales.orange[2]]}
        format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
        showTotalLabel={true}
      />
    </div>
  {/snippet}
</Story>
