from functools import total_ordering
from typing import List
from heapq import heappop, heappush, heappushpop

import progressbar

from iohandling import parse_problem, write_solution


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance(self, point):
        return abs(point.x - self.x) + abs(point.y - self.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class Ride:
    def __init__(self, ride_id: int, x_start: int, y_start: int, x_stop: int, y_stop: int, earliest_start: int
                 , latest_finish: int):
        self.start_point = Point(x_start, y_start)
        self.end_point = Point(x_stop, y_stop)
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish
        self.id = ride_id
        self.assigned = None
        self.points = 0
        self.completed_at = 0

        self.distance = self.end_point.distance(self.start_point)
        self.latest_start = self.latest_finish - self.distance

    def __repr__(self):
        return "Ride(id={}, start={}, end={}, earliest_start={}, latest_finish={})".format(self.id, self.start_point,
                                                                                           self.end_point,
                                                                                           self.earliest_start,
                                                                                           self.latest_finish)


class Vehicle:
    def __init__(self):
        self.position = Point(0, 0)
        self.assigned_rides = []  # type: List<Ride>
        self.assigned_rides_free_times = []
        self.points_by_ride = []
        self.position_revert_list = []
        self.free_at_timestep = 0

    def add_ride(self, ride: Ride, end_time: int, bonus: int):
        if ride.assigned:
            ride.assigned.revert_to_ride_previous_of(ride)
        self.assigned_rides.append(ride)
        self.assigned_rides_free_times.append(self.free_at_timestep)
        self.free_at_timestep = end_time
        points = points_calculation(self, ride, bonus)
        self.points_by_ride.append(points)
        ride.assigned = self
        ride.points = points
        ride.completed_at = end_time
        self.position = ride.end_point
        self.position_revert_list.append(self.position)

    def revert_to_ride_previous_of(self, ride: Ride):
        index = self.assigned_rides.index(ride)
        self.free_at_timestep = self.assigned_rides_free_times[index]
        self.position = self.position_revert_list[index]
        for ride in self.assigned_rides[index:]:
            ride.assigned = None
            ride.points = 0
            ride.completed_at = 0
        del self.assigned_rides[index:]  # bis inklusive index
        del self.assigned_rides_free_times[index:]  # bis inklusive index
        del self.points_by_ride[index:]  # bis inklusive index
        del self.position_revert_list[index:]  # bis inklusive index

    def sol_line(self):
        size = len(self.assigned_rides)
        return "{} {}".format(size, ' '.join([str(r.id) for r in self.assigned_rides]))

    def __lt__(self, other):
        return self.free_at_timestep < other.free_at_timestep

    def __repr__(self):
        return "Vehicle(pos={}, rides=[{}], free_at={})".format(self.position,
                                                                ','.join(str(r.id) for r in self.assigned_rides),
                                                                self.free_at_timestep)


def points_calculation(vehicle, ride, bonus):
    points = 0
    distance_to_port = ride.start_point.distance(vehicle.position)
    points += ride.distance
    start_time = max(vehicle.free_at_timestep + distance_to_port, ride.earliest_start)
    if start_time == ride.earliest_start:
        points += bonus
    return points


def sort_func(vehicle, ride):
    return ride.start_point.distance(vehicle.position)


def can_improve(ride, vehicle, bonus):
    if ride.assigned is None:
        return True
    # ride.points >= points_calculation(v, rides[index], bonus) -
    return False


def process(file_path):
    rows, columns, vehicle_count, rides_count, bonus, steps, rides = parse_problem(file_path)

    rides = [Ride(idx, *ride_info) for idx, ride_info in enumerate(rides)]
    # solution goes here
    vehicles = [Vehicle() for _ in range(vehicle_count)]  # type: List<Vehicle>
    sorted_vehicles = [(0, i, v) for i, v in enumerate(vehicles)]  # type: List<Vehicle>

    t, i, v = sorted_vehicles[0]
    bar = progressbar.ProgressBar(widgets=[file_path.ljust(30), ': ', progressbar.Timer(), ' ', progressbar.Bar(), ' ', progressbar.ETA()], max_value=len(rides))
    index = 0
    max_index = 0
    while len(rides) > index:
        t, i, v = heappushpop(sorted_vehicles, (v.free_at_timestep, i, v))

        rides.sort(key=lambda x: -(points_calculation(v, x, bonus)
                                   / (max(x.start_point.distance(v.position), x.earliest_start) + x.distance)))

        index = 0

        while len(rides) > index and \
                (rides[index].latest_start < v.free_at_timestep
                 or not can_improve(rides[index], v, bonus)
                 or rides[index].latest_start + rides[index].start_point.distance(v.position) < v.free_at_timestep):
            index += 1

        if len(rides) <= index:
            break

        start = max(rides[index].earliest_start, v.free_at_timestep)
        end = start + rides[index].distance

        overruled_vehicle = rides[index].assigned
        v.add_ride(rides[index], end, bonus)

        if overruled_vehicle:
            for idx, t in enumerate(sorted_vehicles):
                if t[2] == overruled_vehicle:
                    sorted_vehicles.pop(idx)
                    break
            heappush(sorted_vehicles, (overruled_vehicle.free_at_timestep, t[1], overruled_vehicle))


        # rides.remove(rides[index])
        max_index = max(index, max_index)
        bar.update(max_index)


    solution = [vehicle.sol_line() for vehicle in vehicles]

    write_solution(file_path, solution)
