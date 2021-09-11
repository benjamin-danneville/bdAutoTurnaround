######################################################
## BENJAMIN DANNEVILLE                              ##
## bdGenerator                                      ##
##                                                  ##
## Version : 0.1.3                                  ##
## Date : Septembre 2021                            ##
## Website : https://www.benjamindanneville.com/    ##
######################################################

import maya.cmds as cmds
import maya.mel as mel
import random

geoDuplicatedObj_grp_list =[]

#Vient enregistrer les items selectionner dans une liste
selection_list = []

def Generator(reset):
        #Append global
    #if selection_list == []:
    if reset == 1:
        selection_list[:] = []
        selection = cmds.ls(sl=True)
        for i in range(len(selection)):
            selection_list.append(selection[i])
    else:
        selection = selection_list

    ##############
    ## Variable ##
    ##############

    #Liste que l'on va remplir de nos groupes de blocking que l'on veut remplacer, et des groupes de configurations de locator
    config_grp_list = []
    geo_grp_list = []
    
    #########################
    ## TRIE DE MES GROUPES ##
    #########################

    #Boucle autant de fois que de groupe selectionner
    for i in range(len(selection)):
        #Si la shape du premier objet de mon groupe est un locator, alors on ajoute ce groupe dans la liste de groupe de config
        if (cmds.nodeType(cmds.listRelatives(cmds.listRelatives(selection[i])[0])[0]) == "locator"):
            config_grp_list.append(selection[i])
        #Si la shape du premier objet de mon groupe est un mesh/geo , alors on ajoute ce groupe dans la liste de groupe de geo
        elif (cmds.nodeType(cmds.listRelatives(cmds.listRelatives(selection[i])[0])[0]) == "mesh"):
            geo_grp_list.append(selection[i])

    ##############################
    ## BOUCLE QUI VA TOUT FAIRE ##
    ##############################

    #Clearing list to be able to change that list
    geoDuplicatedObj_grp_list[:] = []
    #Boucle : Pour chaque groupe dans ma liste de groupe de geo/mesh
    for geo_grp in geo_grp_list:
        #On remet a 0 l'iteration afin d'avoir pour chaque groupe de geo selectionne, une nomenclature commencant au debut, et non depuis la derniere iteration du dernier groupe
        iteration = 0
        
        #Creation du groupe contenant toutes mes objets pour chaque groupe selectionne
        geoDuplicatedObj_grp = cmds.group( em=True, name=geo_grp[0:-3] + "All_grp")
        geoDuplicatedObj_grp_list.append(geoDuplicatedObj_grp)

        #Boucle : Pour chaque mesh dans mon groupe geo/mesh
        for geo in cmds.listRelatives(geo_grp):
            iteration += 1

            #Groupe pour chaque objet remplacant un objet du blocking
            obj_grp = cmds.group( em=True, name=geo_grp[0:-3] + str(iteration) + "_grp")

            #On choisit parmis les differentes configurations d'objets possibles
            random_config = random.choice(config_grp_list)

            #Boucle : Pour chaque locator dans mon groupe de configuration choisit precedemment
            for clockPart in cmds.listRelatives(random_config):
                #"locator" ici est en fait la shape de notre objet, et nous n'en voulons pas pour la suite donc nous ne le "sortons" de notre iteration, les locator sont en fait de type "transform" et leur shape de type "locator"
                if not cmds.nodeType(clockPart) == "locator" :
                    #On va chercher le nom de nos variations de modelisation, situe dans l'attr en question
                    variationObj_input = cmds.getAttr(clockPart + ".Variation_obj")
                    #on separe la str en liste pour qu'elle soit utilisable
                    variationObj_output = variationObj_input.split(",")
                    #on pC(parentConstraint) pour venir deplacer l'objet(la variation aleatoire) a l'endroit exact de notre locator de la config choisit et on delete la pC
                    randomObj_variation = random.choice(variationObj_output)   
                    duplicated = cmds.duplicate(randomObj_variation, n=randomObj_variation[0:-3] + "DUPLICATED_" + str(iteration) + "_geo")
                    cmds.parentConstraint(clockPart, duplicated, mo=False)
                    cmds.delete(duplicated[0] + "_parentConstraint1")

                    #On parent l'objet sous le groupe cree precedemment et on center pivot afin de bien pouvoir deplacer le groupe plus tard
                    cmds.parent(duplicated, obj_grp)
                    cmds.select(obj_grp)
                    mel.eval("CenterPivot;")
            #On deplace l'objet creee au niveau de l'objet du blocking que l'on veut remplacer
            cmds.parentConstraint(geo, obj_grp)
            cmds.delete(obj_grp + "_parentConstraint1")
            #On parent l'objet sous l'equivalent du groupe geo selectionne que l'on a creer en debut de boucle
            cmds.parent(obj_grp, geoDuplicatedObj_grp)

def GeneratorButton(_):
    Generator(1)

def RandomButton(_):
    cmds.delete(geoDuplicatedObj_grp_list)
    Generator(0)



bdGenerator_win = 'bdGenerator'

if cmds.window(bdGenerator_win, exists=True):
    cmds.deleteUI(bdGenerator_win)

# Start with the Window 
cmds.window(bdGenerator_win, widthHeight=(370, 170)) 
# Add a single column layout to add controls into 
cmds.columnLayout(adjustableColumn=True) 

cmds.text("\n1 - Select all the blocking groups that you want to apply Generator to", align='left')
cmds.text("2 - Select all the config groups containing the locator", align='left')
cmds.text("\n3 - Click the Generate Button !", align='left')
cmds.text("   - You can generate new seeds by clicking on random\n", align='left')

# Add controls to the Layout 
cmds.button( label="Generate", command=GeneratorButton) 
cmds.button( label="Random", command=RandomButton) 

#Credits
cmds.text("-------------------------------------------------------------------------------------------", align='left')
cmds.text("copyright Benjamin Danneville                                          licence GNU GPL", align='left')
 
# Display the window 
cmds.showWindow(bdGenerator_win)