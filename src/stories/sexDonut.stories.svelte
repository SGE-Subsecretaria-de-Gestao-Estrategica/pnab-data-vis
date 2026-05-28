<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DonutChart, colorPairs, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import { sexoQuantityDonutData, sexoValueDonutData, totalPF, valorTotalPF } from '$lib/data/section3';

  // @ts-ignore
  const formatNum = (v) => v.toLocaleString('pt-BR');
  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);

  // feminino=purple, masculino=blue
  const sexColors = [colorPairs.bluePurple[1], colorPairs.bluePurple[0]];

  const { Story } = defineMeta({
    title: 'Section 3/sexDonut',
    component: DonutChart,
    tags: ['autodocs'],
    decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição por sexo — quantidade e valor**

Entre as **${totalPF.toLocaleString('pt-BR')} pessoas físicas** contempladas, os homens representam **53,2%** e as mulheres, **46,8%**. Quando olhamos o valor recebido, a proporção é muito semelhante: **53,9%** para homens e **46,1%** para mulheres.

Os dois donuts permitem comparar as distribuições por quantidade de agentes e por valor recebido, revelando que não há diferença expressiva entre as duas dimensões.

*Nota: a variável sexo refere-se ao sexo biológico registrado na base da Receita Federal.*

**Fonte**: \`aggregate_contemplados_by_sexo_proportion.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Donut — distribuição por quantidade de agentes">
  {#snippet template()}
    <DonutChart
      data={sexoQuantityDonutData}
      colors={sexColors}
      centerLabel="PF contemplados"
      centerValue={totalPF.toLocaleString('pt-BR')}
      format={formatNum}
      height={360}
    />
  {/snippet}
</Story>

<Story name="Donut — distribuição por valor recebido">
  {#snippet template()}
    <DonutChart
      data={sexoValueDonutData}
      colors={sexColors}
      centerLabel="valor total"
      centerValue={formatBRL(valorTotalPF)}
      format={formatBRL}
      height={360}
    />
  {/snippet}
</Story>
