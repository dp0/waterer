import machine
import utime

# Some values for context:
#  48000 - sensor in air
#  40000 - sensor in dry compost
#  20000 - hand wrapped around sensor
#  18000 - sensor in water
# If the sensor reads above this value, then the soil will be considered dry
DRYNESS_LIMIT = 30000

PUMP_TIME_SECONDS = 1      # When needed, pump for 1 second
PUMP_INTERVAL_SECONDS = 60 # and then wait 60 seconds

led = machine.Pin("LED", machine.Pin.OUT)

# Flash LEDs for an easy-to-detect sign of life when booting
led.low()
utime.sleep_ms(200)
led.high()
utime.sleep_ms(200)
led.low()
utime.sleep_ms(100)
for _ in range(5):
    led.high()
    utime.sleep_ms(20)
    led.low()
    utime.sleep_ms(20)

sensor = machine.ADC(26)

def get_soil_moisture_level():
    return sensor.read_u16()

def is_soil_dry():
    return get_soil_moisture_level() > DRYNESS_LIMIT

gp2 = machine.Pin(2, machine.Pin.OUT)
gp3 = machine.Pin(3, machine.Pin.OUT)

# Command the motor driver to give no power to the pump (i.e. coast)
gp2.low()
gp3.low()

def pump(time_seconds):
    gp2.high()
    gp3.low()
    utime.sleep(time_seconds)
    gp2.low()
    gp3.low()

while True:
    # Sleep at the start of the loop to prevent any system crash loop from
    # triggering more-than-intended pump activity
    utime.sleep(PUMP_INTERVAL_SECONDS)

    # Turn on the LED while we check the moisture level (and pump)
    led.high()
    utime.sleep_ms(50) # Power LED for at least 50ms for a short blink

    if is_soil_dry():
        pump(PUMP_TIME_SECONDS)

    led.low()
