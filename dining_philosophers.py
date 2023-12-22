import threading
import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math


class Fork(threading.Semaphore):  # Değişiklik burada
    def __init__(self, index):
        super().__init__(1)  # Semaphore, başlangıçta serbest bırakılmış (1) olarak oluşturulur
        self.index = index

class Philosopher(threading.Thread):
    def __init__(self, index, left_fork, right_fork, spaghetti):
        super().__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.spaghetti = spaghetti
        self.eating = False

    def think(self):
        time.sleep(3 + random.random() * 3)

    def eat(self):
        with self.left_fork, self.right_fork:
            time.sleep(5 + random.random() * 5)
            self.spaghetti -= 1
            self.eating = True
            time.sleep(5 + random.random() * 5)
            self.eating = False

    def run(self):
        while self.spaghetti > 0:
            self.think()
            self.eat()
def animated_table(philosophers: list[Philosopher], forks: list[Fork], m: int):
    """
    Creates an animated table with the philosophers and forks.

    :param philosophers: The list of philosophers.
    :param forks: The list of forks.
    :param m: The amount of spaghetti each philosopher has.
    """
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Dining Philosophers")
    philosopher_circles: list[plt.Circle] = [
        plt.Circle((0, 0), 0.2, color="black") for _ in range(len(philosophers))
    ]
    philosopher_texts: list[plt.Text] = [
        plt.Text(
            0,
            0,
            str(philosopher.index),
            horizontalalignment="center",
            verticalalignment="center",
        )
        for philosopher in philosophers
    ]
    fork_lines: list[plt.Line2D] = [
        plt.Line2D((0, 0), (0, 0), color="black") for _ in range(len(forks))
    ]
    fork_texts: list[plt.Text] = [
        plt.Text(
            0,
            0,
            str(fork.index),
            horizontalalignment="center",
            verticalalignment="center",
        )
        for fork in forks
    ]
    for philosopher_circle in philosopher_circles:
        ax.add_patch(philosopher_circle)
    for fork_line in fork_lines:
        ax.add_line(fork_line)
    for philosopher_text in philosopher_texts:
        ax.add_artist(philosopher_text)
    for fork_text in fork_texts:
        ax.add_artist(fork_text)

    def update(frame):
        """
        Updates the table.
        """
        # get the philosophers and forks from the global scope
        nonlocal philosophers, forks
        for i in range(len(philosophers)):
            philosopher_circles[i].center = (
                0.5 * math.cos(2 * math.pi * i / len(philosophers)),
                0.5 * math.sin(2 * math.pi * i / len(philosophers)),
            )
            # update the labels as text on the plot
            philosopher_texts[i].set_position(
                (
                    0.9 * math.cos(2 * math.pi * i / len(philosophers)),
                    0.9 * math.sin(2 * math.pi * i / len(philosophers)),
                )
            )
            philosopher_texts[i].set_text(
                str(philosophers[i]) if philosophers[i].spaghetti > 0 else "X"
            )
            if philosophers[i].eating:
                philosopher_circles[i].set_color("red")
            else:
                philosopher_circles[i].set_color("black")
            philosopher_circles[i].radius = 0.2 * philosophers[i].spaghetti / m
            fork_lines[i].set_data(
                (
                    0.5 * math.cos(2 * math.pi * i / len(philosophers)),
                    0.5 * math.cos(2 * math.pi * (i + 1) / len(philosophers)),
                ),
                (
                    0.5 * math.sin(2 * math.pi * i / len(philosophers)),
                    0.5 * math.sin(2 * math.pi * (i + 1) / len(philosophers)),
                ),
            )
            # add the labels of the forks as text on the plot
            fork_texts[i].set_position(
                (
                    0.5 * math.cos(2 * math.pi * i / len(philosophers))
                    + 0.5 * math.cos(2 * math.pi * (i + 1) / len(philosophers)),
                    0.5 * math.sin(2 * math.pi * i / len(philosophers))
                    + 0.5 * math.sin(2 * math.pi * (i + 1) / len(philosophers)),
                )
            )
            fork_texts[i].set_text(str(forks[i]))
            if forks[i].picked_up:
                fork_lines[i].set_color("red")
            else:
                fork_lines[i].set_color("black")
        return philosopher_circles + fork_lines + philosopher_texts + fork_texts

    ani = animation.FuncAnimation(
        fig, update, frames=range(100000), interval=10, blit=False
    )
    plt.show()


def table(philosophers: list[Philosopher], forks: list[Fork], m: int):
    """
    Prints the table with the philosophers and forks.

    :param philosophers: The list of philosophers.
    :param forks: The list of forks.
    :param m: The amount of spaghetti each philosopher has.
    """
    while sum(philosopher.spaghetti for philosopher in philosophers) > 0:
        eating_philosophers: int = sum(
            philosopher.eating for philosopher in philosophers
        )
        # clear the screen
        print("\033[H\033[J")
        print("=" * (len(philosophers) * 16))
        # print a line for each philosopher if they are eating, thinking, or done
        print(
            "         ",
            "             ".join(
                ["E" if philosopher.eating else "T" for philosopher in philosophers]
            ),
        )
        print("       ".join(map(str, forks)), "     ", forks[0])
        print(
            "      ",
            "       ".join(map(str, philosophers)),
            "      : ",
            str(eating_philosophers),
        )
        time.sleep(0.1)

class DiningPhilosophers:
    def __init__(self, number_of_philosophers=5, meal_size=7):
        self.meals = [meal_size for _ in range(number_of_philosophers)]
        self.chopsticks = [Fork(i) for i in range(number_of_philosophers)]

    def philosopher(self, i):
        j = (i + 1) % len(self.chopsticks)
        while self.meals[i] > 0:
            time.sleep(random.random())
            if self.chopsticks[i].acquire(blocking=False):  # acquire metodunu kullanarak kilidi denemek
                time.sleep(random.random())
                if self.chopsticks[j].acquire(blocking=False):
                    time.sleep(random.random())
                    self.meals[i] -= 1
                    self.chopsticks[j].release()
                    self.chopsticks[i].release()
                else:
                    self.chopsticks[i].release()

def main():
    n = 5
    m = 7
    dining_phi = DiningPhilosophers(n, m)
    philosophers = [Philosopher(i, dining_phi.chopsticks[i], dining_phi.chopsticks[(i + 1) % n], m) for i in range(n)]

    for philosopher in philosophers:
        philosopher.start()
    threading.Thread(target=table, args=(philosophers, dining_phi.chopsticks, m), daemon=True).start()
    animated_table(philosophers, dining_phi.chopsticks, m)    

    for philosopher in philosophers:
        philosopher.join()

if __name__ == "__main__":
    main()
