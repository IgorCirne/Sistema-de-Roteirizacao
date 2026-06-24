# Sistema de Apoio à Roteirização Logística com OR-Tools, OSRM e Folium

## Descrição

Este projeto foi desenvolvido como Trabalho de Conclusão de Curso (TCC) e apresenta uma solução para o Problema de Roteirização de Veículos Capacitados (CVRP), integrando técnicas de otimização combinatória, geoprocessamento e visualização geográfica.

A aplicação utiliza o Google OR-Tools para geração das rotas otimizadas, o OSRM para obtenção de trajetos compatíveis com a malha viária real e a biblioteca Folium para criação de mapas interativos.

## Funcionalidades

* Modelagem e resolução do CVRP;
* Restrições de capacidade dos veículos;
* Suporte a múltiplos veículos;
* Construção automática da matriz de distâncias a partir de coordenadas geográficas;
* Utilização da fórmula de Haversine para cálculo das distâncias entre vértices;
* Geração de trajetos reais utilizando o serviço OSRM;
* Integração com dados cartográficos do OpenStreetMap;
* Visualização das rotas em mapas interativos utilizando Folium;
* Exportação dos resultados em formato HTML.

## Tecnologias Utilizadas

* Python
* Google OR-Tools
* OSRM (Open Source Routing Machine)
* OpenStreetMap
* Folium

## Estrutura do Projeto

```text
```text
docs/
└── TCC_Igor_Cirne_Roteirização.pdf          # Versão final do Trabalho de Conclusão de Curso

src/
├── Routing.py              # Execução principal do sistema
├── distance.py             # Construção da matriz de distâncias
├── Cargas.py               # Rotinas auxiliares relacionadas às cargas
├── dados.txt               # Instância de teste
├── dados2.txt              # Instância de teste
└── dados3.txt              # Instância de teste
```

```

## Execução

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
```

Acesse a pasta do projeto:

```bash
cd Sistema-de-Roteirizacao
```

Instale as dependências necessárias:

```bash
pip install ortools folium requests
```

Execute o sistema:

```bash
python src/Routing.py
```

O sistema realizará:

1. Leitura dos dados da instância selecionada;
2. Construção da matriz de distâncias;
3. Resolução do problema de roteirização utilizando OR-Tools;
4. Consulta ao OSRM para obtenção dos trajetos reais;
5. Geração do mapa interativo em formato HTML.

## Trabalho Acadêmico

Este repositório contém o código-fonte desenvolvido para o Trabalho de Conclusão de Curso:

**Sistema de Apoio à Roteirização Logística Utilizando Técnicas de Otimização Combinatória e Geoprocessamento**

O objetivo do trabalho é investigar a integração entre otimização matemática, roteamento geográfico e visualização interativa para apoio ao planejamento logístico.

## Autor

Igor Cirne

## Licença

Projeto desenvolvido para fins acadêmicos e educacionais.
