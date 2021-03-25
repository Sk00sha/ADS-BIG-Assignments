import sys
import numpy as np
import pandas as pd
#reprezentacia objektov v programe a samotnej matici,len na vizualizaciu :)
def make_visual(roots):
    matrix_numpy=[]
    for item in roots:
        help_matrix=[]
        for row_data in item:
            if row_data is None:
                help_matrix.append("000")
            else:
                help_matrix.append("Obj")
        matrix_numpy.append(help_matrix)
    return_array=pd.DataFrame(matrix_numpy)
    return_array.to_csv('matrix.csv')
    print(return_array.head(5))

#obycajne nacitanie dat do dict.
def load_data(name):
    try:
        with open(name) as textFile:
            lines = [line.split(' ') for line in textFile]
        dictionary={}
        freq_sum=0
        for item in lines:
            string=item[1].splitlines()
            freq_sum=freq_sum+int(item[0])
            dictionary[string[0]]=int(item[0])
        return dictionary,freq_sum
    except:
        print("Wrong input")

#funkcia dumpuje 3 listy
def dump_lists():
    return list(),list(),list()



#p_q kalkulacia<nepouzivam, nahradil ju calculate_probability() funkcia
def calc_q_p(freq):
    flag=0
    if(freq>50000):
        p_i=frekvencia/freq_vsetky_slova
        q_i=freq_dummy_klucov/freq_vsetky_slova
    else:
        freq_dummy_klucov=freq_dummy_klucov+frekvencia
    return None
    #kalkulacie podla zadania v PDF
def required_calculations(freq,freq_dummy,freq_sum):
    return freq/freq_sum,freq_dummy/freq_sum

#source---> https://www.radford.edu/~nokie/classes/360/dp-opt-bst.html
#Podla knihy Cormen
def calculate_probabilityandsave(dict,freq_sum): 
    pravdepodobnosti,p_predosle,value_predosle=dump_lists()
    freq_vsetky_slova=freq_sum
    freq_dummy_klucov=0
    poradie_kluca=0
    p_predosle.append(0.0)
    value_predosle.append("")
    for key in sorted(dict): #pointa je prejst dictionary a zobrat len data 
        frekvencia=dict[key]
        if (frekvencia>50000):
            p_i,q_i=required_calculations(frekvencia,freq_dummy_klucov,freq_sum)
            freq_dummy_klucov=0
            pravdepodobnosti.append({"poradie_kluca":poradie_kluca,"predosle_p":p_predosle.pop(),"q_i":q_i,"value_predosle":value_predosle.pop()})
            poradie_kluca+=1
            p_predosle.append(p_i)
            value_predosle.append(key)
        else:
            freq_dummy_klucov=freq_dummy_klucov+frekvencia
    pravdepodobnosti.append({"poradie_kluca":poradie_kluca,"predosle_p":p_predosle.pop(),"q_i":freq_dummy_klucov/freq_vsetky_slova,"value_predosle":value_predosle.pop()})
    return pravdepodobnosti


#funkcia na vytvorenie binarneho stromu
#source-----> https://www.tutorialspoint.com/design_and_analysis_of_algorithms/design_and_analysis_of_algorithms_optimal_cost_binary_search_trees.htm
def vytvorbinarny_strom(table_pravdepodobnosti,dlzka,koren,pravdepodobnosti,Ceny):
    Max = sys.maxsize
    for i in range(1,dlzka+2):
        pravdepodobnosti[i][i-1]=table_pravdepodobnosti[i-1]["q_i"]#dummy kluc vyberame
        Ceny[i][i-1]=table_pravdepodobnosti[i-1]["q_i"]
    for j in range(1,dlzka+1):
        for i in range(1,dlzka-j+2):
            Ceny[i][j+i-1]=sys.maxsize
           # print(j+i-1)
            pravdepodobnosti[i][j+i-1]=pravdepodobnosti[i][j+i-2]+table_pravdepodobnosti[j+i-1]["predosle_p"]+table_pravdepodobnosti[j+i-1]["q_i"]
            for l in range(i,j+i):
                ocakavana_cena=Ceny[i][l-1] + Ceny[l+1][j+i-1] + pravdepodobnosti[i][j+i-1]
                if(ocakavana_cena<Ceny[i][j+i-1]):
                    Ceny[i][j+i-1]=ocakavana_cena
                    koren[i][j+i-1]=table_pravdepodobnosti[l]
                    
    return koren,koren[1][len(koren)-1]["value_predosle"],Ceny
    
#tato funkcia pomaha pri korigovani ci treba v strome do lava alebo do prava
def string_comparing(a,b):
    if a==b:
        return 0
    if a>b: 
        return 1
    else:
        return -1

#rekurzivna funkcia hlada v strome ci su v nom slova
#source->https://www.tutorialspoint.com/data_structures_algorithms/tree_data_structure.htm
#source2->https://www.geeksforgeeks.org/binary-search-tree-set-1-search-and-insertion/

def check_string(string,start,koniec,korene):
    global porovnania#premenna porovnania je global aby bol k pocitadlu lahky pristup
    if (start > koniec):#start nemoze byt viac ako koniec
        return None
    if(koniec <1):#ak je koniec menej ako 1 tak logicky nemozeme hladat v strome, ktory zacina na 1
        return None
    if (korene[start][koniec]==None):#nenasli sme hodnotu, teda je tam None padding 
        inc_comparison()
        return None
    string_pociatok=korene[start][koniec]["value_predosle"]#pociatocny string sa vracia z korena ak sme nenarazili na hdnotu None
    print("-"*porovnania,string_pociatok)
    IDroot=korene[start][koniec]["poradie_kluca"]#poradie kluca odpovedajucej [value_predosle]> je to hodnota na mieste korena
    if (string_pociatok==None or len(string_pociatok)==0 or string_pociatok==string):  #nenasli sme hodnotu, teda je tam None padding 
        inc_comparison()
        return string_pociatok
    if(string_comparing(string,string_pociatok)<0):
        inc_comparison()
        IDroot=IDroot-1
        return check_string(string,start,IDroot,korene)
    inc_comparison()
    IDroot=IDroot+1
    return check_string(string,IDroot,koniec,korene)

#riadiaca funkcia pre check_string f()
def pocet_porovnani(string,roots):
    global porovnania
    if len(string)>0:
        najdene=check_string(string,1,len(roots)-1,roots)#odchytavame navratove hodnoty z rekurz. funkcie
        if najdene==None: #pri zlyhani checkstring vracia None a preto mame porovnanie s None
            print(string," SA NENACHADZA V STROME")
            print("Pocet porovnani je: ",porovnania)
        else:
            print("SLOVO >",string," SA NACHADZA NA UROVNI: ",porovnania)
    return porovnania


def inc_comparison():
    global porovnania
    porovnania+=1
                


                                
                    
porovnania=0

def main():
    dictionary,freq=load_data('dictionary.txt')
    probab=calculate_probabilityandsave(dictionary,freq-1)
    #print(probab)
    dlzka=len(probab)-1
    #padding 2D matrixu pre pouzitie na naplnenie stromu
    koren=[[None for x in range((dlzka)+1)] for y in range((dlzka)+1)]  
    pravdepodobnosti=[[None for x in range((dlzka)+1)] for y in range((dlzka)+2)] 
    Ceny=[[None for x in range((dlzka)+1)] for y in range((dlzka)+2)] 
    #do korenov sa vracia 2D Matrix roots
    kluce=list(dictionary.keys())

    
    korene,koren_stromu,ceny=vytvorbinarny_strom(probab,dlzka,koren,pravdepodobnosti,Ceny)
    #make_visual(korene)
    print(f"Cena optimálneho stromu je: {ceny[1][151]}")
    
    input_na_word = input("Zadaj slovo na porovnanie:")
    print("KOREN STROMU JE: ",koren_stromu)
    pocet_porovnani(input_na_word,korene)
    
   
if __name__ == "__main__":
    main()





        
 
