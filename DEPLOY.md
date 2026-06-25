# Especificações de Deploy — PNAB Data Vis

## Visão geral

Aplicação web estática (SPA) gerada via SvelteKit + adapter-static.
O build produz arquivos HTML/CSS/JS puros em `build/`, servidos por nginx.
**Não há servidor de aplicação em runtime** — apenas um servidor HTTP estático.

---

## Opção A: Imagem Docker (recomendada)

### Requisitos da máquina host

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| CPU | 1 vCPU | 2 vCPUs |
| RAM | 512 MB | 1 GB |
| Disco | 1 GB | 5 GB |
| SO | Linux (qualquer distro com Docker) | Ubuntu 22.04 LTS |
| Docker | 24+ | 27+ |

### Construir a imagem

```bash
# Na raiz do projeto
docker build -t pnab-data-vis:latest .
```

> O build requer acesso à internet para baixar dependências do npm (pacote `sniic-design-system` e outros).
> Se o ambiente não tiver acesso externo, veja a seção "Build offline" abaixo.

### Executar o container

```bash
docker run -d \
  --name pnab-data-vis \
  -p 80:80 \
  --restart unless-stopped \
  pnab-data-vis:latest
```

A aplicação ficará disponível em `http://<ip-da-maquina>`.

### Exportar e transferir a imagem (sem registry)

```bash
# Na máquina de build
docker save pnab-data-vis:latest | gzip > pnab-data-vis.tar.gz

# Na máquina de destino
docker load < pnab-data-vis.tar.gz
docker run -d --name pnab-data-vis -p 80:80 --restart unless-stopped pnab-data-vis:latest
```

### Build offline (ambiente sem internet)

Se a máquina de deploy não tiver acesso à internet:

1. Execute o build em uma máquina com acesso
2. Exporte a imagem com `docker save` (acima)
3. Transfira o arquivo `.tar.gz` via SCP, pendrive, etc.
4. Carregue e execute na máquina de destino com `docker load`

---

## Opção B: Deploy sem Docker (servidor bare-metal ou VM)

### Requisitos

| Recurso | Especificação |
|---------|---------------|
| CPU | 1 vCPU |
| RAM | 512 MB |
| Disco | 1 GB |
| SO | Ubuntu 22.04 LTS (ou similar) |
| Software | Node.js 20 LTS, nginx 1.24+ |

### Processo de build (feito uma vez, em qualquer máquina com Node.js 20)

```bash
npm ci
npm run build
# Resultado: diretório build/
```

### Deploy

1. Copiar o conteúdo de `build/` para o servidor (ex: `/var/www/pnab-data-vis/`)
2. Configurar nginx com o arquivo `nginx.conf` deste repositório
3. Não é necessário Node.js na máquina de destino — apenas nginx

---

## Portas e rede

| Porta | Protocolo | Descrição |
|-------|-----------|-----------|
| 80 | HTTP | Acesso à aplicação |

Para HTTPS (recomendado em produção), configurar certificado TLS no nginx ou usar um proxy reverso (ex: Traefik, Caddy) na frente do container.

---

## Variáveis de ambiente (build-time)

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `BASE_PATH` | `""` | Prefixo de caminho se a app for servida em subdiretório (ex: `/pnab`) |

Para deploy em subdiretório:

```bash
docker build --build-arg BASE_PATH=/pnab -t pnab-data-vis:latest .
```

E ajustar o Dockerfile para passar a variável ao build:
```dockerfile
ARG BASE_PATH=""
ENV BASE_PATH=$BASE_PATH
RUN npm run build
```

---

## Arquivos relevantes

```
Dockerfile      # Build multi-stage (Node.js build + nginx serve)
nginx.conf      # Configuração nginx com SPA fallback e cache de assets
.dockerignore   # Arquivos excluídos da imagem Docker
```
