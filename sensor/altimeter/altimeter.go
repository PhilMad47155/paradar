package altimeter

import (
	"fmt"
	"log"
	"math"
	"sync"
	"time"

	"github.com/blinken/paradar/sensor"

	"periph.io/x/periph/conn/gpio"
	"periph.io/x/periph/host/bcm283x"
)

type altimeter struct {
	mutex         sync.RWMutex
	sb            sensor.Bus
	altitude_ft   int32
	pressure_hpa  float64
	temperature_c float64
}

const (
	regCtrl1    uint8 = 0x10
	regCtrl2    uint8 = 0x11
	regCtrl3    uint8 = 0x12
	regCtrlFifo uint8 = 0x14
	regResult1  uint8 = 0xa8 // LSB
	regResult2  uint8 = 0xa9
	regResult3  uint8 = 0xaa // MSB
)

var gpioChipSelect = bcm283x.GPIO2
var gpioDataReady = bcm283x.GPIO3

func NewAltimeter(sb *sensor.Bus) *altimeter {
	gpioChipSelect.Out(gpio.High)
	return &altimeter{sb: *sb}
}

func (a *altimeter) Tx(write []byte) []byte {
	return a.sb.Tx(write, gpioChipSelect)
}

func (a *altimeter) Track() {
	fmt.Printf("altimeter tracking\n")

	if err := gpioDataReady.In(gpio.PullDown, gpio.RisingEdge); err != nil {
		log.Fatal(err)
	}

	// [0], 25Hz update rate [011], Weak low pass filter enable (update rate/9) [10], BDU enabled (reads block updates) [1], 4-wire SPI [0]
	a.Tx([]byte{regCtrl1, 0x3a})
	// Reboot [0], FIFO enable [00], Auto-increment registers on read [1], I2C Disabled [1], Reset [0], [0], One-shot mode [0]
	a.Tx([]byte{regCtrl2, 0x18})
	// Interrupt active-low [0] (active-high), interrupt push-pull(0) vs open-drain (1) [0], FIFO things [000], DRDY pin enable [100]
	a.Tx([]byte{regCtrl3, 0x04})

	// Clear the result register to begin
	// 24-bit pressure
	// 16-bit temperature
	a.Tx([]byte{
		regResult1,
		0x00, 0x00, 0x00,
		0x00, 0x00,
	})

	for {
		// Set a 1s timeout so we read even if there's no edge triggered, to avoid
		// getting into a bad state
		gpioDataReady.WaitForEdge(time.Second)

		r := a.Tx([]byte{
			regResult1,
			0x00, 0x00, 0x00,
			0x00, 0x00,
		})

		pressure_hpa := float64(a.sb.UnpackLEInt24(r[1:4])) / 4096
		temperature_c := float64(a.sb.UnpackInt16(r[4:6])) / 100

		// Note this is IACO standard pressure altitude - assuming MSL pressure of 1013.25
		// hPa and temperature of 15 degrees. We are expected to transmit this
		// number in GDL90 but it does not equal height above ground!
		// ref https://www.weather.gov/media/epz/wxcalc/pressureAltitude.pdf, https://en.wikipedia.org/wiki/Pressure_altitude
		altitude_ft := 145366.45 * (1 - math.Pow((pressure_hpa/1013.25), 0.190284))

		a.mutex.Lock()
		a.altitude_ft = int32(altitude_ft)
		a.pressure_hpa = pressure_hpa
		a.temperature_c = temperature_c
		a.mutex.Unlock()
	}
}

func (a *altimeter) SelfTest() bool {
	// WHO_AM_I register should read 0xb1
	read := a.Tx([]byte{0x8f, 0x00})

	return (int(read[1]) == 0xb1)
}

// Altitude in ft
func (a *altimeter) GetAltitude() int32 {
	a.mutex.RLock()
	defer a.mutex.RUnlock()

	return a.altitude_ft
}

// Temperature in celcius (note - precise but not accurate due to board temp)
func (a *altimeter) GetTemperature() float64 {
	a.mutex.RLock()
	defer a.mutex.RUnlock()

	return a.temperature_c
}

// Pressure in hPa
func (a *altimeter) GetPressure() float64 {
	a.mutex.RLock()
	defer a.mutex.RUnlock()

	return a.pressure_hpa
}
