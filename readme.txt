# 🔥 Firewall Rules Converter

## 📌 Description
Firewall Rules Converter est un outil permettant d'analyser et de convertir des fichiers XML contenant des règles de firewall en un fichier CSV compatible avec Excel. Il offre la possibilité de croiser ces règles avec des fichiers d'adresses IP, de services et de positions.

## 🚀 Fonctionnalités
- 📂 Chargement d'un fichier XML contenant les règles de firewall.
- 🔄 Option pour croiser les règles avec un fichier d'adresses IP.
- 📡 Option pour croiser les règles avec un fichier de services.
- 🔢 Option pour croiser les règles avec un fichier de positions.
- 📊 Exportation des résultats au format **CSV** (compatible Excel).
- 🎛 Interface CLI avec messages informatifs et barre de progression.
- 🎨 Icône personnalisée et métadonnées intégrées dans l'exécutable.

## 🛠️ Prérequis
Aucune installation spécifique n'est requise. L'outil est fourni sous forme d'un exécutable autonome.

## 💻 Utilisation
1️⃣ **Lancer l'outil** :
   - Double-cliquez sur `firewall_rules_menu.exe`
   - Ou ouvrez un terminal et exécutez :
     ```sh
     firewall_rules_menu.exe
     ```

2️⃣ **Sélectionner les fichiers** :
   - Choisissez le fichier des règles firewall (XML).
   - Optionnellement, ajoutez un fichier d'IP, de services et/ou de positions.

3️⃣ **Choisir l'emplacement du fichier CSV de sortie**.

4️⃣ **Lancer le traitement** : L'outil affichera une barre de progression.

5️⃣ **Ouvrir le fichier CSV** dans Excel ou un autre tableur.

## 📝 Format des fichiers supportés
### 📄 **Fichier de règles firewall (XML)**
Contient les différentes règles appliquées sur le firewall.

### 🌍 **Fichier d'adresses IP (XML)**
Permet de croiser les réseaux définis dans les règles avec leurs adresses IP correspondantes.

### 📡 **Fichier de services (XML)**
Associe les services référencés dans les règles à leurs détails (ports et protocoles).

### 🔢 **Fichier de positions (texte brut)**
Associe chaque règle à un ID et une position définis dans l'export du firewall.

## 📂 Structure du CSV généré
Le fichier CSV contient les colonnes suivantes :
- **ID** : Identifiant de la règle (si fichier de positions chargé)
- **Name** : Nom de la règle
- **Description** : Description de la règle
- **IPFamily** : Type d'adresse (IPv4/IPv6)
- **Status** : Statut de la règle (Enable/Disable)
- **PolicyType** : Type de politique (Network, Application...)
- **Action** : Accept, Drop, etc.
- **LogTraffic** : Indique si le trafic est loggé
- **SourceZones / DestinationZones** : Zones concernées
- **SourceNetworks / DestinationNetworks** : Noms des réseaux impliqués
- **Source Network IP / Destination Network IP** : Adresses IP croisées
- **Services** : Liste des services concernés
- **Destination Ports / Protocols** : Ports et protocoles associés

## ❓ FAQ
### 💬 **Pourquoi certaines règles ont "N/A" dans les colonnes IP ?**
Si le fichier d'IP n'a pas été chargé ou si aucune correspondance n'a été trouvée, "N/A" est affiché.

### 💬 **Puis-je utiliser cet outil sur Mac ou Linux ?**
Actuellement, seule une version Windows sous forme d'exécutable est fournie.

### 💬 **Puis-je modifier le CSV généré ?**
Oui ! Le fichier CSV est ouvertement éditable dans Excel, LibreOffice Calc ou tout autre tableur.

## 📜 Licence
Cet outil est fourni sous licence **privée**. Toute redistribution ou modification sans autorisation est interdite.

## 🛠 Support et Contact
Si vous avez des questions ou des suggestions, contactez l'équipe de développement.

