# 📱 Tuto — Obtenir l'application compagnon en APK (la voie fiable)

**But** : transformer le petit programme du module en **vraie application
Android installable** (« ReloadAtlas Camera »), avec un accès garanti à la
caméra — fini les blocages de Pydroid.

**Comment** : le site gratuit **github.com** compile l'application pour
vous, automatiquement, sur leurs ordinateurs. **Vous n'installez rien sur
votre PC.** Il vous faut : votre PC, votre téléphone, un navigateur
internet, et environ 40 minutes (dont ~25 d'attente sans rien faire).

**Le plan** — 5 parties, dans l'ordre :

| Partie | Où | Durée | Objectif |
|---|---|---|---|
| 1 | PC | 5 min | créer un compte GitHub gratuit |
| 2 | PC | 5 min | déposer les 4 fichiers du programme sur GitHub |
| 3 | PC | 1 clic + 25 min d'attente | lancer la compilation automatique |
| 4 | PC puis TÉLÉPHONE | 10 min | télécharger l'APK et l'installer |
| 5 | TÉLÉPHONE puis PC | 5 min | filmer et voir la caméra sur le PC |

---

## PARTIE 1 — PC — Créer votre compte GitHub *(5 min, à faire une seule fois)*

*Sauf si vous en avez déjà un : passez à la partie 2.*

1. Sur le **PC**, ouvrez votre navigateur (Chrome, Edge…) et allez sur
   **github.com**
2. Cliquez sur **« Sign up »** (en haut à droite).
3. Saisissez **votre adresse e-mail** → *Continue*.
4. Inventez un **mot de passe** (notez-le !) → *Continue*.
5. Choisissez un **pseudo** (ex. `nico-reload`) → *Continue*.
6. Recopiez le **code reçu par e-mail** (ouvrez votre messagerie dans un
   autre onglet, revenez, collez le code).

✅ **Contrôle** : vous êtes connecté — l'icône en haut à droite montre une
silhouette avec votre pseudo.

---

## PARTIE 2 — PC — Déposer les fichiers du programme sur GitHub *(5 min)*

### 2.1 — Créer le « dépôt » (l'espace de stockage)

1. Cliquez sur le **＋** en haut à droite → **« New repository »**.
2. **Repository name** : tapez `reloadatlas-camera` (tout en minuscules,
   avec le tiret).
3. Ne touchez à rien d'autre (il doit rester sur **Public** — c'est
   nécessaire pour la compilation gratuite).
4. Cliquez sur le gros bouton vert **« Create repository »**.

✅ **Contrôle** : une page s'affiche avec le nom `reloadatlas-camera` et
des propositions « …or create a new file ».

### 2.2 — Afficher les fichiers cachés de Windows (piège n° 1 !)

Le dossier à envoyer contient un dossier **caché** nommé `.github` — c'est
lui qui contient la consigne de compilation. Sans lui, rien ne se compile.

1. Ouvrez l'**Explorateur de fichiers** Windows (touche Windows + E).
2. En haut, onglet **« Affichage »** (ou « View »).
3. Cochez **« Éléments masqués »** (Hidden items).

### 2.3 — Ouvrir le dossier du projet

Dans la barre d'adresse de l'explorateur, **copiez-collez** ce chemin puis
*Entrée* :
```
D:\PROJET APPLICATION RECHARGEMENT MUNITIONS\BANQUE DE DONNEES\STRELOK PRO\MODULE CONNEXION SMARTPHONE\RELOADATLAS\smartphone\apk_project
```

✅ **Contrôle** : vous devez voir **4 éléments** :
`.github` (dossier), `buildozer.spec`, `camera_server_phone.py`, `main.py`.
*(Si `.github` n'apparaît pas → retour à 2.2.)*

### 2.4 — Envoyer les fichiers

1. Dans le navigateur (page du dépôt créée en 2.1), cliquez sur le lien
   **« uploading an existing file »** (au milieu de la page).
2. Dans l'explorateur, sélectionnez les **4 éléments** (*Ctrl + A* dans le
   dossier).
3. **Glissez-les** dans la grande zone blanche du navigateur
   « drag files here ».
   *(Équivalent : bouton « choose your files » et sélection des 4 éléments.)*
4. Attendez que les 4 lignes apparaissent sans barre de progression.
5. Descendez en bas de la page → bouton vert **« Commit changes »**.

✅ **Contrôle** : la page du dépôt liste bien **4 éléments**, dont le
dossier `.github`.

---

## PARTIE 3 — PC — Lancer la compilation automatique *(1 clic, puis ☕ 15-30 min)*

### 3.0 — Se placer sur la page du DÉPÔT (piège n° 3 !)

L'onglet « Actions » **n'existe que sur la page du dépôt**
`reloadatlas-camera` — pas sur la page d'accueil de GitHub. Si vous ne
voyez aucun onglet « Actions », vous êtes probablement sur l'accueil :

1. Cliquez sur votre **avatar** (photo/silhouette, en haut à droite).
2. Cliquez sur **« Your repositories »** (ou « Vos dépôts »).
3. Cliquez sur la ligne **`reloadatlas-camera`**.
4. ✅ **Contrôle** : sous le nom du dépôt, une rangée d'onglets s'affiche :
   `<> Code · Issues · Pull requests · Actions …`

### 3.1 — Lancer la compilation

1. Sur la page du dépôt, cliquez sur l'onglet **« Actions »**.
2. **La première fois**, GitHub affiche un bandeau avec un bouton vert
   **« I understand my workflows, go ahead and enable them »** → cliquez.
3. À gauche, cliquez sur **« Build APK ReloadAtlas Camera »**.
4. ⚠️ **Piège n° 4 (déjà rencontré) — aucune ligne de compilation ne
   démarre** ? C'est normal quand le workflow a été déposé par l'upload
   web : GitHub ne le lance pas tout seul la première fois, par sécurité.
   La solution :
   1. Cliquez à gauche sur **« Build APK ReloadAtlas Camera »** (s'il
      n'y a rien dans la liste principale, GitHub propose
      « Configure » / ouvre le fichier `build-apk.yml` en édition).
   2. Le fichier s'affiche alors avec un bouton vert **« Commit
      changes »** (en haut à droite) → cliquez dessus **SANS RIEN
      MODIFIER au texte** (et encore « Commit changes » si une fenêtre
      s'ouvre). C'est ce re-enregistrement qui déclenche la compilation.
   3. Revenez à l'onglet **Actions** : une ligne avec un **point orange**
      doit maintenant apparaître.

   **🔑 Solution de secours infaillible (adresse directe)** — si les
   boutons décrits n'apparaissent pas sur votre écran (écrans GitHub
   variables selon les comptes) : sur la page du dépôt, regardez la
   **barre d'adresse** du navigateur (`github.com/VOTRE-PSEUDO/
   reloadatlas-camera`), placez-vous à la fin et ajoutez :
   `/actions/workflows/build-apk.yml` puis *Entrée*. La page obtenue
   possède un unique **bouton vert « Run workflow »** à droite :
   cliquez → cliquez encore **« Run workflow »** dans la petite fenêtre →
   la compilation démarre (point orange dans l'onglet Actions).

5. Le point orange tourne : la compilation est en cours. Vous pouvez faire
   autre chose (ne supprimez pas le dépôt) — comptez **15 à 30 minutes**.

✅ **Contrôle** : la ligne affiche une **coche verte ✓** — l'APK est prêt,
passez à la partie 4.

❌ **Si croix rouge ✗** : cliquez sur la ligne → sur le travail en rouge →
dépliez l'étape « Compiler l'APK » : **copiez les dernières lignes en
rouge et envoyez-les-moi** (je corrigerai le fichier et on refera la
partie 2). Pour réessayer après correction : onglet Actions → la ligne →
bouton **« Re-run jobs »** → « Re-run all jobs ».

---

## PARTIE 4 — Télécharger et installer l'APK *(10 min)*

### 4.1 — PC — Télécharger le fichier compilé

1. Onglet **Actions** → cliquez sur la ligne **verte ✓** de tout à l'heure.
2. **Descendez tout en bas de cette page** : une zone **« Artifacts »**
   montre une ligne **« ReloadAtlasCamera-APK »** → cliquez dessus.
3. Un fichier **.zip** se télécharge (dans Téléchargements).

### 4.2 — PC — Extraire l'APK du zip

1. Ouvrez le dossier **Téléchargements** du PC.
2. **Double-cliquez** sur le zip `ReloadAtlasCamera-APK...`.
3. Vous voyez un fichier du genre
   `reloadatlascamera-1.0-arm64-v8a...debug.apk` → **glissez-le sur le
   Bureau** (faites-le simplement : c'est l'application Android).

### 4.3 — PC → TÉLÉPHONE — Envoyer l'APK au téléphone

⚠️ **Piège n° 2** : **Gmail refuse les pièces jointes .apk**. Utilisez
plutôt :

- **Google Drive (conseillé)** :
  1. Sur le PC, allez sur **drive.google.com** (connectez-vous).
  2. Bouton **＋ Nouveau** → **« Importer un fichier »** → choisissez
     l'APK du Bureau.
  3. Attendez la fin de l'import (l'APK devient visible dans « Mes
     fichiers »).
  4. Sur le **téléphone**, ouvrez l'appli **Drive** → touchez l'APK →
     les **trois points ⋮** → **« Télécharger »**. Une notification
     confirme le téléchargement.
- **Ou câble USB** : téléphone relié → « Transfert de fichiers » →
  glissez l'APK dans *Téléchargements* du téléphone.

### 4.4 — TÉLÉPHONE — Installer l'application

1. Ouvrez l'appli **Fichiers** du téléphone → dossier **Téléchargements**.
2. Touchez le fichier **.apk**.
3. Android affiche « **Installation bloquée** » ou « Pour votre
   sécurité… » → touchez **« Paramètres »** dans cette même fenêtre.
4. Activez **« Autoriser depuis cette source »** (il concerne Drive ou
   votre stockage).
5. Revenez en arrière → touchez de nouveau l'APK → **« Installer »**.
6. Si Android prévient « application non vérifiée / pas optimisée » →
   **« Installer quand même »**.

✅ **Contrôle** : une nouvelle appli **« ReloadAtlas Camera »** apparaît
dans le tiroir d'applications du téléphone.

---

## PARTIE 5 — Utiliser : la caméra du téléphone sur le PC *(5 min)*

### 5.1 — TÉLÉPHONE — Lancer

1. Ouvrez **ReloadAtlas Camera**.
2. Android demande les autorisations (**caméra**, Bluetooth, position) →
   choisissez **« Pendant l'utilisation de l'application »** ou
   **« Autoriser »** — **ne refusez pas la caméra**, c'est elle que l'on
   veut !
3. Appuyez sur **« Démarrer en WiFi »** (bouton conseillé).

✅ **Contrôle** : l'appli affiche **« LE TÉLÉPHONE FILME ✅ »** avec
l'adresse du téléphone.

### 5.2 — Mettre les deux sur le même réseau

1. TÉLÉPHONE : **Paramètres** → **Réseau et Internet** → **Point d'accès
   et partage** → **Point d'accès mobile** → ON (notez nom + mot de passe).
2. PC : icône **WiFi** (en bas à droite) → réseau du téléphone →
   **Se connecter** → mot de passe.

### 5.3 — PC — Voir la caméra

1. Double-cliquez sur **`TestConnexionSmartphone.exe`**.
2. **Source** : « WiFi — compagnon maison ».
3. Bouton **« Détecter »** → l'adresse se remplit toute seule.
4. **« Se connecter »** → **« Autoriser la connexion »**.

✅ **CONTRÔLE FINAL : bandeau orange + l'image RÉELLE de la caméra du
téléphone sur l'écran du PC.** 🎉 *(Ce n'est plus les barres colorées de
test : vous filmez votre pièce !)*

---

## 🛠 Dépannage de la voie APK

| Problème | Solution |
|---|---|
| Compilation en croix rouge (partie 3) | Cliquez la ligne rouge → l'étape « Compiler l'APK » → copiez-moi les dernières lignes rouges. Puis « Re-run jobs » après correction. |
| Pas de zone « Artifacts » | Êtes-vous bien sur une ligne **verte ✓** de l'onglet Actions ? La zone est tout en bas de la page du run. |
| « App not installed » à l'installation | Téléphone trop ancien (il faut Android 7 ou plus) — vérifiez dans Paramètres → À propos. Sinon, retéléchargez l'APK (fichier abîmé). |
| L'appli affiche « ACCÈS CAMÉRA INDISPONIBLE » | Paramètres → Applications → ReloadAtlas Camera → Autorisations → activez **Caméra** → rouvrez l'appli. |
| Image noire | Une seule caméra sur ce téléphone ou mauvais objectif : relancez et si ça persiste, dites-le-moi (j'ajouterai un choix de caméra dans l'appli). |
| « Détecter » ne trouve rien | L'appli affiche-t-elle « LE TÉLÉPHONE FILME ✅ » ? Le PC est-il connecté au point d'accès du téléphone (5.2) ? Réessayez « Détecter ». |

---

## Pour la suite

- L'APK et les fichiers déposés sur GitHub restent disponibles : vous
  pourrez retélécharger l'APK à volonté (onglet Actions → un run vert →
  Artifacts).
- C'est cette même application qui sera distribuée aux utilisateurs de
  ReloadAtlas le jour voulu.
- Bluetooth (plan B sans réseau) : appuyez sur « Démarrer en Bluetooth »
  dans l'appli, téléphone appairé dans Windows, puis sur le PC source
  « Bluetooth » + adresse MAC (voir le README principal du module).
