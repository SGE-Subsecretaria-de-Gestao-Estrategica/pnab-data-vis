<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, TreemapChart, categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { racaCorBarData, racaCorTreemapData } from '$lib/data/section4';

  // @ts-ignore
  const formatN = (v) => v.toLocaleString('pt-BR');

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalByRaca',
    component: HorizontalBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Pardos e brancos dominam o emprego formal no setor cultural**

Entre os beneficiários com vínculo formal, **pardos** respondem por 44,9% e **brancos** por 30,3%. **Pretos/negros** representam apenas 9,6% — desproporcionalmente baixo em relação à presença na população geral.

O treemap torna visível a concentração: Parda e Branca juntas ocupam mais de três quartos do espaço.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras — Beneficiários com vínculo formal por raça/cor">
  {#snippet template()}
    <HorizontalBarChart
      data={racaCorBarData}
      color={categorical8[0]}
      format={formatN}
      xLabel="Beneficiários com vínculo formal"
      margin={{ top: 20, right: 60, bottom: 40, left: 120 }}
    />
  {/snippet}
</Story>

<Story name="Treemap — Proporção por raça/cor">
  {#snippet template()}
    <TreemapChart
      data={racaCorTreemapData}
      height={380}
      format={formatN}
      colors={categorical8}
    />
  {/snippet}
</Story>
