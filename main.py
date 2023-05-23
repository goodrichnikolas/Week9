import random
import simpy
from collections import namedtuple
import pandas as pd


Machine = namedtuple("Machine", ["type", "cost", "time", "load_capacity", "quantity"])
Customer = namedtuple("Customer", ["id", "load", "cost"])


machines = {
    "dryer_large": Machine("dryer_large", 2, 45, 25, 2),
    "dryer_medium": Machine("dryer_medium", 1, 30, 10, 4),
    "dryer_small": Machine("dryer_small", 0.5, 15, 5, 2),
    "washer_large": Machine("washer_large", 2, 40, 40, 1),
    "washer_medium": Machine("washer_medium", 0.75, 30, 20, 4),
    "washer_small": Machine("washer_small", 0.5, 20, 5, 5),
}


laundry_sizes = {"big": 10, "medium": 5, "small": 2}

def generate_customers(num_customers, max_load):
    customers = []
    for i in range(num_customers):
        load = random.choices(list(laundry_sizes.values()), k=max_load)
        customers.append(Customer(i, load, 0))
    return customers

def laundromat_run(env, machine, customer, records):
    
    with machine.request() as req:
        yield req

        
        yield env.timeout(machines[machine.type].time * sum(customer.load))

        
        cost = machines[machine.type].cost * sum(customer.load)
        customer.cost += cost

        
        records.append({
            "customer_id": customer.id,
            "machine_type": machine.type,
            "load_size": sum(customer.load),
            "cost": cost
        })

def simulation():
    
    env = simpy.Environment()

    
    resources = {m: simpy.Resource(env, capacity=machines[m].quantity) for m in machines}

    
    customers = generate_customers(10, 5)

    
    records = []

    
    for customer in customers:
        customer.cost = 0
        env.process(laundromat_run(env, resources['washer_small'], customer, records))
        env.process(laundromat_run(env, resources['dryer_small'], customer, records))
    env.run()

    
    records_df = pd.DataFrame(records)

    
    total_cost = records_df['cost'].sum()

    return total_cost, records_df


num_trials = 1000
total_costs = 0
all_records = pd.DataFrame()

for _ in range(num_trials):
    cost, records_df = simulation()
    total_costs += cost
    all_records = all_records.append(records_df)

print(f"Average total cost: {total_costs / num_trials}")
