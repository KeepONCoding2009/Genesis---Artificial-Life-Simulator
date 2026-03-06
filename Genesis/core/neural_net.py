import random
import math

class Layer:
    def __init__(self, input_size, output_size):
        self.weights = [[random.gauss(0, 1) for _ in range(output_size)] for _ in range(input_size)]
        self.biases = [0.0 for _ in range(output_size)]
        
    def forward(self, inputs):
        self.inputs = inputs
        self.output = [0.0] * len(self.biases)
        for j in range(len(self.biases)):
            sum_val = self.biases[j]
            for i in range(len(inputs)):
                sum_val += inputs[i] * self.weights[i][j]
            self.output[j] = sum_val
        return self.output

class ActivationMethod:
    @staticmethod
    def relu(x):
        return max(0.0, x)
    
    @staticmethod
    def tanh(x):
        x = max(-50.0, min(50.0, x))
        return math.tanh(x)

class NeuralNetwork:
    def __init__(self, topology):
        self.topology = topology
        self.layers = []
        
        for i in range(len(topology) - 1):
            self.layers.append(Layer(topology[i], topology[i+1]))
            
    def predict(self, inputs):
        output = inputs
        for i, layer in enumerate(self.layers):
            output = layer.forward(output)
            if i < len(self.layers) - 1:
                output = [ActivationMethod.relu(x) for x in output]
            else:
                output = [ActivationMethod.tanh(x) for x in output]
        return output
        
    def mutate(self, mutation_rate=0.1, mutation_strength=0.5):
        for layer in self.layers:
            for i in range(len(layer.weights)):
                for j in range(len(layer.weights[i])):
                    if random.random() < mutation_rate:
                        layer.weights[i][j] += random.gauss(0, 1) * mutation_strength
            
            for j in range(len(layer.biases)):
                if random.random() < mutation_rate:
                    layer.biases[j] += random.gauss(0, 1) * mutation_strength
            
    def crossover(self, other_network):
        child = NeuralNetwork(self.topology)
        for i, (layer_self, layer_other) in enumerate(zip(self.layers, other_network.layers)):
            child_layer = child.layers[i]
            
            for wi in range(len(layer_self.weights)):
                for wj in range(len(layer_self.weights[wi])):
                    if random.random() > 0.5:
                        child_layer.weights[wi][wj] = layer_self.weights[wi][wj]
                    else:
                        child_layer.weights[wi][wj] = layer_other.weights[wi][wj]
                        
            for bi in range(len(layer_self.biases)):
                if random.random() > 0.5:
                    child_layer.biases[bi] = layer_self.biases[bi]
                else:
                    child_layer.biases[bi] = layer_other.biases[bi]
                    
        return child
