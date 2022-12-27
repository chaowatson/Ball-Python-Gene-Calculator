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
        
        self.orangeDream = CoDom(None, 'orange dream')
        
        self.spider = Dom('SP', 'spider')
        
        self.desertGhost = Res(None, 'desert ghost') 


class Snake:
    def __init__(self, gender, *genes):
        correct_genders = ['male', 'female']
        if not gender in correct_genders:
            raise Exception(f'Unknown Gender: {gender}')
        self.gender = gender
        self.genes = []
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
            self.genes.append(gene.name)
        if len(self.super) is 0: 
            self.genes_to_provide = len(self.genes)*2
        else:
            self.genes_to_provide = (len(self.genes)-len(self.super))*2
        print(f'Snake Created\n    Gender: {self.gender}\n    Genes: {", ".join(self.genes)}\n')


class Pairing:
    def __init__(self, male, female):
        if not isinstance(male, Snake):
            raise Exception(f'A \"Snake\" object must be create first: {male}')
        if not isinstance(female, Snake):
            raise Exception(f'A \"Snake\" object must be create first: {female}')
        self.male = male
        self.female = female
        
        print(f'Paring created\n    Male: {", ".join(male.genes)}\n    Female: {", ".join(female.genes)}\n')

genes = Genes()

Male = Snake('male', genes.asphalt, genes.orangeDream)
Female = Snake('female', genes.yellowBelly, genes.yellowBelly)

pair = Pairing(Male, Female)
