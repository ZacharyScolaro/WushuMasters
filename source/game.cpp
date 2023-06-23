#include "assets.h"
#include "vcsLib.h"
#include <cstddef>

extern "C" int elf_main(uint32_t * args)
{
	// Always reset PC first, cause it's going to be close to the end of the 6507 address space
	vcsJmp3();

	// Init TIA and RIOT RAM
	vcsLda2(0);
	for (int i = 0; i < 256; i++) {
		vcsSta3((unsigned char)i);
	}
	vcsCopyOverblankToRiotRam();

	vcsStartOverblank();

	// Init stuff here while RIOT RAM keeps 6502 busy

	// Render loop
	while (true) {
		vcsEndOverblank();
		vcsSta3(WSYNC);
		vcsSta3(WSYNC);
		vcsSta3(WSYNC);
		vcsSta3(WSYNC);
		vcsSta3(WSYNC);
		vcsSta3(WSYNC);
		int scan_line = 0;
		while(scan_line < 30)
		{
			vcsSta3(WSYNC);
			vcsWrite5(VBLANK, 0);
			vcsWrite5(COLUBK, TitleCOLUBK[scan_line++]);
			vcsJmp3();
		}

		for (int i = 0; i < 32; i++)
		{
			vcsSta3(WSYNC);
			vcsWrite5(VBLANK, 0);
			vcsWrite5(COLUBK, TitleCOLUBK[scan_line++]);
			vcsWrite5(GRP0, TitleGRPGraphics[i]);
			vcsWrite5(GRP1, ReverseByte[TitleGRPGraphics[i]]);
			vcsLda2(TitleGRPColu[i]);
			vcsSta3(COLUP0);
			vcsSta3(COLUP1);
			vcsJmp3();
		}

		while(scan_line < 192)
		{
			vcsSta3(WSYNC);
			vcsLda2(0);
			vcsSta3(VBLANK);
			vcsSta3(GRP0);
			vcsSta3(GRP1);
			vcsWrite5(COLUBK, TitleCOLUBK[scan_line++]);
			vcsJmp3();
		}

		vcsSta3(WSYNC);
		vcsWrite5(VBLANK, 2);
		vcsStartOverblank();
	}
}