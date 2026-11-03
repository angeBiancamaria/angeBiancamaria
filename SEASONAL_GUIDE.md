# Thèmes saisonniers v4 — fichiers distincts par thème

Cette version règle le problème d’une image Noël affichée à la place d’Anniversaire ou Halloween en utilisant **une URL différente pour chaque thème**.

## Installation

1. Copier `scripts/seasonal.py`, `.github/workflows/seasonal.yml` et les fichiers `img/seasonal/*.svg` du ZIP dans votre dépôt.
2. **Important :** conserver votre README actuel (ne pas le remplacer par celui du ZIP si vous l’avez personnalisé). Le script adaptera ses références existantes (`corsica_current.svg` et `goals_current.svg`) au prochain lancement.
3. Commit/push sur `main`.
4. Actions > Seasonal profile theme > Run workflow > `preview_theme: birthday` ou `halloween`.
5. Vérifier le commit automatique du README : ses liens doivent devenir `corsica_card_birthday.svg` et `my_goals_birthday.svg` pour Anniversaire.

Le workflow ajoute au commit les 16 SVG de thèmes et le README. L’ancienne image `*_current.svg` n’est plus utilisée. Les effets SVG animés dépendent du rendu de GitHub.

Les fichiers de base `img/corsica_card.svg` et `img/my_goals.svg` restent inchangés. Le script conserve la bannière unique, le Snake et les citations.
