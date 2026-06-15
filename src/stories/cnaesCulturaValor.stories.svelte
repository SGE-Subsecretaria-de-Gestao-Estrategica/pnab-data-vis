<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import CnaeTable from '$lib/components/CnaeTable.svelte';
  import { top20CnaesCulturaValTableData, cnaesCulturaValTableHeight } from '$lib/data/section3';

  const { Story } = defineMeta({
    title: 'Section 3/CNAEs Culturais — Valor Repassado',
    component: CnaeTable,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Top 20 CNAEs culturais das pessoas juridicas contempladas — por % do valor repassado**

Ranking das 20 atividades economicas culturais (CNAE principal) entre os CNPJs contemplados pela Aldir Blanc no Ciclo 1, ordenado pelo percentual do valor total repassado.
          `,
        },
      },
    },
  });
</script>

<Story name="Top 20 CNAEs Culturais — Valor Repassado">
  {#snippet template()}
    <svg width={700} height={cnaesCulturaValTableHeight}>
      <CnaeTable data={top20CnaesCulturaValTableData} metric="valor" width={700} />
    </svg>
  {/snippet}
</Story>
