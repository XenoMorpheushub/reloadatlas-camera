# Installer le compagnon ReloadAtlas sur votre smartphone

Le compagnon est la petite application qui diffuse la caméra de votre
téléphone vers ReloadAtlas, **sans dépendre d'aucune application tierce**.
Trois voies possibles, de la plus simple à la plus robuste.

---

## Voie 1 — Pydroid 3 (recommandée pour commencer, ~15 minutes, zéro compilation)

### Ce qu'il vous faut
- un smartphone Android ;
- le fichier `camera_server_phone.py` (dans ce dossier) copié sur le
  téléphone — par Google Drive, un e-mail que vous vous envoyez, ou un câble USB.

### Étapes

1. **Installez Pydroid 3** depuis le Play Store
   (icône verte, nom exact : « Pydroid 3 - IDE for Python 3 »).
2. Ouvrez Pydroid 3. Un tutoriel peut s'afficher : passez-le (bouton de
   fermeture ou retour).
3. **Copiez le fichier** `camera_server_phone.py` dans le téléphone, par
   exemple dans le dossier *Téléchargements*.
4. Dans Pydroid 3, appuyez sur l'icône **dossier** (en haut) → naviguez vers
   *Téléchargements* → ouvrez `camera_server_phone.py`.
5. Appuyez sur le bouton **▶ (lecture)**, en bas à droite.
6. La première fois, Android demande des autorisations (**caméra**,
   **Bluetooth**, éventuellement **position**) : acceptez-les. Pydroid
   peut afficher une publicité : fermez-la avec sa croix.
7. Un **petit menu** s'affiche : tapez **1** (ou *Entrée*) pour le WiFi —
   c'est le mode conseillé — puis **1** pour la caméra arrière
   (ou **2** pour l'avant). L'encadré suivant confirme le lancement :
   ```
   LE TÉLÉPHONE FILME ✅  — le serveur est actif.
   Maintenant, sur le PC : « Détecter » puis « Se connecter ».
   ```
   À ce stade, **plus rien à faire sur le téléphone** : il filme et attend
   le PC. L'installation est terminée. Passez à « Relier le PC » ci-dessous.

⚠️ Si vous voyez plutôt « ACCÈS CAMÉRA INDISPONIBLE » : le script a été
lancé depuis le mode *Terminal* de Pydroid (sans accès Java). Relancez avec
le **gros bouton ▶** de Pydroid. Le compagnon bascule alors de lui-même en
images de test pour ne pas bloquer la suite.

### Conseils
- Le menu suffit pour tout : **1 = WiFi, 2 = Bluetooth**, puis le choix de
  la caméra (arrière ou avant). Les réponses par défaut (validées par la
  touche *Entrée*) conviennent dans la grande majorité des cas.
- Pour le Bluetooth, appairez d'abord le téléphone dans les **paramètres
  Bluetooth de Windows**, puis choisissez **2** au menu du compagnon.

---

## Voie 2 — APK compilé automatiquement (la plus robuste, sans rien installer sur votre PC)

Le dossier `apk_project` contient un projet qui se compile **tout seul sur
GitHub** — vous n'installez aucun outil de développement. L'application
obtenue (« ReloadAtlas Camera », deux boutons : WiFi / Bluetooth) demande
elle-même les autorisations Android, dont la **caméra** — c'est la voie
recommandée quand Pydroid affiche « ACCÈS CAMÉRA INDISPONIBLE ».

> 📘 **Tuto pas-à-pas complet (compte GitHub, envoi des fichiers,
> compilation, installation de l'APK) :**
> `..\..\TEST\TUTO_APK_GitHub.md` — 5 parties, aucune connaissance
> technique requise.

Résumé : dépôt GitHub créé avec le **contenu complet du dossier
`apk_project`** (y compris le dossier caché `.github` !) → onglet
**Actions** → compilation automatique → APK dans **Artifacts** →
installation sur le téléphone (autoriser « depuis cette source »).

---

## Voie 3 — Sans compagnon : webcam virtuelle (Iriun / DroidCam / Camo)

Aucun fichier à copier : installez l'app mobile (Play Store) + le logiciel PC
correspondant, connectez le PC au téléphone (même WiFi, ou câble USB), et
choisissez simplement **« Webcam virtuelle »** dans la page ReloadAtlas.
C'est la voie la plus simple, au prix d'une dépendance à un éditeur tiers.

---

## Relier le PC (toutes voies confondues)

**WiFi — mode conseillé : point d'accès mobile**
1. Sur le téléphone : *Paramètres → Réseau → Point d'accès et partage* →
   activez **Point d'accès mobile** (les données mobiles peuvent rester
   éteintes : le flux est 100 % local).
2. Sur le PC : connectez le WiFi au réseau du téléphone (mot de passe
   affiché sous le nom du point d'accès).
3. Dans ReloadAtlas, page **Connexion smartphone** : source *WiFi* →
   bouton **Détecter** → l'adresse se remplit toute seule → **Se connecter**.
4. Le dialogue d'autorisation s'affiche : **Autoriser** pour voir le flux,
   ou **Refuser** pour ne rien connecter.
5. Le bandeau orange « Connexion smartphone active » confirme le flux.
   **Terminer la connexion** coupe tout à tout moment.

**Bluetooth**
1. *Paramètres Windows → Bluetooth* : appairez le téléphone (code PIN
   affiché des deux côtés).
2. Restez appuyé sur le téléphone appairé → *Propriétés* : l'**adresse MAC**
   (du type `AA:BB:CC:DD:EE:FF`) est indiquée.
3. Lancez le compagnon en mode `bt`, puis côté PC : source *Bluetooth* →
   collez l'adresse MAC → **Se connecter**.

---

## Dépannage

| Symptôme | Solution |
|---|---|
| **« ACCÈS CAMÉRA INDISPONIBLE » / « No JNIEnv available »** | Script lancé depuis le mode *Terminal* de Pydroid. Relancez avec le **gros bouton ▶**. Le compagnon diffuse en attendant des images de test (liaison testable, vraie caméra non). |
| « Détecter » ne trouve rien | Compagnon lancé sur le téléphone (encadré « LE TÉLÉPHONE FILME ✅ ») ? PC connecté au **même** réseau (ou au point d'accès du téléphone) ? Réessayez (la sonde dure ~3 s). |
| Connexion WiFi refusée | Désactivez brièvement le pare-feu pour tester ; vérifiez que le port 8899 n'est pas occupé ; entrez l'adresse à la main (elle s'affiche sur le téléphone). |
| Bluetooth : « téléphone apparié et compagnon lancé ? » | Refaites l'appairage Windows, vérifiez que le compagnon tourne en mode `bt`, rapprochez les appareils. |
| Image noire | Essayez `--camera-id 1` (ou 0). |
| Flux figé puis coupé | Normal : le watchdog coupe après ~5 s sans image (téléphone en veille ? désactivez l'économie d'énergie pour le compagnon). |
| Pydroid plante au démarrage | Fermez les autres apps, relancez ; à défaut, passez par l'APK (voie 2). |

---

## Récapitulatif des options du compagnon

Sur le téléphone (Pydroid 3), le **simple bouton ▶ suffit** : le menu
interactif propose WiFi / Bluetooth et la caméra à utiliser.

Sur un PC (tests avancés), des options en ligne de commande existent :

```
python camera_server_phone.py tcp              # serveur WiFi (défaut)
python camera_server_phone.py bt               # serveur Bluetooth
python camera_server_phone.py selftest         # test sur PC (frames de test)
python camera_server_phone.py tcp --port 8899 --fps 12 --size 480x360 --quality 70
python camera_server_phone.py --list-cameras   # nombre de caméras du téléphone
```

En Bluetooth, réduisez la taille (`--size 320x240`) et la cadence
(`--fps 5`) pour un flux fluide — c'est la bande passante qui commande.
