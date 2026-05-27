<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DivergingBarChart, colorPairs, SvgExportDecorator } from 'sniic-design-system';
  import { ufSplitData } from '$lib/data/section1';

  const { Story } = defineMeta({
    title: 'Section 1/executedValueByUfDiverging',
    component: DivergingBarChart,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Estado ou município? A divisão federativa dos recursos**

Os repasses do PNAB chegam por dois caminhos: diretamente ao **governo estadual** ou aos **municípios**. A proporção entre essas duas vias varia enormemente de estado para estado.

**Rondônia** é o caso extremo municipal: 94,7% dos recursos foram executados pelos municípios, com o governo estadual respondendo por apenas 5,3% — uma anomalia que pode explicar a baixíssima execução total do estado, já que a gestão estadual quase não atuou.

No outro extremo, **Roraima** concentrou 90,6% dos recursos na esfera estadual.

A maioria dos estados mantém uma divisão relativamente equilibrada, próxima de 50/50. Santa Catarina, Minas Gerais, Bahia e Rio de Janeiro são os estados onde os municípios respondem pela maior parte — acima de 54%.
          `,
        },
      },
    },
  });
</script>

<Story name="blueOrange">
  {#snippet template()}
    <div style="overflow: hidden;">
      <div style="margin-left: -80px; width: calc(100% + 80px);">
        <DivergingBarChart
          data={ufSplitData}
          leftLabel="Estado"
          rightLabel="Município"
          referenceValue={50}
          referenceLabel=" "
          colors={colorPairs.blueOrange}
        />
      </div>
    </div>
  {/snippet}
</Story>

<Story name="bluePurple">
  {#snippet template()}
    <div style="overflow: hidden;">
      <div style="margin-left: -80px; width: calc(100% + 80px);">
        <DivergingBarChart
          data={ufSplitData}
          leftLabel="Estado"
          rightLabel="Município"
          referenceValue={50}
          referenceLabel=" "
          colors={colorPairs.bluePurple}
        />
      </div>
    </div>
  {/snippet}
</Story>

<Story name="blueTeal">
  {#snippet template()}
    <div style="overflow: hidden;">
      <div style="margin-left: -80px; width: calc(100% + 80px);">
        <DivergingBarChart
          data={ufSplitData}
          leftLabel="Estado"
          rightLabel="Município"
          referenceValue={50}
          referenceLabel=" "
          colors={colorPairs.blueTeal}
        />
      </div>
    </div>
  {/snippet}
</Story>

<Story name="tealYellow">
  {#snippet template()}
    <div style="overflow: hidden;">
      <div style="margin-left: -80px; width: calc(100% + 80px);">
        <DivergingBarChart
          data={ufSplitData}
          leftLabel="Estado"
          rightLabel="Município"
          referenceValue={50}
          referenceLabel=" "
          colors={colorPairs.tealYellow}
        />
      </div>
    </div>
  {/snippet}
</Story>

<Story name="purpleYellow">
  {#snippet template()}
    <div style="overflow: hidden;">
      <div style="margin-left: -80px; width: calc(100% + 80px);">
        <DivergingBarChart
          data={ufSplitData}
          leftLabel="Estado"
          rightLabel="Município"
          referenceValue={50}
          referenceLabel=" "
          colors={colorPairs.purpleYellow}
        />
      </div>
    </div>
  {/snippet}
</Story>

<Story name="limeRed">
  {#snippet template()}
    <div style="overflow: hidden;">
      <div style="margin-left: -80px; width: calc(100% + 80px);">
        <DivergingBarChart
          data={ufSplitData}
          leftLabel="Estado"
          rightLabel="Município"
          referenceValue={50}
          referenceLabel=" "
          colors={colorPairs.limeRed}
        />
      </div>
    </div>
  {/snippet}
</Story>
