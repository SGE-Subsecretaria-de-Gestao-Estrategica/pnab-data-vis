<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { cadunicoUfData } from '$lib/data/section5';

  const { Story } = defineMeta({
    title: 'Section 5/cadunicoByUf',
    component: HorizontalBarChart,
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
    <HorizontalBarChart
      data={cadunicoUfData}
      color={colorScales.teal[2]}
      format={(v) => `${v.toFixed(1)}%`}
      xLabel="% dos contemplados da UF no CadÚnico"
      margin={{ top: 20, right: 80, bottom: 40, left: 50 }}
    />
  {/snippet}
</Story>

<Story name="HorizontalBarChart — % CadÚnico por UF (blue)">
  {#snippet template()}
    <HorizontalBarChart
      data={cadunicoUfData}
      color={colorScales.blue[2]}
      format={(v) => `${v.toFixed(1)}%`}
      xLabel="% dos contemplados da UF no CadÚnico"
      margin={{ top: 20, right: 80, bottom: 40, left: 50 }}
    />
  {/snippet}
</Story>
