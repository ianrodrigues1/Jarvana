"""State, resource simulation and terminal presentation for MIRROR-9."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import ceil
import os
import sys
from typing import Optional


AREA_NAMES = {
    "doca": "DOCA DE ACOPLAMENTO",
    "manutencao": "MANUTENÇÃO",
    "laboratorio": "LABORATÓRIO LÁZARO",
    "alojamentos": "ALOJAMENTOS",
    "ponte": "PONTE DE COMANDO",
    "nucleo": "NÚCLEO DE LÁZARO",
}


ITEM_NAMES = {
    "lanterna": "lanterna magnética",
    "kit_medico": "kit médico",
    "cartao_manutencao": "cartão de manutenção",
    "kit_vedacao": "kit de vedação",
    "fusivel_reserva": "fusível de reserva",
    "chave_comando": "chave de comando",
    "neurochave": "neurochave de Elias",
    "modulo_lazaro": "módulo portátil LÁZARO",
}


class Ansi:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"


def enable_terminal_colors() -> None:
    """Enable ANSI output on supported Windows terminals without dependencies."""
    if os.name == "nt":
        os.system("")


def colors_available() -> bool:
    return sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def paint(text: str, *styles: str) -> str:
    if not colors_available() or not styles:
        return text
    return "".join(styles) + text + Ansi.RESET


@dataclass
class GameState:
    """All mutable game state in one deliberately serializable structure."""

    hp: int = 100
    oxygen: int = 84
    power: int = 68
    hull: int = 76
    time_remaining: int = 4800
    initial_time: int = 4800
    lazaro_trust: int = 0
    inventory: set[str] = field(default_factory=lambda: {"lanterna", "kit_medico"})
    logs_found: set[str] = field(default_factory=set)
    unlocked_areas: set[str] = field(default_factory=lambda: {"doca"})
    flags: dict[str, bool] = field(
        default_factory=lambda: {
            "dock_explored": False,
            "oxygen_sealed": False,
            "power_restored": False,
            "hull_patched": False,
            "lazaro_contact": False,
            "trusted_lazaro": False,
            "agency_orders": True,
            "agency_signal_blocked": False,
            "bridge_scanned": False,
            "lazaro_transferred": False,
            "zero_protocol_known": False,
            "zero_protocol_ready": False,
        }
    )
    location: str = "doca"
    turn: int = 0
    ended: bool = False
    ending: Optional[str] = None

    def add_log(self, log_id: str) -> bool:
        """Record a log and report whether it was newly found."""
        if log_id in self.logs_found:
            return False
        self.logs_found.add(log_id)
        return True

    def change_trust(self, amount: int) -> int:
        self.lazaro_trust = max(-5, min(10, self.lazaro_trust + amount))
        return self.lazaro_trust


def format_time(seconds: int) -> str:
    seconds = max(0, seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def visual_bar(value: int, maximum: int = 100, width: int = 10) -> str:
    value = max(0, min(maximum, value))
    filled = round((value / maximum) * width) if maximum else 0
    return "█" * filled + "░" * (width - filled)


def _resource_style(value: int) -> str:
    if value <= 25:
        return Ansi.RED
    if value <= 50:
        return Ansi.YELLOW
    return Ansi.GREEN


def _meter(label: str, value: int, suffix: str = "%") -> str:
    bar = visual_bar(value, width=20)
    colored_bar = paint(bar[: bar.count("█")], _resource_style(value)) + paint(
        bar[bar.count("█") :], Ansi.DIM, Ansi.WHITE
    )
    label_plain = label.ljust(20)
    label_text = paint(label_plain, Ansi.BOLD, Ansi.CYAN)
    value_text = paint(f"{value:>3}{suffix}", Ansi.BOLD, _resource_style(value))
    raw_content = f"  {label_plain} [{bar}]  {value:>3}{suffix}"
    styled_content = f"  {label_text} {paint('[', Ansi.DIM)}{colored_bar}{paint(']', Ansi.DIM)}  {value_text}"
    return f"│{styled_content}{' ' * max(0, 82 - len(raw_content))}│"


def connection_percent(state: GameState) -> int:
    if not state.flags["lazaro_contact"]:
        return 0
    return max(10, min(100, 45 + state.lazaro_trust * 8))


def render_hud(state: GameState) -> str:
    reentry = round((state.time_remaining / state.initial_time) * 100)
    connection = connection_percent(state)
    title = "  L Á Z A R O  //  Ó R B I T A   Z E R O"
    location_prefix = "  MIRROR-9  /  LOCALIZAÇÃO  "
    location_name = AREA_NAMES[state.location]
    location_plain = location_prefix + location_name
    location_styled = paint(location_prefix, Ansi.DIM, Ansi.BLUE) + paint(location_name, Ansi.BOLD, Ansi.WHITE)
    lines = [
        paint("╭" + "─" * 82 + "╮", Ansi.CYAN),
        "│" + paint(title, Ansi.BOLD, Ansi.CYAN) + " " * (82 - len(title)) + "│",
        "│" + location_styled + " " * (82 - len(location_plain)) + "│",
        paint("├" + "─" * 82 + "┤", Ansi.CYAN),
        _meter("OXYGEN", state.oxygen),
        _meter("POWER", state.power),
        _meter("HULL", state.hull),
        _meter("RE-ENTRY", reentry, f"%  {format_time(state.time_remaining)}"),
        _meter("LAZARO CONNECTION", connection),
        paint("╰" + "─" * 82 + "╯", Ansi.CYAN),
    ]
    return "\n".join(lines)


def render_message(message: str) -> str:
    """Apply restrained colour cues while leaving narrative text easy to read."""
    rendered: list[str] = []
    for line in message.splitlines():
        stripped = line.strip()
        if stripped.startswith("[SIMULAÇÃO"):
            rendered.append(paint(line, Ansi.DIM, Ansi.BLUE))
        elif stripped.startswith("ALERTA:"):
            rendered.append(paint(line, Ansi.BOLD, Ansi.YELLOW))
        elif stripped.startswith("FALHA") or stripped.startswith("SISTEMAS") or stripped.startswith("RUPTURA"):
            rendered.append(paint(line, Ansi.BOLD, Ansi.RED))
        elif stripped.startswith("[LOG"):
            rendered.append(paint(line, Ansi.BOLD, Ansi.MAGENTA))
        elif stripped.startswith("FINAL"):
            rendered.append(paint(line, Ansi.BOLD, Ansi.MAGENTA))
        elif stripped.startswith("Rota liberada:"):
            rendered.append(paint(line, Ansi.GREEN))
        else:
            rendered.append(line)
    return "\n".join(rendered)


def advance_systems(state: GameState, seconds: int) -> list[str]:
    """Advance the simulated station clock and apply deterioration."""
    if state.ended or seconds <= 0:
        return []

    state.turn += 1
    state.time_remaining = max(0, state.time_remaining - seconds)

    oxygen_rate = 0.032 if state.flags["oxygen_sealed"] else 0.072
    power_rate = 0.018 if state.flags["power_restored"] else 0.046
    hull_rate = 0.006 if state.flags["hull_patched"] else 0.020

    oxygen_loss = max(1, ceil(seconds * oxygen_rate))
    power_loss = max(1, ceil(seconds * power_rate))
    hull_loss = max(0, ceil(seconds * hull_rate))

    state.oxygen = max(0, state.oxygen - oxygen_loss)
    state.power = max(0, state.power - power_loss)
    state.hull = max(0, state.hull - hull_loss)

    hp_loss = 0
    if state.oxygen <= 25:
        hp_loss += max(1, ceil((26 - state.oxygen) / 8))
    if state.hull <= 20:
        hp_loss += 1
    state.hp = max(0, state.hp - hp_loss)

    notices = [
        f"[SIMULAÇÃO +{seconds}s | O₂ -{oxygen_loss} | energia -{power_loss} | casco -{hull_loss} | HP -{hp_loss}]"
    ]
    if state.oxygen <= 25:
        notices.append("ALERTA: reserva de oxigênio crítica.")
    if state.power <= 20:
        notices.append("ALERTA: a rede elétrica está à beira do apagão.")
    if state.hull <= 20:
        notices.append("ALERTA: integridade estrutural crítica.")

    if state.time_remaining <= 0:
        state.ended = True
        state.ending = "Falha de reentrada"
        notices.append("FALHA DE REENTRADA: a janela orbital se fechou antes da decisão final.")
    elif state.oxygen <= 0:
        state.ended = True
        state.ending = "Asfixia"
        notices.append("SISTEMAS VITAIS ENCERRADOS: o ar da MIRROR-9 acabou.")
    elif state.power <= 0:
        state.ended = True
        state.ending = "Apagão"
        notices.append("APAGÃO TOTAL: os corredores selam e a estação perde orientação.")
    elif state.hull <= 0:
        state.ended = True
        state.ending = "Ruptura do casco"
        notices.append("RUPTURA CATASTRÓFICA: a MIRROR-9 se abre para o vazio.")
    elif state.hp <= 0:
        state.ended = True
        state.ending = "Falência dos sistemas vitais"
        notices.append("SISTEMAS VITAIS ENCERRADOS: Elias não resistiu aos danos da estação.")

    return notices
