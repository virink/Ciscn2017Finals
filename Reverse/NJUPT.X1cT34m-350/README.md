# Reverse1
是个加密程序，密文：
```
zyXuYsxOz7mU9jmAJjCo6Wq7mFCNY4JLmj3d9OJez6JH9uJAJsGFE7RCP7d2YjxqTl8=
```
用IDA打开程序，发现加密流程主要是sub_401610函数，这其中又经过了4个函数的变换。

## 第一个变换sub_400A30

观察函数流程图，发现经过了ollvm的控制流平坦化变换，使用基于angr与barf的deflat.py脚本进行处理：

```bash
$ python deflat.py Reverse1 0x400A30
```

函数流程为先生成一个`0~0xFFFFFFF`的随机种子，然后生成一系列`0~0xFF`的随机数依次与原字符数组中的每个元素异或。

## 第二个变换sub_400B50
同样是经过了ollvm控制流平坦化，使用deflat.py处理

```bash
$ python deflat.py Reverse1 0x400B50
```

仍然含有一些花指令，可以动态分析也可继续静态分析，函数的功能为先将字符数组转化为大写16进制，然后将16进制分成两栏栅栏加密。

## 第三个变换sub_401100

```bash
$ python deflat.py Reverse1 0x401100
```

是一个变形的vigenere加密算法，对数字也进行了处理。

## 第四个变换sub_4007A0

根据算法的特征，判断这是一个手写的base64编码，字符集有变化。

## 解题过程

1. 自定义base64解码
2. vigenere算法解码
3. 16进制串解栅栏，并变回字符数组
4. 对随机种子爆破，进行异或解密，直到前四位为‘flag’。

## 脚本
```c++
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdbool.h>

int hex2int(char x)
{
	if (x >= 'A' && x <= 'F')
	{
		return x - 65 + 10;
	}
	else return x - 48;
}

const char * base64char = "pGoIFluOwf/r8RBVimY07x6yEPzT9JQgbXKnjqWsHdeUkA+5NCtaSh42DLcv13MZ";

int base64_decode( const char * base64, unsigned char * bindata )
{
	int i, j;
	unsigned char k;
	unsigned char temp[4];
	for ( i = 0, j = 0; base64[i] != '\0' ; i += 4 )
	{
		memset( temp, 0xFF, sizeof(temp) );
		for ( k = 0 ; k < 64 ; k ++ )
		{
			if ( base64char[k] == base64[i] )
				temp[0]= k;
		}
		for ( k = 0 ; k < 64 ; k ++ )
		{
			if ( base64char[k] == base64[i+1] )
				temp[1]= k;
		}
		for ( k = 0 ; k < 64 ; k ++ )
		{
			if ( base64char[k] == base64[i+2] )
				temp[2]= k;
		}
		for ( k = 0 ; k < 64 ; k ++ )
		{
			if ( base64char[k] == base64[i+3] )
				temp[3]= k;
		}

		bindata[j++] = ((unsigned char)(((unsigned char)(temp[0] << 2))&0xFC)) | ((unsigned char)((unsigned char)(temp[1]>>4)&0x03));
		if ( base64[i+2] == '=' )
			break;

		bindata[j++] = ((unsigned char)(((unsigned char)(temp[1] << 4))&0xF0)) | ((unsigned char)((unsigned char)(temp[2]>>2)&0x0F));
		if ( base64[i+3] == '=' )
			break;

		bindata[j++] = ((unsigned char)(((unsigned char)(temp[2] << 6))&0xF0)) | ((unsigned char)(temp[3]&0x3F));
	}
	return j;
}

void xordecrypt(unsigned char * input, char * output, const int length,int seed=0)
{
	srand(seed);
	int i;
	unsigned char key;
	for (i = 0; i < length; i++)
	{
		key = rand() % 0xFF;
		output[i] = input[i] ^ key;
	}
	return;
}

void hexdefence(unsigned char * input, unsigned char * output, int length)
{
	int i;
	unsigned char ch;
	char temp[4096];
	for (i = 0; i < length / 2; i++)
	{
		temp[i] = input[2 * i];
		temp[i + length / 2] = input[2 * i + 1];
	}
	for (i = 0; i < length / 2; i++)
	{
		ch = hex2int(temp[2 * i]) * 16 + hex2int(temp[2 * i + 1]);
		sprintf((char *)(output + i), "%c", ch);
	}
	return;
}

void fuckdecrypt(unsigned char * input, unsigned char * output, int length)
{
	char s[26*26];
	char key[9] = "CODINGAY";
	for (int i = 0; i <= 25; ++i )
	{
		for (int j = 0; j <= 25; ++j )
			*(&s[26 * i] + j) = (i + j) % 26 + 97;
	}
	for (int i = 0; i < length; i++)
	{
		if (input[i] >= 'a' && input[i] <= 'z')
		{
			for (int j = 0; j < 10; j++)
			{
				if (input[i] == s[(key[i % 8] - 65) * 26 + j])
				{
					output[i] = j + 48;
				}
			}

		}
		else
		{
			for (int j = 0; j < 26; j++)
			{
				if (input[i] == (s[(key[i % 8] - 65) + 26 * j]) - 32)
				{
					output[i] = j + 65;
				}
			}
		}
	}
	return;
}

void decrypt(char * input, char * output)
{
	unsigned char temp1[4096]={0};
	unsigned char temp2[4096]={0};
	unsigned char temp[4096]={0};
	int length = base64_decode(input, temp1);
	fuckdecrypt(temp1, temp, length);
	for (int i = 0; i < length; i++)
	{
		printf("%c", temp1[i]);
	}
	puts(" ");
	for (int i = 0; i < length; i++)
	{
		printf("%c", temp[i]);
	}
	puts(" ");
	hexdefence(temp, temp2, length);
	for(int i=0;i<0xffffffff;i++)
	{
		xordecrypt(temp2, output, 4,i);
		if(output[0]=='f'&&output[1]=='l'&&output[2]=='a'&&output[3]=='g') 
		{
			xordecrypt(temp2, output, length / 2,i);
			break;
		}
	}
}

int main()
{
	char input[4096];
	char output[1536];
	puts("Input the string you want to decrypt:");
	gets(input);
	decrypt(input, output);
	printf("The decrypted string is: %s\n", output);
	return 0;
}
```


# Reverse2

程序指令量非常大，使用IDA Python脚本。

## 脚本
```python
import ctypes

flag = [0x92, 0x91, 0xc2, 0xd9, 0xc6, 0x8d, 0x13, 0x8f, 0x0d, 0x3d, 0x92, 0x82, 0x22, 0x2b, 0x58, 0xb5, 0x8c, 0xfa, 0x55, 0xab, 0x0f, 0x36, 0x00, 0x91, 0xa5]

ref = 0x492d32
while (ref > 0x40064e):
	ref = FindCode(ref, SEARCH_UP | SEARCH_NEXT)
	if (GetMnem(ref) == 'nop' or 'byte:694160' in GetOpnd(ref,0) or 'byte_694160' in GetOpnd(ref,1)):
		continue
	if (GetMnem(ref) == 'mov') and ('cs:byte_6941' in GetOpnd(ref, 0)):
		#   print ref
		operate = FindCode(ref, SEARCH_UP | SEARCH_NEXT)
# make offset 694160 as an array, Do not make offset 694100 as an array
		offset = int(GetOpnd(ref, 0)[-2:], 16)
		operator = GetMnem(operate)
		if (operator == 'movzx'):
			ref = operate
# flag[offset - 1] = ctypes.c_ubyte(flag[offset]).value^ctypes.c_ubyte(flag[offset - 1]).value
			continue
	number = GetOpnd(operate, 1)
	if number[-1:] == 'h':
		number = number[-3:-1]
	num = int(number, 16)

#"Reversing"

	if (operator == 'add'):
		ope = '-='
		flag[offset] -= num
	elif (operator == 'sub'):
		ope = '+=' 
		flag[offset] += num
	elif (operator == 'xor'):
		ope = '^='
		flag[offset] = ctypes.c_ubyte(flag[offset]).value ^ ctypes.c_ubyte(num).value

	print "%x" % operate + ": flag[" + str(offset) + "]" , ope , "0x%x" % num + 'u;'

	ref = FindCode(operate, SEARCH_UP | SEARCH_NEXT)

	for i in flag:
		print "%x" % ctypes.c_ubyte(i).value,

	print "\n"

	for i in flag:
		print chr(ctypes.c_ubyte(i).value),
```


# Flag
```
flag{I_th1nk_y0u_ar3_a_g00ooooO0d_R3ver5er_233333}
```




