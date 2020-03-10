from common.serialtalks import *



arduino = SerialTalks("/dev/ttyS0")

# Connect 
arduino.connect()


class KalmanFilter(object):

    def __init__(self, process_variance, estimated_measurement_variance):
        self.process_variance = process_variance
        self.estimated_measurement_variance = estimated_measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def input_latest_noisy_measurement(self, measurement):
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance

        blending_factor = priori_error_estimate / (priori_error_estimate + self.estimated_measurement_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

    def get_latest_estimated_measurement(self):
        return self.posteri_estimate


#Send some instruction

class LED(SerialTalks):
    def __init__(self,uuid='led'):
        SerialTalks.__init__(self,uuid)

    def led_on(self):
        arduino.send(0x10,BYTE(0))

    def led_off(self):
        arduino.send(0x10,BYTE(1))

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def Trapeze(dt,a1,a2): #Calcul une integrale
    aire = (dt/2)*(a1 +a2)
    return aire

import random
iteration_count = 500

#actual_values = [-0.37727 + j * j * 0.00001 for j in xrange(iteration_count)]
#noisy_measurement = [random.random() * 2.0 - 1.0 + actual_val for actual_val in actual_values]

# in practice we would take our sensor, log some readings and get the
# standard deviation
#import numpy
measurement_standard_deviation = 0#numpy.std([random.random() * 2.0 - 1.0 for j in range(iteration_count)])

# The smaller this number, the fewer fluctuations, but can also venture off
# course...
process_variance = 1e-3
estimated_measurement_variance = measurement_standard_deviation ** 2  # 0.05 ** 2
kalman_filter = KalmanFilter(process_variance, estimated_measurement_variance)
posteri_estimate_graph = []

for iteration in xrange(1, iteration_count):
    kalman_filter.input_latest_noisy_measurement(noisy_measurement[iteration])
    posteri_estimate_graph.append(kalman_filter.get_latest_estimated_measurement())


#Get name
#print("uuid : ", arduino.getuuid())


#On ouvre et on teste la connection
test_co = arduino.execute(0x11)
connection_ok = test_co.read(INT)
print("Si 1, conection MPU ok : " , connection_ok)

calib = arduino.execute(0x13)
AccErrorX,AccErrorY,AccErrorZ,GyroErrorX,GyroErrorY,GyroErrorZ = calib.read(FLOAT,FLOAT,FLOAT,FLOAT,FLOAT,FLOAT)
print("Error accx  :",AccErrorX , "accy = ", AccErrorY , "accz = ", AccErrorZ, "  gyrox = ", GyroErrorX, " gyroy = ", GyroErrorY,"gyroz = ", GyroErrorZ)

time.sleep(2)

#  Get mesure and deserial it
print("Mesure de l'accelération")
t2 = t1 =  time.time()
dt = cptdt = 0
vx1 = vy1= vx2 = vy2 = 0
ax1 = ay1 = gz1 = ax2 = ay2 = gz2 = 0
px = py = ang_gz = 0
offax = AccErrorX
offay = AccErrorY
offgz = GyroErrorZ

while cptdt<30 and connection_ok :
    #Initialisation des variables 
    t1 = t2 
    ax1,ay1,gz1 = ax2,ay2,gz2

    vx1,vy1 = vx2,vy2

    result = arduino.execute(0x12)
    abx,aby,gbz = result.read(FLOAT,FLOAT,FLOAT)
    ax2 = abx - offax # on enlève l'offset
    ay2 = aby - offay
    gz2 = gbz - offgz

    #ax2 = float(truncate(abx,4))
    #ay2 = float(truncate(aby,4))
    #gz2 = float(truncate(gbz,4))

    t2 = time.time()
    dt = t2 - t1
    
    cptdt = dt + cptdt

    print("A :  %.3f" %cptdt,  "%.4f" %ax2  ,"  %.4f" %ay2 ," Gz = %.4f" %gz2)

    #Calculation of the speed
    vx2 += Trapeze(dt,ax1,ax2) *1000
    vy2 += Trapeze(dt,ay1,ay2) *1000

    print("V :          %.3f" %vx2 , "  %.3f" %vy2)

    #Calculation of position (en gros c'est une)
    px += Trapeze(dt,vx1,vx2) 
    py += Trapeze(dt,vy1,vy2) 
    ang_gz += Trapeze(dt,gz1,gz2)
    
    print("P :  %.3f" %cptdt," %.3f" %px , "  %.3f" %py, "  %.3f" %ang_gz)
    #vx2 = vx2 *0.95
    #vy2 = vy2 *0.95

    print(" ")

    

