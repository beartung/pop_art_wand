rm pop_art 
gcc -o pop_art `pkg-config --cflags --libs MagickWand` pop_art.c
./pop_art palette/1886982.palette in/test.jpg dd_1886982.jpg
