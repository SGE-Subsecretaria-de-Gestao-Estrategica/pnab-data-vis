<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  import { percapitaData } from '$lib/data/section1';

  // @ts-ignore
  const format = (v) =>
    `R$ ${v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

  const { Story } = defineMeta({
    title: 'Section 1/Grafico 2',
    component: HorizontalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Quem recebe mais por habitante? A régua per capita inverte o ranking**

A métrica per capita equaliza a comparação e revela um ranking completamente diferente do ordenado por volume absoluto.

**Amapá (R$ 29,44/hab), Acre (R$ 27,63/hab) e Roraima (R$ 22,96/hab)** lideram — estados pequenos em população que concentraram recursos de forma proporcionalmente mais favorável. Tocantins (R$ 20,36/hab) e Amazonas também ficam acima da média.

No extremo oposto, **Rondônia (R$ 5,06/hab)** — cujo baixo total executado já chamou atenção — confirma ser o grande outlier negativo. Santa Catarina (R$ 10,19/hab) e Rio de Janeiro (R$ 10,81/hab) fecham a lista, mesmo sendo estados com volume absoluto considerável.

São Paulo, que lidera em valor total, cai para uma posição intermediária quando normalizado pela população: R$ 12,09 por habitante.
          `,
        },
      },
    },
  });
</script>

<Story name="Grafico 2">
  {#snippet template()}
    <HorizontalStackedBarChartCustom width={600}
      data={percapitaData}
      keys={['valor_percapita_uf']}
      categoryKey="uf"
      labels={{ valor_percapita_uf: 'Valor per capita (R$)' }}
      colors={[colorScales.blue[2]]}
      {format}
      marginLeft={50}
      showTotalLabel={false}
    />
  {/snippet}
</Story>
