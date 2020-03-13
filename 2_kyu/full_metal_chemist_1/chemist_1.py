# https://www.codewars.com/kata/5a27ca7ab6cfd70f9300007a

valence = {
    "H" : 1,
    "B" : 3,
    "C" : 4,
    "N" : 3,
    "O" : 2,
    "F" : 1,
    "Mg": 2,
    "P" : 3,
    "S" : 2,
    "Cl": 1,
    "Br": 1,
}

weight = {
    "H" : 1.0,
    "B" : 10.8,
    "C" : 12.0,
    "N" : 14.0,
    "O" : 16.0,
    "F" : 19.0,
    "Mg": 24.3,
    "P" : 31.0,
    "S" : 32.1,
    "Cl": 35.5,
    "Br": 80.0,
}

order = ['C', 'O', 'B', 'Br', 'Cl', 'F', 'Mg', 'N', 'P', 'S', 'H']

class UnlockedMolecule(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "UnlockedMolecule exception"

    def __str__(self):
        return self.message

class LockedMolecule(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "LockedMolecule exception"

    def __str__(self):
        return self.message

class EmptyMolecule(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "EmptyMolecule exception"

    def __str__(self):
        return self.message

class InvalidBond(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "InvalidBond exception"

    def __str__(self):
        return self.message

class Atom(object):
    
    def __init__ (self, elt, id_):
        self.element = elt
        self.id = id_
        self.bonds = []

        assert(self.element in valence.keys())
        
    def __hash__(self):      return self.id
    def __eq__(self, other): return self.id == other.id
    
    def bond(self, atom):
        if len(self.bonds) >= valence[self.element] or atom == self: raise InvalidBond()
        
        self.bonds.append(atom)

    def unbond(self, atom):
        for idx, bond in enumerate(self.bonds):
            if bond == atom:
                del self.bonds[idx]
                return

    def hydrogens(self):
        return len(list(filter(lambda atom: atom.element == "H", self.bonds)))

    def release_hydrogens(self):
        n_atoms_before = len(self.bonds)
        self.bonds = list(filter(lambda atom: atom.element != "H", self.bonds))

        n_hydrogens_released = n_atoms_before - len(self.bonds)

        return n_hydrogens_released

    def filled(self):
        return len(self.bonds) == valence[self.element]

    def fill(self, id):
        missing = valence[self.element] - len(self.bonds)
        hydrogens = []

        for hydrogen_num in range(missing):
            hydrogens.append(Atom("H", id))
            id += 1

            self.bond(hydrogens[hydrogen_num])
            hydrogens[hydrogen_num].bond(self)

        return hydrogens

    def __str__(self):
        order = ['C', 'O', 'B', 'Br', 'Cl', 'F', 'Mg', 'N', 'P', 'S', 'H']

        matched = [(order.index(atom.element), atom.id, atom) for atom in self.bonds]
        self.bonds = [ match[2] for match in sorted(matched, key = lambda atom: (atom[0], atom[1])) ]

        bonds = [bond.element if bond.element == "H" else bond.element + str(bond.id) for bond in self.bonds]
        
        if bonds: return "Atom({}.{}: {})".format(self.element, self.id, ",".join(bonds))
        else: return "Atom({}.{})".format(self.element, self.id)
        
    
class Molecule(object):
    
    def __init__ (self, name=""):
        self.__formula = ""
        self.__molecular_weight = 0.0

        self.__atoms = []
        self.name = name
        
        self.branches = []
        self.locked = False

    def __str__(self):
        result = ""
        result += "Name: {}\n".format(self.name)
        result += "Formula: {}\n".format(self.__formula)
        result += "Weight: {} g/mol\n".format(self.__molecular_weight)

        for branch_id, branch in enumerate(self.branches):
            result += "Branch {}:\n".format(branch_id)
            for atom in branch:
                result += " " + str(atom) + "\n"

        result += "Atoms:\n"
        for atom in self.__atoms:
            result += " " + str(atom) + "\n"

        result += "\n"
        
        return result

    @property
    def formula(self):
        if not self.locked: raise UnlockedMolecule()
        return self.__formula

    @property
    def molecular_weight(self):
        if not self.locked: raise UnlockedMolecule()
        return self.__molecular_weight

    @property
    def atoms(self):
        return self.__atoms

    def update_formula(self):
        formula = ""
        order = ['C', 'H', 'O', 'B', 'Br', 'Cl', 'F', 'Mg', 'N', 'P', 'S']
        counter = dict()

        for element in order:
            counter[element] = 0

        for atom in self.__atoms:
            counter[atom.element] += 1

        for element in order:
            if counter[element] > 0:
                formula += "{}{}".format(element, counter[element] if counter[element] > 1 else "")
        
        self.__formula = formula
        
    def brancher(self, *branches):
        if self.locked: raise LockedMolecule()

        id_counter = len(self.__atoms)

        for carbons in branches:
            branch = len(self.branches)
            self.branches.append([])
            for carbon in range(carbons):
                self.__atoms.append(Atom("C", id_counter + 1))
                self.branches[branch].append(self.__atoms[id_counter])
                self.__molecular_weight += weight["C"]
                id_counter += 1

                if carbon - 1 >= 0:
                    self.branches[branch][carbon].bond(self.branches[branch][carbon - 1])
                    self.branches[branch][carbon - 1].bond(self.branches[branch][carbon])
        
        return self

    def bounder(self, *bounds):
        if self.locked: raise LockedMolecule()

        for (c1, b1, c2, b2) in bounds:
            carbon_1 = self.branches[b1 - 1][c1 - 1]
            carbon_2 = self.branches[b2 - 1][c2 - 1]

            carbon_1.bond(carbon_2)

            try:
                carbon_2.bond(carbon_1)
            except InvalidBond:
                carbon_1.unbond(carbon_2)
                raise InvalidBond()

        return self

    def mutate(self, *mutations):
        if self.locked: raise LockedMolecule()

        for (c, b, e) in mutations:
            carbon = self.branches[b - 1][c - 1]

            if len(carbon.bonds) > valence[e]: raise InvalidBond()
            
            self.__molecular_weight -= weight[carbon.element]
            self.__molecular_weight += weight[e]

            carbon.element = e

        return self

    def add(self, *elements):
        if self.locked: raise LockedMolecule()

        id_counter = len(self.__atoms)

        for (c, b, e) in elements:
            carbon = self.branches[b - 1][c - 1]

            new_atom = Atom(e, id_counter + 1)

            carbon.bond(new_atom)
            new_atom.bond(carbon)

            self.__atoms.append(new_atom)
            id_counter += 1

            self.__molecular_weight += weight[e]

        return self

    def add_chaining(self, c, b, *elements):
        if self.locked: raise LockedMolecule()

        id_counter = len(self.__atoms)
        to_be_bonded = self.branches[b - 1][c - 1]
        new_atoms = []

        try:
            for e in elements:
                new_atom = Atom(e, id_counter + 1)

                to_be_bonded.bond(new_atom)
                new_atom.bond(to_be_bonded)

                self.__atoms.append(new_atom)
                id_counter += 1

                self.__molecular_weight += weight[new_atom.element]

                new_atoms.append(new_atom)
                to_be_bonded = new_atom
        except InvalidBond:
            for new_atom in new_atoms:
                self.__molecular_weight -= weight[new_atom.element]
                for idx, atom in enumerate(self.__atoms):
                    atom.unbond(new_atom)
            self.__atoms = list(filter(lambda atom: atom not in new_atoms, self.__atoms))

            raise InvalidBond()

        return self

    def closer(self):
        if self.locked: raise LockedMolecule()

        for atom in self.__atoms:
            if not atom.filled():
                id_counter = len(self.__atoms)

                hydrogens = atom.fill(id_counter + 1)
                self.__atoms += hydrogens
                self.__molecular_weight += len(hydrogens) * weight["H"]

        self.update_formula()
        self.locked = True
        
        return self

    def unlock(self):
        if not self.locked: raise UnlockedMolecule()

        branches = []
        for branch in self.branches:
            new_branch = list(filter(lambda atom: atom.element != "H", branch))
            if new_branch: branches.append(new_branch)

        if not branches: raise EmptyMolecule()

        self.branches = branches

        new_atoms = list(filter(lambda atom: atom.element != "H", self.__atoms))
        self.__molecular_weight -= (len(self.__atoms) - len(new_atoms)) * weight["H"]
        self.__atoms = new_atoms

        for atom in self.__atoms:
            released = atom.release_hydrogens()

        for idx, atom in enumerate(self.__atoms):
            atom.id = idx + 1

        self.locked = False
        return self
