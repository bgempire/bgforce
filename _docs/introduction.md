---
title: Introdução
description: 
---

# Introdução

BGForce é um framework para Blender Game Engine e UPBGE com sistemas comuns 
pré programados, como interface de usuário e gerenciamento de dados. Ele age 
como um código padrão (boilerplate), mas também provê várias abstrações para 
tarefas comuns do desenvolvimento de jogos. O framework tenta facilitar ao 
máximo a execução das rotinas mais comuns, de forma que elas sejam amigáveis 
de serem realizadas até mesmo para quem não tem um conhecimento avançado a 
respeito de programação.

## Principais Funcionalidades
Dentre as diversas funcionalidades do BGForce, destacamos:

- Arquitetura focada na granularidade, facilitando o trabalho em equipe ao 
usar sistemas de versionamento (como Git)
- Sistema de interface de usuário versátil e altamente customizável
- Sistema de operadores através de mensagens, permitindo a execução de 
funções de forma simples
- Gerenciador de dados, permitindo o carregamento e manipulação de árvores 
de dados complexas
- Gerenciador de contextos, permitindo a suave alteração de grupos de cenas, 
música de fundo e mais

## O Problema dos Monólitos
A maioria dos projetos desenvolvidos no Blender Game Engine e UPBGE tem uma abordagem de monólito, isto é, tem todos os 
seus dados embutidos em um único arquivo blend, incluindo cenas, grupos, texturas, sons, scripts, etc. Essa abordagem é 
aceitável para projetos pequenos e feitos por uma única pessoa, mas torna extremamente difícil trabalhar em equipe ou em 
projetos mais complexos e/ou escaláveis devido a necessidade de trocar arquivos entre as pessoas envolvidas, inclusive 
necessitando fazer uma mistura manual de alterações através de `File` > `Append` no caso das duas pessoas fazerem alterações 
ao mesmo tempo e precisarem unir essas alterações em um blend só.

Esse problema se agrava ainda mais caso a equipe pretenda utilizar um sistema de versionamento como o Git, pois como os 
arquivos blends são binários não há como versionar apenas a parte que foi alterada (como é o caso de linhas de código em 
texto), e nesse caso o arquivo blend inteiro será versionado, criando assim um histórico que não permitirá o uso do 
potencial real do sistema de versionamento.

## Arquitetura Granular
O contraponto da abordagem de monólito no desenvolvimento em BGE e UPBGE é a arquitetura granular. Neste caso, ao invés de 
termos todos os dados embutidos em um único arquivo blend, teremos todos os dados que pudermos (e for conveniente) separar 
guardados em arquivos externos. Desta forma, scripts, texturas e sons ficarão em arquivos externos em 100% das vezes (o que 
facilita o uso de editores externos para estes arquivos), e arquivos blends serão separados em ordem de funcionalidades do 
jogo (como `LibJogador.blend`, `LibCenario.blend`) funcionando como uma espécie de 'árvore' de bibliotecas, e se 
interligarão através de linkagem (`File` > `Link`) em arquivos blend e cenas que de fato serão mostradas no jogo (como 
`ScnFase1.blend`, `Jogo.blend`), seja através de instâncias de grupos como instâncias de cenas. 
O [`bge.logic.LibLoad`](https://docs.blender.org/api/2.79/bge.logic.html#bge.logic.LibLoad) também é uma abordagem aceitável para esse 
fim, porém o uso de `File` > `Link` é mais transparente para não-programadores.

O BGForce é desenvolvido e testado na prática pela equipe de desenvolvedores e artistas do BGEmpire, e foi pensado com a 
granularidade de dados como um de seus grandes focos, assim facilitando o trabalho em equipe quando usado com um sistema de 
versionamento (por diminuir a possibilidade de conflitos de arquivos blend), além de permitir estruturas de arquivos intrincadas 
e complexas sem perder a simplicidade em seu conceito.