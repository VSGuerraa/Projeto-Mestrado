import random
import math
import gerador_topologia as gt
import ILP_ciente as ilp_solver
import networkx as nx

def simulated_annealing(objective_function, initial_solution, neighbor_function, 
                        initial_temperature, cooling_rate, stopping_temperature):
    """
    Perform simulated annealing to minimize the objective function.
    
    :param objective_function: Function to minimize.
    :param initial_solution: Starting point for the optimization.
    :param neighbor_function: Function to generate a neighboring solution.
    :param initial_temperature: Starting temperature.
    :param cooling_rate: Rate at which the temperature decreases.
    :param stopping_temperature: Temperature at which the algorithm stops.
    :return: Best solution found and its objective function value.
    """
    current_solution = initial_solution
    current_value = objective_function()
    best_solution = current_solution
    best_value = current_value
    
    temperature = initial_temperature
    
    while temperature > stopping_temperature:
        neighbor_solution = neighbor_function(current_solution)
        neighbor_value = objective_function()
        
        delta = neighbor_value - current_value
        acceptance_probability = math.exp(-delta / temperature) if delta > 0 else 1.0
        
        if random.random() < acceptance_probability:
            current_solution = neighbor_solution
            current_value = neighbor_value
            
            # Update the best solution found
            if current_value < best_value:
                best_solution = current_solution
                best_value = current_value
        
        # Cool down the temperature
        temperature *= cooling_rate
    
    return best_solution, best_value

def objective_function():
    value = ilp_solver.main()
    return value[0]

def neighbor_function(current_solution):
    nr_nodos = len(list(current_solution.nodes))
    nr_links = nr_nodos * 1.3
    neighbor = gt.gerador_Topologia(nr_nodos, nr_links, current_solution)
    return neighbor
    
def main ():
    nr_nodos = 20
    nr_links = int(nr_nodos * 1.3)
    
    initial_solution = gt.gerador_Topologia(nr_nodos, nr_links)
    
    # Parameters for simulated annealing
    initial_temperature = 1000
    cooling_rate = 0.99
    stopping_temperature = 1e-8
    
    # Run simulated annealing
    best_solution, best_value = simulated_annealing(objective_function, initial_solution, neighbor_function, 
                                                    initial_temperature, cooling_rate, stopping_temperature)
    
    print(f"Best solution: {best_solution}")
    print(f"Best value: {best_value}")
    

if __name__ == "__main__":
    main()