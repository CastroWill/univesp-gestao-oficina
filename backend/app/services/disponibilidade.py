from datetime import time


HORARIOS_PADRAO = [
    time(8, 0),
    time(9, 0),
    time(10, 0),
    time(11, 0),
    time(13, 0),
    time(14, 0),
    time(15, 0),
    time(16, 0),
    time(17, 0),
]


def formatar_horario(horario):
    return horario.strftime("%H:%M")