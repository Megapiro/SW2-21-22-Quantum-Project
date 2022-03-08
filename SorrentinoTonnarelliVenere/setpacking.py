from dimod import BinaryQuadraticModel
from dwave.system import DWaveSampler
from dwave.system import LeapHybridSampler
from dwave.system import EmbeddingComposite
from dwave.inspector import *
import json
import JSONGenerator

class SetPackingProblem:
    """This class represents a set-packing problem, 
    in which set elements must be inserted into n different subsets, 
    such that each element is inserted in at most one subset.
    If differents weights are associated to each subset, the goal is to achieve
    a subsets selection of maximum weight. """
    def __init__(self, subsets, weights, constraints): 
        """This is the constructor of the SetPackingProblem class.
        Params:
        sets_number: number of possible subsets
        weights: weight associated to each different subset.
            Defaults weights are unitary for each subset.
        constraints: a list of sets_number constraints.""" 
        self.s = subsets 
        if weights == None:
            weights = [1] * len(subsets)
        self.w = weights
        self.c = constraints

    def prepare(self):
        """
            This method prepares the resolution of this problem by using the BQM API of D-Wave Leap.
            Returns the problem itself. a dictionary in which subsets are the key of the dictionary, and their
            corresponding value is 1 if that subset is selected, 0 otherwise.
        """
        self.bqm = BinaryQuadraticModel({}, {}, 0, 'BINARY')
        for i in range(len(self.s)):
            self.bqm.offset += 1
            self.bqm.add_variable(self.s[i], 0-(self.w[i])) #add variable for subset
        for cons in self.c:
            for i in range(len(cons)):
                for j in range(i):
                    self.bqm.add_interaction(cons[i], cons[j], 6) #add constraint to avoid two non-disjoint subsets being selected       
        return self

    def sample_hybrid(self):
        """
            This method resolves this problem by using the LeapHybridSampler.
            Returns a dictionary in which subsets are the key of the dictionary, and their
            corresponding value is 1 if that subset is selected, 0 otherwise. 
        """
        sampler = LeapHybridSampler(solver={'category': 'hybrid'})
        sampleset = sampler.sample(self.bqm, label="Set Packing")
        return sampleset
    
    def sample_composite(self):
        
        """
            This method resolves this problem by using the LeapHybridSampler. It shows the inspector screen.
            Returns a dictionary in which subsets are the key of the dictionary, and their
            corresponding value is 1 if that subset is selected, 0 otherwise. 
        """
        sampler = EmbeddingComposite(DWaveSampler(solver={'topology__type': 'chimera'}))
        sampleset = sampler.sample(self.bqm, label="Set Packing")
        show(sampleset) 
        return sampleset


def read_sanitized_file(filename):
    """
        This method receives input from a file, verifies if it is consistent and constructs a list of instances of the class SetPackingProblem.
        Returns a list of instances of the class SetPackingProblem, if problems are correctly inserted.
        Throws a ValueError exception if data type is not consistent.
        Throws a json.decoder.JSONDecodeError exception if file is not correctly encoded.
    """
    with open(filename, "r") as f:
        data = json.load(f)
        problems = []
        for problem in data:
            subsets = problem["subsets"]
            sets = []
            weights = []
            for set in subsets:
                sets.append(set["name"])
                if "weight" in set:
                    try:
                        weights.append(int(set["weight"]))
                    except ValueError:
                        print("Weight attribute must be integer")
                        exit()
                else:
                    weights.append(1)
                for i in range(len(sets)):
                        for j in range(i):
                            if(sets[i] == sets[j]):
                                print("Identifier already inserted in subsets list")
                                exit()
            constraints = problem["constraints"]
            c = []
            for cons in constraints:
                c.append(cons["sets"])
                for elem in cons["sets"]:
                    if elem not in sets:
                        print("Undefined subsets")
                        exit()
                for i in range(len(cons["sets"])):
                    for j in range(i):
                        if(cons["sets"][i] == cons["sets"][j]):
                            print("Identifier already inserted in this constraint")
                            exit()
        problems.append(SetPackingProblem(sets, weights, c))
    return problems

def get_sanitized_input():
    """This method receives input from the user, verifies if it is consistent and constructs an instance of the class SetPackingProblem.
    Returns an instance of the class SetPackingProblem, if problem is correctly inserted.
    Throws a ValueError exception otherwise."""
    while True:
        print("Insert the number of the subsets: ")
        n = input()
        try:
            n = int(n)
            if n < 0:
                raise ValueError("A positive integer number must be inserted")
            subsets = []
            for i in range(n):
                print("Insert one-character identifier for element: ", i + 1)
                value = input()
                if(len(value) > 1):
                    raise ValueError("Identifiers must have only one character")
                if value in subsets:
                    raise ValueError("Identifier already inserted")
                subsets += value
            print("Do you wish to insert weights for subsets? Y/N")
            ans = input()
            try:
                weights = []
                if ans == "Y" or ans == "y":
                    for i in range(n):
                        print("Insert numeric weight for subset: ", subsets[i])
                        value = input()
                        value = int(value)
                        weights.append(value)
                elif ans == "N" or ans == "n":
                    weights = None
                else:
                    raise TypeError("Only Y/y or N/n are acceptable answers.")
                print("Insert the number of the constraints: ")
                m = input()
                try:
                    m = int(m)
                except ValueError:
                    print("A positive integer number must be inserted")
                    continue
                if m < 0: 
                    raise ValueError("A positive integer number must be inserted")
                constraints = []
                for i in range(m):
                    print("Insert the number of subsets for constraint #{}:".format(i+1))
                    num = input()
                    num = int(num)
                    if num < 0:
                        raise ValueError("A positive integer number must be inserted")
                    c = []
                    print("Insert elements:")
                    for i in range(num):
                        c1 = input()
                        if c1 in c:
                            raise ValueError("Identifier already inserted in this constraint")
                        c += c1
                        if c[i] not in subsets:
                            raise ValueError("Identifier not valid.")
                    constraints.append(c)
                return SetPackingProblem(subsets, weights, constraints)
            except TypeError as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                continue
        except ValueError as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            continue

JSONGenerator.generate('SorrentinoTonnarelliVenere/data.json', 4)

problem = read_sanitized_file('SorrentinoTonnarelliVenere/data.json')[0]
print(problem.prepare().sample_composite())

