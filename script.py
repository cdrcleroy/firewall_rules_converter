import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import csv

def select_file(file_type):
    """Ouvre un explorateur de fichiers pour sélectionner un fichier."""
    file_path = filedialog.askopenfilename(title=f"Sélectionner le fichier {file_type}", filetypes=[("Fichiers XML", "*.xml"), ("Tous les fichiers", "*.*")])
    return file_path if file_path else None

def parse_ip_hosts(xml_file):
    """Analyse le fichier XML des adresses IP et retourne un dictionnaire associant les noms aux IPs."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ip_data = {}
    
    for host in root.findall(".//IPHost"):
        name = host.findtext("Name", "")
        ip_address = host.findtext("IPAddress", "")
        start_ip = host.findtext("StartIPAddress", "")
        end_ip = host.findtext("EndIPAddress", "")
        
        if ip_address:
            ip_data[name] = ip_address
        elif start_ip and end_ip:
            ip_data[name] = f"{start_ip} - {end_ip}"
    
    return ip_data

def clean_ip_list(ip_list):
    """Supprime les doublons et ne garde qu'un seul 'any' si présent."""
    if "any" in ip_list:
        return ["any"]
    return list(dict.fromkeys(ip_list))

def parse_firewall_rules(xml_file, ip_data):
    """Analyse le fichier XML et extrait les règles de firewall en les croisant avec les IPs."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    rules = []
    
    for rule in root.findall(".//FirewallRule"):
        source_networks = [net.text for net in rule.findall(".//SourceNetworks/Network")]
        destination_networks = [net.text for net in rule.findall(".//DestinationNetworks/Network")]
        
        source_ips = clean_ip_list([ip_data.get(net, "any") for net in source_networks])
        destination_ips = clean_ip_list([ip_data.get(net, "any") for net in destination_networks])
        
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
            "SourceZones": " | ".join([zone.text for zone in rule.findall(".//SourceZones/Zone")]),
            "DestinationZones": " | ".join([zone.text for zone in rule.findall(".//DestinationZones/Zone")]),
            "SourceNetworks": " | ".join(source_networks),
            "SourceIP": " | ".join(source_ips),
            "DestinationNetworks": " | ".join(destination_networks),
            "DestinationIP": " | ".join(destination_ips),
            "Services": " | ".join([service.text for service in rule.findall(".//Services/Service")])
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
    ip_data = {}
    if load_ip == 'o':
        ip_file = select_file("des IP")
        if ip_file:
            ip_data = parse_ip_hosts(ip_file)
    
    if firewall_rules_file:
        rules = parse_firewall_rules(firewall_rules_file, ip_data)
        save_to_csv(rules, "firewall_rules.csv")
    else:
        print("Aucun fichier XML sélectionné. Fin du programme.")
    
    
if __name__ == "__main__":
    tk.Tk().withdraw()  # Empêche l'affichage de la fenêtre Tkinter
    main()
