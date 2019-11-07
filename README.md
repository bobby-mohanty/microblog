A micro blog


to generate language packs run

  (venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .

to generate the '.pot' (portable object template) file
and then run

  (venv) $ pybabel init -i messages.pot -d app/translations -l es

to generate the language catalog
