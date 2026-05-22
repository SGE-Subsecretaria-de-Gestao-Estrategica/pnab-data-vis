<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DataTable } from 'sniic-design-system';
  import { ufData } from '$lib/data/section1';

  // @ts-ignore
  const brl = (v) => `R$ ${v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  // @ts-ignore
  const pct = (v) => `${v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%`;

  const columns = [
    { key: 'uf', label: 'UF', align: 'left', width: 80 },
    { key: 'valor_executado_estado', label: 'Valor Executado Estado', align: 'right', width: 200 },
    { key: 'valor_executado_municipio', label: 'Valor Executado Município', align: 'right', width: 200 },
    { key: 'valor_executado_total_uf', label: 'Valor Executado Total UF', align: 'right', width: 200 },
    { key: 'perc_valor_executado_estado', label: '% Estado', align: 'right', width: 120 },
    { key: 'perc_valor_executado_municipio', label: '% Município', align: 'right', width: 120 },
    { key: 'valor_executado_perc', label: '% Total', align: 'right', width: 100 },
  ];

  const rows = ufData.map((d) => ({
    uf: d.uf,
    valor_executado_estado:         brl(d.valor_executado_estado),
    valor_executado_municipio:      brl(d.valor_executado_municipio),
    valor_executado_total_uf:       brl(d.valor_executado_total_uf),
    perc_valor_executado_estado:    pct(d.perc_valor_executado_estado),
    perc_valor_executado_municipio: pct(d.perc_valor_executado_municipio),
    valor_executado_perc:           pct(d.valor_executado_perc),
  }));

  const { Story } = defineMeta({
    title: 'Section 1/executedValueByUf',
    component: DataTable,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Tabela completa: valor executado por UF com divisão estado/município**

Referência de dados para todas as 27 unidades federativas. Exibe o valor executado pelo governo estadual, pelo conjunto de municípios e o total por UF — além das proporções percentuais de cada esfera e a participação no total nacional.

Use esta tabela para verificar valores exatos que os gráficos representam visualmente. Os destaques notáveis:
- **SP**: R$ 555 milhões no total (19,5% do país), com divisão quase equilibrada entre estado (52,2%) e municípios (47,8%).
- **RO**: R$ 8,8 milhões, com 94,7% via municípios — a maior concentração municipal do país.
- **RR**: R$ 16,5 milhões, com 90,6% via estado — a maior concentração estadual.
- **SC**: único estado onde municípios superam 65% da execução.
          `,
        },
      },
    },
  });
</script>

<Story name="Valor executado por UF">
  {#snippet template()}
    <svg width={1020} height={920}>
      <DataTable {columns} {rows} />
    </svg>
  {/snippet}
</Story>
