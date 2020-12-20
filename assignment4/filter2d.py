from sim.plot2d import plot
import random as r
import math
import numpy as np


class Position:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.theta = pos[2]


class Pole(Position):
    def __init__(self, pos):
        Position.__init__(self, pos)


class Measurement:
    def __init__(self, distance, angle):
        self.distance = distance
        self.angle = angle


class Robot(Position):
    def __init__(self, pos):
        Position.__init__(self, pos)
        self.measurements = []
        self.max_measurement = 100
        self.angular_vel_variance = 0.1
        self.linear_vel_variance = 0.3


    # Movement is perfectly accurate, even though we are assuming it isn't.
    def move(self, speed, theta_dot):
        ### START STUDENT CODE
        self.theta += theta_dot
        self.x += math.cos(self.theta) * speed
        self.y += math.sin(self.theta) * speed
        ### END STUDENT CODE

    def move_with_error(self, speed, theta_dot):
        ### START STUDENT CODE
        theta_dot = r.normalvariate(theta_dot, self.angular_vel_variance)
        speed = r.normalvariate(speed, self.linear_vel_variance)
        self.move(speed, theta_dot)
        ### END STUDENT CODE

    # Measurement is perfectly accurate even though we are assuming it isn't.
    def measure(self, poles):
        ### START STUDENT CODE
        self.measurements.clear()

        for pole in poles:
            diff_x = pole.x - self.x
            diff_y = pole.y - self.y

            distance = math.sqrt(diff_x**2 + diff_y**2)

            if distance < self.max_measurement:
                angle = math.atan2(diff_y, diff_x)
                angle -= self.theta

                if angle > 2*math.pi:
                    angle -= 2*math.pi
                elif angle < 2*math.pi:
                    angle += 2*math.pi

                self.measurements.append(Measurement(distance, angle))
            
        ### END STUDENT CODE


class Particle(Robot):
    def __init__(self, pos):
        Robot.__init__(self, pos)
        self.weight = 0.0
        self.weight_treshold = 0.01

        self.distance_sigma = 2.5
        self.distance_distribution_peak = 1 / \
            (math.sqrt(2 * math.pi) * self.distance_sigma)
        self.distance_weight = 1

        self.angle_sigma = 0.5
        self.angle_distribution_peak = 1 / \
            (math.sqrt(2 * math.pi) * self.angle_sigma)
        self.angle_weight = 1

        self.theta_dot_sigma = 0.2
        self.speed_sigma = 0.5

    def predict(self, speed, theta_dot):
        ### START STUDENT CODE
        theta = r.normalvariate(theta_dot, self.theta_dot_sigma)
        speed = r.normalvariate(speed, self.speed_sigma)
        self.move(speed, theta)
        ### END STUDENT CODE

    def probability_density_function(self, mu, sigma, x):
        ### START STUDENT CODE
        weight = np.exp((-1/2)*((x - mu)/sigma)**2)/(sigma * np.sqrt(2 * np.pi))
        return weight
        ### END STUDENT CODE

    def calc_distance_weight(self, robot_distance, particle_distance):
        weight = self.probability_density_function(robot_distance, self.distance_sigma, particle_distance)

        weight /= self.distance_distribution_peak
        weight *= self.distance_weight

        return weight        

    def calc_angle_weight(self, robot_angle, particle_angle):
        # Need to use minimum angle
        diff_angle = abs(robot_angle - particle_angle)
        if diff_angle > np.pi:
            diff_angle = abs(diff_angle - np.pi * 2)

        weight = self.probability_density_function(0, self.angle_sigma, diff_angle)

        weight /= self.angle_distribution_peak
        weight *= self.angle_weight

        return weight  

    def update_weight(self, robot_measurements):
        ### START STUDENT CODE
        self.weight = 0
        for measure in self.measurements:
            best_weight = 0
            for r_measure in robot_measurements:
                dist_weight = self.calc_distance_weight(r_measure.distance, measure.distance)
                angle_weight = self.calc_angle_weight(r_measure.angle, measure.angle)

                if dist_weight < self.weight_treshold or angle_weight < self.weight_treshold:
                    weight = 0
                else:
                    weight = dist_weight * angle_weight
                
                if weight > best_weight:
                    best_weight = weight

            self.weight += best_weight
        if len(self.measurements) > 0:
            self.weight /= len(self.measurements)
        self.weight *= self.weight
        ### END STUDENT CODE


def resample_particles(particles):
    ### START STUDENT CODE
    resampled_particles = []
    num_of_particles = len(particles)

    weights = [part.weight for part in particles]
    scale = num_of_particles / (sum(weights) * 2)

    if scale > 10:
        scale = 10
    elif scale < 0.5:
        scale = 0

    resamples = r.choices(population=range(num_of_particles), weights=weights, k=num_of_particles)
    for i in resamples:
        x = r.normalvariate(particles[i].x, particles[i].speed_sigma * scale)
        y = r.normalvariate(particles[i].y, particles[i].speed_sigma * scale)
        theta = r.normalvariate(particles[i].theta, particles[i].theta_dot_sigma * scale)

        resampled_particles.append(Particle([x, y, theta]))

    return resampled_particles
    ### END STUDENT CODE
