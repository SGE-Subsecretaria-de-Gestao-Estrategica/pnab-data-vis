<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber, SvgExportDecorator } from 'sniic-design-system';
  import { percExecEstados, percExecMunicipios } from '$lib/data/section1';

  const { Story } = defineMeta({
    title: 'Section 1/executedValueTotals',
    component: BigNumber,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**O ponto de partida: quanto o PNAB investiu?**

O Programa Nacional de Atenção Básica (PNAB) transferiu cerca de **R$ 2,85 bilhões** ao longo do período analisado, divididos entre repasses aos governos estaduais (R$ 1,45 bi) e municipais (R$ 1,40 bi).

A taxa de execução foi alta em ambas as esferas: **96,1%** para estados e **93,7%** para municípios — sinalizando que os recursos empenhados, em sua grande maioria, foram de fato aplicados.

Este painel apresenta os grandes números que abrem a narrativa: quanto foi, de fato, investido e com que eficiência.
          `,
        },
      },
    },
    argTypes: {
      value: { control: 'text' },
      suffix: { control: 'text' },
      label: { control: 'text' },
      fontSize: { control: { type: 'range', min: 24, max: 200, step: 4 } },
      color: { control: 'color' },
      shadowColor: { control: 'color' },
      shadowDepth: { control: { type: 'range', min: 0, max: 20, step: 1 } },
    },
  });
</script>

<Story
  name="Estados - Valor Executado (R$)"
  args={{
    value: 'R$ 1,45 bi',
    label: 'Repasses a Estados e DF',
    fontSize: 96,
  }}
/>

<Story
  name="Municípios - Valor Executado (R$)"
  args={{
    value: 'R$ 1,40 bi',
    label: 'Repasses a Municípios e DF',
    fontSize: 96,
  }}
/>

<Story
  name="Estados - % Executado"
  args={{
    value: percExecEstados.toFixed(1),
    suffix: '%',
    fontSize: 96,
  }}
/>

<Story
  name="Municípios - % Executado"
  args={{
    value: percExecMunicipios.toFixed(1),
    suffix: '%',
    fontSize: 96,
  }}
/>
