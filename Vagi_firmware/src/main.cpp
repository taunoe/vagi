/*
Vägi - Current and Power monitor
Tauno Erik
Started: 15.05.2023
Edited:  15.05.2023
*/
#include <Arduino.h>
#include <Wire.h>
#include <INA219_WE.h>
#include <Adafruit_NeoPixel.h>

#define I2C_ADDRESS 0x40
INA219_WE ina219 = INA219_WE(I2C_ADDRESS);

const int pin_0 = 0;
const int pin_1 = 1;
const int pin_2 = 2;
const int pin_3 = 3;
const int pin_4 = 4;
const int pin_26 = 26;
const int pin_27 = 27;
const int pin_28 = 28;
const int pin_29 = 29;

const int user_led_green = 16;
const int user_led_red   = 17;
const int user_led_blue  = 25;

const int rgb_power_pin  = 11;
const int rgb_data_pin   = 12;

constexpr int num_of_pins = 14;
int all_pins[num_of_pins] = {
  pin_0,
  pin_1,
  pin_2,
  pin_3,
  pin_4,
  pin_26,
  pin_27,
  pin_28,
  pin_29,
  user_led_green,
  user_led_red,
  user_led_blue,
  rgb_power_pin,
  rgb_data_pin
};

constexpr int NUM_RGB_COLORS = 5;
int rgb_colors[NUM_RGB_COLORS][3] = {
  {254,10,10},
  {10,254,10},
  {10,10,254},
  {254,254,10},
  {10,254,254}
};

// https://learn.microsoft.com/en-us/cpp/cpp/constexpr-cpp?view=msvc-170&viewFallbackFrom=vs-2019
constexpr int RGB_PIXELS = 1;

constexpr int DELAY_TIME = 500;

Adafruit_NeoPixel pixels(RGB_PIXELS, rgb_data_pin, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);

  Wire.begin();
  if(!ina219.init()){
    Serial.println("INA219 not connected!");
  }

  /* Set ADC Mode for Bus and ShuntVoltage
  * Mode *            * Res / Samples *       * Conversion Time *
  BIT_MODE_9        9 Bit Resolution             84 µs
  BIT_MODE_10       10 Bit Resolution            148 µs  
  BIT_MODE_11       11 Bit Resolution            276 µs
  BIT_MODE_12       12 Bit Resolution            532 µs  (DEFAULT)
  SAMPLE_MODE_2     Mean Value 2 samples         1.06 ms
  SAMPLE_MODE_4     Mean Value 4 samples         2.13 ms
  SAMPLE_MODE_8     Mean Value 8 samples         4.26 ms
  SAMPLE_MODE_16    Mean Value 16 samples        8.51 ms     
  SAMPLE_MODE_32    Mean Value 32 samples        17.02 ms
  SAMPLE_MODE_64    Mean Value 64 samples        34.05 ms
  SAMPLE_MODE_128   Mean Value 128 samples       68.10 ms
  */
  //ina219.setADCMode(SAMPLE_MODE_128); // choose mode and uncomment for change of default
  
  /* Set measure mode
  POWER_DOWN - INA219 switched off
  TRIGGERED  - measurement on demand
  ADC_OFF    - Analog/Digital Converter switched off
  CONTINUOUS  - Continuous measurements (DEFAULT)
  */
  // ina219.setMeasureMode(CONTINUOUS); // choose mode and uncomment for change of default
  
  /* Set PGain
  * Gain *  * Shunt Voltage Range *   * Max Current (if shunt is 0.1 ohms) *
   PG_40       40 mV                    0.4 A
   PG_80       80 mV                    0.8 A
   PG_160      160 mV                   1.6 A
   PG_320      320 mV                   3.2 A (DEFAULT)
  */
  ina219.setPGain(PG_320); // choose gain and uncomment for change of default
  
  /* Set Bus Voltage Range
   BRNG_16   -> 16 V
   BRNG_32   -> 32 V (DEFAULT)
  */
  ina219.setBusRange(BRNG_16); // choose range and uncomment for change of default

  /* If the current values delivered by the INA219 differ by a constant factor
     from values obtained with calibrated equipment you can define a correction factor.
     Correction factor = current delivered from calibrated equipment / current delivered by INA219
  */
  // ina219.setCorrectionFactor(0.98); // insert your correction factor if necessary
  
  /* If you experience a shunt voltage offset, that means you detect a shunt voltage which is not 
     zero, although the current should be zero, you can apply a correction. For this, uncomment the 
     following function and apply the offset you have detected.   
  */
  // ina219.setShuntVoltOffset_mV(0.5); // insert the shunt voltage (millivolts) you detect at zero current 


  for (int i = 0; i < num_of_pins; i++){
    pinMode(all_pins[i], OUTPUT);
  }

  digitalWrite(rgb_power_pin, HIGH); // RGB Power ON

  pixels.begin();
}

void loop() {
  float shuntVoltage_mV = 0.0;
  float loadVoltage_V = 0.0;
  float busVoltage_V = 0.0;
  float current_mA = 0.0;
  float power_mW = 0.0; 
  bool ina219_overflow = false;
  
  shuntVoltage_mV = ina219.getShuntVoltage_mV();
  busVoltage_V = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  power_mW = ina219.getBusPower();
  loadVoltage_V  = busVoltage_V + (shuntVoltage_mV/1000);
  ina219_overflow = ina219.getOverflow();

  Serial.print("Shunt_mv:");    Serial.print(shuntVoltage_mV);
  Serial.print(", Bus_v:");     Serial.print(busVoltage_V);
  Serial.print(", Load_v:");    Serial.print(loadVoltage_V);
  Serial.print(", Current_mA:");Serial.print(current_mA);
  Serial.print(", Power_mW:");  Serial.print(power_mW);
  Serial.println();

  delay(100);

}
