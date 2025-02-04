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

def parse_services(xml_file):
    """Analyse le fichier XML des services et retourne un dictionnaire associant les services à leurs détails."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    service_data = {}
    
    for service in root.findall(".//Services"):
        name = service.findtext("Name", "")
        details = []
        for detail in service.findall(".//ServiceDetail"):
            destination_port = detail.findtext("DestinationPort", "N/A")
            protocol = detail.findtext("Protocol", detail.findtext("ProtocolName", "N/A"))
            details.append((protocol, destination_port))
        
        service_data[name] = details
    
    return service_data

def clean_list(value_list):
    """Supprime les doublons et enlève 'N/A' si d'autres valeurs sont présentes."""
    cleaned_list = list(dict.fromkeys(value_list))
    if "N/A" in cleaned_list and len(cleaned_list) > 1:
        cleaned_list.remove("N/A")
    return cleaned_list

def clean_ip_list(ip_list):
    """Si 'any' est présent, ne conserve que 'any'."""
    cleaned_list = list(dict.fromkeys(ip_list))
    return ["any"] if "any" in cleaned_list else cleaned_list

def parse_firewall_rules(xml_file, ip_data, service_data):
    """Analyse le fichier XML et extrait les règles de firewall en les croisant avec les IPs et services."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    rules = []
    
    for rule in root.findall(".//FirewallRule"):
        source_networks = [net.text for net in rule.findall(".//SourceNetworks/Network")]
        destination_networks = [net.text for net in rule.findall(".//DestinationNetworks/Network")]
        services = [srv.text for srv in rule.findall(".//Services/Service")]
        
        source_ips = clean_ip_list([ip_data.get(net, "any") for net in source_networks])
        destination_ips = clean_ip_list([ip_data.get(net, "any") for net in destination_networks])
        service_details = [service_data.get(srv, [("N/A", "N/A")]) for srv in services]
        
        flat_service_details = [item for sublist in service_details for item in sublist]
        destination_ports = clean_list([d[1] for d in flat_service_details])
        protocols = clean_list([d[0] for d in flat_service_details])
        
        rule_data = {
            "ID": rule.attrib.get("transactionid", "N/A"),
            "Name": rule.findtext("Name", ""),
            "Description": rule.findtext("Description", ""),
            "IPFamily": rule.findtext("IPFamily", ""),
            "Status": rule.findtext("Status", ""),
            "PolicyType": rule.findtext("PolicyType", ""),
            "Action": rule.find(".//Action").text if rule.find(".//Action") is not None else "",
            "LogTraffic": rule.find(".//LogTraffic").text if rule.find(".//LogTraffic") is not None else "",
            "SourceZones": "; ".join([zone.text for zone in rule.findall(".//SourceZones/Zone")]),
            "DestinationZones": "; ".join([zone.text for zone in rule.findall(".//DestinationZones/Zone")]),
            "Schedule": rule.find(".//Schedule").text if rule.find(".//Schedule") is not None else "",
            "Exclusions": "",  # Placeholder for exclusions if needed
            "SourceNetworks": "; ".join(source_networks),
            "Source Network IP": "; ".join(source_ips),
            "DestinationNetworks": "; ".join(destination_networks),
            "Destination Network IP": "; ".join(destination_ips),
            "Services": "; ".join(services),
            "Destination Ports": "; ".join(destination_ports),
            "Protocols": "; ".join(protocols)
        }
        rules.append(rule_data)
    
    return rules

def save_to_csv(rules, output_file):
    """Sauvegarde les règles extraites dans un fichier CSV formaté pour Excel."""
    if not rules:
        print("Aucune règle à sauvegarder.")
        return
    
    fieldnames = ["ID", "Name", "Description", "IPFamily", "Status", "PolicyType", "Action", "LogTraffic", "SourceZones", "DestinationZones", "Schedule", "Exclusions", "SourceNetworks", "Source Network IP", "DestinationNetworks", "Destination Network IP", "Services", "Destination Ports", "Protocols"]
    
    with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rules)
    
    print(f"Fichier CSV généré : {output_file}")

def main():
    print("=== Menu de Chargement des Fichiers Firewall ===")
    
    firewall_rules_file = select_file("des règles firewall")
    
    load_ip = input("Voulez-vous charger un fichier d'IP ? (O/N) : ").strip().lower()
    ip_data = {}
    if load_ip == 'o':
        ip_file = select_file("des IP")
        if ip_file:
            ip_data = parse_ip_hosts(ip_file)
    
    load_services = input("Voulez-vous charger un fichier de services ? (O/N) : ").strip().lower()
    service_data = {}
    if load_services == 'o':
        service_file = select_file("des Services")
        if service_file:
            service_data = parse_services(service_file)
    
    if firewall_rules_file:
        rules = parse_firewall_rules(firewall_rules_file, ip_data, service_data)
        save_to_csv(rules, "firewall_rules.csv")
    else:
        print("Aucun fichier XML sélectionné. Fin du programme.")
    
if __name__ == "__main__":
    tk.Tk().withdraw()
    main()
