# Firewall Rules Converter

Outil Python permettant d'analyser des exports XML de règles firewall et de les convertir en un fichier Excel exploitable.

Le programme peut enrichir les règles en croisant plusieurs sources de données : objets réseau, services et positions des règles.

## Fonctionnalités

- Analyse d'exports XML de règles firewall
- Croisement avec les objets réseau et leurs adresses IP
- Croisement avec les services, ports et protocoles
- Association des règles avec leurs identifiants et positions
- Nettoyage et normalisation des données
- Export au format XLSX
- Mise en forme automatique du classeur Excel
- Sélection des fichiers via une interface système
- Exécutable Windows autonome

## Stack

- Python
- XML / ElementTree
- OpenPyXL
- Tkinter
- PyInstaller

## Fonctionnement

L'outil charge un export de règles firewall puis extrait les principales informations :

- nom et description de la règle
- statut et action
- zones source et destination
- objets réseau
- adresses IP correspondantes
- services
- ports
- protocoles

Des fichiers XML complémentaires peuvent être fournis afin d'enrichir les données avant la génération du fichier Excel final.

## Objectif

Ce projet a été développé pour transformer rapidement des exports firewall difficiles à exploiter en un tableau lisible et filtrable.

Il permet d'automatiser un travail de rapprochement qui serait autrement long et répétitif.

## Auteur

Cédric Leroy

🌐 https://cedricleroy.fr
