<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber } from 'sniic-design-system';
  // @ts-ignore
  import {
    percContempladosCadunico,
    qtdContempladosCadunico,
    qtdDocumentosUnicos,
    valorRecebidoCadunico,
    percValorCadunico,
    percFemCadunico,
    perc2554Cadunico,
    percUrbanoCadunico,
    percPequenoPorteCadunico,
    percBolsaFamilia,
    valorBolsaFamilia,
    percBpc,
    valorBpc,
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
    parameters: {
      docs: {
        description: {
          component: `
**Grandes números — CadÚnico**

Cruzamento dos contemplados da Aldir Blanc com o Cadastro Único (CadÚnico).

- **${formatPct(percContempladosCadunico)}** das pessoas físicas contempladas estão no CadÚnico (${formatNum(qtdContempladosCadunico)} pessoas, ${formatNum(qtdDocumentosUnicos)} documentos únicos).
- O valor repassado a esse grupo foi de **${formatBRL(valorRecebidoCadunico)}**, representando **${formatPct(percValorCadunico)}** dos recursos totais.
- **${formatPct(percFemCadunico)}** são mulheres; **${formatPct(perc2554Cadunico)}** têm entre 25 e 54 anos.
- **${formatPct(percUrbanoCadunico)}** vivem em área urbana; **${formatPct(percPequenoPorteCadunico)}** em municípios de pequeno porte.
- **${formatPct(percBolsaFamilia)}** são beneficiários do Bolsa Família (${formatBRL(valorBolsaFamilia)} repassados).
- **${formatPct(percBpc)}** são beneficiários do BPC (${formatBRL(valorBpc)} repassados).

**Fonte**: \`aggregate_cadunico_summary.csv\`, \`aggregate_cadunico_profile_summary_by_sexo.csv\`, \`aggregate_cadunico_profile_summary_by_faixa_etaria.csv\`, \`aggregate_cadunico_by_situacao_domicilio.csv\`, \`aggregate_cadunico_by_population_size.csv\`, \`aggregate_bolsa_familia_summary.csv\`, \`aggregate_bpc_summary.csv\`.
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

<Story name="BigNumber — % dos recursos totais destinados ao CadÚnico">
  {#snippet template()}
    <BigNumber value={formatPct(percValorCadunico)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — % feminino no CadÚnico">
  {#snippet template()}
    <BigNumber value={formatPct(percFemCadunico)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — % faixa 25-54 anos no CadÚnico">
  {#snippet template()}
    <BigNumber value={formatPct(perc2554Cadunico)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — % urbano no CadÚnico">
  {#snippet template()}
    <BigNumber value={formatPct(percUrbanoCadunico)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — % pequeno porte no CadÚnico">
  {#snippet template()}
    <BigNumber value={formatPct(percPequenoPorteCadunico)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — % Bolsa Família">
  {#snippet template()}
    <BigNumber value={formatPct(percBolsaFamilia)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — valor Bolsa Família">
  {#snippet template()}
    <BigNumber value={formatBRL(valorBolsaFamilia)} fontSize={72} />
  {/snippet}
</Story>

<Story name="BigNumber — % BPC">
  {#snippet template()}
    <BigNumber value={formatPct(percBpc)} fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — valor BPC">
  {#snippet template()}
    <BigNumber value={formatBRL(valorBpc)} fontSize={72} />
  {/snippet}
</Story>
