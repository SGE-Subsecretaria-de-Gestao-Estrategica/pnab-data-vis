<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  import {
    porteCpfCnpjStackedData,
    porteCpfCnpjKeys,
    porteCpfCnpjLabels,
  } from '$lib/data/section1';

  // @ts-ignore
  const formatPerc = (v) => `${v.toFixed(1)}%`;

  const cpfCnpjColors = [colorScales.blue[2], colorScales.yellow[2]];

  const { Story } = defineMeta({
    title: 'Section 3/Grafico 17',
    component: HorizontalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**CPF vs CNPJ: proporção do valor executado por porte municipal**

A distribuição entre Pessoa Física (CPF) e Pessoa Jurídica (CNPJ) varia conforme o porte do município. Municípios menores tendem a concentrar uma fatia maior do recurso em CPF, enquanto os de grande porte apresentam maior participação de CNPJ — reflexo da maior densidade de organizações culturais formalizadas.
          `,
        },
      },
    },
  });
</script>

<Story name="Stacked — CPF vs CNPJ por Porte Populacional">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={porteCpfCnpjStackedData}
      keys={porteCpfCnpjKeys}
      categoryKey="label"
      labels={porteCpfCnpjLabels}
      colors={cpfCnpjColors}
      format={formatPerc}
      showTotalLabel={false}
      marginLeft={120}
    />
  {/snippet}
</Story>
