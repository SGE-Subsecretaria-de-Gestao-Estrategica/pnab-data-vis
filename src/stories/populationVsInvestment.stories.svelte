<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BubbleChart, categorical8 } from 'sniic-design-system';
  import { bubbleStateData } from '$lib/data/section1';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency', currency: 'BRL',
      notation: 'compact', maximumFractionDigits: 0,
    }).format(v);

  // @ts-ignore
  const formatPop = (v) =>
    new Intl.NumberFormat('pt-BR', { notation: 'compact', maximumFractionDigits: 1 }).format(v);

  const { Story } = defineMeta({
    title: 'Section 1/populationVsInvestment',
    component: BubbleChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Tamanho vs proporcionalidade: quem recebe além do que justifica sua população?**

Volume absoluto importa menos do que proporcionalidade. Este gráfico cruza a **população total** de cada estado com o **valor executado**, colorindo cada bolha pela região.

Estados próximos à linha de tendência receberam de forma relativamente proporcional ao seu tamanho. **Bolhas acima** da tendência receberam mais per capita; **abaixo**, menos.

Chama atenção que vários estados do Norte e Nordeste aparecem acima da diagonal — CE, MA, PA e AL, por exemplo. Já SC e PR ficam consistentemente abaixo. Isso sugere que o programa, em alguma medida, favorece estados de maior vulnerabilidade histórica — mas os dados dos próximos gráficos testam essa hipótese com mais precisão.
          `,
        },
      },
    },
  });
</script>

<Story name="Bubble — População vs Investimento por estado">
  {#snippet template()}
    <BubbleChart
      data={bubbleStateData}
      xLabel="População total"
      yLabel="Valor executado (R$)"
      sizeLabel="Entes contemplados"
      yFormat={formatBRL}
      xFormat={formatPop}
      colors={categorical8}
    />
  {/snippet}
</Story>
