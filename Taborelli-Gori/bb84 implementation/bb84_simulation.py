from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np


def encode_message(bits, bases):
    message = []
    for i in range(string_dimension):
        qc = QuantumCircuit(1,1)
        if bases[i] == 0: # Prepare qubit in |1>/|0> basis
            if bits[i] == 0:
                pass
            else:
                qc.x(0)
        else: # Prepare qubit in |+>/|-> basis
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()
        message.append(qc)
    return message


def measure_message(message, bases):
    measurements = []
    for q in range(string_dimension):
        if bases[q] == 0: # measuring in |1>/|0> basis
            message[q].measure(0,0)
        if bases[q] == 1: # measuring in |+>/|-> basis
            message[q].h(0)
            message[q].measure(0,0)
        aer_sim = Aer.get_backend('aer_simulator')
        qobj = assemble(message[q], shots=1, memory=True)
        result = aer_sim.run(qobj).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements


def remove_garbage(a_bases, b_bases, bits):
    good_bits = []
    for q in range(string_dimension):
        if a_bases[q] == b_bases[q]:
            # If both used the same basis, add
            # this to the list of good bits
            good_bits.append(bits[q])
    return good_bits


def sample_bits(bits, selection):
    sample = []
    for i in selection:
        i = np.mod(i, len(bits))
        # pop(i) removes the element of the
        # list at index i
        sample.append(bits.pop(i))
    return sample


string_dimension=100

np.random.seed(seed=3)
## initialize the random classical bit string
alice_bits = randint(2, size=string_dimension)
print('Alice random bit sequence: % s' % (alice_bits))

# initialize the random sequence of bases of Alice
alice_bases = randint(2, size=string_dimension)
print('Alice random base sequence % s: ' % (alice_bases))

# initialize the random sequence of bases of Bob
bob_bases = randint(2, size=string_dimension)
print('Bob random base sequence: % s' % (bob_bases))

# initialize the random sequence of bases of Eve
eve_bases = randint(2, size=string_dimension)
print('Eve random base sequence: % s' % (eve_bases))

# Alice encodes its message by applying her bases
message = encode_message(alice_bits, alice_bases)
print('encoded qubit string: ' + str(message))

## Eve interepts the message, changing its state with high probabilities
intercepted_message = measure_message(message, eve_bases)
print("Eve's measurement: " + str(intercepted_message))

# Bob measures the quibit sequence with its bases
bob_results = measure_message(message, bob_bases)
print("Bob's measurement: " + str(bob_results))

## both Bob and Alice filter the bit sequence based on the matching position of their bases
bob_key = remove_garbage(alice_bases, bob_bases, bob_results)
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)

# a further random filtering is made on the remaining bit sequence
sample_size = 15
bit_selection = randint(string_dimension, size=sample_size)

# print the sequence of bits
bob_sample = sample_bits(bob_key, bit_selection)
print("bob_sample = " + str(bob_sample))
alice_sample = sample_bits(alice_key, bit_selection)
print("alice_sample = "+ str(alice_sample))

# check if the keys are equal
if bob_sample == alice_sample:
    print("the keys are equal")
else:
    print("the keys are not equal")