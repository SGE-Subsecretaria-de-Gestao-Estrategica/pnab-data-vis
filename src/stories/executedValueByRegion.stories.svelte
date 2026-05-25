<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import ChoroplethMapRegions from '$lib/components/ExecutedValueByRegionMap.svelte';
  import { regions } from '$lib/data/section1';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 0 }).format(v);

  // @ts-ignore
  const formatPerc = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 1/executedValueByRegion',
    component: ChoroplethMapRegions,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**O mapa dos recursos: o programa segue a população?**

Com os totais em mãos, a próxima pergunta é: *onde* o dinheiro chegou?

O mapa revela distribuições que não seguem linearmente o peso demográfico de cada região. O **Sudeste** concentrou **35,6%** dos recursos, mas abriga **41,7%** da população — proporcionalmente, recebeu menos por habitante do que seu tamanho sugere.

Já o **Nordeste**, com 26,9% da população, absorveu 30,9% dos recursos. O **Norte**, a região com menor população relativa (8,8%), captou 13% — uma fatia acima do seu peso demográfico.

Essa assimetria indica que o programa, em certa medida, direciona recursos para além da lógica puramente proporcional — mas será que isso se reflete em equidade de fato?
          `,
        },
      },
    },
  });
</script>

<Story name="Valor Executado por Região">
  {#snippet template()}
    <ChoroplethMapRegions
      {regions}
      metric="valor_executado_rs"
      format={formatBRL}
      formatLine2={(row) => formatPerc(row.perc_valor_executado)}
    />
  {/snippet}
</Story>

<Story name="Percentual da População">
  {#snippet template()}
    <ChoroplethMapRegions
      {regions}
      metric="perc_populacao"
      format={(v) => formatPerc(v)}
    />
  {/snippet}
</Story>
