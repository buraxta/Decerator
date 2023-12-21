from threading import Thread ,Lock
import time
import random

class DiningPhilosophers:
    def __init__(self,number_of_philosophers = 5,meal_size = 7):
        self.meals = [meal_size for _ in range(number_of_philosophers)]
        self.chopsticks = [Lock() for _ in range(number_of_philosophers)]

    def philosopher(self,i):
        j = (i+1) % 5 
        while self.meals[i] > 0:
            time.sleep(random.random())
            if not self.chopsticks[i].locked():
                self.chopsticks[i].acquire()
                time.sleep(random.random())
                if not self.chopsticks[j].locked():
                    self.chopsticks[j].acquire()
                    time.sleep(random.random())
                    self.meals[i] -= 1
                    self.chopsticks[j].release()
                    self.chopsticks[i].release()
                else:
                    self.chopsticks[i].release()    
    
def main():
    n = 5
    m = 4
    dining_phi = DiningPhilosophers(n,m)
    philosophers = [Thread(target=dining_phi.philosopher,args=(i,))for i in range(n)]
    for philosopher in philosophers:
        philosopher.start()
    while sum(dining_phi.meals) > 0:
        print(dining_phi.meals)
        time.sleep(0.1)
    for philosopher in philosophers:
        philosopher.join()

if __name__ == "__main__":
    main()
