<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DonutChart, colorScales, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import { pfPjDonutData, totalBeneficiarios } from '$lib/data/section3';

  // @ts-ignore
  const formatNum = (v) => v.toLocaleString('pt-BR');

  const pfPjColors = [colorScales.teal[2], colorScales.orange[2]];

  const { Story } = defineMeta({
    title: 'Section 3/pfPjSplit',
    component: DonutChart,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**A grande maioria é pessoa física**

Dos **${totalBeneficiarios.toLocaleString('pt-BR')} agentes culturais** contemplados pela Política Nacional Aldir Blanc, **80,7% são pessoas físicas** — artistas, músicos, cineastas e demais trabalhadores individuais da cultura.

Apenas **19,3%** correspondem a organizações formais como associações, coletivos e empresas culturais (CNPJ).

Essa proporção é central para interpretar as análises de valor: embora as pessoas físicas representem a esmagadora maioria dos beneficiários, o valor médio recebido por entidade é significativamente maior — reflexo da natureza de projetos institucionais de maior escala.
          `,
        },
      },
    },
  });
</script>

<Story name="Donut — Pessoa Física vs Pessoa Jurídica">
  {#snippet template()}
    <DonutChart
      data={pfPjDonutData}
      colors={pfPjColors}
      centerLabel="total"
      centerValue={totalBeneficiarios.toLocaleString('pt-BR')}
      format={formatNum}
      height={360}
    />
  {/snippet}
</Story>
