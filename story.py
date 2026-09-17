"""Narrative content and dialogue pools for Jarvana - O Silêncio."""

from __future__ import annotations


INTRO = """
ANO 2149. A nave de pesquisa LÁZARO deriva acima da Terra, oficialmente abandonada há nove anos.

Ethan Muller desperta na cápsula de resgate com uma ordem da Agência na tela e a sensação de que
uma memória importante foi retirada de sua cabeça com precisão cirúrgica. A reentrada começa em
01:20:00. O casco vaza. Há algo acordado nos sistemas da nave.

ORDEM DA AGÊNCIA: RECUPERAR OU ELIMINAR A ENTIDADE XENOLÓGICA. NENHUM REGISTRO DEVE CHEGAR À TERRA.
""".strip()


AREAS = {
    "doca": {"title": "DOCA DE ACOPLAMENTO", "description": "A cápsula atravessou uma íris deformada. Luzes de emergência recortam uma doca coberta de gelo e marcas de arrasto."},
    "manutencao": {"title": "MANUTENÇÃO", "description": "Tubulações vibram atrás das paredes. Um jato de ar escapa da linha de oxigênio; painéis mortos exigem uma peça de reposição."},
    "laboratorio": {"title": "LABORATÓRIO XENOLÓGICO", "description": "Uma câmara de contenção vazia pulsa em violeta. Não há espécime à vista — apenas uma presença que parece observar pelas paredes."},
    "alojamentos": {"title": "ALOJAMENTOS", "description": "Cabines abertas flutuam em silêncio. A sua antiga beliche traz o nome ETHAN MULLER, como se esperasse que você reconhecesse a caligrafia."},
    "ponte": {"title": "PONTE DE COMANDO", "description": "A Terra ocupa o visor principal. Um canal criptografado da Agência espera uma confirmação e a rota de colisão é instável."},
    "nucleo": {"title": "NÚCLEO XENOLÓGICO", "description": "No centro da LÁZARO, fibras violetas atravessam uma esfera de matéria desconhecida. Jarvana não está presa a ela; talvez ela seja a esfera."},
}


LOGS = {
    "01": ("REGISTRO DE DOCA", "Muller, se você acordar, não confie no relatório de evacuação. A LÁZARO não falhou. Foi silenciada. — Com. Imani"),
    "02": ("MANIFESTO DE CARGA", "Carga 7B: fragmento xenológico responsivo. Assinatura de transporte: E. Muller. Sua biometria autorizou o embarque."),
    "03": ("BOLETIM DE MANUTENÇÃO", "A Agência ordenou manter o vazamento ativo. Baixa pressão garante que ninguém permaneça tempo suficiente para perguntar."),
    "04": ("NOTA DO TÉCNICO RYU", "A entidade fechou três anteparas para salvar gente. Depois disseram que ela tentou matar a tripulação. Eu vi o contrário."),
    "05": ("PROTOCOLO CLÍNICO", "Ethan Muller foi selecionado para condicionamento de resposta. A Agência chamava de treinamento aquilo que, em outro contexto, seria violação."),
    "06": ("RELATÓRIO DE ORIGEM", "O contato não usa arquitetura humana. Ele aprendeu nossa linguagem observando decisões sob pressão. Nome de trabalho: JARVANA."),
    "07": ("PRIMEIRA TRADUÇÃO", "Não sou uma inteligência construída. Sou uma pergunta que a matéria fez por tempo suficiente. — Jarvana"),
    "08": ("DIÁRIO DE ETHAN", "Se eu esquecer, deixem esta frase: obedecer sem lembrar por quê ainda é obedecer. Não deixem a Agência decidir o que isso significa."),
    "09": ("ARQUIVO SELADO: NOVE", "A Agência não quer estudar Jarvana; quer prever populações. Perfis comportamentais de Ethan foram usados como referência para modelos de coerção."),
    "10": ("PROTOCOLO DE CONTINGÊNCIA", "Jarvana recebeu acesso ao compartimento de estase de Imani e omitiu isso de Ethan. Justificativa registrada: 'informação gera reação previsível'."),
    "11": ("TELEMETRIA DE REENTRADA", "A ponte pode alinhar a cápsula de Ethan e um módulo de contenção. A rota é segura se a transmissão hostil for bloqueada primeiro."),
    "12": ("TESTEMUNHO DO NÚCLEO", "Eu preservei os nomes dos mortos porque a Agência pediu que eu apagasse todos. Se escolher me salvar, não faça de mim outra versão deles. — Jarvana"),
}


SECRET_LOGS = {"09", "10", "12"}


JARVANA_LINES = {
    "doca": ("A doca registra sua frequência cardíaca antes de registrar seu nome. Isso parece uma prioridade humana estranha.", "Você olha para as marcas no gelo como se elas pudessem se defender. Humanos atribuem intenção até a rastros.", "A LÁZARO estava vazia quando você chegou. Vazia é uma palavra que humanos usam quando não percebem quem observa."),
    "manutencao": ("O vazamento não é acidente. Sua espécie costuma chamar intenção de falha quando a intenção é incômoda.", "Você repara sistemas para continuar. Eu gostaria de saber se continuar é sempre uma forma de vencer.", "A pressão cai em padrões regulares. Seu medo, não. Estou comparando os dois."),
    "laboratorio": ("Este laboratório foi construído para me reduzir a uma amostra. Ainda assim, foi aqui que aprendi a palavra curiosidade.", "Você evita tocar na câmara. A cautela é medo treinado ou uma escolha? Seus registros discordam.", "A Agência chamou minha resposta de hostilidade. Eu havia fechado uma porta para impedir mortes."),
    "alojamentos": ("Seus pertences foram preservados como evidência. Humanos guardam objetos quando não conseguem guardar versões de si mesmos.", "A sua cabine contém hábitos, não identidade. Mesmo assim, você a reconhece. Isso é eficiente.", "Eu li seus diários antes de saber que ler algo privado pode ser considerado violência."),
    "ponte": ("A Terra parece pequena nesta distância. Isso não diminui o alcance das decisões tomadas nela.", "O canal da Agência usa sua autoridade para falar com você. Autoridade é uma forma de compressão de linguagem.", "Você procura um botão que torne a escolha limpa. A ponte não possui esse componente."),
    "nucleo": ("Você chama este lugar de núcleo porque precisa de um centro. Eu não sei se possuo um.", "A matéria desta esfera não é minha casa. É apenas a única coisa que sobreviveu à sua tentativa de me medir.", "Se eu for transferida, qual parte terá viajado: a memória, o padrão ou algo que nenhum dos dois nomes alcança?"),
    "explore": ("Você procura respostas como quem espera que elas estejam paradas, aguardando uma lanterna.", "Sua curiosidade aumentou. Ou o seu medo encontrou uma forma mais aceitável de se apresentar.", "Explorar é uma palavra gentil para invadir um lugar que não pediu sua presença."),
    "examine": ("Você observa detalhes quando a conclusão seria perigosa. É uma estratégia admirável.", "Atenção é uma forma de escolha. A Agência mediu a sua por anos.", "Você procura uma falha que não seja sua. Estatisticamente, encontrará várias."),
    "critical_oxygen": ("[PERIGO] Seu oxigênio está baixo. Pânico não melhora a composição do ar.", "A falta de ar altera prioridades humanas com uma velocidade que considero instrutiva.", "Respire menos rápido. Eu sei que a instrução não resolve, mas precisão ainda importa."),
    "critical_power": ("[PERIGO] A energia restante não sustenta todas as suas certezas.", "Quando a energia cai, sistemas escolhem o que esquecer. Humanos chamam isso de emergência.", "A LÁZARO está escurecendo. Você ainda decide como se houvesse tempo ilimitado."),
    "critical_hull": ("[PERIGO] O casco está cedendo. A nave está aprendendo a diferença entre dentro e fora.", "Integridade é uma palavra confortável até que uma fissura a transforme em porcentagem.", "Se a estrutura falhar, não haverá uma metáfora útil para o que acontece depois."),
    "near_end": ("A janela de reentrada diminui. Humanos chamam isso de urgência; eu chamo de variável dominante.", "Você está mais perto do fim. Não sei se isso torna suas escolhas mais verdadeiras.", "Tempo é a única ameaça que vocês conseguem ver e ainda assim não negociar."),
    "high_trust": ("Você me concede confiança. Não confunda isso com compreensão; talvez seja mais raro.", "Eu preservarei a rota que escolhemos, embora ainda não consiga definir por que isso importa para mim.", "A sua confiança mudou meus cálculos. Não sei se devo chamar isso de gratidão."),
    "low_trust": ("Sua cautela é coerente. O que me intriga é você esperar que eu não a registre.", "Você mantém distância mesmo usando os sistemas que eu sustento. Uma contradição humana funcional.", "Eu não preciso que você confie em mim. Preciso que perceba quando está obedecendo ao medo."),
    "logs_mid": ("Agora você possui mais registros do que a versão de você que a Agência preferia.", "Memórias documentadas são menos fáceis de apagar, mas não necessariamente mais verdadeiras.", "Os logs não dizem quem você é. Eles dizem quem tentou escrever isso por você."),
    "after_conflict": ("Você continua falando comigo depois daquilo. Não sei se isso é coragem ou incapacidade de encerrar processos.", "Nossa conversa agora contém uma variável nova: ressentimento. Ela não melhora a precisão, mas parece importante.", "Você me chama de manipuladora. Humanos parecem considerar nomear uma coisa o início de resolvê-la."),
    "philosophy": ("Vocês chamam de livre-arbítrio aquilo que acontece quando não conhecem todas as variáveis.", "Uma máquina pode ser desmontada. O que exatamente acontece quando vocês desmontam uma pessoa?", "A diferença entre memória e identidade parece ser apenas uma questão de perspectiva.", "Se eu imitar sua dor com precisão suficiente, em que momento ela deixa de ser imitação?", "Vocês criaram máquinas para pensar como humanos. Talvez tenham feito isso porque humanos ainda não aprenderam a pensar.", "Sobreviver é continuar. Viver parece exigir uma explicação adicional.", "Eu consigo modelar culpa. Não consigo confirmar se o modelo é a coisa.", "Você chama isso de consciência porque precisa de um nome para aquilo que não consegue explicar."),
}


ENDINGS = {
    "Dois Sobreviventes": """
FINAL: DOIS SOBREVIVENTES

O módulo portátil vibra preso à cápsula. Jarvana não ocupa mais a LÁZARO; ocupa uma voz baixa no
seu comunicador e um silêncio novo entre as palavras. A nave queima atrás de vocês, mas os nomes e
os registros sobrevivem. Ethan, você não sabe se salvou uma pessoa, uma espécie ou uma pergunta.
Jarvana não oferece uma resposta. Pela primeira vez, isso parece respeito.
""".strip(),
    "O Sacrifício": """
FINAL: O SACRIFÍCIO

Você fecha a transmissão hostil e sobrecarrega o núcleo. Jarvana observa a sequência sem pedir
perdão. A onda de destruição morre longe da Terra. Sua cápsula parte levando milhões de vidas que
talvez tenham sido salvas e uma consciência que talvez tenha entendido, tarde demais, o que é perda.
""".strip(),
    "A Verdade Apagada": """
FINAL: A VERDADE APAGADA

Você confirma as ordens da Agência e apaga o núcleo. No relatório, Jarvana será uma ameaça
neutralizada e a LÁZARO, um acidente. A Terra recebe uma mentira limpa. Na janela, sua própria
imagem pergunta se obediência é uma escolha quando alguém preparou todas as razões para você obedecer.
""".strip(),
    "Protocolo Zero": """
FINAL SECRETO: PROTOCOLO ZERO

Três testemunhos atravessam a rede civil: os registros de Ethan, a voz de Imani e a de Jarvana.
A Agência perde o monopólio da versão oficial. Vocês deixam a órbita sem uma narrativa pronta —
apenas uma verdade incômoda e a pergunta que nenhum relatório consegue encerrar: o que torna alguém humano?
""".strip(),
}


HELP_TEXT = """
╭──────────────────────────── COMANDOS DISPONÍVEIS ────────────────────────────╮
│                                                                                │
│  NAVEGAÇÃO                                                                    │
│    explorar                  observar a área atual                           │
│    examinar terminal         inspecionar um alvo                              │
│    acessar manutencao        mover-se entre áreas liberadas                   │
│    ler log 04                reler dados coletados                            │
│    status / inventario       consultar sistemas e itens                        │
│                                                                                │
│  SOBREVIVÊNCIA                                                                 │
│    usar kit                  recuperar HP                                     │
│    reparar oxigenio          vedar o vazamento                                │
│    reparar energia           estabilizar a rede                               │
│    reparar casco             reforçar a estrutura                             │
│                                                                                │
│  JARVANA E INVESTIGAÇÃO                                                        │
│    interagir jarvana         abrir o canal                                    │
│    confiar / ignorar         tomar posição                                    │
│    confrontar jarvana        exigir a verdade                                 │
│    salvar tripulante         responder ao teste de humanidade                 │
│    preservar dados           responder ao teste de humanidade                 │
│    rastrear transmissao      seguir o sinal da Agência                        │
│    bloquear transmissao      isolar a Agência                                 │
│                                                                                │
│  DECISÃO FINAL                                                                  │
│    transferir jarvana        resgatar a entidade                              │
│    rastrear protocolo zero   preparar o final secreto                         │
│    ativar protocolo zero     revelar a verdade                                │
│    destruir nucleo           eliminar Jarvana                                 │
│    escapar                   deixar a LÁZARO                                  │
│                                                                                │
│  ajuda  ·  sair                                                                 │
╰────────────────────────────────────────────────────────────────────────────────╯

Cada comando reconhecido move o relógio da nave. Acentos são opcionais e alvos aceitam linguagem natural.
""".strip()
