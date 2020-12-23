# Autonomous Robots: Localization
Repositary for Localization Course

Course link: https://www.udemy.com/course/autonomous-robots-localization/

Required Packages <br>
python=3.7.4 <br>
numpy=1.16.4 <br>
matploblib=3.1.0

<h4>Assigment 1: Least Squares</h4>
-> Based on locations of poles and distance from robot´s position to each of the pole calculate robot´s location.<br>
-> You don´t know which measuremnet corespond to which pole. <br>
-> Based on cost function, you will find the location with lowest total cost.<br>
-> Cost function: (Minimal total distance diference between guess location and pole measurements)**2 <br>

<h4>Assigment 2: Bayes rule</h4>
-> Bayes rule used to determinate location of robot in 1D world <br>
-> Bayes rule is used to update probability of some phenomena based on new observation or in other words update your beliefs based on evidence <br>
-> Bayes rule: https://en.wikipedia.org/wiki/Bayes%27_theorem or https://www.youtube.com/watch?v=HZGCoVF3YvM <br>
-> 2-1 -> Robot moves every time exactly same distance with 0 uncertainty <br>
-> 2-2 -> Robots moves with some move uncertainty <br>

<h4>Assigment 3: 1D Particle filter</h4>
-> Using Particle filter to determinate location of robot in 1D world <br>
-> Particle filter used multiple particles (virtual copy of robot) to determinate it position. <br>
In every loop particles will: <br>
    1. Move -> movement of particles is identical to real movement of robot. Only difference is that every particle moves with some uncertainty which is based on gaussian distribution <br>
    2. Measure -> Robot and particles scan its environment. Measurement has also some uncertainty <br>
    3. Update -> Based on difference between what robot sees and particle sees weights are calculated. <br>
    4. Resample -> Some portion of particles with the highest weights will be choosen to be fundamental, and rest of the particles will be resampled around these fundamentals ones. <br>

<h4>Assigment 4: 2D Particle filter</h4>
-> Using Particle filter to determinate location of robot in 2D world
