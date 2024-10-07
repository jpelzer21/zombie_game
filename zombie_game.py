class Agent:

    def __init__(self, energy, state, neighbors=None):
        self.energy = max(0, min(100, energy))  # Ensure energy is within the range [0, 100]
        self.state = state  # ALIVE, INFECTED, DEAD for Humans - ALIVE, DEAD for Zombies
        self.neighbors = neighbors if neighbors is not None else []  # Initialize with an empty list if none provided

    def update_state(self):
        if self.energy <= 0:
            self.state = 'DEAD'

    def update_energy(self, change):
        self.energy = max(0, min(100, self.energy + change))  # Ensure energy stays within [0, 100]
        self.update_state()  # Check if the state needs to be updated after energy change

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor):
        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)

    def interact_with_neighbors(self):
        pass

    def __str__(self):
        # String representation of the agent for easy debugging.
        return f"Agent(State: {self.state}, Energy: {self.energy}, Neighbors: {len(self.neighbors)})"






class Human(Agent):
    def __init__(self, energy, state='ALIVE', neighbors=None):
        super().__init__(energy, state, neighbors)

    def get_bitten(self, bite_energy_loss):
        if self.state == 'ALIVE':
            self.state = 'INFECTED'  # Only change state if the human was ALIVE
        self.update_energy(-bite_energy_loss)  # Reduce energy by the bite amount

    def recover(self, recovery_rate):
        if self.state == 'INFECTED':
            self.state = 'ALIVE'  # If cured, the state returns to ALIVE
        self.update_energy(recovery_rate)  # Increase energy by recovery rate, max of 100

    def lose_energy_over_time(self, energy_loss_rate):
        if self.state == 'INFECTED':
            self.update_energy(-energy_loss_rate)  # Gradually lose energy while infected

    def interact_with_neighbors(self):
        for neighbor in self.neighbors:
            if isinstance(neighbor, Zombie) and neighbor.state == 'ALIVE':
                neighbor.bite(self)  # A zombie might bite the human
            elif isinstance(neighbor, Doctor) and self.state == 'INFECTED':
                neighbor.cure(self)  # A doctor might cure the human




class Zombie(Agent):
    def __init__(self, energy, state='ALIVE', neighbors=None):
        super().__init__(energy, state, neighbors)

    def bite(self, target):
        if isinstance(target, Human) and target.state != 'DEAD' and self.state == 'ALIVE':
            bite_energy_loss = 10  # Define how much energy the target loses
            target.get_bitten(bite_energy_loss)  # Target loses energy and may get infected
            self.gain_energy(5)  # Zombie gains energy from a successful bite

    def lose_energy_over_time(self, energy_loss_rate):
        self.update_energy(-energy_loss_rate)  # Decrease the zombie's energy over time
        self.update_state()  # Check if zombie's state should change to DEAD

    def gain_energy(self, energy_gain):
        self.update_energy(energy_gain)  # Increase zombie's energy, ensuring it stays within limits

    def interact_with_neighbors(self):
        for neighbor in self.neighbors:
            if isinstance(neighbor, Human) and neighbor.state != 'DEAD':
                self.bite(neighbor)  # Attempt to bite any alive human or doctor

    def __str__(self):
        return f"Zombie(State: {self.state}, Energy: {self.energy}, Neighbors: {len(self.neighbors)})"





class Doctor(Human):
    def __init__(self, energy, state='ALIVE', neighbors=None):
        super().__init__(energy, state, neighbors)
    
    def cure(self, target):
        """Attempt to cure an INFECTED agent."""
        pass





