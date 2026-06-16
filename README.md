# Sistema de Roteirização Logística com OR-Tools, OSRM e Folium

## Descrição

Este projeto foi desenvolvido como Trabalho de Conclusão de Curso (TCC) e apresenta uma solução para o Problema de Roteirização de Veículos Capacitados (CVRP), integrando técnicas de otimização combinatória, geoprocessamento e visualização geográfica.

A aplicação utiliza o Google OR-Tools para geração das rotas, o OSRM para obtenção de trajetos compatíveis com a malha viária real e a biblioteca Folium para criação de mapas interativos.

## Funcionalidades

* Modelagem e resolução do CVRP;
* Restrições de capacidade dos veículos;
* Distribuição das demandas entre os veículos;
* Geração de trajetos reais utilizando OSRM;
* Integração com dados cartográficos do OpenStreetMap;
* Visualização das rotas em mapas interativos;
* Exportação dos resultados em formato HTML.

## Tecnologias Utilizadas

* Python
* Google OR-Tools
* OSRM (Open Source Routing Machine)
* OpenStreetMap
* Folium
* PuLP

## Estrutura do Projeto

```text
data/          # Arquivos de entrada
routing/       # Modelagem e otimização das rotas
output/        # Resultados gerados pelo sistema
main.py        # Execução principal
```

## Execução

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o sistema:

```bash
python main.py
```

Os mapas e relatórios gerados serão armazenados na pasta de saída configurada no projeto.

## Trabalho Acadêmico

Este repositório contém o código-fonte desenvolvido para o Trabalho de Conclusão de Curso:

**Sistema de Apoio à Roteirização Logística Utilizando Técnicas de Otimização Combinatória e Geoprocessamento**

O objetivo do trabalho é investigar a integração entre otimização matemática, roteamento geográfico e visualização interativa para apoio ao planejamento logístico.

## Autor

Igor Cirne

## Licença

Este projeto foi desenvolvido para fins acadêmicos.

