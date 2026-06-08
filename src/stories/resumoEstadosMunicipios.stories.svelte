<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';

  const { Story } = defineMeta({
    title: 'Section 2/resumoEstadosMunicipios',
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Tabela-resumo comparativa: Estados × Municípios**

Síntese dos principais indicadores de execução financeira comparando os dois níveis de esfera pública:

- **Número de contemplados**: estados (22.050) vs municípios (144.836)
- **Ticket médio**: estados concentram pagamentos muito maiores (R$52.711 vs R$7.839)
- **Concentração por faixa**: estados lideram na faixa R$10–50k (contemplados) e acima de R$200k (valor); municípios na faixa R$2–10k e R$10–50k respectivamente

**Fonte**: execução estadual e municipal agregada por faixa de valor.
          `,
        },
      },
    },
  });
</script>

<Story name="Tabela resumo — Estados vs Municípios">
  {#snippet template()}
    <div style="max-width: 680px; padding: 16px;">
      <table style="
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
        font-family: 'Space Grotesk', sans-serif;
      ">
        <thead>
          <tr>
            <th style="padding: 0.6rem 0.75rem; text-align: left; font-weight: 700; color: #6b7280; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; border-bottom: 2px solid #d1d5db;">Indicador</th>
            <th style="padding: 0.6rem 0.75rem; text-align: center; font-weight: 700; color: #6b7280; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; border-bottom: 2px solid #d1d5db;">Estados</th>
            <th style="padding: 0.6rem 0.75rem; text-align: center; font-weight: 700; color: #6b7280; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; border-bottom: 2px solid #d1d5db;">Municípios</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="padding: 0.6rem 0.75rem; text-align: left; border-bottom: 1px solid #e5e7eb;">Número de contemplados</td>
            <td style="padding: 0.6rem 0.75rem; text-align: center; font-weight: 500; border-bottom: 1px solid #e5e7eb;">22.050</td>
            <td style="padding: 0.6rem 0.75rem; text-align: center; font-weight: 500; border-bottom: 1px solid #e5e7eb;">144.836</td>
          </tr>
          <tr>
            <td style="padding: 0.6rem 0.75rem; text-align: left; border-bottom: 1px solid #e5e7eb;">Ticket médio dos pagamentos</td>
            <td style="padding: 0.6rem 0.75rem; text-align: center; font-weight: 500; border-bottom: 1px solid #e5e7eb;">R$ 52.711</td>
            <td style="padding: 0.6rem 0.75rem; text-align: center; font-weight: 500; border-bottom: 1px solid #e5e7eb;">R$ 7.839</td>
          </tr>
          <tr>
            <td style="padding: 0.6rem 0.75rem; text-align: left; border-bottom: 1px solid #e5e7eb;">Concentração dos contemplados, por faixa de valor</td>
            <td style="padding: 0.6rem 0.75rem; text-align: center; font-weight: 500; border-bottom: 1px solid #e5e7eb;">De 10 a 50 mil</td>
            <td style="padding: 0.6rem 0.75rem; text-align: center; font-weight: 500; border-bottom: 1px solid #e5e7eb;">De 2 a 10 mil</td>
          </tr>
          <tr>
            <td style="padding: 0.6rem 0.75rem; text-align: left;">Concentração do recurso executado, por faixa de valor</td>
            <td style="padding: 0.6rem 0.75rem; text-align: center; font-weight: 500;">Acima de 200 mil</td>
            <td style="padding: 0.6rem 0.75rem; text-align: center; font-weight: 500;">De 10 a 50 mil</td>
          </tr>
        </tbody>
      </table>
    </div>
  {/snippet}
</Story>
