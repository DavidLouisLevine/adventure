import solve.utils as utils
import itertools

class Tuners:
    def __init__(self, tuners):
        self.tuners = tuners

    def get_values(self):
        values = []
        for tuner in self.tuners:
            values += [(tuner.name, tuner.value)]
        return values

    def set_value(self, tuner, value):
        tuner.value = value
        self.solver_data[tuner.name] = value

    def tune(self, solver_data, solver_fn):
        place = 0
        top_place = 0
        num_places = len(self.tuners)
        self.solver_data = solver_data

        for tuner in self.tuners:
            self.set_value(tuner, tuner.lower_bound)

        bestScore = None
        bestValue = None

        records = []
        total_points = self.num_values()
        point = 1

        for value in self.values():
            self.update_to_values(self.get_value_pairs(value))
            scores = []
            for _ in range(solver_data['NUM_TRIES']):
                self.solver = solver_fn()
                run_scores = self.solver.execute()
                scores += [max(run_scores[-1])]
            score = utils.avg(scores)
            #score = utils.avg(list(map(lambda x: x[-1], run_scores)))
            records += [(score, self.get_values())]
            print("Point:", str(point) + '/' + str(total_points), score, scores, self.get_values())
            point += 1
            if bestScore is None or score > bestScore:
                bestScore = score
                bestValue = self.get_values()

        return bestValue, bestScore, records

    def get_value_pairs(self, values):
        assert len(values) == len(self.tuners)
        return list(map(lambda x: (self.tuners[x].name, values[x]), range(len(values))))

    def update_to_values(self, value_pairs):
        i = 0
        for value in value_pairs:
            self.tuners[i].value = value[1]
            self.solver_data[value[0]] = value[1]
            i += 1

    def __str__(self):
        return ' '.join(list(map(lambda x: str(x), self.tuners)))

    def num_values(self):
        return utils.product(list(map(lambda x: x.num_values(), self.tuners)))

    def values(self):
        return itertools.product(*map(lambda x: x.values(), self.tuners))

class Tuner:
    def __init__(self, name, lower_bound, upper_bound, increment=None, num_samples=None):
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.num_samples = num_samples
        assert (num_samples is None) != (increment is None)
        if increment is None:
            self.increment = (upper_bound - lower_bound) / num_samples
        else:
            self.increment = increment

    def set_to_next(self, tuners):
        if utils.are_close(self.value, self.upper_bound):
            return False
        tuners.set_value(self, self.value + self.increment)
        return True

    def __str__(self):
        return "{}={:0.6f}".format(self.name, self.value)

    def num_values(self):
        return round((self.upper_bound - self.lower_bound) / self.increment) + 1

    def values(self):
        return list(map(lambda x: self.lower_bound + self.increment * x, range(self.num_values())))


