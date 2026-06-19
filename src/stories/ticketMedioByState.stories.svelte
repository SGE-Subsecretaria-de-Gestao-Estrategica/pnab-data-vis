<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import ExecutedValueByStateMap from '$lib/components/ExecutedValueByStateMap.svelte';
  import { mediaValorByState } from '$lib/data/section2';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(v);

  const { Story } = defineMeta({
    title: 'Section 2/ticketMedioByState',
    component: ExecutedValueByStateMap,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Ticket médio por estado: quanto cada contemplado recebeu em média?**

O mapa mostra o valor médio por pagamento em cada estado. A tonalidade mais intensa indica um ticket médio mais elevado.

Estados do Centro-Oeste e do Sudeste concentraram os maiores valores médios por contemplado, enquanto estados do Nordeste — que lideraram em quantidade de contemplados — apresentaram tickets médios menores, refletindo uma política de distribuição mais pulverizada.
          `,
        },
      },
    },
  });
</script>

<Story name="Ticket Médio por Estado">
  {#snippet template()}
    <div style="font-family: 'Space Grotesk', system-ui, sans-serif;">
      <ExecutedValueByStateMap
        states={mediaValorByState}
        metric="media_aparada_1pct_valor"
        label="Ticket médio (R$) pago por unidade federativa"
        format={formatBRL}
        showSideLegend={true}
        legCols={2}
        mapFrac={0.72}
      />
    </div>
  {/snippet}
</Story>
