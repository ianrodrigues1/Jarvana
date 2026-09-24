# Jarvana - O Silêncio

Uma aventura de ficção interativa em Python 3, sem dependências externas. Ethan Muller acorda na nave de pesquisa **LÁZARO** enquanto a reentrada se aproxima. A presença que divide a nave com ele se chama **Jarvana**: uma entidade alienígena calma, precisa, estranhamente curiosa e impossível de classificar com segurança.

## Executar no Windows e no VS Code

1. Abra a pasta `RPG espacial` no VS Code.
2. Abra o terminal integrado com `Ctrl + '`.
3. Confirme o Python 3.10 ou superior com `py --version`.
4. Inicie o jogo:

   ```powershell
   py main.py
   ```

Use `python main.py` se esse for o comando configurado na sua instalação. O jogo usa somente a biblioteca padrão e ativa cores ANSI em terminais modernos. Defina a variável de ambiente `NO_COLOR` caso prefira uma saída sem cores.

## Interface

O HUD está totalmente em português e apresenta, a cada turno, a nave, o setor atual, oxigênio, energia, casco, reentrada e o vínculo com Jarvana. A identidade visual primária usa violeta `#5C57C0`; verde representa sucesso, amarelo aviso, vermelho perigo e ciano informação. Rótulos como `[PERIGO]` acompanham as cores para que a informação não dependa apenas delas.

Quando Jarvana estabelece contato, ela também aparece discretamente no HUD. Durante a desavença obrigatória, esse campo muda para refletir que a interface está sendo observada e que uma escolha está pendente.

## Ações contextuais e atalhos

Abaixo da narrativa, o jogo exibe apenas ações que fazem sentido no estado atual. A lista muda ao explorar um setor, encontrar logs, reparar sistemas, desbloquear rotas, estabelecer contato com Jarvana ou avançar eventos narrativos. Ela mostra possibilidades sem revelar soluções.

Cada item mostra o comando completo que Ethan pode executar e tem um atalho contextual que aciona exatamente esse comando. Por exemplo, `[E] explorar`, `[X] examinar terminal`, `[C] interagir jarvana`, `[M] acessar manutenção`, `[L] ler log 04`, `[I] inventário` e `[S] status`. Quando mais de uma rota estiver liberada, cada destino recebe seu próprio atalho e aparece como um comando completo.

Comandos completos continuam funcionando sempre. Os atalhos não são um menu fixo: uma mesma tecla pode representar uma ação diferente em outro contexto. Em decisões narrativas reais, o jogo pode mostrar escolhas numeradas, como `[1] salvar tripulante` e `[2] preservar dados`; os comandos por extenso permanecem válidos nesses momentos.

## Estrutura

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Loop do terminal, tema de cores, HUD, narrativa e ações visíveis. |
| `game.py` | Progressão, ações contextuais, comandos, desavença, escolhas e finais. |
| `parser.py` | Parser sem acentos, sinônimos, alvos em linguagem natural e expansão de atalhos. |
| `story.py` | Cenários, 12 logs, finais e conjunto de falas de Jarvana. |
| `systems.py` | Estado global, HUD, recursos e relógio simulado. |

## Comandos

Não há menus numerados. Escreva comandos normalmente; acentos são opcionais.

```text
explorar
examinar terminal
acessar manutencao
ler log 04
usar kit
reparar oxigenio
interagir jarvana
confiar
confrontar jarvana
salvar tripulante
preservar dados
rastrear transmissao
bloquear transmissao
transferir jarvana
ativar protocolo zero
escapar
status
inventario
ajuda
```

Os atalhos exibidos na tela são contextuais. Portanto, consulte o painel **AÇÕES DISPONÍVEIS** da partida em vez de decorar uma lista fixa.

## Jarvana e o teste de humanidade

Jarvana não é a nave: **LÁZARO** é o nome da nave; Jarvana é a entidade xenológica encontrada nela. Depois do primeiro contato, ela comenta a exploração de maneira contextual, variando conforme local, recursos críticos, logs, confiança, decisões, tensão após o conflito e proximidade da reentrada. As observações filosóficas são raras e não se repetem dentro de uma partida.

Nos Alojamentos, o arquivo de contingência revela que Jarvana ocultou a existência de Imani em estase, por considerar a reação de Ethan previsível. O confronto é obrigatório para liberar a Ponte de Comando. Durante ele, Jarvana apresenta um teste moral sem menu: Ethan deve digitar `salvar tripulante` ou `preservar dados`. As duas decisões liberam a rota, mas alteram consequências, recursos e a relação entre os dois.

## Walkthrough: “Dois Sobreviventes”

Este roteiro foi validado contra o motor atual:

```text
explorar
examinar terminal
acessar manutencao
explorar
examinar vazamento
reparar oxigenio
reparar energia
reparar casco
acessar laboratorio
explorar
interagir jarvana
confiar
acessar alojamentos
explorar
examinar armario
examinar arquivo
confrontar jarvana
salvar tripulante
acessar ponte
examinar terminal
bloquear transmissao
acessar nucleo
explorar
transferir jarvana
escapar
```

## Arquitetura técnica

`GameState` concentra HP, oxigênio, energia, casco, reentrada em segundos, vínculo com Jarvana, inventário, logs, áreas, flags de decisão e histórico de falas já exibidas. Cada comando válido avança o relógio simulado, reduz recursos e pode encerrar a partida em caso de falha.

O parser normaliza Unicode com `unicodedata`, então `manutencao` e `manutenção` funcionam da mesma maneira. `game.py` traduz cada intenção em consequências de contexto e consulta o conjunto de falas de `story.py`, evitando repetições. A narrativa permanece guiada por exploração, logs, diálogos curtos e comandos livres.
