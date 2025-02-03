import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import csv

def select_file(file_type):
    """Ouvre un explorateur de fichiers pour sélectionner un fichier."""
    file_path = filedialog.askopenfilename(title=f"Sélectionner le fichier {file_type}", filetypes=[("Fichiers XML", "*.xml"), ("Tous les fichiers", "*.*")])
    return file_path if file_path else None

def parse_firewall_rules(xml_file):
    """Analyse le fichier XML et extrait les règles de firewall."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    rules = []
    
    for rule in root.findall(".//FirewallRule"):
        rule_data = {
            "Name": rule.findtext("Name", ""),
            "Description": rule.findtext("Description", ""),
            "IPFamily": rule.findtext("IPFamily", ""),
            "Status": rule.findtext("Status", ""),
            "Position": rule.findtext("Position", ""),
            "PolicyType": rule.findtext("PolicyType", ""),
            "Action": rule.find(".//Action").text if rule.find(".//Action") is not None else "",
            "LogTraffic": rule.find(".//LogTraffic").text if rule.find(".//LogTraffic") is not None else "",
            "Schedule": rule.find(".//Schedule").text if rule.find(".//Schedule") is not None else "",
            "SourceZones": "; ".join([zone.text for zone in rule.findall(".//SourceZones/Zone")]),
            "DestinationZones": "; ".join([zone.text for zone in rule.findall(".//DestinationZones/Zone")]),
            "SourceNetworks": "; ".join([net.text for net in rule.findall(".//SourceNetworks/Network")]),
            "DestinationNetworks": "; ".join([net.text for net in rule.findall(".//DestinationNetworks/Network")]),
            "Services": "; ".join([service.text for service in rule.findall(".//Services/Service")])
        }
        rules.append(rule_data)
    
    return rules

def save_to_csv(rules, output_file):
    """Sauvegarde les règles extraites dans un fichier CSV formaté pour Excel."""
    if not rules:
        print("Aucune règle à sauvegarder.")
        return
    
    fieldnames = rules[0].keys()
    
    with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rules)
    
    print(f"Fichier CSV généré : {output_file}")

def main():
    print("=== Menu de Chargement des Fichiers Firewall ===")
    
    # Charger le fichier principal XML
    input("Appuyez sur Entrée pour sélectionner le fichier XML principal...")
    firewall_rules_file = select_file("des règles firewall")
    
    # Charger le fichier des IP (optionnel)
    load_ip = input("Voulez-vous charger un fichier d'IP ? (O/N) : ").strip().lower()
    ip_file = select_file("des IP") if load_ip == 'o' else None
    
    # Charger le fichier des services (optionnel)
    load_services = input("Voulez-vous charger un fichier de services ? (O/N) : ").strip().lower()
    services_file = select_file("des services") if load_services == 'o' else None
    
    # Affichage des fichiers sélectionnés
    print("\n=== Fichiers chargés ===")
    if firewall_rules_file:
        print(f"Fichier XML principal : {firewall_rules_file}")
    if ip_file:
        print(f"Fichier IP : {ip_file}")
    if services_file:
        print(f"Fichier Services : {services_file}")
    if not (firewall_rules_file or ip_file or services_file):
        print("Aucun fichier sélectionné.")

    if firewall_rules_file:
        rules = parse_firewall_rules(firewall_rules_file)
        save_to_csv(rules, "firewall_rules.csv")
    else:
        print("Aucun fichier XML sélectionné. Fin du programme.")
    
if __name__ == "__main__":
    tk.Tk().withdraw()  # Empêche l'affichage de la fenêtre Tkinter
    main()
