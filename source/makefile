wushu_masters: *.cpp assets
	arm-none-eabi-gcc -r -mlong-calls -fno-exceptions -march=armv6-m *.cpp -oWushuMasters.bin -O3 -Wall -lgcc
	arm-none-eabi-strip WushuMasters.bin -d -R.comment -R.ARM.attributes
	cp WushuMasters.bin ../../ChameleonCartFirmware/Core/Lib/libelfrom.a
	touch ../../ChameleonCartFirmware/Core/Src/main.c
	../../Gopher2600/gopher2600 WushuMasters.bin

assets: ../assets/** 
	python3 parse_assets.py

