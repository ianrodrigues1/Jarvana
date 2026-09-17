"""Accent-insensitive command parser for the game."""

from __future__ import annotations

from dataclasses import dataclass
import re
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
    "status": "status", "estado": "status", "inventario": "inventory", "itens": "inventory",
    "ajuda": "help", "help": "help", "comandos": "help", "sair": "quit", "quit": "quit",
}

TARGET_ALIASES = {
    "doca de acoplamento": "doca", "acoplamento": "doca", "manutencao": "manutencao",
    "laboratorio lazaro": "laboratorio", "laboratorio": "laboratorio", "lazaro": "lazaro",
    "alojamento": "alojamentos", "alojamentos": "alojamentos", "ponte de comando": "ponte",
    "ponte": "ponte", "nucleo de lazaro": "nucleo", "nucleo": "nucleo", "terminal": "terminal",
    "painel": "painel", "vazamento": "vazamento", "oxigenio": "oxigenio", "o2": "oxigenio",
    "energia": "energia", "casco": "casco", "kit": "kit", "kit medico": "kit_medico",
    "armario": "armario", "arquivo": "arquivo", "transmissao": "transmissao",
    "sinal": "transmissao", "ordens": "ordens", "protocolo zero": "protocolo_zero",
    "zero": "protocolo_zero", "lazaro para modulo": "lazaro", "ia": "lazaro",
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


def parse_command(raw: str) -> ParsedCommand:
    cleaned = normalize(raw)
    if not cleaned:
        return ParsedCommand("", "", raw)
    words = cleaned.split()
    first = words.pop(0)
    verb = VERB_ALIASES.get(first, "unknown")
    return ParsedCommand(verb, _target_from(words), raw)
