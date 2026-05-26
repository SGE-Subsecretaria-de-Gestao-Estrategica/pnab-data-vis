<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorPairs } from 'sniic-design-system';
  import PyramidChartCustom from '$lib/components/PyramidChartCustom.svelte';
  // @ts-ignore
  import { pyramidData } from '$lib/data/section3';

  // @ts-ignore
  const formatNum = (v) => v.toLocaleString('pt-BR');

  const { Story } = defineMeta({
    title: 'Section 3/ageGroupPyramid',
    component: PyramidChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Adultos em idade ativa dominam o programa**

A pirâmide etária dos agentes culturais contemplados pela Aldir Blanc revela um perfil concentrado na população economicamente ativa.

A faixa de **25 a 54 anos** concentra cerca de **70,5%** do total dos beneficiários. Jovens de 15 a 24 anos representam apenas **8%**, e idosos acima de 65 anos, **8,6%**. O perfil reflete o mercado de trabalho cultural: uma população em plena carreira.

Um detalhe relevante: nas faixas de **55 a 64 anos** e **65 anos ou mais**, as mulheres superam os homens em quantidade, invertendo a tendência das faixas mais jovens — possivelmente relacionado à maior longevidade feminina e à participação de mulheres mais velhas em práticas culturais tradicionais.
          `,
        },
      },
    },
  });
</script>

<Story name="Pirâmide etária por sexo">
  {#snippet template()}
    <PyramidChartCustom
      data={pyramidData}
      leftLabel="Masculino"
      rightLabel="Feminino"
      colors={colorPairs.bluePurple}
      format={formatNum}
      height={400}
      centerGap={96}
    />
  {/snippet}
</Story>
