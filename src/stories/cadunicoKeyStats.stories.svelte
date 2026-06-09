<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber } from 'sniic-design-system';
  // @ts-ignore
  import {
    percContempladosCadunico,
    qtdContempladosCadunico,
    valorRecebidoCadunico,
    percValorCadunico,
    percFemCadunico,
    perc2554Cadunico,
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
    title: 'Section 5/cadunicoKeyStats',
    component: BigNumber,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Grandes números — Capítulo 5: Agentes Culturais e Vulnerabilidade Social**

Estatísticas-chave sobre os agentes culturais pessoas físicas contemplados no Ciclo 1 da Aldir Blanc e cadastrados no Cadastro Único.

1. **${formatPct(percContempladosCadunico)}** das pessoas físicas contempladas estão no CadÚnico
2. **${formatNum(qtdContempladosCadunico)}** agentes culturais representam esse grupo
3. **${formatPct(percValorCadunico)}** dos recursos destinados a pessoas físicas foram para esse grupo
4. **${formatPct(percFemCadunico)}** dos contemplados são mulheres
5. **${formatPct(perc2554Cadunico)}** estão entre 25 e 54 anos
6. **87,9%** têm renda familiar per capita de até 1 salário mínimo
7. **43,6%** estão em situação de pobreza (renda familiar per capita de até R$218)

**Fonte**: \`aggregate_cadunico_summary.csv\`, \`aggregate_cadunico_profile_summary_by_sexo.csv\`, \`aggregate_cadunico_profile_summary_by_faixa_etaria.csv\`, \`aggregate_cadunico_by_fx_renda_per_capita.csv\`, \`aggregate_cadunico_by_situacao_renda.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="BigNumber — % pessoas fisicas no CadUnico">
  {#snippet template()}
    <BigNumber value={formatPct(percContempladosCadunico)} fontSize={96} label="cadastrados no CadÚnico" />
  {/snippet}
</Story>

<Story name="BigNumber — quantidade de agentes culturais no CadUnico">
  {#snippet template()}
    <BigNumber value={formatNum(qtdContempladosCadunico)} fontSize={96} label="contemplados no CadÚnico" />
  {/snippet}
</Story>

<Story name="BigNumber — valor total transferido ao grupo CadUnico">
  {#snippet template()}
    <BigNumber value={formatBRL(valorRecebidoCadunico)} fontSize={72} label="transferidos ao grupo CadÚnico" />
  {/snippet}
</Story>

<Story name="BigNumber — % recursos destinados a pessoas fisicas CadUnico">
  {#snippet template()}
    <BigNumber value={formatPct(percValorCadunico)} fontSize={96} label="dos recursos para esse grupo" />
  {/snippet}
</Story>

<Story name="BigNumber — % mulheres no CadUnico">
  {#snippet template()}
    <BigNumber value={formatPct(percFemCadunico)} fontSize={96} label="são mulheres (CadÚnico)" />
  {/snippet}
</Story>

<Story name="BigNumber — % entre 25 e 54 anos no CadUnico">
  {#snippet template()}
    <BigNumber value={formatPct(perc2554Cadunico)} fontSize={96} label="entre 25 e 54 anos" />
  {/snippet}
</Story>

<Story name="BigNumber — % renda familiar per capita ate 1 salario minimo">
  {#snippet template()}
    <BigNumber value="87,9%" fontSize={96} label="renda familiar até 1 salário mínimo" />
  {/snippet}
</Story>

<Story name="BigNumber — % em situacao de pobreza ate R$218">
  {#snippet template()}
    <BigNumber value="43,6%" fontSize={96} label="em situação de pobreza" subtitle="renda per capita até R$218" />
  {/snippet}
</Story>
