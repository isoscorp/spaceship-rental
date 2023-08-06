import cProfile
import pstats
import timeit

from optimizer.contract_optimizer import ContractOptimizerFast
from test.contract_generator import ContractGenerator


class Profiler:
    """
    Profiler for contract optimization.
    """

    MEASURE_REPETITIONS = 5

    def __init__(self, contract_generator: ContractGenerator):
        self.profiler = cProfile.Profile()
        self.contract_generator = contract_generator
        self.optimizer_class = ContractOptimizerFast

    def profile_stats(self, nb_contracts: int) -> None:
        """
        Runs optimization on a set of contracts randomly generated
        and prints most time-consuming instructions (based on cProfile library).
        :param nb_contracts: number of contracts to be optimized.
        """
        contracts = self.contract_generator.generate(nb_contracts)
        optimizer = self.optimizer_class(contracts)

        print("starting optimization")
        self.profiler.enable()
        result = optimizer.optimize()
        self.profiler.disable()
        print(f"=> result: {result}")

        stats = pstats.Stats(self.profiler).sort_stats("cumtime")
        stats.print_stats()

    def profile_time(self, nb_contracts: int) -> None:
        """
        Repeats optimization on a set of contracts randomly generated
        and prints average execution time (based on timeit library).
        Number of repetitions is defined at the class level.
        :param nb_contracts: number of contracts to be optimized.
        """
        print(f"Measuring time of contract optimization for {nb_contracts} contracts")
        contracts = self.contract_generator.generate(nb_contracts)
        optimizer = self.optimizer_class(contracts)
        results = timeit.repeat(
            lambda: optimizer.optimize(), repeat=self.MEASURE_REPETITIONS, number=1
        )
        print(f" => average time: {sum(results) / len(results)}\n")

    def profile_memory(self, nb_contracts: int) -> None:
        """
        Simply runs optimization on a set of contracts randomly generated.
        Method 'optimize' must be decorated by @profile (based on memory_profiler library).
        :param nb_contracts: number of contracts to be optimized.
        """
        print(
            f"Measuring memory usage of contract optimization for {nb_contracts} contracts"
        )
        contracts = self.contract_generator.generate(nb_contracts)
        self.optimizer_class(contracts).optimize()


if __name__ == "__main__":
    contract_generator = ContractGenerator(from_file=True)
    profiler = Profiler(contract_generator)

    # profiler.profile_stats(nb_contracts=10000)

    # profile time
    for n in (10, 100, 1000, 10000, 20000, 50000, 100000, 500000):
        profiler.profile_time(nb_contracts=n)

    # profile memory
    # WARNING: requires the decorator @profile to the method being profiled
    # for n in (10, 100, 1000, 10000, 20000, 50000, 100000, 500000):
    #     profiler.profile_memory(nb_contracts=n)


# naive
# num       | memory (MB)   | time
# =============================================
# 10        | 23.8          | 30us
# 100       | -             | 1.5ms
# 1000      | -             | 200ms
# 10000     | -             | 30s

# naive improved
# num       | memory (MB)   | time
# =============================================
# 10        | 22.9          | 20us
# 100       | 23            | 0.5ms
# 1000      | 23.4          | 50ms
# 10000     | -             | 5s
# 20000     | -             | 20s
# 50000     | -             | 215s

# fast
# num       | memory (MB)   | time
# =============================================
# 10        | 23.4          | 20us
# 100       | 23.4          | 0.2ms
# 1000      | 23.8          | 2ms
# 10000     | 28.4          | 40ms
# 20000     | 33.5          | 80ms
# 50000     | 48.6          | 0.2s
# 100000    | 73.9          | 0.5s
# 500000    | 271.6         | 4s
