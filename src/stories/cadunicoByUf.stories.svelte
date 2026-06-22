<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import HorizontalBarChartCustom from '$lib/components/HorizontalBarChartCustom.svelte';
  // @ts-ignore
  import { cadunicoUfData } from '$lib/data/section5';

  const { Story } = defineMeta({
    title: 'Section 5/cadunicoByUf',
    component: HorizontalBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Taxa de penetração do CadÚnico por UF**

Para cada unidade federativa, mostra o percentual dos contemplados pela Aldir Blanc que estão inscritos no CadÚnico. Estados do Nordeste e Norte tendem a apresentar maior penetração, reflexo da maior vulnerabilidade socioeconômica nessas regiões.

**Fonte**: \`aggregate_cadunico_by_uf.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="HorizontalBarChart — % CadÚnico por UF (teal)">
  {#snippet template()}
    <HorizontalBarChartCustom width={600}
      data={cadunicoUfData}
      color={colorScales.teal[2]}
      format={(v) => `${v.toFixed(1)}%`}
      xLabel="% dos contemplados da UF no CadÚnico"
      rowHeight={52}
      margin={{ top: 20, right: 80, bottom: 40, left: 50 }}
    />
  {/snippet}
</Story>

<Story name="HorizontalBarChart — % CadÚnico por UF (blue)">
  {#snippet template()}
    <HorizontalBarChart
      data={cadunicoUfData}
      color={colorScales.orange[2]}
      rowHeight={52}
      format={(v) => `${v.toFixed(1)}%`}
      xLabel="% dos contemplados da UF no CadÚnico"
      margin={{ top: 20, right: 80, bottom: 40, left: 50 }}
    />
  {/snippet}
</Story>
