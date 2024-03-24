#ifndef __EXAMPLE_C__
#define __EXAMPLE_C__
#include "example.c"

void hola_mundo(int a, int c, char d) { 
    /*
     *  agrs: 
     *      - a numero entero sirve para x
     *      - b numero entero, sirve para calcular c
     *      - c resultado
     *  return: void (vacio == nada)
     * 
     */
    puts("hola mundo"); 
}
uint8_t adios_3mundo(void) { puts("adios mundo"); }
long long __attribute__((destructor)) __destructor_debug_c__()
{

    puts(1);
    return 10;
}
long __attribute__((constructor)) mi_constructy()
{
    puts(1);
    puts(1);
    return 0xff;
}
int a = 0000;
#define hola(a) puts(aa)

char *__attribute__((atre2_ibuto1)) __attribute__((atrib_uto1)) __attribute__((atributo1)) a33423() {}
int __attribute__((asdsa)) a34() {}

#endif
