# Activitat Git

El projecte és una primera aproximació amb les API RestFul

## Instal·lació

Per poder instal·lar el projecte s'haurà de tenir:
* La versió 3.13 de python
* Instal·lar [Pipenv](https://pipenv-es.readthedocs.io/es/latest/)

Instal·lar els paquets de python:
```bash
pipenv install --dev
```

Activar entorn virtual:
```bash
pipenv shell
```

Si dona error a l'utilitzar `pipenv``
```bash
python -m pipenv install --dev
python -m pipenv shell
```

Per executar el projecte:
```bash
cd app/
uvicorn main:app --reload
```
