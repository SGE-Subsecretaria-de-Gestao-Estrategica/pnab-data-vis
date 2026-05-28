<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import {
    percContempladosCadunico,
    qtdContempladosCadunico,
    qtdDocumentosUnicos,
    valorRecebidoCadunico,
  } from '$lib/data/section5';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);
  // @ts-ignore
  const formatNum = (v) => v.toLocaleString('pt-BR');
  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 5/cadunicoBigNumbers',
    component: BigNumber,
    tags: ['autodocs'],
    decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Contemplados inscritos no Cadastro Único**

O cruzamento dos dados da Política Nacional Aldir Blanc com o Cadastro Único (CadÚnico) revela que **${formatPct(percContempladosCadunico)}** das pessoas físicas contempladas integram o cadastro — evidência de que a política alcançou populações em situação de vulnerabilidade econômica.

Ao todo, **${formatNum(qtdContempladosCadunico)} pessoas** foram identificadas no CadÚnico, com **${formatNum(qtdDocumentosUnicos)} documentos únicos** no cruzamento. O valor total repassado a esse grupo foi de **${formatBRL(valorRecebidoCadunico)}**.

**Fonte**: \`aggregate_cadunico_summary.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="BigNumber — % contemplados no CadÚnico">
  {#snippet template()}
    <BigNumber value={formatPct(percContempladosCadunico)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — quantidade de contemplados no CadÚnico">
  {#snippet template()}
    <BigNumber value={formatNum(qtdContempladosCadunico)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — documentos únicos">
  {#snippet template()}
    <BigNumber value={formatNum(qtdDocumentosUnicos)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — valor repassado ao grupo CadÚnico">
  {#snippet template()}
    <BigNumber value={formatBRL(valorRecebidoCadunico)} fontSize={72} />
  {/snippet}
</Story>
