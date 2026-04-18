# HôpitalStat 🏥
Système de Gestion et d'Analyse de Données Médicales
INF232 — EC2 · Université de Yaoundé I

## Déploiement sur Render.com

### Étape 1 — Préparer le dépôt GitHub
```bash
git init
git add .
git commit -m "HôpitalStat v1.0"
git remote add origin https://github.com/VOTRE_USER/hopitalstat.git
git push -u origin main
```

### Étape 2 — Déployer sur Render
1. Aller sur https://render.com → New → Web Service
2. Connecter le repo GitHub
3. Remplir :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`
4. Cliquer **Create Web Service**
5. Attendre le déploiement → copier le lien

## Fonctionnalités
- ✅ Tableau de bord avec statistiques en temps réel
- ✅ Enregistrement de patients avec ID unique automatique
- ✅ 35+ services médicaux disponibles
- ✅ Recherche par nom, prénom ou ID
- ✅ Filtres par service et statut
- ✅ Fiche patient complète
- ✅ Diagnostic & traitement
- ✅ Statistiques descriptives (service, sexe, groupe sanguin)
- ✅ Interface professionnelle responsive
