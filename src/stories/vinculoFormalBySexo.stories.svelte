<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DivergingBarChart, colorPairs } from 'sniic-design-system';
  // @ts-ignore
  import { sexoDivergingData } from '$lib/data/section4';

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalBySexo',
    component: DivergingBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Mulheres são mais afetadas pela informalidade**

Entre as mulheres beneficiárias, **60,1%** não possuem vínculo formal — proporção significativamente maior do que a observada entre os homens (**51,1%**). A informalidade atinge ambos os sexos, mas pesa estruturalmente mais sobre as trabalhadoras do setor cultural.
          `,
        },
      },
    },
  });
</script>

<Story name="Divergente — Sem vs. com vínculo formal por sexo">
  {#snippet template()}
    <DivergingBarChart
      data={sexoDivergingData}
      leftLabel="Sem vínculo formal"
      rightLabel="Com vínculo formal"
      referenceValue={50}
      referenceLabel="50%"
      colors={colorPairs.limeRed}
    />
  {/snippet}
</Story>
