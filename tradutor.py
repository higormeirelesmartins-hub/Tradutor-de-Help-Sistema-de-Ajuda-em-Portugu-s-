import argostranslate.translate

import io
import contextlib
import time
import logging
logging.getLogger('stanza').setLevel(logging.ERROR)
logging.disable(logging.WARNING)


c=  ('\033[m',
   '\033[0;30;41m',#vermelho
   '\033[0;30;42m',#verde
   '\033[0;30;44m',#azul
   '\033[7m',#inverter
   '\033[m'
   );

#Trudaçao do programa
_cache_traducao = {}

# Monta o tradutor en->pt UMA UNICA VEZ, ao iniciar o programa
_idiomas_instalados =argostranslate.translate.get_installed_languages()
_idioma_origem = next((l for l in _idiomas_instalados if l.code == "en"), None)
_idioma_destino = next((l for l in _idiomas_instalados if l.code == "pt"), None)

if _idioma_origem is None or _idioma_destino is None:
    print("Pacote de idioma en->pt nao encontrado. Rode 'instalar_idioma.py' primeiro.")
    _tradutor = None
else:
    _tradutor = _idioma_origem.get_translation(_idioma_destino)



def traduzir(texto):
   if not texto.strip():
    return texto
   if texto in _cache_traducao:
    return _cache_traducao
   if _tradutor is None:
    return texto
   try:
    resultado =_tradutor.translate(texto)
   except Exception as e:
       print(f'Erro ao traduzir {e}')
       resultado = texto
   _cache_traducao[texto] = resultado
   return resultado



# fim da parte de traduçao
#Rodamento do progrma

def titulo(msg, cor=0):
    tam = len(msg) + 4
    print(c[cor],end='')
    print('-' * tam)
    print(f'{msg} ')
    print('-' *tam)
    print(c[0],end='')



def aju (com):
   titulo(f'Acessando o comando {com}',2)
   print(c[4],end='')
   bufer=io.StringIO()
   with contextlib.redirect_stdout(bufer):
       help(com)
   texto_help=bufer.getvalue()
   traduzido=traduzir(texto_help)
   print(traduzido)
   print(c[0],end='')
   print('-'*40)




ajuda=' '
while True:
        titulo('Sistema de ajuda : ',1)
        ajuda=str(input('Funçao ou biblioteca :',))
        if ajuda.upper()=='FIM':
            break
        else:
         aju(ajuda)
         print('-'*40)
