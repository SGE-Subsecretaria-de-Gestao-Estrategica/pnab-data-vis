<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { SlopeGraph, categorical8, SvgExportDecorator } from 'sniic-design-system';
  import { slopeItems, slopeLabels, formatSlope } from '$lib/data/section1';

  const { Story } = defineMeta({
    title: 'Section 1/equityRankSlope',
    component: SlopeGraph,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Quem subiu ou caiu quando a régua é a população?**

O gráfico de inclinação (slope) compara a posição de cada estado no **ranking por valor executado** com sua posição no **ranking por população**. Todos os 27 estados são exibidos.

Quando a linha sobe da esquerda para a direita, o estado recebeu *mais* do que seu peso populacional justificaria. Quando desce, recebeu *menos*.

**Ganharam proporcionalmente mais:** AL, CE, PI, MA e PA — estados do Nordeste e Norte com histórico de maior vulnerabilidade social.

**Receberam proporcionalmente menos:** SC, RO, PR, RS e MT — estados do Sul e Centro-Oeste, geralmente com indicadores socioeconômicos melhores.

Este padrão indica que o PNAB possui, ao menos parcialmente, um viés redistributivo — mas ainda insuficiente para estados como RO, onde a execução quase não aconteceu.
          `,
        },
      },
    },
  });
</script>

<script>
  let containerEl = $state();
  let containerWidth = $state(800);

  $effect(() => {
    if (!containerEl) return;
    containerWidth = containerEl.clientWidth;
    const ro = new ResizeObserver(([e]) => { containerWidth = e.contentRect.width; });
    ro.observe(containerEl);
    return () => ro.disconnect();
  });
</script>

<Story name="Slope — Posição por valor vs posição por população">
  {#snippet template()}
    <div bind:this={containerEl} style="width:100%">
      <SlopeGraph
        items={slopeItems}
        labels={slopeLabels}
        format={formatSlope}
        width={containerWidth}
        height={600}
        colors={categorical8}
      />
    </div>
  {/snippet}
</Story>
