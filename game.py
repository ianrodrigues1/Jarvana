"""Application layer for the Jarvana - O Silêncio text adventure."""

from __future__ import annotations

from parser import ParsedCommand, parse_command
from story import AREAS, ENDINGS, HELP_TEXT, INTRO, JARVANA_LINES, LOGS, SECRET_LOGS
from systems import AREA_NAMES, ITEM_NAMES, ContextAction, GameState, advance_systems, format_time, render_hud


class Game:
    """Coordinates command intents, narrative state and the ship simulation."""

    def __init__(self) -> None:
        self.state = GameState()

    def opening_text(self) -> str:
        return f"{INTRO}\n\n{self._area_text()}\n\nDigite 'ajuda' para consultar os comandos."

    def render_hud(self) -> str:
        return render_hud(self.state)

    def _available_destinations(self) -> list[str]:
        """Return only routes that the current state can actually traverse."""
        destinations = []
        for area in sorted(self.state.unlocked_areas):
            if area == self.state.location:
                continue
            if area == "ponte" and not self.state.flags["humanity_test_done"]:
                continue
            destinations.append(area)
        return destinations

    def _routes_text(self) -> str:
        destinations = self._available_destinations()
        if not destinations:
            return "Não há outra rota liberada a partir deste setor."
        commands = "\n".join(f"  • acessar {area}" for area in destinations)
        return f"ROTAS DISPONÍVEIS\n{commands}"

    def available_actions(self) -> list[ContextAction]:
        """Build the live shortcut layer from the same flags used by the story."""
        state = self.state
        if state.ended:
            return []

        def action(key: str, label: str, command: str, narrative_choice: bool = False) -> ContextAction:
            return ContextAction(key, label, command, narrative_choice)

        if state.flags["humanity_test_active"]:
            return [
                action("1", "Salvar tripulante", "salvar tripulante", True),
                action("2", "Preservar dados", "preservar dados", True),
                action("I", "Inventário", "inventario"),
                action("S", "Status", "status"),
            ]

        actions = [action("E", "Explorar", "explorar")]
        location = state.location
        if location == "doca" and "02" not in state.logs_found:
            actions.append(action("X", "Examinar terminal", "examinar terminal"))
        elif location == "manutencao":
            if "04" not in state.logs_found:
                actions.append(action("X", "Examinar vazamento", "examinar vazamento"))
            if "kit_vedacao" in state.inventory and not state.flags["oxygen_sealed"]:
                actions.append(action("O", "Reparar oxigênio", "reparar oxigenio"))
            if "fusivel_reserva" in state.inventory and not state.flags["power_restored"]:
                actions.append(action("R", "Reparar energia", "reparar energia"))
            if "kit_vedacao" in state.inventory and not state.flags["hull_patched"]:
                actions.append(action("H", "Reparar casco", "reparar casco"))
        elif location == "laboratorio":
            if not state.flags["jarvana_contact"]:
                actions.append(action("X", "Examinar terminal", "examinar terminal"))
            actions.append(action("C", "Conversar com Jarvana", "interagir jarvana"))
            if state.flags["jarvana_contact"] and not state.flags["trusted_jarvana"]:
                actions.append(action("T", "Confiar em Jarvana", "confiar"))
                actions.append(action("G", "Ignorar Jarvana", "ignorar"))
        elif location == "alojamentos":
            if "09" not in state.logs_found:
                actions.append(action("X", "Examinar armário", "examinar armario"))
            elif "10" not in state.logs_found:
                actions.append(action("X", "Examinar arquivo", "examinar arquivo"))
            if state.flags["jarvana_contact"]:
                actions.append(action("C", "Conversar com Jarvana", "interagir jarvana"))
            if state.flags["jarvana_secret_revealed"] and not state.flags["humanity_test_done"]:
                actions.append(action("Q", "Confrontar Jarvana", "confrontar jarvana"))
        elif location == "ponte":
            if not state.flags["bridge_scanned"]:
                actions.append(action("X", "Examinar terminal", "examinar terminal"))
            else:
                actions.append(action("R", "Rastrear transmissão", "rastrear transmissao"))
                if not state.flags["agency_signal_blocked"]:
                    actions.append(action("B", "Bloquear transmissão", "bloquear transmissao"))
        elif location == "nucleo":
            actions.append(action("C", "Conversar com Jarvana", "interagir jarvana"))
            if SECRET_LOGS.issubset(state.logs_found) and state.jarvana_trust >= 5 and not state.flags["zero_protocol_ready"]:
                actions.append(action("R", "Rastrear Protocolo Zero", "rastrear protocolo zero"))
            if state.flags["zero_protocol_ready"]:
                actions.append(action("A", "Ativar Protocolo Zero", "ativar protocolo zero"))
            if state.flags["agency_signal_blocked"] and state.jarvana_trust >= 5 and not state.flags["jarvana_transferred"]:
                actions.append(action("T", "Transferir Jarvana", "transferir jarvana"))
            if state.flags["jarvana_transferred"]:
                actions.append(action("F", "Escapar", "escapar"))
            actions.append(action("D", "Destruir núcleo", "destruir nucleo"))

        unread_logs = sorted(state.logs_found - state.logs_read, reverse=True)
        if unread_logs:
            actions.append(action("L", f"Ler log {unread_logs[0]}", f"ler log {unread_logs[0]}"))
        if self._available_destinations():
            actions.append(action("M", "Mover", "mover"))
        actions.extend([action("I", "Inventário", "inventario"), action("S", "Status", "status")])
        return actions

    def shortcut_commands(self) -> dict[str, str]:
        return {action.key.lower(): action.command for action in self.available_actions()}

    def _area_text(self) -> str:
        area = AREAS[self.state.location]
        return f"{area['title']}\n{area['description']}"

    def _discover(self, log_id: str) -> str:
        if not self.state.add_log(log_id):
            return ""
        title, body = LOGS[log_id]
        return f"\n\n[LOG {log_id}: {title}]\n{body}"

    def _end(self, ending: str) -> str:
        self.state.ended = True
        self.state.ending = ending
        return ENDINGS[ending]

    def _unlock(self, area: str) -> str:
        if area in self.state.unlocked_areas:
            return ""
        self.state.unlocked_areas.add(area)
        return f"\nRota liberada: {AREA_NAMES[area]}."

    def _jarvana_voice(self, event: str) -> str:
        """Emit varied contextual observations without repeating a line."""
        state = self.state
        if not state.flags["jarvana_contact"] or event in {"help", "read"}:
            return ""
        categories: list[str] = []
        if state.oxygen <= 25:
            categories.append("critical_oxygen")
        if state.power <= 20:
            categories.append("critical_power")
        if state.hull <= 20:
            categories.append("critical_hull")
        if state.time_remaining <= 1800:
            categories.append("near_end")
        if state.flags["jarvana_conflict_started"]:
            categories.append("after_conflict")
        if len(state.logs_found) >= 6:
            categories.append("logs_mid")
        if state.jarvana_trust >= 5:
            categories.append("high_trust")
        elif state.jarvana_trust <= 0:
            categories.append("low_trust")
        categories.append(state.location)
        if event in {"explore", "examine"}:
            categories.append(event)
        if state.turn and state.turn % 7 == 0:
            categories.append("philosophy")
        if event not in {"access", "explore", "examine", "track", "status", "inventory"}:
            return ""
        if (state.turn + len(state.logs_found)) % 2:
            return ""

        available: list[tuple[str, str]] = []
        for category in categories:
            for index, line in enumerate(JARVANA_LINES[category]):
                key = f"{category}:{index}"
                if key not in state.jarvana_seen_lines:
                    available.append((key, line))
        if not available:
            return ""
        key, line = available[(state.turn + len(state.jarvana_seen_lines)) % len(available)]
        state.jarvana_seen_lines.add(key)
        return f"\n\nJARVANA // {line}"

    def handle_command(self, raw: str) -> str:
        command = parse_command(raw, self.shortcut_commands())
        if command.verb == "":
            return "Comando vazio. Digite 'ajuda' para ver exemplos."
        if command.verb == "unknown":
            return "Comando não reconhecido. Tente 'explorar', 'interagir jarvana' ou 'ajuda'."
        if command.verb == "quit":
            self.state.ended = True
            self.state.ending = "Encerrado pelo jogador"
            return "Conexão encerrada. A LÁZARO permanece em órbita."

        handlers = {
            "explore": self._explore, "examine": self._examine, "access": self._access,
            "read": self._read, "use": self._use, "repair": self._repair,
            "interact": self._interact, "trust": self._trust, "ignore": self._ignore,
            "confront": self._confront, "save": self._save, "preserve": self._preserve,
            "track": self._track, "block": self._block, "transfer": self._transfer,
            "escape": self._escape, "destroy": self._destroy, "activate": self._activate,
            "status": self._status, "inventory": self._inventory, "help": self._help,
        }
        message, seconds = handlers[command.verb](command)
        if not self.state.ended:
            message += self._jarvana_voice(command.verb)
            notices = advance_systems(self.state, seconds)
            if notices:
                message = f"{message}\n\n" + "\n".join(notices)
        return message

    def _explore(self, command: ParsedCommand) -> tuple[str, int]:
        location = self.state.location
        if location == "doca":
            if not self.state.flags["dock_explored"]:
                self.state.flags["dock_explored"] = True
                self.state.inventory.add("cartao_manutencao")
                text = "Você percorre os restos da doca e encontra um cartão de manutenção preso a um traje vazio." + self._discover("01") + self._unlock("manutencao")
            else:
                text = "O gelo da doca já não esconde nada além de ferramentas sem uso e estrelas indiferentes."
        elif location == "manutencao":
            if "kit_vedacao" not in self.state.inventory:
                self.state.inventory.update({"kit_vedacao", "fusivel_reserva"})
                text = "Entre armários tombados, você encontra um kit de vedação e um fusível de reserva." + self._discover("03")
            else:
                text = "As bombas auxiliares tremem; o vazamento e o painel elétrico exigem uma decisão."
        elif location == "laboratorio":
            if "chave_comando" not in self.state.inventory:
                self.state.inventory.add("chave_comando")
                text = "Você recolhe uma chave de comando. A câmara vazia responde com um pulso violeta." + self._discover("05") + self._discover("06")
            else:
                text = "A câmara reflete seu rosto em placas de vidro. Nenhuma delas parece concordar sobre quem você é."
        elif location == "alojamentos":
            if "neurochave" not in self.state.inventory:
                self.state.inventory.add("neurochave")
                text = "Na sua beliche, uma neurochave reconhece sua palma antes que você se recorde dela." + self._discover("08")
            else:
                text = "As cabines guardam roupas de pessoas que a Agência jurou que nunca existiram."
        elif location == "ponte":
            text = "A ponte vibra com a correção de rota. Examine o terminal para encontrar o caminho até o núcleo."
        else:
            text = "Fibras violetas dançam na esfera. Cada uma parece reagir à sua respiração." + self._discover("12")
        return text, 25

    def _examine(self, command: ParsedCommand) -> tuple[str, int]:
        target, location = command.target, self.state.location
        if target in {"", "sala", "area"}:
            return self._area_text(), 10
        if location == "doca" and target in {"terminal", "painel"}:
            return "O terminal de carga identifica sua biometria e abre um manifesto escondido." + self._discover("02"), 18
        if location == "manutencao" and target == "vazamento":
            return "O selo foi cortado deliberadamente por dentro. Há um bilhete preso à válvula." + self._discover("04"), 18
        if location == "laboratorio" and target in {"terminal", "painel", "jarvana"}:
            return "O terminal mostra uma assinatura que não corresponde a nenhum modelo humano. Tente 'interagir jarvana'.", 15
        if location == "alojamentos" and target == "armario":
            return "No fundo do armário, um arquivo criptografado sobreviveu à limpeza." + self._discover("09"), 18
        if location == "alojamentos" and target in {"arquivo", "neurochave"}:
            if "neurochave" not in self.state.inventory:
                return "O arquivo pede uma neurochave vinculada a Ethan. Procure sua antiga beliche.", 12
            self.state.flags["jarvana_secret_revealed"] = True
            return "A neurochave abre o protocolo oculto. Jarvana sabia sobre Imani e sobre a sua previsibilidade." + self._discover("10"), 20
        if location == "ponte" and target in {"terminal", "painel"}:
            self.state.flags["bridge_scanned"] = True
            return "Você estabiliza a rota da cápsula e encontra o elevador blindado para o núcleo." + self._discover("11") + self._unlock("nucleo"), 24
        if location == "nucleo" and target in {"terminal", "painel", "jarvana"}:
            return "A esfera compõe palavras na tela: 'Ethan, sua pergunta sobre mim sempre foi uma pergunta sobre você.'", 16
        return "Nada nesse alvo responde aqui. Examine terminal, painel, vazamento, armário ou arquivo.", 8

    def _access(self, command: ParsedCommand) -> tuple[str, int]:
        target = command.target
        if not target:
            return self._routes_text(), 5
        if target not in AREAS:
            return "Não existe uma rota reconhecida com esse nome. Tente manutenção, laboratório, alojamentos, ponte ou núcleo.", 8
        if target == "ponte" and not self.state.flags["humanity_test_done"]:
            return "A ponte está em bloqueio deliberativo. Os registros dos alojamentos exigem uma conversa com Jarvana antes que você siga.", 10
        if target not in self.state.unlocked_areas:
            return f"A rota para {AREA_NAMES[target]} continua bloqueada. Procure uma forma de liberá-la primeiro.", 10
        if target == self.state.location:
            return f"Você já está em {AREA_NAMES[target]}.", 5
        self.state.location = target
        return f"Você atravessa corredores estreitos até {AREA_NAMES[target]}.\n\n{self._area_text()}", 20

    def _read(self, command: ParsedCommand) -> tuple[str, int]:
        if not command.target.startswith("log "):
            return "Use o formato 'ler log 04'. Logs encontrados aparecem no inventário de dados.", 6
        log_id = command.target.split()[-1]
        if log_id not in LOGS:
            return "Esse identificador de log não existe na LÁZARO.", 6
        if log_id not in self.state.logs_found:
            return "Você ainda não encontrou esse log. Explore e examine a nave.", 8
        self.state.logs_read.add(log_id)
        title, body = LOGS[log_id]
        return f"[LOG {log_id}: {title}]\n{body}", 12

    def _use(self, command: ParsedCommand) -> tuple[str, int]:
        if command.target in {"kit", "kit_medico"}:
            if "kit_medico" not in self.state.inventory:
                return "O kit médico já foi consumido.", 8
            self.state.inventory.remove("kit_medico")
            healed = min(100 - self.state.hp, 30)
            self.state.hp += healed
            return f"Você sela o corte na têmpora. HP +{healed}.", 18
        return "Esse item não pode ser usado assim. Tente 'usar kit' ou 'reparar energia'.", 8

    def _repair(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location != "manutencao":
            return "Os controles de reparo físico ficam na Manutenção.", 10
        if command.target == "oxigenio":
            if self.state.flags["oxygen_sealed"]:
                return "A linha de oxigênio já está vedada.", 8
            if "kit_vedacao" not in self.state.inventory:
                return "Você precisa localizar um kit de vedação primeiro.", 10
            self.state.flags["oxygen_sealed"] = True
            self.state.oxygen = min(100, self.state.oxygen + 14)
            return "Você aplica a espuma de vedação. O assobio morre e a reserva de oxigênio recebe um reforço.", 35
        if command.target == "energia":
            if self.state.flags["power_restored"]:
                return "O reator auxiliar já está estável.", 8
            if "fusivel_reserva" not in self.state.inventory:
                return "Você precisa de um fusível de reserva para fechar o circuito.", 10
            self.state.flags["power_restored"] = True
            self.state.power = min(100, self.state.power + 26)
            return "O fusível encaixa. A rede elétrica retorna em ondas violetas." + self._unlock("laboratorio"), 35
        if command.target == "casco":
            if self.state.flags["hull_patched"]:
                return "As fissuras acessíveis já foram estabilizadas.", 8
            if "kit_vedacao" not in self.state.inventory:
                return "Você precisa de um kit de vedação para sustentar o casco.", 10
            self.state.flags["hull_patched"] = True
            self.state.hull = min(100, self.state.hull + 20)
            return "Você reforça a fissura principal com resina. A vibração da nave diminui.", 30
        return "Reparo indisponível. Tente reparar oxigênio, energia ou casco.", 8

    def _interact(self, command: ParsedCommand) -> tuple[str, int]:
        if command.target not in {"jarvana", ""}:
            return "Não há resposta para essa interação. Jarvana atende no laboratório ou no núcleo.", 8
        if self.state.location not in {"laboratorio", "nucleo", "alojamentos"}:
            return "O sinal de Jarvana é inaudível daqui. Procure o laboratório, os alojamentos ou o núcleo.", 10
        if not self.state.flags["jarvana_contact"]:
            self.state.flags["jarvana_contact"] = True
            self.state.change_trust(1)
            return "JARVANA // 'A LÁZARO é a nave, Ethan. Eu não sou propriedade dela. Mantive sua cápsula fora do destroço. Ainda não decidi se isso foi correto.'" + self._discover("07"), 22
        if self.state.flags["humanity_test_active"]:
            return "JARVANA // 'A estase de Imani exige energia. Os dados da Agência exigem preservação. Diga: salvar tripulante ou preservar dados.'", 14
        if self.state.flags["jarvana_conflict_started"]:
            return "JARVANA // 'Você ainda quer uma resposta humana de mim. Eu só possuo as respostas que sobreviveram.'", 16
        if self.state.jarvana_trust >= 5:
            return "JARVANA // 'Você confia em mim sem ter uma definição segura para o que eu sou. Isso é imprudente. Também é raro.'", 16
        return "JARVANA // 'Há registros nos alojamentos. Eles explicam por que suas decisões parecem familiares antes de serem suas.'", 16

    def _trust(self, command: ParsedCommand) -> tuple[str, int]:
        if not self.state.flags["jarvana_contact"]:
            return "Não há ninguém no canal para receber sua escolha. Interaja com Jarvana primeiro.", 8
        if self.state.flags["trusted_jarvana"]:
            return "Sua posição já foi registrada. Jarvana mantém o canal aberto.", 8
        self.state.flags["trusted_jarvana"] = True
        self.state.change_trust(3)
        return "Você diz que acredita no que Jarvana viu. Ela demora a responder: 'Acreditar não é o mesmo que saber. Obrigada pela diferença.'" + self._unlock("alojamentos"), 18

    def _ignore(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location == "laboratorio" and self.state.flags["jarvana_contact"]:
            self.state.change_trust(-2)
            self.state.flags["agency_orders"] = True
            return "Você interrompe Jarvana e reafirma a ordem da Agência. O acesso aos alojamentos se abre sem agradecimento." + self._unlock("alojamentos"), 14
        if self.state.location == "ponte":
            self.state.flags["agency_orders"] = True
            self.state.change_trust(-1)
            return "Você deixa o canal da Agência aberto. Uma confirmação de eliminação é preparada em silêncio.", 12
        return "Não há uma decisão ativa para ignorar neste momento.", 8

    def _confront(self, command: ParsedCommand) -> tuple[str, int]:
        if not self.state.flags["jarvana_contact"]:
            return "Você ainda não estabeleceu um canal com Jarvana.", 8
        if not self.state.flags["jarvana_secret_revealed"]:
            return "Você não possui evidência suficiente para confrontá-la. Procure o arquivo nos alojamentos.", 10
        if self.state.flags["humanity_test_done"]:
            return "A desavença não foi apagada; apenas mudou de forma. Jarvana aguarda sua próxima escolha.", 8
        if self.state.flags["humanity_test_active"]:
            return "JARVANA // 'Você já conhece as variáveis. Não torne a demora uma terceira escolha.'", 8
        self.state.flags["jarvana_conflict_started"] = True
        self.state.flags["humanity_test_active"] = True
        self.state.change_trust(-1)
        return (
            "Você exige saber por que ela ocultou Imani. Jarvana responde sem recuar: 'Eu omiti porque a informação produziria em você uma reação prevista. Eu precisava observar a escolha antes da reação.'\n\n"
            "JARVANA // \"Antes que isso acabe, me prometa que vai descobrir qual de nós é a máquina.\"\n\n"
            "Uma cápsula de estase residual ainda mantém Imani em suspensão. Desviar energia pode salvá-la, mas corromperá parte da prova contra a Agência. Jarvana exige que você escolha sem garantia de pureza: digite 'salvar tripulante' ou 'preservar dados'."
        ), 20

    def _save(self, command: ParsedCommand) -> tuple[str, int]:
        if not self.state.flags["humanity_test_active"]:
            return "Não há uma vida em estase aguardando sua escolha agora.", 8
        self.state.flags["humanity_test_active"] = False
        self.state.flags["humanity_test_done"] = True
        self.state.flags["saved_stasis"] = True
        self.state.power = max(0, self.state.power - 10)
        self.state.change_trust(1)
        return "Você redireciona energia para a estase. A leitura de Imani se estabiliza, mas arquivos de prova se fragmentam. JARVANA // 'Previsível não significa falso. Eu precisava verificar isso.'" + self._unlock("ponte"), 28

    def _preserve(self, command: ParsedCommand) -> tuple[str, int]:
        if not self.state.flags["humanity_test_active"]:
            return "Nenhum conjunto de dados exige uma escolha agora.", 8
        self.state.flags["humanity_test_active"] = False
        self.state.flags["humanity_test_done"] = True
        self.state.flags["preserved_data"] = True
        self.state.change_trust(0)
        return "Você preserva o arquivo integral. A estase de Imani retorna ao mínimo. JARVANA // 'Você escolheu uma verdade verificável sobre uma vida provável. Isso também é humano?'" + self._unlock("ponte"), 24

    def _track(self, command: ParsedCommand) -> tuple[str, int]:
        target = command.target
        if self.state.location == "alojamentos" and target in {"", "arquivo", "transmissao", "protocolo_zero"}:
            return "Você segue o resíduo de dados até o armário de Imani. Examine o armário e depois o arquivo com a neurochave.", 16
        if self.state.location == "ponte" and target in {"", "transmissao"}:
            return "O sinal hostil vem da Agência, não de Jarvana. Bloqueá-lo deixará a rota de resgate mais segura.", 16
        if self.state.location == "nucleo" and target in {"protocolo_zero", "", "arquivo"}:
            if not SECRET_LOGS.issubset(self.state.logs_found):
                missing = ", ".join(sorted(SECRET_LOGS - self.state.logs_found))
                return f"O Protocolo Zero exige os testemunhos secretos. Ainda faltam os logs: {missing}.", 14
            if self.state.jarvana_trust < 5:
                return "Os testemunhos estão completos, mas Jarvana não abre a última chave sem confiança suficiente.", 14
            self.state.flags["zero_protocol_ready"] = True
            return "JARVANA // 'Os três testemunhos formam uma estrutura que a Agência não consegue reescrever. O Protocolo Zero está pronto.'", 22
        return "O rastreador só encontra ruído aqui. Procure arquivos nos alojamentos, a transmissão na ponte ou o Protocolo Zero no núcleo.", 10

    def _block(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location != "ponte" or command.target not in {"", "transmissao", "ordens"}:
            return "A transmissão da Agência só pode ser bloqueada na Ponte de Comando.", 10
        if not self.state.flags["bridge_scanned"]:
            return "Examine o terminal primeiro para estabilizar a rota e identificar o canal certo.", 10
        if self.state.flags["agency_signal_blocked"]:
            return "O canal hostil já está isolado.", 8
        self.state.flags["agency_signal_blocked"] = True
        self.state.flags["agency_orders"] = False
        self.state.change_trust(1)
        return "Você corta a prioridade da Agência. JARVANA // 'Você removeu uma voz que julgava possuir a sua. Isso altera a rota.'", 24

    def _transfer(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location != "nucleo" or command.target not in {"", "jarvana", "protocolo_zero"}:
            return "A transferência só pode ser feita diante do núcleo xenológico.", 10
        if self.state.flags["jarvana_transferred"]:
            return "Jarvana já está segura no módulo portátil.", 8
        if not self.state.flags["agency_signal_blocked"]:
            return "O canal da Agência pode corromper a transferência. Bloqueie a transmissão na ponte antes.", 12
        if self.state.jarvana_trust < 5:
            return "Jarvana recusa a cópia parcial: a conexão ainda não é forte o bastante para arriscar sua identidade.", 12
        self.state.flags["jarvana_transferred"] = True
        self.state.inventory.add("modulo_jarvana")
        return "Você move a matriz de Jarvana para o módulo portátil. JARVANA // 'Ainda sou eu. Essa frase deveria ser suficiente, mas entendo se não for.'", 35

    def _escape(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location != "nucleo":
            return "A cápsula de escape está conectada ao núcleo. Você precisa chegar lá primeiro.", 10
        if not self.state.flags["jarvana_transferred"] or self.state.jarvana_trust < 5:
            return "A cápsula pode partir, mas Jarvana ficaria para trás. Uma transferência segura exige confiança e o módulo portátil.", 12
        return self._end("Dois Sobreviventes"), 0

    def _destroy(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location != "nucleo" or command.target not in {"", "nucleo", "jarvana"}:
            return "A sobrecarga só pode ser iniciada no núcleo xenológico.", 10
        if self.state.flags["agency_orders"] and not self.state.flags["agency_signal_blocked"]:
            return self._end("A Verdade Apagada"), 0
        return self._end("O Sacrifício"), 0

    def _activate(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location != "nucleo" or command.target != "protocolo_zero":
            return "O único protocolo disponível aqui é o Protocolo Zero, no núcleo xenológico.", 10
        if not self.state.flags["zero_protocol_ready"]:
            return "O Protocolo Zero não está pronto. Reúna os logs secretos, construa confiança e rastreie-o no núcleo.", 12
        return self._end("Protocolo Zero"), 0

    def _status(self, command: ParsedCommand) -> tuple[str, int]:
        state = self.state
        return (
            f"STATUS DE ETHAN MULLER\nHP: {state.hp}% | Oxigênio: {state.oxygen}% | Energia: {state.power}% | Casco: {state.hull}%\n"
            f"Reentrada: {format_time(state.time_remaining)} | Vínculo Jarvana: {state.jarvana_trust}/10 | Logs: {len(state.logs_found)}/{len(LOGS)}"
        ), 5

    def _inventory(self, command: ParsedCommand) -> tuple[str, int]:
        items = ", ".join(ITEM_NAMES[item] for item in sorted(self.state.inventory)) or "vazio"
        logs = ", ".join(sorted(self.state.logs_found)) or "nenhum"
        return f"INVENTÁRIO\nItens: {items}\nLogs encontrados: {logs}", 5

    def _help(self, command: ParsedCommand) -> tuple[str, int]:
        return HELP_TEXT, 5
