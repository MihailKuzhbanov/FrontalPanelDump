//configure network settings (for 192.168.137.5 target, 192.168.137.1 host)
sudo nano /etc/network/interfaces :
  auto eth0
  iface eth0 inet static
  address 192.168.137.5
  netmask 255.255.255.0
  broadcast 192.168.137.255
  gateway 192.168.137.1


//install lxde
sudo apt install lxde

//build kernel img
git clone https://github.com/raspberrypi/linux
git checkout rpi-4.9.y-stable
cd linux
KERNEL=kernel7
make bcm2709_defconfig
make -j4 zImage modules dtbs
sudo make modules_install
sudo cp arch/arm/boot/dts/*.dtb /boot/
sudo cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/
sudo cp arch/arm/boot/dts/overlays/README /boot/overlays/
sudo cp arch/arm/boot/zImage /boot/$KERNEL.img

//add drivers for touchscreen and keypad and modify for current kernel or place modified (rpi-4.9.y-stable) drivers in linux/drivers/...
https://github.com/raspberrypi/linux/blob/rpi-4.9.y-stable/drivers/input/keyboard/tca8418_keypad.c
https://github.com/patrickhwood/linux/blob/kk4.4.2_1.0.0-ga-uib/drivers/input/touchscreen/ssd2543.c

//configure drivers
cd linux
sudo make menuconfig

//select drivers->input-> check "M" on necessary drivers

//build drivers
cd linux
sudo make scripts prepare modules_prepare
make -C . M=drivers/input/touchscreen
make -C . M=drivers/input/keyboard

//build dts
cd /boot/overlays
sudo cp /linux/arch/arm64/boot/dts/ssd2543.dts .
sudo cp /linux/arch/arm64/boot/dts/tca8418_keypad.dts .
sudo dtc -@ -I dts -O dtb -o ssd2543.dtbo ssd2543.dts
sudo dtc -@ -I dts -O dtb -o tca8418_keypad.dtbo tca8418_keypad.dts

//modify config.txt in /boot or place modified config.txt file
gpio=42=op,dh
gpio=43=ip,pu

[all]
dtoverlay=vc4-fkms-v3d
gpu_mem=124

dtoverlay=dpi24
dtoverlay=i2c0-bcm2708,sda0_pin=28,scl0_pin=29
dtoverlay=ssd2543
dtoverlay=tca8418
overscan_left=0
overscan_right=0
overscan_top=0
overscan_bottom=0
framebuffer_width=800
framebuffer_height=480
enable_dpi_lcd=1
display_default_lcd=1
dpi_group=2
dpi_mode=87
dpi_output_format=0x00117
dpi_timings=800 0 0 48 48 480 0 0 3 24 0 0 0 60 0 32000000 6

//rename kernel image to current

//check hardware on addresses 0x34, 0x60, 0x48
sudo i2cdetect -y 0

//reboot and install drivers
cd linux
sudo insmod drivers/input/touchscreen/ssd2543.ko
sudo insmod drivers/input/keyboard/tca8418_keypad.ko

//check interrupts
cat /proc/interrupts

//add autoload modules
/etc/modules :
  i2c-dev
  ssd2543
  tca8418_keypad

cd linux
sudo cp drivers/input/touchscreen/ssd2543.ko /lib/modules/4.9.90-v7+/ssd2543.ko
sudo cp drivers/input/keyboard/tca8418_keypad.ko /lib/modules/4.9.90-v7+/tca8418_keypad.ko

//set chromium start at boot
sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart :
@xset s off
@xset -dpms
@xset s noblank
@chromium-browser --kiosk https://spa.veber.now.sh/

/*troubleshooting*/
black borders on screen : change dpi_timings parameter in config.txt
display colors are wrong : change dpi_output_format in config.txt
driver compiled with warning "undefined symbol" : check used functions in driver source code
driver install with warning "undefined symbol" : compile driver for current kernel
driver install with "segmentation fault" error : check i2c-dev driver in lsmod; check i2c-0 in /dev; check correct i2c_device structure pointer in probe()
