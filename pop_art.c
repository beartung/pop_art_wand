#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <wand/MagickWand.h>

int palette[5][3] = {
    { 0xEF, 0xC6, 0x16 },
    { 0xDC, 0x15, 0x1A },
    { 0x16, 0x55, 0x9A },
    { 0x0F, 0x30, 0x65 },
    { 0x15, 0x8B, 0x71 },
};

void print_palette(){
    int i;
    int j;
    printf("--    using palette   --\n");
    for (i = 0; i < 5; i++){
        for (j = 0; j < 3; j++){
            printf("0x%02X[%03d] ", palette[i][j], palette[i][j]);
        }
        printf("\n");
    }
    printf("----\n");
}

void read_palette(char * path){
    FILE *fp;
    fp = fopen(path, "r");
    if (fp == NULL) {
        printf("no such palette!\n");
        exit(0);
    }
    int i = 0;
    int j = 0;
    for (i = 0; i < 5; i++){
        for (j = 0; j < 3; j++){
            fscanf(fp, "%x", &palette[i][j]);
        }
    }
    fclose(fp);
}

static float get_color(float r, int index){
    int ix = 0;
    if (r < 50){
        ix = 0;
    }else if (r < 100){
        ix = 1;
    }else if (r < 150){
        ix = 2;
    }else if (r < 200){
        ix = 3;
    }else{
        ix = 4;
    }
    return palette[ix][index]*257;
}



static MagickBooleanType recolor(WandView *view, const ssize_t y, const int id, void *context){

  RectangleInfo extent;
  MagickPixelPacket pixel;
  PixelWand **pixels;
  register ssize_t x;
  register float t;

  extent = GetWandViewExtent(view);
  pixels = GetWandViewPixels(view);
  for (x = 0; x < (ssize_t) (extent.width - extent.x); x++){
    PixelGetMagickColor(pixels[x], &pixel);
    t = ScaleQuantumToChar(pixel.red);
    pixel.red = get_color(t, 0);
    pixel.green = get_color(t, 1);
    pixel.blue = get_color(t, 2);
    PixelSetMagickColor(pixels[x], &pixel);
  }
  return(MagickTrue);
}

int main(int argc, char **argv){
    if (argc != 4){
        (void) fprintf(stdout,"Usage: %s palette input-file output-file\n",argv[0]);
        exit(0);
    }
    read_palette(argv[1]);
    print_palette();
    
    char *description;
    ExceptionType severity;


    #define ThrowWandException(wand) \
    { \
        description=MagickGetException(wand,&severity); \
        (void) fprintf(stderr,"%s %s %lu %s\n",GetMagickModule(),description); \
        description=(char *) MagickRelinquishMemory(description); \
        exit(-1); \
    }

    MagickBooleanType status;
    MagickPixelPacket pixel;
    MagickWand *wand;
    WandView *view;
    /*
       Read an image.
       */
    MagickWandGenesis();
    wand = NewMagickWand();
    status = MagickReadImage(wand, argv[2]);
    if (status == MagickFalse) ThrowWandException(wand);

    /*
       Sigmoidal non-linearity contrast control.
       */
    view = NewWandView(wand);
    if (view == (WandView *) NULL) ThrowWandException(wand);
    status = UpdateWandViewIterator(view, recolor, (void *)NULL);
    if (status == MagickFalse) ThrowWandException(wand);
    view = DestroyWandView(view);

    /*
       Write the image then destroy it.
       */
    status = MagickWriteImages(wand, argv[3], MagickTrue);
    if (status == MagickFalse) ThrowWandException(wand);
    wand = DestroyMagickWand(wand);
    MagickWandTerminus();

    return 0;
}
