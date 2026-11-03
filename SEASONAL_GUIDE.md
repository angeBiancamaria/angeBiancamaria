# Thèmes v6 — lisibilité et texte saisonnier

## Changements
- Décorations des cartes cantonnées à une bordure fine (haut/bas), sans motifs sur les objectifs ou les descriptions.
- Suppression des gros objets dessinés au-dessus du contenu des cartes.
- Ajout d'un encart Markdown saisonnier entre l'en-tête animé et la carte de Corse.
- Huit messages différents, dont Anniversaire le 9 janvier, Halloween et Noël.
- Le script ne touche pas aux citations quotidiennes, aux objectifs textuels ni aux autres sections.
- Les liens vers des SVG distincts pour chaque thème restent inchangés.

## Installation depuis la v5
Remplacer `scripts/seasonal.py` par celui-ci et conserver `.github/workflows/seasonal.yml`.
Exécuter Actions > Seasonal profile theme > Run workflow avec le thème désiré.
Le script met à jour automatiquement le README et les SVG.

## Attention
Les images et le texte du profil sont personnalisables, mais GitHub ne permet pas d'appliquer
du CSS arbitraire au README. Les changements textuels restent donc du Markdown standard.
Les animations SVG peuvent varier selon le moteur de rendu.
