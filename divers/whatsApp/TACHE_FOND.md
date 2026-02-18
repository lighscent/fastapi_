# Selenium en tâche de fond

## 🌙 1) Le principe général : un programme qui tourne sans interface visible

Quand on dit *« faire tourner en tâche de fond »*, on parle de plusieurs idées :

- ✔ Le script Python continue de tourner même si tu fermes la console  
- ✔ Le navigateur peut être invisible (mode *headless*)  
- ✔ Le script peut être lancé automatiquement (planification)  
- ✔ Le script ne dépend plus du focus clavier/souris  

C’est exactement ce que Selenium permet.

---

## 🧠 2) Comment Selenium peut tourner sans fenêtre visible (*mode headless*)

Selenium peut lancer Chrome en **mode headless**, c’est‑à‑dire :

- aucune fenêtre  
- aucun onglet visible  
- aucune interface  
- tout se passe “dans l’ombre”

Chrome exécute WhatsApp Web **sans jamais apparaître à l’écran**.  
C’est comme si tu avais un mini‑navigateur invisible qui travaille pour toi.

---

## 🧩 3) Comment faire tourner le script sans garder la console ouverte

Plusieurs méthodes existent :

### ✔ A. Lancer le script en arrière‑pla

Sous Windows :

```bash
python ton_script.pyw
```

Un fichier `.pyw` **ne crée pas de fenêtre console**.

---

### ✔ B. Lancer le script via un service Windows

Tu peux transformer ton script en **service Windows** :

- il démarre automatiquement  
- il tourne en arrière‑plan  
- il ne dépend d’aucune console  

---

### ✔ C. Utiliser le Planificateur de tâches Windows

Tu peux programmer :

- “tous les jours à 14h, exécute ce script”  
- “toutes les 10 minutes”  
- “au démarrage du PC”  

Le script tourne même si tu n’es pas connecté.

---

### ✔ D. Lancer le script dans un thread ou un process séparé

Ton programme principal continue,  
et l’envoi WhatsApp tourne **en parallèle**.

---

## 🔄 4) Comment le script continue même si tu fermes la fenêtre

Deux options :

### ✔ Utiliser `pythonw.exe`

- pas de console
- pas de fenêtre
- le script tourne jusqu’à la fin

### ✔ Utiliser un “daemon” Python

- un thread qui continue même si le programme principal se termine  

---

## 🧩 5) Comment Selenium gère WhatsApp Web en tâche de fond

Même en mode invisible, Selenium :

- charge WhatsApp Web  
- ouvre la conversation  
- trouve la zone de saisie  
- envoie le message  
- ferme proprement Chrome  

Tout cela **sans jamais interagir avec ton bureau**.

Donc :

- pas de clics  
- pas de focus perdu  
- pas de lignes ajoutées dans ton éditeur  
- pas de fenêtre qui s’ouvre  
- pas de perturbation de ton travail  

---

## ✨ 6) Résultat final

Une version “tâche de fond” :

- tourne sans console  
- tourne sans fenêtre Chrome  
- tourne même si tu fermes tout  
- tourne même si tu travailles sur autre chose  
- ne perturbe jamais ton éditeur  
- envoie les messages automatiquement  

C’est exactement ce que font les bots WhatsApp professionnels.
