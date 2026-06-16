# ASCII Mandelbrot

Ceci est un projet générant une fractale de Mandelbrot en ASCII.

## Comment lancer le projet sur votre ordinateur ?

Puisque le code est sur GitHub, vous devez d'abord le télécharger sur votre machine locale avant de l'exécuter.

### 1. Cloner le dépôt
Ouvrez votre terminal et clonez le dépôt en utilisant `git` :
```bash
git clone https://github.com/votre-nom-utilisateur/nom-du-repo.git
```
*(Remarque : remplacez l'URL par l'URL réelle de ce dépôt GitHub)*

### 2. Naviguer dans le dossier
Allez dans le dossier du projet que vous venez de télécharger :
```bash
cd nom-du-repo
```

### 3. Lancer le script
Pour voir le rendu du script, il vous suffit de l'exécuter avec Python :
```bash
python3 mandelbrot.py
```
*(Ou `python mandelbrot.py` si vous êtes sous Windows)*

Vous devriez voir la fractale s'afficher directement dans votre terminal !

---

# Todo Manager (Nouveau !)

J'ai également ajouté un gestionnaire de tâches (Todo list) en ligne de commande, plus poussé et très utile pour votre quotidien !
Il utilise `sqlite3` pour sauvegarder vos tâches de façon permanente.

## Comment l'utiliser ?

Le script s'appelle `todo.py`. Voici les commandes disponibles :

### Ajouter une tâche
```bash
python3 todo.py add "Acheter du pain"
```
Vous pouvez spécifier une priorité de 1 (Haute) à 3 (Basse) avec `-p` :
```bash
python3 todo.py add "Finir le projet" -p 1
```

### Lister les tâches
Pour voir vos tâches en cours (triées par priorité) :
```bash
python3 todo.py ls
```
Pour voir **toutes** vos tâches, y compris celles terminées :
```bash
python3 todo.py ls -a
```

### Marquer une tâche comme terminée
Utilisez l'ID de la tâche (visible quand vous faites `ls`) :
```bash
python3 todo.py done 1
```

### Supprimer une tâche
```bash
python3 todo.py rm 1
```

*Note : Les données sont sauvegardées dans un fichier caché dans votre dossier personnel (`~/.todo_list.db`), vous ne perdrez donc pas vos tâches même si vous fermez le terminal !*

---

# Interface Graphique (GUI)

Vous préférez les interfaces visuelles au terminal ? J'ai également créé une interface graphique pour le gestionnaire de tâches !
Elle utilise exactement la même base de données que la version en ligne de commande, vos tâches sont donc synchronisées entre les deux outils.

## Lancer l'interface graphique

Il vous suffit d'exécuter ce script Python :

```bash
python3 todo_gui.py
```

Une fenêtre va s'ouvrir. Vous pourrez y ajouter des tâches, définir leur priorité, cocher celles qui sont terminées, et les supprimer très facilement à la souris !
