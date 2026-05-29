<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { categorical8 } from 'sniic-design-system';
  import { specialTerritoriesMetrics } from '$lib/data/section1';

  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);

  const { Story } = defineMeta({
    title: 'Section 1/specialTerritoryMetrics',
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Quatro dimensões da sub-representação nos territórios especiais**

Comparação entre Valor (R$), % dos recursos executados, % dos agentes contemplados e % da população total
para Favelas e Comunidades Urbanas, Quilombolas e Territórios Indígenas.

Em todos os territórios, a fatia da **população** supera a fatia de **recursos** e de **agentes contemplados** — evidenciando um padrão sistemático de sub-representação.
          `,
        },
      },
    },
  });
</script>

<!-- ===== Grouped bars — 4 métricas por território ===== -->

<Story name="Grouped bars — 4 métricas por território">
  {#snippet template()}
    <svg
      viewBox="0 0 560 310"
      style="width: 560px; overflow: visible; display: block; font-family: 'Space Grotesk', system-ui, sans-serif;"
      role="img"
      aria-label="Comparação de quatro métricas por território especial"
    >
      <!-- Legend -->
      <rect x={0}   y={2}  width={12} height={12} fill={categorical8[0]} rx={2} />
      <text x={16}  y={12} style="font-size:10px;dominant-baseline:middle;fill:#334155;">% da população no território</text>
      <rect x={190} y={2}  width={12} height={12} fill={categorical8[2]} rx={2} />
      <text x={206} y={12} style="font-size:10px;dominant-baseline:middle;fill:#334155;">% dos recursos executados</text>
      <rect x={370} y={2}  width={12} height={12} fill={categorical8[4]} rx={2} />
      <text x={386} y={12} style="font-size:10px;dominant-baseline:middle;fill:#334155;">% dos agentes contemplados</text>

      {#each specialTerritoriesMetrics as d, ti}
        {@const blockY = 30 + ti * 92}
        {@const w0 = d.perc_populacao / 10 * 290}
        {@const w1 = d.perc_recurso   / 10 * 290}
        {@const w2 = d.perc_agentes   / 10 * 290}

        <!-- Territory header -->
        <text x={0}   y={blockY + 10} style="font-size:12px;font-weight:700;dominant-baseline:middle;fill:#334155;">{d.shortLabel}</text>
        <text x={560} y={blockY + 10} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.55;">{formatBRL(d.valor)}</text>
        <line x1={0} y1={blockY + 16} x2={560} y2={blockY + 16} stroke="#e2e8f0" stroke-width="1" />

        <!-- % da população -->
        <text x={154} y={blockY + 34} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% da população</text>
        <rect x={160} y={blockY + 22} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={blockY + 22} width={w0}  height={14} fill={categorical8[0]} rx={2} />
        <text x={160 + w0 + 5} y={blockY + 33} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_populacao.toFixed(2)}%</text>

        <!-- % dos recursos -->
        <text x={154} y={blockY + 56} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% dos recursos</text>
        <rect x={160} y={blockY + 44} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={blockY + 44} width={w1}  height={14} fill={categorical8[2]} rx={2} />
        <text x={160 + w1 + 5} y={blockY + 55} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_recurso.toFixed(2)}%</text>

        <!-- % dos agentes -->
        <text x={154} y={blockY + 78} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% dos agentes</text>
        <rect x={160} y={blockY + 66} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={blockY + 66} width={w2}  height={14} fill={categorical8[4]} rx={2} />
        <text x={160 + w2 + 5} y={blockY + 77} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_agentes.toFixed(2)}%</text>
      {/each}
    </svg>
  {/snippet}
</Story>

<!-- ===== Grouped bars — Favela apenas ===== -->

<Story name="Grouped bars — Favela apenas">
  {#snippet template()}
    {#each specialTerritoriesMetrics.filter((d) => d.territorio === 'Favela e Comunidade Urbana') as d}
      {@const w0 = d.perc_populacao / 10 * 290}
      {@const w1 = d.perc_recurso   / 10 * 290}
      {@const w2 = d.perc_agentes   / 10 * 290}
      <svg viewBox="0 0 560 110" style="width:560px;overflow:visible;display:block;font-family:'Space Grotesk',system-ui,sans-serif;">
        <text x={0}   y={10} style="font-size:12px;font-weight:700;dominant-baseline:middle;fill:#334155;">{d.shortLabel}</text>
        <text x={560} y={10} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.55;">{formatBRL(d.valor)}</text>
        <line x1={0} y1={16} x2={560} y2={16} stroke="#e2e8f0" stroke-width="1" />

        <text x={154} y={34} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% da população</text>
        <rect x={160} y={22} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={22} width={w0}  height={14} fill={categorical8[0]} rx={2} />
        <text x={160 + w0 + 5} y={33} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_populacao.toFixed(2)}%</text>

        <text x={154} y={56} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% dos recursos</text>
        <rect x={160} y={44} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={44} width={w1}  height={14} fill={categorical8[2]} rx={2} />
        <text x={160 + w1 + 5} y={55} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_recurso.toFixed(2)}%</text>

        <text x={154} y={78} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% dos agentes</text>
        <rect x={160} y={66} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={66} width={w2}  height={14} fill={categorical8[4]} rx={2} />
        <text x={160 + w2 + 5} y={77} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_agentes.toFixed(2)}%</text>
      </svg>
    {/each}
  {/snippet}
</Story>

<!-- ===== Grouped bars — Quilombola apenas ===== -->

<Story name="Grouped bars — Quilombola apenas">
  {#snippet template()}
    {#each specialTerritoriesMetrics.filter((d) => d.territorio === 'Agrupamento quilombola') as d}
      {@const w0 = d.perc_populacao / 10 * 290}
      {@const w1 = d.perc_recurso   / 10 * 290}
      {@const w2 = d.perc_agentes   / 10 * 290}
      <svg viewBox="0 0 560 110" style="width:560px;overflow:visible;display:block;font-family:'Space Grotesk',system-ui,sans-serif;">
        <text x={0}   y={10} style="font-size:12px;font-weight:700;dominant-baseline:middle;fill:#334155;">{d.shortLabel}</text>
        <text x={560} y={10} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.55;">{formatBRL(d.valor)}</text>
        <line x1={0} y1={16} x2={560} y2={16} stroke="#e2e8f0" stroke-width="1" />

        <text x={154} y={34} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% da população</text>
        <rect x={160} y={22} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={22} width={w0}  height={14} fill={categorical8[0]} rx={2} />
        <text x={160 + w0 + 5} y={33} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_populacao.toFixed(2)}%</text>

        <text x={154} y={56} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% dos recursos</text>
        <rect x={160} y={44} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={44} width={w1}  height={14} fill={categorical8[2]} rx={2} />
        <text x={160 + w1 + 5} y={55} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_recurso.toFixed(2)}%</text>

        <text x={154} y={78} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% dos agentes</text>
        <rect x={160} y={66} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={66} width={w2}  height={14} fill={categorical8[4]} rx={2} />
        <text x={160 + w2 + 5} y={77} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_agentes.toFixed(2)}%</text>
      </svg>
    {/each}
  {/snippet}
</Story>

<!-- ===== Grouped bars — Indígena apenas ===== -->

<Story name="Grouped bars — Indigena apenas">
  {#snippet template()}
    {#each specialTerritoriesMetrics.filter((d) => d.territorio === 'Agrupamento indígena') as d}
      {@const w0 = d.perc_populacao / 10 * 290}
      {@const w1 = d.perc_recurso   / 10 * 290}
      {@const w2 = d.perc_agentes   / 10 * 290}
      <svg viewBox="0 0 560 110" style="width:560px;overflow:visible;display:block;font-family:'Space Grotesk',system-ui,sans-serif;">
        <text x={0}   y={10} style="font-size:12px;font-weight:700;dominant-baseline:middle;fill:#334155;">{d.shortLabel}</text>
        <text x={560} y={10} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.55;">{formatBRL(d.valor)}</text>
        <line x1={0} y1={16} x2={560} y2={16} stroke="#e2e8f0" stroke-width="1" />

        <text x={154} y={34} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% da população</text>
        <rect x={160} y={22} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={22} width={w0}  height={14} fill={categorical8[0]} rx={2} />
        <text x={160 + w0 + 5} y={33} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_populacao.toFixed(2)}%</text>

        <text x={154} y={56} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% dos recursos</text>
        <rect x={160} y={44} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={44} width={w1}  height={14} fill={categorical8[2]} rx={2} />
        <text x={160 + w1 + 5} y={55} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_recurso.toFixed(2)}%</text>

        <text x={154} y={78} text-anchor="end" style="font-size:11px;dominant-baseline:middle;fill:#334155;opacity:0.7;">% dos agentes</text>
        <rect x={160} y={66} width={290} height={14} fill="#f1f5f9" rx={2} />
        <rect x={160} y={66} width={w2}  height={14} fill={categorical8[4]} rx={2} />
        <text x={160 + w2 + 5} y={77} style="font-size:11px;font-weight:600;dominant-baseline:middle;fill:#334155;">{d.perc_agentes.toFixed(2)}%</text>
      </svg>
    {/each}
  {/snippet}
</Story>
