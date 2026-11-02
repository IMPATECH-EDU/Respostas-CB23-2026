import re
import time
import tracemalloc


# Regex para capturar a linha do log (data/hora, nivel e mensagem)
LINHA = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+"
    r"(?P<level>[A-Z]+)\s+"
    r"(?P<message>.*)$"
)


def criar_conversores(esquema):
    """Cria conversores de tipo corrigindo o problema de late binding do lambda."""
    conversores = {}
    for chave, tipo in esquema.items():
        # Utiliza argumento padrão (tipo_fixo=tipo) para evitar late binding
        conversores[chave] = lambda val, tipo_fixo=tipo: tipo_fixo(val)
    return conversores


def ler_log(caminho_arquivo):
    """Lê o arquivo de log linha a linha e extrai os dados usando a regex LINHA."""
    registros = []
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha_str = linha.strip()
            if not linha_str:
                continue
            match = LINHA.match(linha_str)
            if match:
                registros.append(match.groupdict())
    return registros


def por_tag(registros, tag):
    """Filtra e retorna apenas os registros que correspondem à tag informada."""
    return [reg for reg in registros if reg.get("tag") == tag]


def medir_execucao(func, *args, **kwargs):
    """Mede o tempo de execução e o pico de memória utilizada por uma função."""
    tracemalloc.start()
    inicio_tempo = time.perf_counter()

    resultado = func(*args, **kwargs)

    fim_tempo = time.perf_counter()
    _, pico_memoria = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tempo_total = fim_tempo - inicio_tempo
    return resultado, tempo_total, pico_memoria