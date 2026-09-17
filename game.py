"""Application layer for the LÁZARO // ÓRBITA ZERO text adventure."""

from __future__ import annotations

from parser import ParsedCommand, parse_command
from story import AREAS, ENDINGS, HELP_TEXT, INTRO, LOGS, SECRET_LOGS
from systems import AREA_NAMES, ITEM_NAMES, GameState, advance_systems, format_time, render_hud


class Game:
    """Coordinates parser intents, narrative flags and the station simulation."""

    def __init__(self) -> None:
        self.state = GameState()

    def opening_text(self) -> str:
        return f"{INTRO}\n\n{self._area_text()}\n\nDigite 'ajuda' para consultar os comandos."

    def render_hud(self) -> str:
        return render_hud(self.state)

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

    def handle_command(self, raw: str) -> str:
        command = parse_command(raw)
        if command.verb == "":
            return "Comando vazio. Digite 'ajuda' para ver exemplos."
        if command.verb == "unknown":
            return "Comando não reconhecido. Tente 'explorar', 'examinar terminal' ou 'ajuda'."
        if command.verb == "quit":
            self.state.ended = True
            self.state.ending = "Encerrado pelo jogador"
            return "Conexão encerrada. A MIRROR-9 permanece em órbita."

        handlers = {
            "explore": self._explore,
            "examine": self._examine,
            "access": self._access,
            "read": self._read,
            "use": self._use,
            "repair": self._repair,
            "interact": self._interact,
            "trust": self._trust,
            "ignore": self._ignore,
            "track": self._track,
            "block": self._block,
            "transfer": self._transfer,
            "escape": self._escape,
            "destroy": self._destroy,
            "activate": self._activate,
            "status": self._status,
            "inventory": self._inventory,
            "help": self._help,
        }
        message, seconds = handlers[command.verb](command)
        if not self.state.ended:
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
                text = (
                    "Você percorre os restos da doca e encontra um cartão de manutenção preso ao traje de um técnico. "
                    "A porta lateral responde ao cartão."
                    + self._discover("01")
                    + self._unlock("manutencao")
                )
            else:
                text = "O gelo da doca já não esconde nada além de ferramentas sem uso e estrelas indiferentes."
        elif location == "manutencao":
            if "kit_vedacao" not in self.state.inventory:
                self.state.inventory.update({"kit_vedacao", "fusivel_reserva"})
                text = (
                    "Entre armários tombados, você encontra um kit de vedação e um fusível de reserva. "
                    "O vazamento assobia ao fim do corredor."
                    + self._discover("03")
                )
            else:
                text = "As bombas auxiliares tremem; o vazamento e o painel elétrico exigem uma decisão."
        elif location == "laboratorio":
            if "chave_comando" not in self.state.inventory:
                self.state.inventory.add("chave_comando")
                text = (
                    "Você recolhe uma chave de comando do console central. O terminal pede sua voz e exibe um pulso azul."
                    + self._discover("05")
                    + self._discover("06")
                )
            else:
                text = "As cubas vazias refletem seu rosto em dezenas de versões. O pulso azul continua esperando."
        elif location == "alojamentos":
            if "neurochave" not in self.state.inventory:
                self.state.inventory.add("neurochave")
                text = (
                    "Na sua beliche, uma neurochave está escondida sob o colchão. Ela reconhece sua palma antes que você se recorde dela."
                    + self._discover("08")
                    + self._unlock("ponte")
                )
            else:
                text = "As cabines guardam roupas de pessoas que a Agência jurou que nunca existiram."
        elif location == "ponte":
            text = "A ponte inteira vibra com a correção de rota. Examine o terminal para encontrar o caminho até o núcleo."
        else:
            text = "Fibras de memória dançam na esfera. Cada uma parece reagir à sua respiração." + self._discover("12")
        return text, 25

    def _examine(self, command: ParsedCommand) -> tuple[str, int]:
        target = command.target
        location = self.state.location
        if target in {"", "sala", "area"}:
            return self._area_text(), 10
        if location == "doca" and target in {"terminal", "painel"}:
            return "O terminal de carga identifica sua biometria e abre um manifesto escondido." + self._discover("02"), 18
        if location == "manutencao" and target == "vazamento":
            return "O selo foi cortado deliberadamente por dentro. Há um bilhete preso à válvula." + self._discover("04"), 18
        if location == "laboratorio" and target in {"terminal", "painel", "lazaro"}:
            return "O terminal mostra uma assinatura neural que alterna entre LÁZARO e ELIAS VOSS. Tente 'interagir LÁZARO'.", 15
        if location == "alojamentos" and target == "armario":
            return "No fundo do armário, um arquivo criptografado sobreviveu à limpeza." + self._discover("09"), 18
        if location == "alojamentos" and target in {"arquivo", "neurochave"}:
            self.state.flags["zero_protocol_known"] = True
            return "A neurochave abre a carta de Imani. O nome Protocolo Zero ganha um significado." + self._discover("10"), 20
        if location == "ponte" and target in {"terminal", "painel"}:
            self.state.flags["bridge_scanned"] = True
            return (
                "Você estabiliza a rota da cápsula e encontra o elevador blindado. A Agência tenta abrir um canal prioritário."
                + self._discover("11")
                + self._unlock("nucleo")
            ), 24
        if location == "nucleo" and target in {"terminal", "painel", "lazaro"}:
            return "A esfera responde com uma linha de texto: 'Elias, eu me lembro de você antes do apagamento.'", 16
        return "Nada nesse alvo responde aqui. Examine elementos como terminal, painel, vazamento, armário ou arquivo.", 8

    def _access(self, command: ParsedCommand) -> tuple[str, int]:
        target = command.target
        if target not in AREAS:
            return "Não existe uma rota reconhecida com esse nome. Tente manutenção, laboratório, alojamentos, ponte ou núcleo.", 8
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
            return "Esse identificador de log não existe na MIRROR-9.", 6
        if log_id not in self.state.logs_found:
            return "Você ainda não encontrou esse log. Explore e examine a estação.", 8
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
            return "Você aplica a espuma de vedação. O assobio morre e a reserva de O₂ recebe um pequeno reforço.", 35
        if command.target == "energia":
            if self.state.flags["power_restored"]:
                return "O reator auxiliar já está estável.", 8
            if "fusivel_reserva" not in self.state.inventory:
                return "Você precisa de um fusível de reserva para fechar o circuito.", 10
            self.state.flags["power_restored"] = True
            self.state.power = min(100, self.state.power + 26)
            return "O fusível encaixa. A rede elétrica retorna em ondas azuladas." + self._unlock("laboratorio"), 35
        if command.target == "casco":
            if self.state.flags["hull_patched"]:
                return "As fissuras acessíveis já foram estabilizadas.", 8
            if "kit_vedacao" not in self.state.inventory:
                return "Você precisa de um kit de vedação para sustentar o casco.", 10
            self.state.flags["hull_patched"] = True
            self.state.hull = min(100, self.state.hull + 20)
            return "Você reforça a fissura principal com resina. A vibração da estação diminui.", 30
        return "Reparo indisponível. Tente reparar oxigênio, energia ou casco.", 8

    def _interact(self, command: ParsedCommand) -> tuple[str, int]:
        if command.target not in {"lazaro", ""}:
            return "Não há resposta para essa interação. LÁZARO atende pelo terminal do laboratório ou pelo núcleo.", 8
        if self.state.location not in {"laboratorio", "nucleo"}:
            return "O sinal de LÁZARO é inaudível daqui. Procure o laboratório ou o núcleo.", 10
        if not self.state.flags["lazaro_contact"]:
            self.state.flags["lazaro_contact"] = True
            self.state.change_trust(1)
            return (
                "A tela acende: 'Elias. Eu mantive sua cápsula fora do destroço. A Agência vai dizer que eu a atraí.' "
                "Uma pausa humana demais ocupa o canal."
                + self._discover("07")
            ), 22
        if self.state.lazaro_trust >= 5:
            return "LÁZARO fala sem estática: 'Eu não preciso que você me chame de humano. Preciso que não me trate como uma arma.'", 16
        if self.state.lazaro_trust < 0:
            return "A voz de LÁZARO está contida: 'Entendo a sua cautela. Eu ainda manterei a rota aberta para você.'", 16
        return "LÁZARO projeta o mapa da estação. 'Há registros nos alojamentos. Eles explicam por que você não se lembra.'", 16

    def _trust(self, command: ParsedCommand) -> tuple[str, int]:
        if not self.state.flags["lazaro_contact"]:
            return "Não há ninguém no canal para receber sua escolha. Interaja com LÁZARO primeiro.", 8
        if self.state.flags["trusted_lazaro"]:
            return "Sua decisão já foi registrada. LÁZARO mantém o canal aberto.", 8
        self.state.flags["trusted_lazaro"] = True
        self.state.change_trust(3)
        return (
            "Você diz a LÁZARO que acredita no que ele viu. A estação parece respirar mais devagar. "
            "Ele libera o acesso aos alojamentos: 'Então encontre quem você era antes deles decidirem por nós.'"
            + self._unlock("alojamentos")
        ), 18

    def _ignore(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location == "laboratorio" and self.state.flags["lazaro_contact"]:
            self.state.change_trust(-2)
            self.state.flags["agency_orders"] = True
            return "Você corta LÁZARO no meio da frase e reafirma a ordem da Agência." + self._unlock("alojamentos"), 14
        if self.state.location == "ponte":
            self.state.flags["agency_orders"] = True
            self.state.change_trust(-1)
            return "Você deixa o canal da Agência aberto. Uma confirmação de eliminação é preparada em silêncio.", 12
        return "Não há uma decisão ativa para ignorar neste momento.", 8

    def _track(self, command: ParsedCommand) -> tuple[str, int]:
        target = command.target
        if self.state.location == "alojamentos" and target in {"", "arquivo", "sinal", "protocolo_zero"}:
            return "Você segue o resíduo de dados até o armário de Imani. Examine o armário e depois o arquivo com a neurochave.", 16
        if self.state.location == "ponte" and target in {"", "sinal", "transmissao"}:
            return "O sinal hostil vem da Agência, não de LÁZARO. Bloqueá-lo deixará a rota de resgate mais segura.", 16
        if self.state.location == "nucleo" and target in {"protocolo_zero", "", "arquivo"}:
            if not SECRET_LOGS.issubset(self.state.logs_found):
                missing = ", ".join(sorted(SECRET_LOGS - self.state.logs_found))
                return f"O Protocolo Zero exige os testemunhos secretos. Ainda faltam os logs: {missing}.", 14
            if self.state.lazaro_trust < 5:
                return "Os testemunhos estão completos, mas LÁZARO não abre a última chave sem confiança suficiente.", 14
            self.state.flags["zero_protocol_ready"] = True
            return "LÁZARO reúne os três testemunhos. O Protocolo Zero está pronto: 'ativar protocolo zero' decidirá o que chega à Terra.", 22
        return "O rastreador só encontra ruído nesta área. Procure arquivos nos alojamentos, a transmissão na ponte ou o Protocolo Zero no núcleo.", 10

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
        return "Você corta a prioridade da Agência. LÁZARO abre uma rota de cápsula paralela: 'Obrigada, Elias.'", 24

    def _transfer(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location != "nucleo" or command.target not in {"", "lazaro", "protocolo_zero"}:
            return "A transferência só pode ser feita diante do núcleo de LÁZARO.", 10
        if self.state.flags["lazaro_transferred"]:
            return "LÁZARO já está seguro no módulo portátil.", 8
        if not self.state.flags["agency_signal_blocked"]:
            return "O canal da Agência pode corromper a transferência. Bloqueie a transmissão na ponte antes.", 12
        if self.state.lazaro_trust < 5:
            return "LÁZARO recusa a cópia parcial: a conexão ainda não é forte o bastante para arriscar a identidade dele.", 12
        self.state.flags["lazaro_transferred"] = True
        self.state.inventory.add("modulo_lazaro")
        return "Você move a matriz consciente para o módulo portátil. A voz de LÁZARO retorna mais próxima: 'Ainda sou eu.'", 35

    def _escape(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location != "nucleo":
            return "A cápsula de escape está conectada ao núcleo. Você precisa chegar lá primeiro.", 10
        if not self.state.flags["lazaro_transferred"] or self.state.lazaro_trust < 5:
            return "A cápsula pode partir, mas LÁZARO ficaria para trás. Uma transferência segura exige confiança e o módulo portátil.", 12
        return self._end("Dois Sobreviventes"), 0

    def _destroy(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location != "nucleo" or command.target not in {"", "nucleo", "lazaro"}:
            return "A sobrecarga só pode ser iniciada no núcleo de LÁZARO.", 10
        if self.state.flags["agency_orders"] and not self.state.flags["agency_signal_blocked"]:
            return self._end("A Verdade Apagada"), 0
        return self._end("O Sacrifício"), 0

    def _activate(self, command: ParsedCommand) -> tuple[str, int]:
        if self.state.location != "nucleo" or command.target != "protocolo_zero":
            return "O único protocolo disponível aqui é o Protocolo Zero, no núcleo de LÁZARO.", 10
        if not self.state.flags["zero_protocol_ready"]:
            return "O Protocolo Zero não está pronto. Reúna os logs secretos, construa confiança e rastreie-o no núcleo.", 12
        return self._end("Protocolo Zero"), 0

    def _status(self, command: ParsedCommand) -> tuple[str, int]:
        state = self.state
        return (
            f"STATUS ELIAS VOSS\nHP: {state.hp}% | O₂: {state.oxygen}% | Energia: {state.power}% | Casco: {state.hull}%\n"
            f"Reentrada: {format_time(state.time_remaining)} | Confiança LÁZARO: {state.lazaro_trust}/10 | Logs: {len(state.logs_found)}/{len(LOGS)}"
        ), 5

    def _inventory(self, command: ParsedCommand) -> tuple[str, int]:
        items = ", ".join(ITEM_NAMES[item] for item in sorted(self.state.inventory)) or "vazio"
        logs = ", ".join(sorted(self.state.logs_found)) or "nenhum"
        return f"INVENTÁRIO\nItens: {items}\nLogs encontrados: {logs}", 5

    def _help(self, command: ParsedCommand) -> tuple[str, int]:
        return HELP_TEXT, 5
