Auteurs: 

Nassera Nabgaoui
Janna Gudumac

Fonctionnalités du script

1. Scan récursif d’un dossier: la fonction scan, qui explore tous les sous-dossiers du répertoire donné en argument.
Elle ajoute dans la liste globale photos tous les fichiers dont l’extension est : jpg, jpeg, png

2. Extraction de la date

Pour chaque image le script tente d’abord de lire les métadonnées EXIF via DateTimeOriginal. 
Si cette information existe il récupère l’année et le mois, il note "exif" comme source.
Sinon, il prend la date de modification du fichier (os.path.getmtime) source notée "file".

3. Classement automatique dans des dossiers

Les photos sont rangées dans un dossier classified_photos, après classifiés par année et mois.
Les dossiers sont créés automatiquement si nécessaires.

4. Déplacement des fichiers

Le script utilise os.rename(photo, dest_path) pour déplacer les images dans les bons dossiers.

5. Génération d’un CSV

Le fichier listePhotos.csv récapitule :
- le nom du fichier,
- le dossier de destination (YYYY/MM),
- la source de la date (EXIF ou file system).

Format CSV séparé par ;

6. Exécution en ligne de commande

Le script lit le dossier à analyser depuis sys.argv[1].

Bugs et limitations:

Le bug venait des séparateurs de chemins différents entre Windows et Linux. 
On a corrigé ça en utilisant os.path.join(), qui crée automatiquement des chemins compatibles sur tous les systèmes.

Parmi les limites du script, il n’y a pas de gestion d’erreurs (photos corrompues, permissions, etc.) et aucune prise en 
charge des fichiers portant le même nom, ce qui peut provoquer des conflits lors du déplacement.




