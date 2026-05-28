<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, categorical8 } from 'sniic-design-system';
  import { rankingData } from '$lib/data/section1';

  // @ts-ignore
  const format = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency', currency: 'BRL',
      notation: 'compact', maximumFractionDigits: 1,
    }).format(v);

  const { Story } = defineMeta({
    title: 'Section 1/rankingByState',
    component: HorizontalBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**O ranking dos estados: SP muito à frente de todos**

O gráfico de barras deixa explícita a hierarquia: São Paulo aparece isolado no topo, seguido de Minas Gerais, Rio de Janeiro, Ceará e Bahia. A diferença visual entre os cinco primeiros e o restante do país é marcante.

No extremo oposto, **Rondônia** registrou apenas R$ 467 mil executados — um valor tão baixo que mal aparece na escala. Isso não é apenas uma anomalia estatística: é um sinal de que a execução naquele estado enfrentou barreiras estruturais específicas.

O ranking por valor absoluto é um primeiro recorte necessário — mas esconde o fato de que estados grandes naturalmente terão volumes maiores. A próxima análise traz a perspectiva per capita para nivelar a comparação.
          `,
        },
      },
    },
  });
</script>

<Story name="Ranking — Valor executado por estado">
  {#snippet template()}
    <HorizontalBarChart
      data={rankingData}
      color={categorical8[0]}
      {format}
      xLabel="Valor executado (R$)"
      margin={{ top: 20, right: 40, bottom: 40, left: 50 }}
    />
  {/snippet}
</Story>
