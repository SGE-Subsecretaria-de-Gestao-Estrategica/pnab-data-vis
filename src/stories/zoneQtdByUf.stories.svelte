<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { VerticalStackedBarChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { zoneQtdData } from '$lib/data/section1';

  const { Story } = defineMeta({
    title: 'Section 1/zoneQtdByUf',
    component: VerticalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Agentes contemplados: urbano vs rural por UF**

Cada barra representa um estado, normalizada a 100%, mostrando a proporção de agentes culturais contemplados em zona **urbana** vs **rural**. Os estados estão ordenados pela maior participação rural (da esquerda para a direita).

O padrão é consistente: em todos os estados, a maioria esmagadora dos beneficiários está na zona urbana. Mesmo os estados com maior proporção rural raramente ultrapassam 15% dos contemplados. Isso complementa o olhar sobre o valor financeiro e confirma que o alcance do programa nas zonas rurais é estruturalmente limitado.

**Fonte**: cruzamento de dados de beneficiários PNAB com informação de zona (urbana/rural) da Receita Federal.
          `,
        },
      },
    },
  });
</script>

<Story name="Agentes contemplados por zona (urbano vs rural) por UF">
  {#snippet template()}
    <VerticalStackedBarChart
      data={zoneQtdData}
      keys={['qtde_rural', 'qtde_urbano']}
      labels={{ qtde_urbano: 'Urbano', qtde_rural: 'Rural' }}
      colors={[colorScales.red[2], colorScales.blue[2]]}
      normalize={true}
      height={320}
      sortDirection="desc"
    />
  {/snippet}
</Story>
