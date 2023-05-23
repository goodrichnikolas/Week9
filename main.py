import random
import simpy
from collections import namedtuple
import pandas as pd

# Define the structure of a machine and a customer using namedtuple
Machine = namedtuple("Machine", ["type", "cost", "time", "load_capacity", "quantity"])
Customer = namedtuple("Customer", ["id", "load", "cost"])

# Declare the available machines with their respective properties
machines = {
    "dryer_large": Machine("dryer_large", 2, 45, 25, 2),
    "dryer_medium": Machine("dryer_medium", 1, 30, 10, 4),
    "dryer_small": Machine("dryer_small", 0.5, 15, 5, 2),
    "washer_large": Machine("washer_large", 2, 40, 40, 1),
    "washer_medium": Machine("washer_medium", 0.75, 30, 20, 4),
    "washer_small": Machine("washer_small", 0.5, 20, 5, 5),
}

# Function to generate a list of customers
def generate_customers(num_customers):
    customers = []
    for i in range(num_customers):
        # Randomly assign a laundry load size from 1 to 40
        load = random.randint(1, 40)
        # Initialize the cost as 0
        customers.append(Customer(i, load, 0))
    return customers

# Function to simulate the laundromat run for a customer
def laundromat_run(env, machine, customer, records):
    with machine.request() as req:
        # Request the machine resource
        yield req

        # Simulate the time it takes to finish the laundry
        yield env.timeout(machines[machine.type].time)

        # Calculate cost and update the customer's cost
        cost = machines[machine.type].cost
        customer = Customer(customer.id, customer.load, customer.cost + cost)

        # Record the customer's information and cost
        records.append({
            "customer_id": customer.id,
            "machine_type": machine.type,
            "load_size": customer.load,
            "cost": cost
        })

# Function to simulate the entire process
def simulation():
    # Create a simulation environment
    env = simpy.Environment()

    # Create a dictionary with machine resources
    resources = {m: simpy.Resource(env, capacity=machines[m].quantity) for m in machines}

    # Generate customers
    customers = generate_customers(10)

    # List to store the records of each run
    records = []

    for customer in customers:
        # Select the smallest machine that can handle the customer's load
        available_machines = sorted(
            (m for m in machines.values() if m.load_capacity >= customer.load),
            key=lambda m: m.load_capacity,
        )

        # If there are suitable machines available, use the smallest one
        if available_machines:
            smallest_suitable_machine = available_machines[0]
            resource = resources[smallest_suitable_machine.type]
            # Start the process for this customer
            env.process(laundromat_run(env, resource, customer, records))

    # Run the simulation
    env.run()

    # Convert the records to a DataFrame
    records_df = pd.DataFrame(records)

    # Calculate the total cost
    total_cost = records_df['cost'].sum()

    return total_cost, records_df

# Number of trials to run the simulation
num_trials = 1000
total_costs = 0
all_records =
all_records = pd.DataFrame()

for _ in range(num_trials):
    cost, records_df = simulation()
    total_costs += cost
    all_records = all_records.append(records_df)

print(f"Average total cost: {total_costs / num_trials}")
