# Thèmes saisonniers v5 — illustrations renforcées

Cette version conserve le système v4 des SVG séparés par thème, et ajoute des illustrations propres à chaque événement (gâteau d'anniversaire, citrouille, sapin, bonhomme de neige, fleurs, soleil, feuilles et œufs de Pâques). Les décorations sont placées près des bords pour conserver les illustrations d'origine.

## Installation depuis v4

Copiez `scripts/seasonal.py` et le dossier `img/seasonal/` dans votre dépôt. Le workflow `.github/workflows/seasonal.yml` de la v4 peut rester inchangé. Le README existant sera mis à jour au prochain lancement du workflow. Ne remplacez pas votre README par celui du ZIP si vous avez effectué d'autres modifications depuis la v4.

## Tester

Dans GitHub : Actions > Seasonal profile theme > Run workflow, choisissez un thème (`birthday`, `halloween`, `christmas`, `winter`, `spring`, `summer`, `autumn`, `easter`). Le thème automatique revient lors de la prochaine exécution planifiée.

## Compatibilité

Les illustrations principales sont statiques et restent visibles même si GitHub bloque certaines animations SVG. Les petites animations SVG peuvent varier selon le navigateur, le rendu GitHub et les réglages d'accessibilité. Le Snake est inchangé.
