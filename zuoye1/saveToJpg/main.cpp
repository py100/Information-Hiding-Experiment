#include "jpg.h"
#include <string>

using namespace std;

extern HuffEntry huffTable_AC_0[255];
extern HuffEntry huffTable_AC_1[255];
extern BYTE huffData[huffLen];

bool fillHuffTables()
{
	std::ifstream AC0("AC0.txt");
	std::ifstream AC1("AC1.txt");
	if (!AC0 || !AC1)
	{
		cerr << "Cannot load huffman tables" << endl;
		return false;
	}
	unsigned i, j;
	std::string res0, res1;
	std::string len0, len1;
	BYTE cat;
	for (i = 0; i <= 0xF; ++i)
		for (j = 0; j <= 0xA; ++j)
		{
			if (j != 0 || (i == 0 || i == 0xF))
			{
				AC0 >> res0 >> len0 >> res0;
				AC1 >> res1 >> len1 >> res1;
				cat = (i << 4) | j;
				huffTable_AC_0[cat].len = strtol(len0.data(), nullptr, 10);
				huffTable_AC_0[cat].code = strtol(res0.data(), nullptr, 2);
				huffTable_AC_1[cat].len = strtol(len1.data(), nullptr, 10);
				huffTable_AC_1[cat].code = strtol(res1.data(), nullptr, 2);
			}
		}
	AC0.close();
	AC1.close();
	return true;
}

bool fillHuffData()
{
	std::ifstream huffIn("HuffData.txt");
	if (!huffIn)
	{
		cerr << "Cannot load JPEG headers data" << endl;
		return false;
	}
	std::string res;
	for (unsigned i = 0; i < huffLen; ++i)
	{
		huffIn >> res;
		huffData[i] = strtol(res.data(), nullptr, 16);
	}
	huffIn.close();
}

int main()
{
	fillHuffTables();
	fillHuffData();
	prepareDCT();
	unsigned height, width;

	int quality = 50;
	unsigned long long sizeIn, sizeOut;
	string bmp, jpg;
	RGB *data;
	jpg = "out.jpg";
	string mat = "mat.txt";
	ifstream mat_in(mat);
	mat_in >> width >> height;
	mat_in.close();
	if ( saveToJpg(jpg.data(), height, width, "mat.txt", quality) )
		cout << "save ok" << endl;
	else
		cout << "save error" << endl;
	return 0;
}
