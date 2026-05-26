<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber } from 'sniic-design-system';
  // @ts-ignore
  import { percBenefCPF, percBenefCNPJ, percValorCPF, percValorCNPJ, totalBenefCPF, totalBenefCNPJ } from '$lib/data/section2';

  const { Story } = defineMeta({
    title: 'Section 3/personTypeBigNumbers',
    component: BigNumber,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Quem recebe o quê? O contraste entre CPF e CNPJ**

O PNAB atinge dois perfis bem distintos: **pessoas físicas (CPF)** — agricultores familiares, pescadores, extrativistas — e **entidades (CNPJ)** — cooperativas, associações e empresas.

O contraste é imediato: **${totalBenefCPF.toLocaleString('pt-BR')} pessoas físicas** contra **${totalBenefCNPJ.toLocaleString('pt-BR')} entidades** — razão de quase 4 para 1 em número de beneficiários. Mas o dinheiro vai na direção oposta: o CPF representa **${percBenefCPF.toFixed(1)}%** dos beneficiários e recebe apenas **${percValorCPF.toFixed(1)}%** do valor, enquanto o CNPJ concentra **${percValorCNPJ.toFixed(1)}%** dos recursos com apenas **${percBenefCNPJ.toFixed(1)}%** dos beneficiários.
          `,
        },
      },
    },
    argTypes: {
      value: { control: 'text' },
      suffix: { control: 'text' },
      fontSize: { control: { type: 'range', min: 24, max: 200, step: 4 } },
      color: { control: 'color' },
    },
  });
</script>

<Story name="CPF — % dos beneficiários">
  {#snippet template()}
    <BigNumber
      value={percBenefCPF.toFixed(1)}
      suffix="%"
      fontSize={96}
    />
  {/snippet}
</Story>

<Story name="CNPJ — % do valor total">
  {#snippet template()}
    <BigNumber
      value={percValorCNPJ.toFixed(1)}
      suffix="%"
      fontSize={96}
    />
  {/snippet}
</Story>

<Story name="CPF — % do valor total">
  {#snippet template()}
    <BigNumber
      value={percValorCPF.toFixed(1)}
      suffix="%"
      fontSize={96}
    />
  {/snippet}
</Story>

<Story name="CNPJ — % dos beneficiários">
  {#snippet template()}
    <BigNumber
      value={percBenefCNPJ.toFixed(1)}
      suffix="%"
      fontSize={96}
    />
  {/snippet}
</Story>
