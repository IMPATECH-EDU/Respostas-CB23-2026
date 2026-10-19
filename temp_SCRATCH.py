# from datetime import datetime
# from elevatoria.dados import  LINHA
# import re
from fornecido.simulador import gerar_log
from elevatoria.dados import ler_log
import unittest
from fornecido.simulador import gerar_log
# match = LINHA.fullmatch('2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5')
# d = match.groupdict()
# print(re.findall(r'(\w+)=(\S+)',d['resto']))
print(gerar_log(3501))