# Gestor d'Administració del Sistema

## Paràmetres de la Línia d'Ordres

Aquest programa admet diversos paràmetres per a una execució més flexible:

```sh
-h          # Mostra l'ajuda amb els paràmetres disponibles
-t XX       # Elimina fitxers més antics que XX dies (XX > 0)
-b XXXXXX   # Modifica el color de fons de la interfície (color hexadecimal, per exemple -b FF0000 per vermell)
-x          # Només es pot utilitzar la línia d'ordres (la interfície gràfica es deshabilita)
hackeao     # Canvia la interfície per mostrar text verd amb fons negre, estil "hacker"
```
## Registre d'Errors

El programa guarda un registre d'activitats i errors en el fitxer `log.txt`.

## Exemple d'Execució

Executar el programa amb interfície gràfica:
```sh
python3 sysadmin_pro.py
```

Eliminar fitxers antics (més de 30 dies):
```sh
python3 sysadmin_pro.py -t 30
```

Canviar el color de fons a blau:
```sh
python3 sysadmin_pro.py -b 0000FF
```

Activar mode "hacker":
```sh
python script.py hackeao
