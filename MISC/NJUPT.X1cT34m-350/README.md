# MISC 350 - Coding Gay

首先把图片下下来，找jpg的文件尾FF D9，将第一个FF D9之后的内容分离出来。

然后观察分离出的文件，是PNG的头PNG的尾，但是文件结构仍然是JPG的。

```
89 50 4E 47 -> FF D8 FF E1
```

```
AE 42 60 82 -> FF D9
```

得到一张flag is not here的图片。

这里有个脑洞，改图片的长度为800像素。

```
00 64 -> 03 20
```

对比两张图片，发现是反相了，并有一些奇怪的线条。

用PS把另一张图片反相，然后用“减去”方法覆盖图层。（实际上只要能看清，怎么覆盖都可以），拼起来得到一个key
```
NjUp7_Cg_T34m
```

对原图用outguess，用这个key。

```
outguess -r logo.jpg -k NjUp7_Cg_T34m flag
```

# Flag

```
flag{S0shit3_wat4shiTach1_w4_m3gur1aU}
```