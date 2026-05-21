<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart } from 'sniic-design-system';

  // Data from data/section_1/executed_value_by_uf.csv
  const chartData = [
    { uf: 'AC', valor_percapita_uf: 27.63 },
    { uf: 'AL', valor_percapita_uf: 18.72 },
    { uf: 'AM', valor_percapita_uf: 17.31 },
    { uf: 'AP', valor_percapita_uf: 29.44 },
    { uf: 'BA', valor_percapita_uf: 11.91 },
    { uf: 'CE', valor_percapita_uf: 14.80 },
    { uf: 'DF', valor_percapita_uf: 13.80 },
    { uf: 'ES', valor_percapita_uf: 13.59 },
    { uf: 'GO', valor_percapita_uf: 14.35 },
    { uf: 'MA', valor_percapita_uf: 16.39 },
    { uf: 'MG', valor_percapita_uf: 12.59 },
    { uf: 'MS', valor_percapita_uf: 14.59 },
    { uf: 'MT', valor_percapita_uf: 12.61 },
    { uf: 'PA', valor_percapita_uf: 14.32 },
    { uf: 'PB', valor_percapita_uf: 16.94 },
    { uf: 'PE', valor_percapita_uf: 14.83 },
    { uf: 'PI', valor_percapita_uf: 16.97 },
    { uf: 'PR', valor_percapita_uf: 12.96 },
    { uf: 'RJ', valor_percapita_uf: 10.81 },
    { uf: 'RN', valor_percapita_uf: 15.69 },
    { uf: 'RO', valor_percapita_uf: 5.06 },
    { uf: 'RR', valor_percapita_uf: 22.96 },
    { uf: 'RS', valor_percapita_uf: 13.46 },
    { uf: 'SC', valor_percapita_uf: 10.19 },
    { uf: 'SE', valor_percapita_uf: 17.65 },
    { uf: 'SP', valor_percapita_uf: 12.09 },
    { uf: 'TO', valor_percapita_uf: 20.36 },
  ];

  const flagModules = import.meta.glob(
    '/node_modules/sniic-design-system/dist/flags/states/*.svg',
    { query: '?url', import: 'default', eager: true }
  );

  // @ts-ignore
  const icons = Object.fromEntries(
    Object.entries(flagModules).map(([path, url]) => {
      const uf = path.split('/').pop().replace('.svg', '');
      return [uf, url];
    })
  );

  // @ts-ignore
  const format = (v) =>
    `R$ ${v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

  const { Story } = defineMeta({
    title: 'Section 1/valuePerCaptaByState',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
  });
</script>

<Story name="Valor per capita por UF (abreviação)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={chartData}
      keys={['valor_percapita_uf']}
      categoryKey="uf"
      labels={{ valor_percapita_uf: 'Valor per capita (R$)' }}
      {format}
    />
  {/snippet}
</Story>

<Story name="Valor per capita por UF (bandeiras)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={chartData}
      keys={['valor_percapita_uf']}
      categoryKey="uf"
      labels={{ valor_percapita_uf: 'Valor per capita (R$)' }}
      {format}
      {icons}
      iconSize={24}
    />
  {/snippet}
</Story>
