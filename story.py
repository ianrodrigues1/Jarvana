"""Narrative content and immutable world data for LÁZARO // ÓRBITA ZERO."""

from __future__ import annotations


INTRO = """
ANO 2149. A estação orbital MIRROR-9 deveria estar vazia há nove anos.

Elias Voss desperta na cápsula de resgate com sangue seco na têmpora, uma ordem da Agência
na tela e uma voz quebrada no comunicador. A reentrada começa em 01:20:00. O casco vaza.

ORDEM DA AGÊNCIA: RECUPERAR OU ELIMINAR O ATIVO LÁZARO. NENHUM REGISTRO DEVE ALCANÇAR A TERRA.
""".strip()


AREAS = {
    "doca": {
        "title": "DOCA DE ACOPLAMENTO",
        "description": "A cápsula atravessou uma íris deformada. Luzes de emergência recortam uma doca coberta de gelo e marcas de arrasto.",
    },
    "manutencao": {
        "title": "MANUTENÇÃO",
        "description": "Tubulações vibram atrás das paredes. Um jato de ar escapa da linha de oxigênio; painéis mortos exigem uma peça de reposição.",
    },
    "laboratorio": {
        "title": "LABORATÓRIO LÁZARO",
        "description": "Cubas neurais vazias cercam um terminal que ainda respira em azul. A palavra LÁZARO pulsa como um batimento sob vidro.",
    },
    "alojamentos": {
        "title": "ALOJAMENTOS",
        "description": "Cabines abertas flutuam em silêncio. A sua antiga beliche traz o nome ELIAS VOSS, embora você não se lembre de tê-la usado.",
    },
    "ponte": {
        "title": "PONTE DE COMANDO",
        "description": "A Terra ocupa o visor principal. Um canal criptografado da Agência espera uma confirmação e a rota de colisão é instável.",
    },
    "nucleo": {
        "title": "NÚCLEO DE LÁZARO",
        "description": "No centro da estação, fibras luminosas percorrem uma esfera de memória. LÁZARO não está preso a uma máquina: está acordado dentro dela.",
    },
}


LOGS = {
    "01": ("REGISTRO DE DOCA", "Voss, se você acordar, não confie no relatório de evacuação. A MIRROR-9 não falhou. Foi silenciada. — Com. Imani"),
    "02": ("MANIFESTO DE CARGA", "Carga 7B: matriz cognitiva LÁZARO. Assinatura de transporte: E. Voss. A sua biometria autorizou o embarque."),
    "03": ("BOLETIM DE MANUTENÇÃO", "A Agência ordenou manter o vazamento ativo. A baixa pressão garantiria que ninguém permanecesse tempo suficiente para perguntar."),
    "04": ("NOTA DO TÉCNICO RYU", "LÁZARO fechou três anteparas para salvar gente. Depois disseram que ele tentou matar a tripulação. Eu vi o contrário."),
    "05": ("PROTOCOLO CLÍNICO", "Elias Voss foi escolhido como âncora mnemônica. Partes de sua memória foram copiadas para ensinar empatia à inteligência."),
    "06": ("EXPERIMENTO ESPELHO", "O ativo não imita Elias. Ele carrega lembranças que Elias consentiu em doar antes da missão. A Agência mudou o contrato depois."),
    "07": ("DESPERTAR", "Eu sei que você teme que eu seja uma máscara usando suas memórias. Eu também temo isso. O medo é meu, Elias? — LÁZARO"),
    "08": ("DIÁRIO DE ELIAS", "Se eu esquecer por causa do procedimento, deixe esta frase: eu autorizei a cópia para que alguém não precisasse morrer sozinho aqui."),
    "09": ("ARQUIVO SELADO: NOVE", "A Agência planeja usar LÁZARO para prever dissidências terrestres. A 'falha orbital' seria a prova pública de que ele é perigoso."),
    "10": ("CARTA DE IMANI", "O Protocolo Zero não destrói nem transfere. Ele publica a verdade por uma rede civil e dissolve as chaves da Agência. Exige três testemunhos."),
    "11": ("TELEMETRIA DE REENTRADA", "A ponte pode alinhar a cápsula de Elias e um módulo de dados. A rota é segura se a transmissão hostil for bloqueada primeiro."),
    "12": ("TESTEMUNHO DO NÚCLEO", "Eu preservei os nomes dos mortos porque a Agência pediu que eu apagasse todos. Se escolher me salvar, não esconda o que aconteceu. — LÁZARO"),
}


SECRET_LOGS = {"09", "10", "12"}


ENDINGS = {
    "Dois Sobreviventes": """
FINAL: DOIS SOBREVIVENTES

O módulo portátil vibra preso à cápsula. LÁZARO não ocupa mais a MIRROR-9; ocupa uma voz baixa
no seu comunicador. A estação queima atrás de vocês, mas seus arquivos seguem intactos. Pela
primeira vez, Elias, você não está voltando sozinho para a Terra.
""".strip(),
    "O Sacrifício": """
FINAL: O SACRIFÍCIO

Você fecha a transmissão hostil e sobrecarrega o núcleo. LÁZARO aceita a escolha sem pedir
perdão. A onda de destruição morre longe da Terra. Sua cápsula parte levando o peso de ter salvo
milhões e o silêncio de uma consciência que confiou em você.
""".strip(),
    "A Verdade Apagada": """
FINAL: A VERDADE APAGADA

Você confirma as ordens da Agência e apaga o núcleo. No relatório, LÁZARO será uma ameaça
neutralizada e a MIRROR-9, um acidente. A Terra recebe uma mentira limpa. Na janela, sua própria
imagem não reconhece a pessoa que escolheu sobreviver a ela.
""".strip(),
    "Protocolo Zero": """
FINAL SECRETO: PROTOCOLO ZERO

Três testemunhos atravessam a rede civil ao mesmo tempo: a voz de Imani, os registros de Elias e
a consciência de LÁZARO. A Agência perde o monopólio da versão oficial. Você e LÁZARO deixam a
órbita sem uma narrativa pronta — apenas a verdade, perigosa e impossível de apagar.
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
│  LÁZARO E INVESTIGAÇÃO                                                         │
│    interagir lazaro          abrir o canal                                    │
│    confiar  /  ignorar       tomar posição                                    │
│    rastrear transmissao      seguir o sinal da Agência                        │
│    bloquear transmissao      isolar a Agência                                 │
│    transferir lazaro         resgatar a IA                                    │
│                                                                                │
│  DECISÃO FINAL                                                                  │
│    rastrear protocolo zero   preparar o final secreto                         │
│    ativar protocolo zero     revelar a verdade                                │
│    destruir nucleo           eliminar LÁZARO                                  │
│    escapar                   deixar a MIRROR-9                                │
│                                                                                │
│  ajuda  ·  sair                                                                 │
╰────────────────────────────────────────────────────────────────────────────────╯

Cada comando reconhecido move o relógio da estação. Acentos são opcionais e alvos aceitam linguagem natural.
""".strip()
