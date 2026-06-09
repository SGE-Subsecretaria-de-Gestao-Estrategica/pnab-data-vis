<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import {
    pncvNatJuridicaData,
    pncvNatJuridicaKeys,
    pncvNatJuridicaLabels,
  } from '$lib/data/section6';

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 6/pncvNatJuridica',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição por Modalidade e Natureza Jurídica — PNCV**

Participação percentual entre **CNPJ** e **CPF** dentro de cada modalidade da Política Nacional de Cultura Viva:

- **Ação Cultural** — predominância de CNPJ (~82%)
- **Prêmio** — distribuição equilibrada entre CNPJ e CPF (~50%/50%)

**Fonte**: \`capitulo_6_grafico_5.csv\`
          `,
        },
      },
    },
  });
</script>

<Story name="HorizontalStackedBarChart — PNCV por Modalidade e Natureza Jurídica (blue e orange)">
  {#snippet template()}
    <div style="padding-left: 220px;">
      <HorizontalStackedBarChart
        data={pncvNatJuridicaData}
        keys={[...pncvNatJuridicaKeys]}
        labels={pncvNatJuridicaLabels}
        colors={[colorScales.blue[2], colorScales.orange[2]]}
        format={formatPct}
        showTotalLabel={false}
      />
    </div>
  {/snippet}
</Story>

<Story name="HorizontalStackedBarChart — PNCV por Modalidade e Natureza Jurídica (teal e orange)">
  {#snippet template()}
    <div style="padding-left: 220px;">
      <HorizontalStackedBarChart
        data={pncvNatJuridicaData}
        keys={[...pncvNatJuridicaKeys]}
        labels={pncvNatJuridicaLabels}
        colors={[colorScales.teal[2], colorScales.orange[2]]}
        format={formatPct}
        showTotalLabel={false}
      />
    </div>
  {/snippet}
</Story>
