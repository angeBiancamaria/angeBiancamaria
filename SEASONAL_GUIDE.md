# GitHub Profile — Seasonal v7

## Installation depuis la v6
Copier **uniquement** `scripts/seasonal.py` dans le dépôt.
Garder le README actuel, les workflows, les logos et les images.
Dans GitHub Actions > Seasonal profile theme > Run workflow, choisir `birthday`, `halloween`, etc.

## Modifications
- Titres et courtes notes saisonnières dans Current Goal, Featured Project,
  Currently Learning, Languages/Frameworks/Tools et GitHub Stats.
- Titre saisonnier dans Profile et titres Frontend, Backend, Frameworks & Libraries, Tools.
- Textes permanents, tableaux de logos, citation quotidienne, liens et snake inchangés.
- Les SVG saisonniers dédiés de v6 sont conservés.
- La mise à jour est répétable : les notes précédentes sont remplacées, pas empilées.

## Compatibilité
Le script recherche les titres de la version v6 et ceux qu'il génère.
Si le README a été profondément modifié depuis, le script refuse de l'écraser :
adapter les titres attendus dans `SECTION_BASE` avant de relancer.
