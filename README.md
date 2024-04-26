

# Présentation de l'application APOGEE

APOGEE, qui signifie "Application Pour l’Organisation et la Gestion des Enseignements et des Étudiants", est un Progiciel de Gestion Intégrée (PGI). Il est spécifiquement conçu pour gérer les dossiers des étudiants et leurs inscriptions.

## Fonctionnalités Principales

- **Inscription Administrative**: Création automatique des formulaires d'inscription pour les étudiants lors de leurs réinscriptions.
  
- **Dossier Étudiant**: Gestion des données administratives des étudiants, y compris leur cursus, inscription pédagogique, adresse, etc.
  
- **Stage**: Gestion des conventions de stage pour les étudiants.
  
- **Contrôle des Connaissances**: Saisie des barèmes, coefficients, et règles de calcul des notes et résultats.
  
- **Résultat**: Saisie des notes, calcul automatique, classement des étudiants, et production de documents tels que les procès-verbaux de notes, relevés de notes, diplômes.

## Aperçu de Docker Compose pour APOGEE

Le fichier `docker-compose.yml` est utilisé pour orchestrer les différents services nécessaires à l'exécution de l'application APOGEE. Voici une brève explication des services définis dans ce fichier :

- **web**: Service principal qui exécute l'application APOGEE basée sur Django et servie via Gunicorn. Il est exposé sur le port 8000 de l'hôte.
  
- **db**: Service de base de données PostgreSQL (version 13) qui stocke toutes les données nécessaires pour l'application, y compris les dossiers des étudiants, les inscriptions, etc.
  
- **nginx**: Serveur web Nginx utilisé comme proxy inverse pour rediriger les requêtes vers le service Web et gérer les connexions SSL.
  
- **letsencrypt**: Service pour la gestion des certificats SSL, permettant d'assurer une connexion sécurisée à l'application.

### Volumes

- **postgres_data**: Volume Docker utilisé pour stocker les données de la base de données PostgreSQL afin de garantir la persistance des données.
  
- **letsencrypt**: Volume externe utilisé pour stocker les certificats SSL générés par Let's Encrypt.
  
- **static_volume**: Volume Docker utilisé pour gérer les fichiers statiques de l'application, garantissant ainsi une gestion efficace et persistante des ressources statiques nécessaires à l'exécution de l'application.

## Instructions pour exécuter l'application APOGEE avec Docker Compose

### Prérequis

Avant de commencer, assurez-vous d'avoir installé Docker et Docker Compose sur votre système.

### Étapes pour exécuter l'application

1. **Accédez au serveur**:
   Connectez-vous à votre serveur en utilisant SSH :
   ```
   ssh root@185.84.163.227
   ```
   Entrez votre mot de passe lorsque cela vous est demandé.

2. **Naviguez vers le répertoire de l'application**:
   Une fois connecté, accédez au répertoire de l'application APOGEE :
   ```
   cd /home/saladin/apogee-prod
   ```

3. **Exécutez Docker Compose**:
   Pour construire et démarrer les conteneurs Docker, utilisez la commande suivante :
   ```
   docker-compose up --build
   ```

4. **Arrêter l'application (si nécessaire)**:
   Pour arrêter les conteneurs sans supprimer les volumes Docker :
   ```
   docker-compose stop
   ```

5. **Redémarrer l'application (après l'arrêt)**:
   Pour redémarrer les conteneurs après les avoir arrêtés :
   ```
   docker-compose start
   ```

### Accès à l'application

Après avoir démarré les conteneurs, vous pouvez accéder à l'application APOGEE via un navigateur web en utilisant l'adresse IP de votre serveur et le port 8000, par exemple : [http://185.84.163.227](http://185.84.163.227).

Alternativement, pour une meilleure sécurité et accessibilité, vous pouvez utiliser 'le domain name' avec SSL pour accéder à l'application via l'URL sécurisée suivante : [https://apogee.twc1.net](https://apogee.twc1.net).

### Note

Assurez-vous que tous les services nécessaires (web, db, nginx, letsencrypt) sont en cours d'exécution et accessibles avant d'accéder à l'application via le navigateur.

### Ressources supplémentaires

Pour plus d'informations sur Docker Compose et Docker, vous pouvez consulter les ressources suivantes :

- [Documentation Docker Compose](https://docs.docker.com/compose/)

--- 

