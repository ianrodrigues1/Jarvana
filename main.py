"""Executable entry point for LÁZARO // ÓRBITA ZERO."""

from __future__ import annotations

import os
import sys

from game import Game
from systems import Ansi, enable_terminal_colors, paint, render_message


def clear_terminal() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    enable_terminal_colors()

    game = Game()
    message = game.opening_text()
    while not game.state.ended:
        clear_terminal()
        print(game.render_hud())
        print()
        print(render_message(message))
        print(paint("┄" * 84, Ansi.DIM, Ansi.BLUE))
        print(paint("  Escreva uma ação em linguagem natural.  •  'ajuda' mostra os comandos.", Ansi.DIM, Ansi.WHITE))
        print()
        try:
            command = input(paint("  ELIAS", Ansi.BOLD, Ansi.CYAN) + paint("@MIRROR-9", Ansi.MAGENTA) + paint("  › ", Ansi.BOLD, Ansi.WHITE))
        except (EOFError, KeyboardInterrupt):
            print("\nConexão encerrada.")
            return
        message = game.handle_command(command)

    clear_terminal()
    print(game.render_hud())
    print()
    print(render_message(message))
    if game.state.ending not in {"Encerrado pelo jogador", None}:
        print("\nFim da transmissão.")


if __name__ == "__main__":
    main()
