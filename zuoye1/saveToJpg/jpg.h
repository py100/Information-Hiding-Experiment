#ifndef JPGCONVERTER_H
#define JPGCONVERTER_H

//#define TEST_MODE

#define ALLOW_UNALIGNED

#include "bmp.h"
#include <iomanip>

#define CAPACITY 8
#define BYTE_MASK 0xFF

#pragma pack(push, 1)
struct HuffEntry
{
	BYTE len;
	WORD code;
};
#pragma pack(pop)

const WORD huffLen = 0x01A2;

bool saveToJpg(const char *fileName, unsigned height, unsigned width, const char* mat, const char& quality);
void prepareDCT();
#endif