import simpy
import random
import statistics

total_wait_times = []
entry_times = []
baggage_times = []
checking_times = []

class Airport:
    def __init__(self, env, num_guard, num_airline_rep, num_security_line) -> None:
        self.env = env
        self.guard = simpy.Resource(env, num_guard)
        self.airline_rep = simpy.Resource(env, num_airline_rep)
        self.security_line = simpy.Resource(env, num_security_line)

    def enter_airport(self, passenger):
        yield self.env.timeout(random.randint(1, 2))

    def ticket_verification(self, passenger):
        yield self.env.timeout(random.randint(5, 10))

    def security_check(self, passenger):
        yield self.env.timeout(random.randint(1, 2))


def go_to_airport(env, passenger, airport):
    arrival_time = env.now

    with airport.guard.request() as request:
        yield request
        yield env.process(airport.enter_airport(passenger))

    entry_times.append(env.now - arrival_time)
    entry_time = env.now

    with airport.airline_rep.request() as request:
        yield request
        yield env.process(airport.ticket_verification(passenger))

    baggage_times.append(env.now - entry_time)
    baggage_time = env.now

    with airport.security_line.request() as request:
        yield request
        yield env.process(airport.security_check(passenger))

    checking_times.append(env.now - baggage_time)
    total_wait_times.append(env.now - arrival_time)


def run_airport(env, num_guard, num_airline_rep, num_security_line):
    airport = Airport(env, num_guard, num_airline_rep, num_security_line)

    passenger = 1

    while True:
        yield env.timeout(0.2)
        passenger += 1
        env.process(go_to_airport(env, passenger, airport))


def get_avg_wait_time(total_wait_times):
    avg_wait_time = statistics.mean(total_wait_times)
    minutes, frac_minutes = divmod(avg_wait_time, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


def get_user_input():
    num_guard = int(input('Enter # of Terminal Gate Guards: '))
    num_airline_rep = int(input('Enter # of Baggage Counters: '))
    num_security_line = int(input('Enter # of Security Check Lines: '))
    return num_guard, num_airline_rep, num_security_line


def main():
    random.seed(42)
    num_guard, num_airline_rep, num_security_line = get_user_input()

    env = simpy.Environment()
    print("Running simulation...")
    env.process(run_airport(env, num_guard, num_airline_rep, num_security_line))
    env.run(until= 60 * 24)

    mins, secs = get_avg_wait_time(total_wait_times)
    print(f"\nThe average wait time is {mins} minutes and {secs} seconds.")

    mins, secs = get_avg_wait_time(entry_times)
    print(f"\nThe average entry time is {mins} minutes and {secs} seconds.")

    mins, secs = get_avg_wait_time(baggage_times)
    print(f"\nThe average baggage time is {mins} minutes and {secs} seconds.")

    mins, secs = get_avg_wait_time(checking_times)
    print(f"\nThe average checking time is {mins} minutes and {secs} seconds.")


if __name__ == '__main__':
    main()



