# Examen Streamlit — Réseaux & Sécurité Cisco

Application d'examen sur **40 points** couvrant : routage, switching, VLAN, STP, NAT, ACL Cisco, cryptographie et PKI.

## Nouveauté CLI interactive

La partie Cisco CLI fonctionne comme un terminal simulé :

```text
R1> enable
R1# configure terminal
R1(config)# interface g0/0
R1(config-if)# no shutdown
R1(config-if)# end
R1# show ip route
```

L'étudiant saisit une commande, appuie sur **Entrée**, puis le prompt évolue automatiquement selon le mode Cisco IOS :

- `>` : mode utilisateur
- `#` : mode privilégié
- `(config)#` : configuration globale
- `(config-if)#` : configuration d'interface
- `(config-vlan)#` : configuration VLAN
- `(config-router)#` : configuration routage

Les commandes invalides affichent un message d'erreur et ne sont pas comptées dans la correction.

## Installation

```bash
pip install -r requirements_examen.txt
streamlit run app_examen_reseaux_securite.py
```

## Fichiers

- `app_examen_reseaux_securite.py` : application principale Streamlit.
- `requirements_examen.txt` : dépendances Python.
- `README_examen_streamlit.md` : guide d'utilisation.

## Barème

- Questions de cours : 20 points.
- Scénarios Cisco CLI : 20 points.
- Total : 40 points.

## Export

Après correction, l'enseignant peut télécharger :

- un rapport JSON ;
- un rapport CSV.
