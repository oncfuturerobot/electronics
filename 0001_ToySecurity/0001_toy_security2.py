from gpiozero import DistanceSensor
ultrasonic = DistanceSensor(echo=23, trigger=24, threshold_distance=0.1)

while True: 
    print("distance =",ultrasonic.distance*1000)
