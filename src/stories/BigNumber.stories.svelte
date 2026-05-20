<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber } from 'sniic-design-system';

  // Data from data/section_1/bignumber1.csv
  const data = {
    estados_df: 1450514327,
    municipios_df: 1395481268,
    perc_executado_estados: 0.9606055145695365,
    perc_executado_municipios: 0.9365646093959732,
  };

  const { Story } = defineMeta({
    title: 'Section 1/BigNumber',
    component: BigNumber,
    tags: ['autodocs'],
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
    value: (data.perc_executado_estados * 100).toFixed(1),
    suffix: '%',
    label: 'Execução Estados e DF',
    fontSize: 96,
  }}
/>

<Story
  name="Municípios - % Executado"
  args={{
    value: (data.perc_executado_municipios * 100).toFixed(1),
    suffix: '%',
    label: 'Execução Municípios e DF',
    fontSize: 96,
  }}
/>
