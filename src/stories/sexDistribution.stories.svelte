<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber, PictogramChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { totalPF, sexoPropMasculino, sexoPropFeminino } from '$lib/data/section3';

  // @ts-ignore
  const formatNum = (v) => v.toLocaleString('pt-BR');
  // @ts-ignore
  const formatPct = (v) =>
    (v * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const pictogramData = [
    { label: 'Masculino', value: 8, color: colorScales.lime[2] },
    { label: 'Feminino', value: 7, color: colorScales.orange[2] },
  ];

  const { Story } = defineMeta({
    title: 'Section 2/sexDistribution',
    component: BigNumber,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Leve maioria masculina, perto da paridade**

Entre as **${totalPF.toLocaleString('pt-BR')} pessoas físicas** contempladas pela Aldir Blanc, os homens representam **53,2%** e as mulheres, **46,8%** — uma diferença de cerca de 7 pontos percentuais.

Quando olhamos o valor recebido, a proporção é muito semelhante: **53,9%** para homens e **46,1%** para mulheres, indicando que não há diferença expressiva no valor médio recebido entre os sexos.

*Nota: a variável sexo (masculino/feminino) é adotada conforme disponibilidade da base da Receita Federal, referindo-se ao sexo biológico registrado — o que não contempla a diversidade de identidades de gênero.*
          `,
        },
      },
    },
    argTypes: {
      value: { control: 'text' },
      fontSize: { control: { type: 'range', min: 24, max: 200, step: 4 } },
    },
  });
</script>

<Story name="BigNumber — % masculino">
  {#snippet template()}
    <BigNumber value={formatPct(sexoPropMasculino)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — % feminino">
  {#snippet template()}
    <BigNumber value={formatPct(sexoPropFeminino)} fontSize={96} />
  {/snippet}
</Story>

<Story name="Pictograma — 1 ícone = 1 em cada 15 agentes">
  {#snippet template()}
    <PictogramChart
      data={pictogramData}
      unitValue={1}
      columns={15}
      iconSize={32}
      gap={6}
      showLabels={true}
      format={formatNum}
    />
  {/snippet}
</Story>
