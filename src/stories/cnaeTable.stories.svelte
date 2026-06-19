<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import CnaeTable from '$lib/components/CnaeTable.svelte';
  import { top20CnaesQtdTableData, top20CnaesValTableData, cnaesQtdTableHeight, cnaesValTableHeight } from '$lib/data/section3';

  const { Story } = defineMeta({
    title: 'Section 3/cnaeTable',
    component: CnaeTable,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Infográfico: top 20 CNAEs principais das pessoas jurídicas contempladas pela PNAB**

Ranking das 20 atividades econômicas (CNAE principal) entre os CNPJs contemplados pela Aldir Blanc no Ciclo 1.

- Medalhas de **ouro**, **prata** e **bronze** para os três primeiros colocados
- Barra horizontal proporcional à métrica selecionada via prop \`metric\`
- Cores da paleta sniic: teal para quantidade, azul para valor
- Classificação baseada na metodologia CNAE cultural do IBGE (SIIC)
          `,
        },
      },
    },
  });
</script>

<Story name="Top 20 CNAEs — Beneficiarios">
  {#snippet template()}
    <svg width={700} height={cnaesQtdTableHeight}>
      <CnaeTable data={top20CnaesQtdTableData} metric="quantidade" width={700} />
    </svg>
  {/snippet}
</Story>

<Story name="Infografico 1">
  {#snippet template()}
    <svg width={700} height={cnaesValTableHeight}>
      <CnaeTable data={top20CnaesValTableData} metric="valor" width={700} />
    </svg>
  {/snippet}
</Story>
