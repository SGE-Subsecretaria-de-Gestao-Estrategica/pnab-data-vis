<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import CboRaisTable from '$lib/components/CboRaisTable.svelte';
  import { cboRaisTop20, cboRaisTableHeight } from '$lib/data/section4';

  const { Story } = defineMeta({
    title: 'Section 4/cboRaisTable',
    component: CboRaisTable,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Infográfico: top 20 ocupações dos trabalhadores formais contemplados pela PNAB (CBO/RAIS)**

Ranking das 20 ocupações com maior participação no valor total transferido, entre os agentes culturais contemplados pela Aldir Blanc com vínculo formal de trabalho (2022–2024).

- Medalhas de **ouro**, **prata** e **bronze** para os três primeiros colocados
- Barras horizontais proporcionais ao % do valor
- Descrições baseadas no Código Brasileiro de Ocupações (CBO/RAIS)
          `,
        },
      },
    },
  });
</script>

<Story name="Top 20 Ocupações CBO — RAIS">
  {#snippet template()}
    <svg width={700} height={cboRaisTableHeight}>
      <CboRaisTable data={cboRaisTop20} width={700} />
    </svg>
  {/snippet}
</Story>
