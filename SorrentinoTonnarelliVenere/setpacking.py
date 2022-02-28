from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridSampler

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
        self.n = subsets 
        if weights == None:
            weights = [1] * len(subsets)
        self.w = weights
        self.c = constraints

    def solve(self):
        """This method solves this problem by using the BQM API of D-Wave Leap.
            Returns a dictionary in which subsets are the key of the dictionary, and their
            corresponding value is 1 if that subset is selected, 0 otherwise."""
        bqm = BinaryQuadraticModel({}, {}, 0, 'BINARY')
        for i in range(len(self.n)):
            bqm.offset += 1
            bqm.add_variable(self.n[i], 0-(self.w[i])) #add variable for subset
        for cons in self.c:
            for i in range(len(cons)):
                for j in range(i):
                    bqm.add_interaction(cons[i], cons[j], 6) #add constraint to avoid two non-disjoint subsets being selected       
        sampler = LeapHybridSampler()
        sampleset = sampler.sample(bqm, label="Set Packing")
        sample = sampleset.first.sample
        return sample

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
#create problem instance by reading user input
problem = get_sanitized_input()

#compute problem solution and show it
print(problem.solve())
