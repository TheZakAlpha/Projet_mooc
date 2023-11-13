
#étape 1
import json 

def lire_fichier(fichier) :
    import json 
    with open(fichier) as mon_fichier :
        data = json.load(mon_fichier)
    mon_fichier.close()
    return data





def construire_mapping(personnes):
    mapping = {}
    for dic in personnes :
            nom = dic['nom']
            mapping[nom]= dic['enfants']
    return mapping


#étape 2


def compter_descendants_et_profondeur(nom, mapping, cache_compte={}, cache_profondeur={}, generation_courante=1):
    if nom in cache_compte and cache_profondeur:
        return {"name": nom, "total_descendants": cache_compte[nom], "générations": cache_profondeur[nom]}
    total_descendants = 0
    generation_courante = 0
    if nom in mapping:
        for enfant in mapping[nom]:
            child = compter_descendants_et_profondeur(enfant, mapping, cache_compte, cache_profondeur, generation_courante )
            total_descendants += 1 + child["total_descendants"]
            generation_courante = max(generation_courante, child["générations"]+1)
    cache_compte[nom] = total_descendants
    cache_profondeur[nom] = generation_courante
    return {"name": nom, "total_descendants": cache_compte[nom], "générations": cache_profondeur[nom]}
         

data = lire_fichier('projet_personnes.json')
mapping = construire_mapping(data)
metriques = []






#étape 3





def tri_par_selection(personnes,nb_desc_ou_gen) :
    for i in range(len(personnes)):
        minimum = i
        for j in range(i + 1, len(personnes)):
            if nb_desc_ou_gen == "nb_desc":
                if personnes[j]["total_descendants"] < personnes[minimum]["total_descendants"]:
                    minimum = j
                elif personnes[j]["total_descendants"] == personnes[minimum]["total_descendants"]:
                    if personnes[j]["name"] < personnes[minimum]["name"]:
                        minimum = j
            elif nb_desc_ou_gen == "gen":
                if personnes[j]["générations"] < personnes[minimum]["générations"]:
                    minimum = j
                elif personnes[j]["générations"] == personnes[minimum]["générations"]:
                    if personnes[j]["name"] < personnes[minimum]["name"]:
                        minimum = j
        personnes[i], personnes[minimum] = personnes[minimum], personnes[i]
    



#étape 4


def compter_descendants_et_profondeur_2(nom, mapping, cache_compte={}, cache_profondeur={}, generation_courante=1):
    if nom in cache_compte and cache_profondeur:
        return {"name": nom, "total_descendants": cache_compte[nom], "générations": cache_profondeur[nom]}
    total_descendants = 0
    fraterie = []
    
    generation_courante = 0
    if nom in mapping:
        for enfant in mapping[nom]:
            child = compter_descendants_et_profondeur_2(enfant, mapping, cache_compte, cache_profondeur, generation_courante )
            total_descendants += 1 + child["total_descendants"]
            generation_courante = max(generation_courante, child["générations"]+1)
        for parents in mapping :
            enfants = mapping.get(parents)
            for enf in enfants:
                if nom != enf and enf not in fraterie :
                    fraterie.append(enf)
        
        if fraterie != [] :
            for i in range(len(fraterie)) :
                if fraterie[i] != nom :
                    a = fraterie[i]
                    freres_soeurs= compter_descendants_et_profondeur(a, mapping, cache_compte, cache_profondeur, generation_courante )
                    generation_courante = max(generation_courante, freres_soeurs["générations"])
        for parents in mapping:
            if nom in mapping[parents] :
                for i in range(len(mapping[parents])):
                    if nom==mapping[parents][i]:
                        parent = parents
                        metriques_parents = compter_descendants_et_profondeur(parent, mapping, cache_compte, cache_profondeur, generation_courante )
                        generation_courante = metriques_parents["générations"]-1    
    cache_compte[nom] = total_descendants
    cache_profondeur[nom] = generation_courante
    return {"name": nom, "total_descendants": cache_compte[nom], "générations": cache_profondeur[nom]}
 


print(compter_descendants_et_profondeur_2("Byron", mapping, cache_compte={}, cache_profondeur={}, generation_courante=1))

for personne in mapping :  
    """applique la fonction compter_descendants_et_profondeur a tous les noms du fichier projet_personnes
    et les stock dans metriques"""
    metriques.append(compter_descendants_et_profondeur_2(personne, mapping, cache_compte={}, cache_profondeur={}, generation_courante=1))
json_metriques = json.dumps(metriques,indent=2) #transforme metriques en un string compatible avec les manipulations json
with open('metriques.json','w') as fichier_metriques :
   #crée le fichier métriques.json et y écrit les résultats stoqués dans metriques
   fichier_metriques.write(json_metriques)
