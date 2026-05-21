<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import ChoroplethMapRegions from '$lib/components/ChoroplethMapRegions.svelte';

  const regions = {
    'Centro-Oeste': { valor_executado_rs: 125183148.54, populacao: 17071595, perc_valor_executado: 8.630259369900891,  perc_populacao: 8.030526792381826  },
    'Nordeste':     { valor_executado_rs: 448164039.52, populacao: 57112096, perc_valor_executado: 30.89690542560716,  perc_populacao: 26.865692227181054 },
    'Norte':        { valor_executado_rs: 188830083.6,  populacao: 18669345, perc_valor_executado: 13.018146749898552, perc_populacao: 8.782112931962109  },
    'Sudeste':      { valor_executado_rs: 516724465.47, populacao: 88617693, perc_valor_executado: 35.623534092167006, perc_populacao: 41.686014570728005 },
    'Sul':          { valor_executado_rs: 171612588.97, populacao: 31113021, perc_valor_executado: 11.831154362426398, perc_populacao: 14.635653477747004 },
  };

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 0 }).format(v);

  // @ts-ignore
  const formatPerc = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 1/ChoroplethMapRegions',
    component: ChoroplethMapRegions,
    tags: ['autodocs'],
  });
</script>

<Story name="Valor Executado por Região">
  {#snippet template()}
    <ChoroplethMapRegions
      {regions}
      metric="valor_executado_rs"
      format={formatBRL}
      formatLine2={(row) => formatPerc(row.perc_valor_executado)}
    />
  {/snippet}
</Story>

<Story name="Percentual da População">
  {#snippet template()}
    <ChoroplethMapRegions
      {regions}
      metric="perc_populacao"
      format={(v) => formatPerc(v)}
    />
  {/snippet}
</Story>
