"""Accent-insensitive command parser for the game."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Mapping
import unicodedata


@dataclass(frozen=True)
class ParsedCommand:
    verb: str
    target: str
    raw: str


VERB_ALIASES = {
    "explorar": "explore", "explore": "explore", "vasculhar": "explore", "procurar": "explore",
    "olhar": "explore", "examinar": "examine", "examinar": "examine", "inspecionar": "examine",
    "ver": "examine", "acessar": "access", "entrar": "access", "ir": "access", "navegar": "access",
    "mover": "access", "ler": "read", "lerlog": "read", "usar": "use", "reparar": "repair",
    "consertar": "repair", "interagir": "interact", "falar": "interact", "confiar": "trust",
    "acreditar": "trust", "ignorar": "ignore", "recusar": "ignore", "rastrear": "track",
    "localizar": "track", "bloquear": "block", "transferir": "transfer", "escapar": "escape",
    "fugir": "escape", "destruir": "destroy", "ejetar": "destroy", "ativar": "activate",
    "confrontar": "confront", "questionar": "confront", "salvar": "save", "proteger": "save",
    "preservar": "preserve", "manter": "preserve",
    "status": "status", "estado": "status", "inventario": "inventory", "itens": "inventory",
    "ajuda": "help", "help": "help", "comandos": "help", "sair": "quit", "quit": "quit",
}

TARGET_ALIASES = {
    "doca de acoplamento": "doca", "acoplamento": "doca", "manutencao": "manutencao",
    "laboratorio xenologico": "laboratorio", "laboratorio": "laboratorio", "jarvana": "jarvana",
    "alojamento": "alojamentos", "alojamentos": "alojamentos", "ponte de comando": "ponte",
    "ponte": "ponte", "nucleo xenologico": "nucleo", "nucleo": "nucleo", "terminal": "terminal",
    "painel": "painel", "vazamento": "vazamento", "oxigenio": "oxigenio", "o2": "oxigenio",
    "energia": "energia", "casco": "casco", "kit": "kit", "kit medico": "kit_medico",
    "armario": "armario", "arquivo": "arquivo", "transmissao": "transmissao",
    "sinal": "transmissao", "ordens": "ordens", "protocolo zero": "protocolo_zero",
    "zero": "protocolo_zero", "jarvana para modulo": "jarvana", "entidade": "jarvana",
    "tripulante": "tripulante", "pessoa": "tripulante", "imani": "tripulante", "dados": "dados",
}


def normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.lower().strip())
    no_accents = "".join(char for char in decomposed if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", no_accents)).strip()


def _target_from(words: list[str]) -> str:
    while words and words[0] in {"o", "a", "os", "as", "ao", "na", "no", "para", "de"}:
        words.pop(0)
    target = " ".join(words)
    if target.startswith("log"):
        digits = re.search(r"\d{1,2}", target)
        return f"log {int(digits.group(0)):02d}" if digits else "log"
    return TARGET_ALIASES.get(target, target)


def parse_command(raw: str, shortcuts: Mapping[str, str] | None = None) -> ParsedCommand:
    """Parse a free-text command or expand an active contextual shortcut."""
    cleaned = normalize(raw)
    if not cleaned:
        return ParsedCommand("", "", raw)
    if shortcuts:
        expanded = shortcuts.get(cleaned)
        if expanded:
            parsed = parse_command(expanded)
            return ParsedCommand(parsed.verb, parsed.target, raw)
    words = cleaned.split()
    first = words.pop(0)
    verb = VERB_ALIASES.get(first, "unknown")
    return ParsedCommand(verb, _target_from(words), raw)
