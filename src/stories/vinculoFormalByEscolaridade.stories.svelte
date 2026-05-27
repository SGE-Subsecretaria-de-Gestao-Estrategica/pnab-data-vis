<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, colorScales, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import { escolaridadeBarData } from '$lib/data/section4';

  // @ts-ignore
  const formatN = (v) => v.toLocaleString('pt-BR');

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalByEscolaridade',
    component: HorizontalBarChart,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Quanto mais estudo, mais vínculo formal**

Entre os beneficiários com vínculo formal, o perfil educacional é elevado: **médio completo / superior incompleto** e **superior completo** concentram juntos mais de 87% do grupo. Apenas 3,2% têm pós-graduação, mas esse grupo recebe proporcionalmente mais — reflexo de remunerações maiores no emprego formal do setor cultural.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras — Beneficiários com vínculo formal por escolaridade">
  {#snippet template()}
    <HorizontalBarChart
      data={escolaridadeBarData}
      color={colorScales.blue[2]}
      format={formatN}
      xLabel="Beneficiários com vínculo formal"
      margin={{ top: 20, right: 60, bottom: 40, left: 260 }}
    />
  {/snippet}
</Story>
