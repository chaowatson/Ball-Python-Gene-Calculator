import pandas as pd
from itertools import combinations
from copy import deepcopy

class Gene:
    pass


class CoDom(Gene):
    def __init__(self, comp=None, name=None):
        self.complex = comp
        self.name = name


class Dom(Gene):
    def __init__(self, comp=None, name=None):
        self.complex = comp
        self.name = name


class Res(Gene):
    def __init__(self, comp = None, name=None):
        self.complex = comp
        self.name = name


class Genes:
    def __init__(self):
        
        self.yellowBelly = CoDom('YB', 'yellow belly')
        self.gravel = CoDom('YB', 'gravel')
        self.asphalt = CoDom('YB', 'asphalt')
        self.specter = CoDom('YB', 'specter')
        
        self.butter = CoDom('BEL', 'butter')
        self.mojave = CoDom('BEL', 'mojave')
        self.bamboo = CoDom('BEL', 'bamboo')
        self.special = CoDom('BEL', 'special')

        self.fire = CoDom('FR', 'fire')

        self.orangeDream = CoDom('OD', 'orange dream')
        self.enchi = CoDom('EC', 'enchi')
        self.pastel = CoDom('PT', 'pastel')
        self.mario = CoDom('MR', 'mario')  
        self.spider = Dom('SP', 'spider')
        
        self.leopard = Dom('LP', 'leopard')

        self.banana = CoDom('BN', 'banana')

        self.het_desertGhost = Res('DG', 'het_desert ghost') 
        

class Snake:
    def __init__(self, gender, *genes):
        correct_genders = ['male', 'female']
        if not gender in correct_genders:
            raise Exception(f'Unknown Gender: {gender}')
        self.gender = gender
        self.genes = []
        self.genes_name = []
        self.super = []
        self.pos_super = []
        for gene in genes:
            if not isinstance(gene, Gene):
                raise Exception(f'Unknown Gene: {gene}')
            if gene.complex in self.super:
                raise Exception(f'Too many Genes in same complex: {gene.complex}')
            if gene.complex in self.pos_super:
                self.super.append(gene.complex)
            self.pos_super.append(gene.complex)
            self.genes_name.append(gene.name)
            self.genes.append(gene)
        print(f'Snake Created\n    Gender: {self.gender}\n    Genes: {", ".join(self.genes_name)}\n')


class Pairing:
    def __init__(self, male, female):
        if not isinstance(male, Snake):
            raise Exception(f'A \"Snake\" object must be create first: {male}')
        if not isinstance(female, Snake):
            raise Exception(f'A \"Snake\" object must be create first: {female}')
        self.male = male
        self.female = female
        
        print(f'Paring created\n    Male: {", ".join(male.genes_name)}\n    Female: {", ".join(female.genes_name)}\n')
        self.male_genes = male.genes_name
        self.female_genes = female.genes_name
        self.female_super = []
        self.male_super = []
        self.super = []
        self.process_super()
        self.pos_offspring = self.get_pos_offspring()

    def get_pos_offspring(self):
        output = sum([list(map(list, combinations(self.male_genes+self.female_genes, i))) for i in range(len(self.male_genes+self.female_genes) + 1)], [])
        if not self.female.super is []:
            for comp in self.female.super:
                origin_out = deepcopy(output)
                output = []
                if not self.female_super is []:
                    for gene in self.female_super:
                        if gene.complex == comp:
                            temp = deepcopy(origin_out)
                            for l in temp:
                                l.append(gene.name)
                            output = output + temp
        if not self.male.super is []:
            for comp in self.male.super:
                origin_out = deepcopy(output)
                output = []
                if not self.male_super is []:
                    for gene in self.male_super:
                        if gene.complex == comp:
                            temp = deepcopy(origin_out)
                            for l in temp:
                                l.append(gene.name)
                            output = output + temp
        [offspring.sort() for offspring in output]
        out = []
        [out.append(offspring) for offspring in output if offspring not in out]
        return out

    def process_super(self):
        for gene in self.female.genes:
            if gene.complex in self.female.super:
                self.female_super.append(gene)
                self.female_genes.remove(gene.name) 
                
        for gene in self.male.genes:
            if gene.complex in self.male.super:
                self.male_super.append(gene)
                self.male_genes.remove(gene.name) 

    def cal_possibility(self):
        self.super = self.male_super + self.female_super
        min_pos = 1 / (2 ** max([len(amount) for amount in pair.pos_offspring]))
        for offspring in self.pos_offspring:
            offspring.insert(0, min_pos)
            repeat = []
            for gene in offspring:
                if gene in [gene.name for gene in self.super]:
                    for _gene in self.super:
                        if gene == _gene.name:
                            if 2 == [gene.name for gene in self.male_super].count(_gene.name):
                                if not gene in repeat:
                                    offspring[0] = offspring[0]*2
                                    break
                            elif 2 == [gene.name for gene in self.female_super].count(_gene.name):
                                if not gene in repeat:
                                    offspring[0] = offspring[0]*2
                                    break
                            elif gene in [gene.name for gene in self.male_super]:
                                if gene in [gene.name for gene in self.female_super]:
                                    if not gene in repeat:
                                        if not _gene.complex in repeat:
                                            offspring[0] = offspring[0]*2
                                            break
                                    else:
                                        offspring[0] = offspring[0]/2
                                        break
                elif gene in self.male_genes:
                    if gene in self.female_genes:
                        if not gene in repeat:
                            offspring[0] = offspring[0]*2
                        else:
                            offspring[0] = offspring[0]/2
                if type(gene) is str:
                    if gene in [gene.name for gene in self.super]:
                        for _gene in self.super:
                            if gene == _gene.name:
                                repeat.append(_gene.complex)
                                break
                    repeat.append(gene)

        self.pos_offspring = sorted(self.pos_offspring, key = lambda x: x[0], reverse=True)        

genes = Genes()

Male = Snake('male', genes.mario, genes.het_desertGhost, genes.het_desertGhost)
Female = Snake('female', genes.pastel, genes.pastel, genes.het_desertGhost)

pair = Pairing(Male, Female)
pair.get_pos_offspring()
#print(pair.pos_offspring)
pair.cal_possibility()
df = pd.DataFrame(pair.pos_offspring)
print(f'Possible Offsprings\n{df}')
df.to_csv('MarioDG_SuperPastelhetDG.csv')
