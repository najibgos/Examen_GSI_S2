# -*- coding: utf-8 -*-
"""
Examen Streamlit — Réseaux & Sécurité Cisco
Barème total : 60 points
Partie A : Questions de cours (20 pts)
Partie B : Scénarios de configuration Cisco CLI interactif (40 pts)
  - Exercice 1 : Switching/VLAN/STP (5 pts)
  - Exercice 2 : Routage OSPF (5 pts)
  - Exercice 3 : NAT/PAT Overload (5 pts)
  - Exercice 4 : ACL étendue de sécurité (5 pts)
  - Exercice 5 : Configuration MPLS Natif (10 pts)
  - Exercice 6 : VPN IPsec Site-to-Site (10 pts)

Exécution : streamlit run app_examen_reseaux_securite2.py
"""

from __future__ import annotations

import csv
import html
import io
import json
import re
from datetime import datetime
from typing import Any, Dict, List, Tuple

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Examen Réseaux & Sécurité Cisco — 60 pts",
    page_icon="🛡️",
    layout="wide",
)

# -----------------------------------------------------------------------------
# Style
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.15rem;
        font-weight: 800;
        margin-bottom: .2rem;
    }
    .subtitle {
        color: #5f6b7a;
        font-size: 1.02rem;
        margin-bottom: 1.2rem;
    }
    .score-box {
        border-radius: 18px;
        padding: 1rem 1.2rem;
        background: linear-gradient(135deg, #eef6ff, #f7fbff);
        border: 1px solid #d7e8ff;
        margin: .5rem 0 1rem 0;
    }
    .rubric {
        border-left: 4px solid #4d8df7;
        padding-left: .8rem;
        color: #334155;
        margin: .3rem 0 1rem 0;
    }
    .small-note { color: #64748b; font-size: .9rem; }
    .cli-screen {
        background: #070b16;
        color: #d7f7d0;
        border: 1px solid #1f2a44;
        border-radius: 14px;
        padding: 1rem;
        min-height: 260px;
        max-height: 360px;
        overflow-y: auto;
        font-family: "Courier New", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: .93rem;
        line-height: 1.35rem;
        white-space: pre-wrap;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.02);
    }
    .cli-prompt {
        background: #070b16;
        color: #79f28f;
        border: 1px solid #1f2a44;
        border-radius: 10px;
        padding: .53rem .65rem;
        font-family: "Courier New", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-weight: 700;
        min-height: 2.4rem;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }
    div[data-testid="stTextInput"] input {
        font-family: "Courier New", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }
    .cli-help {
        color: #64748b;
        font-size: .86rem;
        margin-top: -.25rem;
        margin-bottom: .5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Données de l'examen
# -----------------------------------------------------------------------------
QCM: List[Dict[str, Any]] = [
    {
        "id": "qcm1",
        "theme": "Routage",
        "question": "Quel élément d'une table de routage indique le routeur voisin vers lequel envoyer un paquet ?",
        "options": ["Adresse MAC", "Next Hop / prochain saut", "VLAN ID", "Numéro d'ACL"],
        "answer": "Next Hop / prochain saut",
        "points": 1.0,
    },
    {
        "id": "qcm2",
        "theme": "Routage",
        "question": "Quel protocole est classé EGP et utilise une logique de politiques entre systèmes autonomes ?",
        "options": ["RIP", "OSPF", "EIGRP", "BGP"],
        "answer": "BGP",
        "points": 1.0,
    },
    {
        "id": "qcm3",
        "theme": "Switching",
        "question": "Sur quel type d'adresse un switch de couche 2 s'appuie-t-il pour prendre ses décisions de forwarding ?",
        "options": ["Adresse IP source", "Adresse MAC", "Port TCP", "Certificat X.509"],
        "answer": "Adresse MAC",
        "points": 1.0,
    },
    {
        "id": "qcm4",
        "theme": "VLAN",
        "question": "Quel type de port transporte plusieurs VLANs entre deux équipements réseau ?",
        "options": ["Port access", "Port trunk", "Port console", "Port loopback"],
        "answer": "Port trunk",
        "points": 1.0,
    },
    {
        "id": "qcm5",
        "theme": "STP",
        "question": "Quelle est la mission principale de STP dans un réseau commuté redondant ?",
        "options": [
            "Chiffrer les trames Ethernet",
            "Éviter les boucles de niveau 2",
            "Attribuer les adresses IP",
            "Traduire les adresses privées en publiques",
        ],
        "answer": "Éviter les boucles de niveau 2",
        "points": 1.0,
    },
    {
        "id": "qcm6",
        "theme": "NAT",
        "question": "Quel type de NAT permet à plusieurs machines de partager une seule adresse IP publique grâce aux ports TCP/UDP ?",
        "options": ["NAT statique", "NAT dynamique", "PAT / NAT overload", "Route statique"],
        "answer": "PAT / NAT overload",
        "points": 1.0,
    },
    {
        "id": "qcm7",
        "theme": "NAT",
        "question": "Dans le vocabulaire NAT, l'adresse privée source avant traduction est appelée :",
        "options": ["Inside local", "Inside global", "Outside local", "Outside global"],
        "answer": "Inside local",
        "points": 1.0,
    },
    {
        "id": "qcm8",
        "theme": "ACL",
        "question": "Une ACL standard filtre principalement selon :",
        "options": ["Adresse source uniquement", "Adresse source + destination + port", "Adresse MAC", "Certificat utilisateur"],
        "answer": "Adresse source uniquement",
        "points": 1.0,
    },
    {
        "id": "qcm9",
        "theme": "ACL",
        "question": "Quel principe explique qu'une ACL s'arrête dès qu'une règle correspond au paquet ?",
        "options": ["Dijkstra", "Première correspondance", "DHCP relay", "Cross-certification"],
        "answer": "Première correspondance",
        "points": 1.0,
    },
    {
        "id": "qcm10",
        "theme": "Cryptographie",
        "question": "Quel algorithme de chiffrement symétrique moderne est recommandé à la place de DES ?",
        "options": ["AES", "MD5", "RSA", "BGP"],
        "answer": "AES",
        "points": 1.0,
    },
    {
        "id": "qcm11",
        "theme": "Cryptographie",
        "question": "Quelle propriété est principalement fournie par une signature numérique ?",
        "options": ["Segmentation VLAN", "Non-répudiation et authenticité", "Translation IPv4", "Élection DR/BDR"],
        "answer": "Non-répudiation et authenticité",
        "points": 1.0,
    },
    {
        "id": "qcm12",
        "theme": "PKI",
        "question": "Dans une PKI, quel composant vérifie l'identité du demandeur avant émission du certificat ?",
        "options": ["RA", "CAM table", "PAT", "VTP"],
        "answer": "RA",
        "points": 1.0,
    },
]

SHORT_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "short1",
        "theme": "Routage",
        "question": "Expliquez la différence entre routage statique et routage dynamique.",
        "points": 2.0,
        "keywords": ["manuel", "administrateur", "protocole", "automatique", "adaptatif", "table"],
        "solution": "Le routage statique est configuré manuellement par l'administrateur et ne s'adapte pas seul. Le routage dynamique utilise des protocoles de routage pour apprendre les réseaux et recalculer automatiquement les chemins.",
    },
    {
        "id": "short2",
        "theme": "ACL",
        "question": "Pourquoi l'ordre des règles est-il critique dans une ACL Cisco ?",
        "points": 2.0,
        "keywords": ["séquentiel", "haut", "bas", "première", "correspondance", "deny", "implicite"],
        "solution": "Les règles sont lues de haut en bas et le traitement s'arrête à la première correspondance. Une règle trop générale placée avant une règle spécifique peut bloquer ou autoriser le mauvais trafic. Un deny all implicite existe à la fin.",
    },
    {
        "id": "short3",
        "theme": "Cryptographie",
        "question": "Comparez brièvement chiffrement symétrique et asymétrique.",
        "points": 2.0,
        "keywords": ["même clé", "clé publique", "clé privée", "rapide", "échange", "signature"],
        "solution": "Le symétrique utilise la même clé pour chiffrer et déchiffrer, il est rapide mais pose un problème de partage de clé. L'asymétrique utilise une clé publique et une clé privée ; il facilite l'échange de clés et les signatures, mais il est plus lent.",
    },
    {
        "id": "short4",
        "theme": "PKI",
        "question": "Citez les grandes étapes du cycle de vie d'un certificat numérique.",
        "points": 2.0,
        "keywords": ["demande", "enregistrement", "vérification", "émission", "utilisation", "renouvellement", "révocation", "expiration"],
        "solution": "Les étapes principales sont la demande/enregistrement, la vérification d'identité par la RA, l'émission et publication par la CA, l'utilisation, le renouvellement, la révocation éventuelle via CRL/OCSP, puis l'expiration.",
    },
]

SCENARIOS: List[Dict[str, Any]] = [
    {
        "id": "sc1",
        "title": "Scénario 1 — Switching, VLAN et STP",
        "device": "S1",
        "points": 5.0,
        "context": "Vous administrez le switch S1. Créez VLAN 10 nommé ADMIN et VLAN 20 nommé USERS. Mettez Fa0/1 en access VLAN 10 et Fa0/2 en access VLAN 20. Configurez G0/1 en trunk 802.1Q autorisant les VLAN 10 et 20. Faites de S1 le root bridge pour les VLAN 10 et 20. Ajoutez une commande de vérification.",
        "criteria": [
            {"label": "Création des VLAN 10 et 20", "points": 1.0, "patterns": [r"\bvlan\s+10\b", r"\bvlan\s+20\b"], "mode": "all"},
            {"label": "Affectation de Fa0/1 au VLAN 10 et Fa0/2 au VLAN 20 en mode access", "points": 1.2, "patterns": [r"interface\s+fa(?:stethernet)?0/1[\s\S]*switchport\s+mode\s+access[\s\S]*switchport\s+access\s+vlan\s+10", r"interface\s+fa(?:stethernet)?0/2[\s\S]*switchport\s+mode\s+access[\s\S]*switchport\s+access\s+vlan\s+20"], "mode": "all"},
            {"label": "Configuration du trunk G0/1 et autorisation VLAN 10,20", "points": 1.2, "patterns": [r"interface\s+g(?:igabitethernet)?0/1[\s\S]*switchport\s+mode\s+trunk", r"switchport\s+trunk\s+allowed\s+vlan\s+(?:10\s*,\s*20|20\s*,\s*10|10\s+20|20\s+10)"], "mode": "all"},
            {"label": "STP : S1 root pour VLAN 10 et 20", "points": 1.0, "patterns": [r"spanning-tree\s+vlan\s+(?:10\s*,\s*20|20\s*,\s*10|10\s+20|20\s+10)\s+root\s+primary"], "mode": "any"},
            {"label": "Vérification pertinente", "points": 0.6, "patterns": [r"show\s+vlan\s+brief", r"show\s+interfaces\s+trunk", r"show\s+spanning-tree"], "mode": "any"},
        ],
        "solution": """S1> enable
S1# configure terminal
S1(config)# vlan 10
S1(config-vlan)# name ADMIN
S1(config-vlan)# vlan 20
S1(config-vlan)# name USERS
S1(config-vlan)# exit
S1(config)# interface fa0/1
S1(config-if)# switchport mode access
S1(config-if)# switchport access vlan 10
S1(config-if)# interface fa0/2
S1(config-if)# switchport mode access
S1(config-if)# switchport access vlan 20
S1(config-if)# interface g0/1
S1(config-if)# switchport mode trunk
S1(config-if)# switchport trunk allowed vlan 10,20
S1(config-if)# exit
S1(config)# spanning-tree vlan 10,20 root primary
S1(config)# end
S1# show vlan brief
S1# show interfaces trunk
S1# show spanning-tree""",
    },
    {
        "id": "sc2",
        "title": "Scénario 2 — Routage OSPF",
        "device": "R1",
        "points": 5.0,
        "context": "Configurez R1 pour participer à OSPF process 1, area 0. R1 possède le LAN 192.168.10.0/24 sur G0/0 et le lien inter-routeur 10.0.12.0/30 sur S0/0/0. Rendez l'interface LAN passive. Ajoutez une route par défaut vers 10.0.12.2 et annoncez-la dans OSPF. Ajoutez une vérification.",
        "criteria": [
            {"label": "Activation du processus OSPF 1", "points": 0.8, "patterns": [r"router\s+ospf\s+1"], "mode": "any"},
            {"label": "Annonce du réseau LAN 192.168.10.0/24 en area 0", "points": 1.0, "patterns": [r"network\s+192\.168\.10\.0\s+0\.0\.0\.255\s+area\s+0"], "mode": "any"},
            {"label": "Annonce du lien 10.0.12.0/30 en area 0", "points": 1.0, "patterns": [r"network\s+10\.0\.12\.0\s+0\.0\.0\.3\s+area\s+0"], "mode": "any"},
            {"label": "LAN en passive-interface", "points": 0.8, "patterns": [r"passive-interface\s+g(?:igabitethernet)?0/0"], "mode": "any"},
            {"label": "Route par défaut et diffusion dans OSPF", "points": 1.0, "patterns": [r"ip\s+route\s+0\.0\.0\.0\s+0\.0\.0\.0\s+10\.0\.12\.2", r"default-information\s+originate"], "mode": "all"},
            {"label": "Commande de vérification", "points": 0.4, "patterns": [r"show\s+ip\s+route", r"show\s+ip\s+ospf\s+neighbor", r"show\s+ip\s+protocols"], "mode": "any"},
        ],
        "solution": """R1> enable
R1# configure terminal
R1(config)# ip route 0.0.0.0 0.0.0.0 10.0.12.2
R1(config)# router ospf 1
R1(config-router)# network 192.168.10.0 0.0.0.255 area 0
R1(config-router)# network 10.0.12.0 0.0.0.3 area 0
R1(config-router)# passive-interface g0/0
R1(config-router)# default-information originate
R1(config-router)# end
R1# show ip ospf neighbor
R1# show ip route""",
    },
    {
        "id": "sc3",
        "title": "Scénario 3 — NAT/PAT Overload",
        "device": "R-NAT",
        "points": 5.0,
        "context": "Configurez un routeur NAT. Le réseau interne 192.168.1.0/24 sort par G0/1 vers Internet. G0/0 est l'interface inside, G0/1 est outside. Utilisez l'ACL 1 pour autoriser le LAN et activez le PAT/overload sur l'interface G0/1. Ajoutez une vérification de la table NAT.",
        "criteria": [
            {"label": "ACL autorisant 192.168.1.0/24", "points": 1.0, "patterns": [r"access-list\s+1\s+permit\s+192\.168\.1\.0\s+0\.0\.0\.255"], "mode": "any"},
            {"label": "Interface G0/0 déclarée NAT inside", "points": 1.0, "patterns": [r"interface\s+g(?:igabitethernet)?0/0[\s\S]*ip\s+nat\s+inside"], "mode": "any"},
            {"label": "Interface G0/1 déclarée NAT outside", "points": 1.0, "patterns": [r"interface\s+g(?:igabitethernet)?0/1[\s\S]*ip\s+nat\s+outside"], "mode": "any"},
            {"label": "PAT/overload activé sur G0/1", "points": 1.5, "patterns": [r"ip\s+nat\s+inside\s+source\s+list\s+1\s+interface\s+g(?:igabitethernet)?0/1\s+overload"], "mode": "any"},
            {"label": "Vérification NAT", "points": 0.5, "patterns": [r"show\s+ip\s+nat\s+translations", r"show\s+ip\s+nat\s+statistics"], "mode": "any"},
        ],
        "solution": """R-NAT> enable
R-NAT# configure terminal
R-NAT(config)# access-list 1 permit 192.168.1.0 0.0.0.255
R-NAT(config)# interface g0/0
R-NAT(config-if)# ip nat inside
R-NAT(config-if)# interface g0/1
R-NAT(config-if)# ip nat outside
R-NAT(config-if)# exit
R-NAT(config)# ip nat inside source list 1 interface g0/1 overload
R-NAT(config)# end
R-NAT# show ip nat translations
R-NAT# show ip nat statistics""",
    },
    {
        "id": "sc4",
        "title": "Scénario 4 — ACL étendue de sécurité",
        "device": "R-SEC",
        "points": 5.0,
        "context": "Le LAN 192.168.10.0/24 arrive sur G0/0. Le serveur interne est 172.16.1.10. Créez une ACL étendue 100 qui bloque Telnet du LAN vers ce serveur, autorise HTTP et HTTPS du LAN vers ce serveur, puis autorise le reste du trafic IP. Appliquez l'ACL en entrée sur G0/0. Ajoutez une vérification.",
        "criteria": [
            {"label": "Blocage Telnet LAN -> serveur", "points": 1.2, "patterns": [r"access-list\s+100\s+deny\s+tcp\s+192\.168\.10\.0\s+0\.0\.0\.255\s+host\s+172\.16\.1\.10\s+eq\s+(?:23|telnet)"], "mode": "any"},
            {"label": "Autorisation HTTP vers le serveur", "points": 0.8, "patterns": [r"access-list\s+100\s+permit\s+tcp\s+192\.168\.10\.0\s+0\.0\.0\.255\s+host\s+172\.16\.1\.10\s+eq\s+(?:80|www|http)"], "mode": "any"},
            {"label": "Autorisation HTTPS vers le serveur", "points": 0.8, "patterns": [r"access-list\s+100\s+permit\s+tcp\s+192\.168\.10\.0\s+0\.0\.0\.255\s+host\s+172\.16\.1\.10\s+eq\s+(?:443|https)"], "mode": "any"},
            {"label": "Permit IP any any ou permit IP LAN any pour éviter le deny implicite total", "points": 0.8, "patterns": [r"access-list\s+100\s+permit\s+ip\s+any\s+any", r"access-list\s+100\s+permit\s+ip\s+192\.168\.10\.0\s+0\.0\.0\.255\s+any"], "mode": "any"},
            {"label": "Application en entrée sur G0/0", "points": 1.0, "patterns": [r"interface\s+g(?:igabitethernet)?0/0[\s\S]*ip\s+access-group\s+100\s+in"], "mode": "any"},
            {"label": "Vérification ACL", "points": 0.4, "patterns": [r"show\s+access-lists", r"show\s+ip\s+interface\s+g(?:igabitethernet)?0/0", r"show\s+running-config"], "mode": "any"},
        ],
        "solution": """R-SEC> enable
R-SEC# configure terminal
R-SEC(config)# access-list 100 deny tcp 192.168.10.0 0.0.0.255 host 172.16.1.10 eq 23
R-SEC(config)# access-list 100 permit tcp 192.168.10.0 0.0.0.255 host 172.16.1.10 eq 80
R-SEC(config)# access-list 100 permit tcp 192.168.10.0 0.0.0.255 host 172.16.1.10 eq 443
R-SEC(config)# access-list 100 permit ip any any
R-SEC(config)# interface g0/0
R-SEC(config-if)# ip access-group 100 in
R-SEC(config-if)# end
R-SEC# show access-lists
R-SEC# show ip interface g0/0"""    },
    {
        "id": "sc5",
        "title": "Scénario 5 — Configuration MPLS Natif",
        "device": "PE1",
        "points": 10.0,
        "context": "Vous configurez le routeur PE1, routeur de bord d'un réseau MPLS d'opérateur. Le backbone MPLS utilise le lien 10.1.12.0/30 sur G0/0 vers le routeur P voisin. Votre loopback0 (LDP/OSPF router-id) doit avoir l'IP 1.1.1.1/32. Activez CEF globalement. Déclarez OSPF process 1 en area 0 pour les réseaux 10.1.12.0/30 et 1.1.1.1/32. Activez le protocole de label MPLS (LDP) et configurez le router-id LDP sur loopback0 avec l'option force. Activez MPLS sur l'interface G0/0. Ajoutez des commandes de vérification MPLS et LDP.",
        "criteria": [
            {"label": "Activation de CEF", "points": 1.0, "patterns": [r"ip\s+cef"], "mode": "any"},
            {"label": "Loopback0 configuré avec IP 1.1.1.1/32", "points": 1.0, "patterns": [r"interface\s+lo(?:opback)?0[\s\S]*ip\s+address\s+1\.1\.1\.1\s+255\.255\.255\.255"], "mode": "any"},
            {"label": "OSPF process 1 activé", "points": 0.8, "patterns": [r"router\s+ospf\s+1"], "mode": "any"},
            {"label": "Réseau 10.1.12.0/30 annoncé en area 0", "points": 1.2, "patterns": [r"network\s+10\.1\.12\.0\s+0\.0\.0\.3\s+area\s+0"], "mode": "any"},
            {"label": "Loopback 1.1.1.1/32 annoncé en area 0", "points": 1.0, "patterns": [r"network\s+1\.1\.1\.1\s+0\.0\.0\.0\s+area\s+0"], "mode": "any"},
            {"label": "Protocole de label MPLS (LDP) activé globalement", "points": 1.2, "patterns": [r"mpls\s+ip"], "mode": "any"},
            {"label": "Router-id LDP configuré sur loopback0", "points": 1.0, "patterns": [r"mpls\s+ldp\s+router-id\s+lo(?:opback)?0"], "mode": "any"},
            {"label": "MPLS activé sur l'interface G0/0", "points": 1.2, "patterns": [r"interface\s+g(?:igabitethernet)?0/0[\s\S]*mpls\s+ip"], "mode": "any"},
            {"label": "Commandes de vérification MPLS/LDP", "points": 1.6, "patterns": [r"show\s+mpls\s+(?:interfaces|ldp\s+(?:neighbor|binding|discovery))", r"show\s+ip\s+cef"], "mode": "any"},
        ],
        "solution": """PE1> enable
PE1# configure terminal
PE1(config)# ip cef
PE1(config)# interface loopback0
PE1(config-if)# ip address 1.1.1.1 255.255.255.255
PE1(config-if)# exit
PE1(config)# router ospf 1
PE1(config-router)# network 10.1.12.0 0.0.0.3 area 0
PE1(config-router)# network 1.1.1.1 0.0.0.0 area 0
PE1(config-router)# exit
PE1(config)# mpls ip
PE1(config)# mpls ldp router-id loopback0 force
PE1(config)# interface g0/0
PE1(config-if)# mpls ip
PE1(config-if)# end
PE1# show mpls interfaces
PE1# show mpls ldp neighbor
PE1# show ip cef""",
    },
    {
        "id": "sc6",
        "title": "Scénario 6 — VPN IPsec Site-to-Site",
        "device": "R1",
        "points": 10.0,
        "context": "Vous configurez un tunnel VPN IPsec site-à-site entre le routeur R1 (LAN 192.168.1.0/24 sur G0/0) et un site distant (peer WAN 203.0.113.2, LAN 192.168.2.0/24). L'interface WAN de R1 est G0/1. Créez une policy ISAKMP 10 avec encryption aes 256, hash sha256, authentication pre-share et group 14. Définissez la clé pré-partagée CISCO123 pour le peer 203.0.113.2. Créez un transform-set nommé ESP-AES256 utilisant esp-aes 256 et esp-sha-hmac. Créez une ACL étendue 101 autorisant le trafic IP du LAN local vers le LAN distant. Créez un crypto map VPN-MAP 10 ipsec-isakmp, définissez le peer, le transform-set et faites un match address 101. Appliquez le crypto map sur G0/1. Ajoutez des vérifications.",
        "criteria": [
            {"label": "Policy ISAKMP 10 créée", "points": 0.5, "patterns": [r"crypto\s+isakmp\s+policy\s+10"], "mode": "any"},
            {"label": "Encryption AES 256 dans la policy ISAKMP", "points": 0.8, "patterns": [r"encryption\s+aes\s+256"], "mode": "any"},
            {"label": "Hash SHA256 dans la policy ISAKMP", "points": 0.7, "patterns": [r"hash\s+sha256"], "mode": "any"},
            {"label": "Authentication pre-share dans la policy ISAKMP", "points": 0.7, "patterns": [r"authentication\s+pre-share"], "mode": "any"},
            {"label": "Diffie-Hellman group 14 dans la policy ISAKMP", "points": 0.7, "patterns": [r"group\s+14"], "mode": "any"},
            {"label": "Clé pré-partagée ISAKMP pour le peer", "points": 1.0, "patterns": [r"crypto\s+isakmp\s+key\s+\S+\s+address\s+203\.0\.113\.2"], "mode": "any"},
            {"label": "Transform-set IPsec (esp-aes 256 + esp-sha-hmac)", "points": 1.0, "patterns": [r"crypto\s+ipsec\s+transform-set\s+\S+\s+esp-aes\s+256\s+esp-sha-hmac"], "mode": "any"},
            {"label": "ACL intéressante 101 (trafic LAN local -> LAN distant)", "points": 1.0, "patterns": [r"access-list\s+101\s+permit\s+ip\s+192\.168\.1\.0\s+0\.0\.0\.255\s+192\.168\.2\.0\s+0\.0\.0\.255"], "mode": "any"},
            {"label": "Crypto map VPN-MAP 10 ipsec-isakmp créé", "points": 0.5, "patterns": [r"crypto\s+map\s+\S+\s+10\s+ipsec-isakmp"], "mode": "any"},
            {"label": "Peer et transform-set configurés dans le crypto map", "points": 1.0, "patterns": [r"set\s+peer\s+203\.0\.113\.2", r"set\s+transform-set\s+\S+"], "mode": "all"},
            {"label": "Match address 101 dans le crypto map", "points": 0.6, "patterns": [r"match\s+address\s+101"], "mode": "any"},
            {"label": "Crypto map appliqué sur G0/1", "points": 0.8, "patterns": [r"interface\s+g(?:igabitethernet)?0/1[\s\S]*crypto\s+map\s+\S+"], "mode": "any"},
            {"label": "Commandes de vérification VPN IPsec", "points": 0.7, "patterns": [r"show\s+crypto\s+(?:isakmp\s+sa|ipsec\s+sa|map)"], "mode": "any"},
        ],
        "solution": """R1> enable
R1# configure terminal
R1(config)# crypto isakmp policy 10
R1(config-isakmp)# encryption aes 256
R1(config-isakmp)# hash sha256
R1(config-isakmp)# authentication pre-share
R1(config-isakmp)# group 14
R1(config-isakmp)# exit
R1(config)# crypto isakmp key CISCO123 address 203.0.113.2
R1(config)# crypto ipsec transform-set ESP-AES256 esp-aes 256 esp-sha-hmac
R1(config)# access-list 101 permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255
R1(config)# crypto map VPN-MAP 10 ipsec-isakmp
R1(config-crypto-map)# set peer 203.0.113.2
R1(config-crypto-map)# set transform-set ESP-AES256
R1(config-crypto-map)# match address 101
R1(config-crypto-map)# exit
R1(config)# interface g0/1
R1(config-if)# crypto map VPN-MAP
R1(config-if)# end
R1# show crypto isakmp sa
R1# show crypto ipsec sa
R1# show crypto map""",
    },
]

SCENARIO_BY_ID = {scenario["id"]: scenario for scenario in SCENARIOS}

# -----------------------------------------------------------------------------
# Fonctions d'évaluation
# -----------------------------------------------------------------------------
def normalize_cli(text: str) -> str:
    """Normalise une configuration Cisco copiée depuis un terminal."""
    text = text.lower()
    text = text.replace("\r", "\n")
    text = re.sub(r"^[\w.-]+(?:\([^)]*\))?[>#]\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"!.*", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def criterion_score(answer: str, criterion: Dict[str, Any]) -> Tuple[float, bool]:
    normalized = normalize_cli(answer)
    patterns = criterion.get("patterns", [])
    mode = criterion.get("mode", "any")
    hits = [bool(re.search(p, normalized, flags=re.IGNORECASE)) for p in patterns]
    ok = all(hits) if mode == "all" else any(hits)
    return (float(criterion["points"]) if ok else 0.0), ok


def grade_cli(answer: str, scenario: Dict[str, Any]) -> Tuple[float, List[Dict[str, Any]]]:
    details: List[Dict[str, Any]] = []
    total = 0.0
    for c in scenario["criteria"]:
        pts, ok = criterion_score(answer, c)
        total += pts
        details.append({"Critère": c["label"], "Points": pts, "Max": c["points"], "Validé": "Oui" if ok else "Non"})
    return round(total, 2), details


def grade_short_answer(answer: str, question: Dict[str, Any]) -> Tuple[float, int, List[str]]:
    text = answer.lower()
    keywords = question["keywords"]
    found = [kw for kw in keywords if kw.lower() in text]
    if len(found) >= 5:
        pts = question["points"]
    elif len(found) >= 3:
        pts = question["points"] * 0.7
    elif len(found) >= 1:
        pts = question["points"] * 0.4
    else:
        pts = 0.0
    return round(float(pts), 2), len(found), found


# -----------------------------------------------------------------------------
# Simulateur Cisco CLI interactif
# -----------------------------------------------------------------------------
def new_cli_state(device: str) -> Dict[str, Any]:
    return {
        "device": device,
        "mode": "user",
        "history": [],
        "accepted_lines": [],
        "last_interface": "",
        "last_vlan": "",
        "last_router": "",
    }


def cli_state_key(scenario_id: str) -> str:
    return f"{scenario_id}_cli_state"


def cli_input_key(scenario_id: str) -> str:
    return f"{scenario_id}_cli_input"


def prompt_for(state: Dict[str, Any]) -> str:
    device = state.get("device", "Router")
    mode = state.get("mode", "user")
    suffix_by_mode = {
        "user": ">",
        "privileged": "#",
        "config": "(config)#",
        "interface": "(config-if)#",
        "vlan": "(config-vlan)#",
        "router": "(config-router)#",
        "crypto-isakmp": "(config-isakmp)#",
        "crypto-map": "(config-crypto-map)#",
    }
    return f"{device}{suffix_by_mode.get(mode, '#')}"


def strip_entered_prompt(raw_command: str) -> str:
    """Autorise l'étudiant à saisir soit 'enable', soit 'R1> enable'."""
    command = raw_command.strip()
    command = re.sub(r"^[\w.-]+(?:\([^)]*\))?[>#]\s*", "", command)
    return command.strip()


def compact(command: str) -> str:
    return re.sub(r"\s+", " ", command.strip()).lower()


def invalid_output(command: str) -> str:
    marker = " " * max(1, min(len(command), 18)) + "^"
    return f"{marker}\n% Invalid input detected at '^' marker."


def fake_show_output(command: str, scenario: Dict[str, Any]) -> str:
    c = compact(command)
    if c.startswith("do "):
        c = c[3:].strip()
    if "show vlan brief" in c:
        return "VLAN Name                             Status    Ports\n10   ADMIN                            active    Fa0/1\n20   USERS                            active    Fa0/2"
    if "show interfaces trunk" in c:
        return "Port        Mode         Encapsulation  Status        Native vlan\nGi0/1       on           802.1q         trunking      1\nVlans allowed on trunk: 10,20"
    if "show spanning-tree" in c:
        return "VLAN0010  Root ID Priority 24586  This bridge is the root\nVLAN0020  Root ID Priority 24596  This bridge is the root"
    if "show ip ospf neighbor" in c:
        return "Neighbor ID     Pri   State           Dead Time   Address         Interface\n10.0.12.2         1   FULL/ -         00:00:36    10.0.12.2       Serial0/0/0"
    if "show ip route" in c:
        return "Gateway of last resort is 10.0.12.2 to network 0.0.0.0\nO    192.168.10.0/24 is directly connected\nS*   0.0.0.0/0 [1/0] via 10.0.12.2"
    if "show ip protocols" in c:
        return "Routing Protocol is \"ospf 1\"\n  Routing for Networks: 192.168.10.0/24, 10.0.12.0/30"
    if "show ip nat translations" in c:
        return "Pro  Inside global      Inside local       Outside local      Outside global\ntcp  G0/1:1025          192.168.1.10:1025  142.250.74.78:80  142.250.74.78:80"
    if "show ip nat statistics" in c:
        return "Total active translations: 1\nOutside interfaces: GigabitEthernet0/1\nInside interfaces: GigabitEthernet0/0"
    if "show access-lists" in c:
        return "Extended IP access list 100\n    deny tcp 192.168.10.0 0.0.0.255 host 172.16.1.10 eq telnet\n    permit tcp 192.168.10.0 0.0.0.255 host 172.16.1.10 eq www\n    permit tcp 192.168.10.0 0.0.0.255 host 172.16.1.10 eq 443\n    permit ip any any"
    if "show ip interface" in c:
        return "GigabitEthernet0/0 is up, line protocol is up\n  Inbound access list is 100"
    if "show running-config" in c or "show run" in c:
        return "Building configuration...\nCurrent configuration : commandes saisies par l'étudiant"
    if "show mpls interfaces" in c:
        return "Interface              IP        Operational   MPLS\nGigabitEthernet0/0     Yes       Yes           Yes"
    if "show mpls ldp neighbor" in c:
        return "    Peer LDP Ident: 2.2.2.2:0; Local LDP Ident 1.1.1.1:0\n        TCP connection: 10.1.12.2 - 10.1.12.1, status: operational\n        Sessions: 1"
    if "show mpls ldp binding" in c:
        return "  lib entry: 10.1.12.0/30, rev 2\n        local binding:  label: 16\n        remote binding: lsr: 2.2.2.2:0, label: 17"
    if "show mpls ldp discovery" in c:
        return "Local LDP Identifier: 1.1.1.1:0\n    Discovery Sources:\n    Interfaces:\n        GigabitEthernet0/0, xmit/recv"
    if "show ip cef" in c:
        return "Prefix              Next Hop             Interface\n0.0.0.0/0           10.1.12.2            GigabitEthernet0/0\n1.1.1.1/32          attached             Loopback0\n10.1.12.0/30        attached             GigabitEthernet0/0"
    if "show crypto isakmp sa" in c:
        return "IPv4 Crypto ISAKMP SA\ndst             src             state          conn-id slot status\n203.0.113.2      198.51.100.1    QM_IDLE           1001   0    ACTIVE"
    if "show crypto ipsec sa" in c:
        return "interface: GigabitEthernet0/1\n    Crypto map tag: VPN-MAP, local addr 198.51.100.1\n   protected vrf: (none)\n   local  ident (addr/mask/prot/port): (192.168.1.0/255.255.255.0/0/0)\n   remote ident (addr/mask/prot/port): (192.168.2.0/255.255.255.0/0/0)\n   current_peer 203.0.113.2 port 500\n     PERMIT, flags={origin_is_acl,}\n    #pkts encaps: 4, #pkts encrypt: 4, #pkts digest: 4"
    if "show crypto map" in c:
        return 'Crypto Map "VPN-MAP" 10 ipsec-isakmp\n        Peer = 203.0.113.2\n        Extended IP access list 101\n        Current peer: 203.0.113.2\n        Security association lifetime: 4608000 kilobytes/3600 seconds\n        Transform set={ESP-AES256, }'
    return f"Commande de vérification exécutée sur {scenario['device']}."


def is_global_config_command(c: str) -> bool:
    patterns = [
        r"^access-list\s+\d+\s+(permit|deny)\s+.+",
        r"^ip\s+route\s+.+",
        r"^ip\s+nat\s+inside\s+source\s+.+",
        r"^ip\s+cef$",
        r"^spanning-tree\s+vlan\s+.+",
        r"^hostname\s+\S+",
        r"^no\s+ip\s+domain-lookup$",
        r"^service\s+.+",
        r"^mpls\s+ip$",
        r"^mpls\s+label\s+protocol\s+.+",
        r"^mpls\s+ldp\s+router-id\s+.+",
        r"^crypto\s+isakmp\s+key\s+.+",
        r"^crypto\s+ipsec\s+transform-set\s+.+",
    ]
    return any(re.match(pattern, c) for pattern in patterns)


def is_interface_command(c: str) -> bool:
    patterns = [
        r"^switchport\s+mode\s+(access|trunk)$",
        r"^switchport\s+access\s+vlan\s+\d+$",
        r"^switchport\s+trunk\s+allowed\s+vlan\s+.+",
        r"^switchport\s+trunk\s+encapsulation\s+dot1q$",
        r"^ip\s+nat\s+(inside|outside)$",
        r"^ip\s+access-group\s+\d+\s+(in|out)$",
        r"^ip\s+address\s+\d+\.\d+\.\d+\.\d+\s+\d+\.\d+\.\d+\.\d+$",
        r"^no\s+shutdown$",
        r"^shutdown$",
        r"^description\s+.+",
        r"^mpls\s+ip$",
        r"^crypto\s+map\s+\S+$",
    ]
    return any(re.match(pattern, c) for pattern in patterns)


def is_router_command(c: str) -> bool:
    patterns = [
        r"^network\s+\d+\.\d+\.\d+\.\d+\s+\d+\.\d+\.\d+\.\d+\s+area\s+\d+$",
        r"^passive-interface\s+\S+$",
        r"^default-information\s+originate$",
        r"^router-id\s+\d+\.\d+\.\d+\.\d+$",
        r"^redistribute\s+.+",
    ]
    return any(re.match(pattern, c) for pattern in patterns)


def is_isakmp_command(c: str) -> bool:
    patterns = [
        r"^encryption\s+aes\s+\d+$",
        r"^hash\s+\S+$",
        r"^authentication\s+pre-share$",
        r"^group\s+\d+$",
        r"^lifetime\s+\d+$",
    ]
    return any(re.match(pattern, c) for pattern in patterns)


def is_crypto_map_command(c: str) -> bool:
    patterns = [
        r"^set\s+peer\s+\d+\.\d+\.\d+\.\d+$",
        r"^set\s+transform-set\s+\S+$",
        r"^set\s+pfs\s+group\d+$",
        r"^match\s+address\s+\d+$",
    ]
    return any(re.match(pattern, c) for pattern in patterns)


def simulate_cli_command(state: Dict[str, Any], command: str, scenario: Dict[str, Any]) -> Tuple[bool, str]:
    """Valide une commande selon le mode IOS courant et modifie l'état si nécessaire."""
    c = compact(command)
    mode = state.get("mode", "user")

    if c in {"", "?"}:
        return True, "Commandes utiles : enable, configure terminal, interface, vlan, router ospf, exit, end, show ..."

    if c == "enable" and mode == "user":
        state["mode"] = "privileged"
        return True, ""

    if c in {"disable"} and mode == "privileged":
        state["mode"] = "user"
        return True, ""

    if c in {"exit", "logout"}:
        if mode == "user":
            return True, "Connection closed."
        if mode == "privileged":
            state["mode"] = "user"
        elif mode in {"interface", "vlan", "router", "crypto-isakmp", "crypto-map"}:
            state["mode"] = "config"
        elif mode == "config":
            state["mode"] = "privileged"
        return True, ""

    if c in {"end", "^z"} and mode in {"config", "interface", "vlan", "router", "crypto-isakmp", "crypto-map"}:
        state["mode"] = "privileged"
        return True, ""

    if c in {"configure terminal", "conf t"} and mode == "privileged":
        state["mode"] = "config"
        return True, "Enter configuration commands, one per line.  End with CNTL/Z."

    if c.startswith("show ") and mode == "privileged":
        return True, fake_show_output(c, scenario)

    if c.startswith("do show ") and mode in {"config", "interface", "vlan", "router", "crypto-isakmp", "crypto-map"}:
        return True, fake_show_output(c, scenario)

    if c in {"write memory", "wr", "copy running-config startup-config", "copy run start"} and mode == "privileged":
        return True, "Building configuration...\n[OK]"

    if mode == "config":
        if re.match(r"^vlan\s+\d+(?:\s*,\s*\d+)*$", c):
            state["mode"] = "vlan"
            state["last_vlan"] = c.split(maxsplit=1)[1]
            return True, ""
        if re.match(r"^interface\s+\S+$", c):
            state["mode"] = "interface"
            state["last_interface"] = c.split(maxsplit=1)[1]
            return True, ""
        if re.match(r"^router\s+ospf\s+\d+$", c):
            state["mode"] = "router"
            state["last_router"] = c
            return True, ""
        if re.match(r"^crypto\s+isakmp\s+policy\s+\d+$", c):
            state["mode"] = "crypto-isakmp"
            return True, ""
        if re.match(r"^crypto\s+map\s+\S+\s+\d+\s+ipsec-isakmp$", c):
            state["mode"] = "crypto-map"
            return True, ""
        if is_global_config_command(c):
            return True, ""

    if mode == "vlan":
        if re.match(r"^name\s+\S+", c):
            return True, ""
        if re.match(r"^vlan\s+\d+(?:\s*,\s*\d+)*$", c):
            state["last_vlan"] = c.split(maxsplit=1)[1]
            return True, ""

    if mode == "interface":
        if re.match(r"^interface\s+\S+$", c):
            state["last_interface"] = c.split(maxsplit=1)[1]
            return True, ""
        if is_interface_command(c):
            return True, ""

    if mode == "router":
        if re.match(r"^router\s+ospf\s+\d+$", c):
            state["last_router"] = c
            return True, ""
        if is_router_command(c):
            return True, ""

    if mode == "crypto-isakmp":
        if re.match(r"^crypto\s+isakmp\s+policy\s+\d+$", c):
            state["mode"] = "crypto-isakmp"
            return True, ""
        if is_isakmp_command(c):
            return True, ""

    if mode == "crypto-map":
        if re.match(r"^crypto\s+map\s+\S+\s+\d+\s+ipsec-isakmp$", c):
            state["mode"] = "crypto-map"
            return True, ""
        if is_crypto_map_command(c):
            return True, ""

    return False, invalid_output(command)


def sync_cli_answer(scenario_id: str) -> None:
    state = st.session_state.get(cli_state_key(scenario_id))
    if state:
        st.session_state[scenario_id] = "\n".join(state.get("accepted_lines", []))


def submit_cli_command(scenario_id: str) -> None:
    scenario = SCENARIO_BY_ID[scenario_id]
    key = cli_state_key(scenario_id)
    input_key = cli_input_key(scenario_id)
    if key not in st.session_state:
        st.session_state[key] = new_cli_state(scenario["device"])
    state = st.session_state[key]

    raw = st.session_state.get(input_key, "")
    command = strip_entered_prompt(raw)
    if not command:
        st.session_state[input_key] = ""
        return

    old_prompt = prompt_for(state)
    ok, output = simulate_cli_command(state, command, scenario)

    state["history"].append({"prompt": old_prompt, "command": command, "output": output, "ok": ok})
    if ok:
        state["accepted_lines"].append(f"{old_prompt} {command}")

    st.session_state[key] = state
    sync_cli_answer(scenario_id)
    st.session_state[input_key] = ""


def reset_cli(scenario_id: str) -> None:
    scenario = SCENARIO_BY_ID[scenario_id]
    st.session_state[cli_state_key(scenario_id)] = new_cli_state(scenario["device"])
    st.session_state[cli_input_key(scenario_id)] = ""
    st.session_state[scenario_id] = ""


def terminal_text(state: Dict[str, Any]) -> str:
    if not state.get("history"):
        return "-- Terminal Cisco IOS simulé --\nTapez enable puis appuyez sur Entrée."
    lines: List[str] = []
    for item in state.get("history", []):
        lines.append(f"{item['prompt']} {item['command']}")
        if item.get("output"):
            lines.append(str(item["output"]))
    return "\n".join(lines)


def render_cli_terminal(scenario: Dict[str, Any]) -> None:
    scenario_id = scenario["id"]
    if cli_state_key(scenario_id) not in st.session_state:
        reset_cli(scenario_id)
    state = st.session_state[cli_state_key(scenario_id)]
    current_prompt = prompt_for(state)

    st.markdown(
        f'<div class="cli-screen">{html.escape(terminal_text(state))}\n{html.escape(current_prompt)} </div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="cli-help">Saisissez uniquement la commande après le prompt, puis appuyez sur Entrée. Les prompts collés comme <code>R1&gt; enable</code> sont aussi acceptés.</div>', unsafe_allow_html=True)
    col_prompt, col_input, col_reset = st.columns([1.25, 5, 1.35])
    with col_prompt:
        st.markdown(f'<div class="cli-prompt">{html.escape(current_prompt)}</div>', unsafe_allow_html=True)
    with col_input:
        st.text_input(
            f"Commande {scenario['device']}",
            key=cli_input_key(scenario_id),
            placeholder="Exemple : enable",
            label_visibility="collapsed",
            on_change=submit_cli_command,
            args=(scenario_id,),
        )
    with col_reset:
        st.button("Réinitialiser", key=f"{scenario_id}_reset", on_click=reset_cli, args=(scenario_id,), use_container_width=True)

    show_accepted = st.checkbox(
        "Afficher les commandes validées qui seront corrigées",
        key=f"{scenario_id}_show_accepted_commands",
    )
    if show_accepted:
        accepted = st.session_state.get(scenario_id, "")
        st.code(accepted if accepted else "Aucune commande validée pour le moment.", language="text")


# -----------------------------------------------------------------------------
# Rapport
# -----------------------------------------------------------------------------
def make_report(student_name: str, class_name: str, scores: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "etudiant": student_name,
        "classe": class_name,
        "date_correction": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score_total": scores.get("total", 0),
        "score_cours": scores.get("course_total", 0),
        "score_cli": scores.get("cli_total", 0),
        "details": scores,
    }


def report_to_csv(report: Dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Etudiant", "Classe", "Date", "Score total", "Cours", "CLI"])
    writer.writerow([
        report["etudiant"],
        report["classe"],
        report["date_correction"],
        report["score_total"],
        report["score_cours"],
        report["score_cli"],
    ])
    writer.writerow([])
    writer.writerow(["Section", "Question/Scénario", "Score", "Max", "Commentaires"])
    for row in report["details"].get("rows", []):
        writer.writerow([row.get("section"), row.get("item"), row.get("score"), row.get("max"), row.get("comment", "")])
    return output.getvalue()


# -----------------------------------------------------------------------------
# Interface Streamlit
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">🛡️ Examen Réseaux & Sécurité Cisco</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Barème total : <b>60 points</b> — Questions de cours + scénarios de configuration en mode commande Cisco interactif.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Paramètres")
    student_name = st.text_input("Nom de l'étudiant", value="")
    class_name = st.text_input("Classe / groupe", value="")
    st.divider()
    st.markdown("### Barème")
    st.write("• Questions de cours : 20 pts")
    st.write("• Scénarios Cisco CLI : 40 pts")
    st.divider()
    correction_visible = st.checkbox("Afficher les corrections après soumission", value=True)
    st.caption("La correction des réponses courtes est automatique et indicative : l'enseignant peut ajuster si nécessaire.")

st.info(
    "Consigne générale : répondez sans utiliser les supports. Dans les scénarios CLI, tapez une commande puis Entrée : le prompt Cisco change automatiquement, par exemple `R1> enable` puis `R1#`. Les commandes invalides affichent un message d'erreur et ne sont pas comptées dans la correction."
)

tab_course, tab_cli, tab_submit = st.tabs(["Partie A — Questions de cours / 20", "Partie B — Scénarios Cisco CLI / 40", "Correction et export"])

with tab_course:
    st.subheader("Partie A — Questions de cours : 20 points")
    st.markdown('<div class="rubric">12 QCM × 1 point = 12 points. 4 questions courtes × 2 points = 8 points.</div>', unsafe_allow_html=True)

    st.markdown("### A1. QCM")
    for idx, q in enumerate(QCM, start=1):
        st.radio(
            f"{idx}. [{q['theme']}] {q['question']} ({q['points']} pt)",
            options=["— Choisir —"] + q["options"],
            key=q["id"],
        )

    st.markdown("### A2. Questions à réponse courte")
    for idx, q in enumerate(SHORT_QUESTIONS, start=1):
        st.text_area(
            f"{idx}. [{q['theme']}] {q['question']} ({q['points']} pts)",
            height=100,
            key=q["id"],
            placeholder="Réponse structurée en 3 à 6 lignes...",
        )

with tab_cli:
    st.subheader("Partie B — Scénarios de configuration Cisco IOS : 40 points")
    st.markdown('<div class="rubric">4 scénarios × 5 points + 2 scénarios × 10 points (MPLS & VPN IPsec). Utilisez le terminal interactif : chaque commande validée fait évoluer le prompt comme sur un équipement Cisco.</div>', unsafe_allow_html=True)

    for scenario in SCENARIOS:
        st.markdown(f"### {scenario['title']} — {scenario['points']} pts")
        st.write(scenario["context"])
        st.markdown("<span class='small-note'>Terminal Cisco simulé :</span>", unsafe_allow_html=True)
        render_cli_terminal(scenario)
        st.markdown("---")

with tab_submit:
    st.subheader("Correction automatique et export")
    submitted = st.button("✅ Corriger l'examen", type="primary", use_container_width=True)

    if submitted:
        rows: List[Dict[str, Any]] = []
        course_total = 0.0
        cli_total = 0.0

        st.markdown("## Résultats")
        if not student_name.strip():
            st.warning("Nom de l'étudiant non renseigné. Le rapport sera généré sans nom.")

        st.markdown("### A1. QCM")
        qcm_rows = []
        for idx, q in enumerate(QCM, start=1):
            user_answer = st.session_state.get(q["id"], "— Choisir —")
            ok = user_answer == q["answer"]
            pts = float(q["points"]) if ok else 0.0
            course_total += pts
            qcm_rows.append({"N°": idx, "Thème": q["theme"], "Réponse": user_answer, "Score": pts, "Max": q["points"], "Résultat": "✅" if ok else "❌"})
            rows.append({"section": "QCM", "item": f"QCM {idx} — {q['theme']}", "score": pts, "max": q["points"], "comment": "Correct" if ok else f"Réponse attendue : {q['answer']}"})
        st.dataframe(pd.DataFrame(qcm_rows), use_container_width=True, hide_index=True)

        st.markdown("### A2. Questions courtes")
        short_rows = []
        for idx, q in enumerate(SHORT_QUESTIONS, start=1):
            user_answer = st.session_state.get(q["id"], "") or ""
            pts, nb_kw, found = grade_short_answer(user_answer, q)
            course_total += pts
            comment = f"Mots-clés trouvés : {', '.join(found) if found else 'aucun'}"
            short_rows.append({"N°": idx, "Thème": q["theme"], "Score": pts, "Max": q["points"], "Mots-clés": nb_kw})
            rows.append({"section": "Question courte", "item": f"Question courte {idx} — {q['theme']}", "score": pts, "max": q["points"], "comment": comment})
        st.dataframe(pd.DataFrame(short_rows), use_container_width=True, hide_index=True)

        if correction_visible:
            with st.expander("Voir les réponses attendues aux questions courtes"):
                for idx, q in enumerate(SHORT_QUESTIONS, start=1):
                    st.markdown(f"**{idx}. {q['theme']}** — {q['solution']}")

        st.markdown("### B. Scénarios Cisco CLI")
        for scenario in SCENARIOS:
            sync_cli_answer(scenario["id"])
            answer = st.session_state.get(scenario["id"], "") or ""
            sc_score, details = grade_cli(answer, scenario)
            cli_total += sc_score
            st.markdown(f"#### {scenario['title']} — {sc_score}/{scenario['points']} pts")
            st.dataframe(pd.DataFrame(details), use_container_width=True, hide_index=True)
            rows.append({"section": "CLI", "item": scenario["title"], "score": sc_score, "max": scenario["points"], "comment": "Voir détail par critère dans l'application"})
            with st.expander(f"Commandes acceptées — {scenario['title']}"):
                st.code(answer if answer else "Aucune commande validée.", language="text")
            if correction_visible:
                with st.expander(f"Correction type — {scenario['title']}"):
                    st.code(scenario["solution"], language="text")

        total = round(course_total + cli_total, 2)
        course_total = round(course_total, 2)
        cli_total = round(cli_total, 2)

        st.markdown(
            f"""
            <div class="score-box">
                <h2>Score final : {total}/60</h2>
                <p><b>Questions de cours :</b> {course_total}/20 &nbsp; | &nbsp; <b>Scénarios Cisco CLI :</b> {cli_total}/40</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        scores = {"total": total, "course_total": course_total, "cli_total": cli_total, "rows": rows}
        report = make_report(student_name, class_name, scores)
        st.session_state["last_report"] = report

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Télécharger le rapport JSON",
                data=json.dumps(report, ensure_ascii=False, indent=2),
                file_name=f"rapport_examen_{student_name or 'etudiant'}.json",
                mime="application/json",
                use_container_width=True,
            )
        with col2:
            st.download_button(
                "⬇️ Télécharger le rapport CSV",
                data=report_to_csv(report),
                file_name=f"rapport_examen_{student_name or 'etudiant'}.csv",
                mime="text/csv",
                use_container_width=True,
            )
    else:
        st.markdown("Cliquez sur **Corriger l'examen** après avoir répondu aux questions et réalisé les configurations Cisco dans les terminaux interactifs.")

st.divider()
st.caption("Examen généré pour évaluer les bases de routage, switching/VLAN/STP, NAT, ACL Cisco, cryptographie et PKI. Barème total : 60 points.")
