import pandas as pd
from itertools import combinations

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
        
        self.butter = CoDom('BEL', 'butter')

        self.fire = CoDom('FR', 'fire')

        self.orangeDream = CoDom('OD', 'orange dream')
        
        self.spider = Dom('SP', 'spider')
        
        self.leopard = Dom('LP', 'leopard')

        self.banana = CoDom('BN', 'banana')

        self.desertGhost = Res('DG', 'desert ghost') 


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
        self.process_super()
        self.pos_offspring = self.get_pos_offspring()

    def get_pos_offspring(self):
        output = sum([list(map(list, combinations(self.male_genes+self.female_genes, i))) for i in range(len(self.male_genes+self.female_genes) + 1)], [])
        if not self.female_super is []:
            for gene in self.female_super:
                for l in output:
                    l.append(gene)
        if not self.male_super is []:
            for gene in self.male_super:
                for l in output:
                    l.append(gene)
        return output

    def process_super(self):
        for gene in self.female.genes:
            if gene.complex in self.female.super:
                self.female_super.append(gene.name)
                self.female_super = list(set(self.female_super))
                self.female_genes.remove(gene.name) 
        for gene in self.male.genes:
            if gene.complex in self.male.super:
                self.male_super.append(gene.name)
                self.male_super = list(set(self.male_super))
                self.male_genes.remove(gene.name) 
        
genes = Genes()

Male = Snake('male', genes.asphalt, genes.asphalt, genes.banana)
Female = Snake('female', genes.yellowBelly, genes.orangeDream, genes.fire, genes.leopard)

pair = Pairing(Male, Female)
pair.get_pos_offspring()
df = pd.DataFrame(pair.pos_offspring)
print(f'Possible Offspring: \n{df}')
