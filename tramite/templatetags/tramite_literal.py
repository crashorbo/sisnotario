def unidades(x):
    if x == 0:
        unidad = "CERO"
    if x == 1:
        unidad = "UN"
    if x == 2:
        unidad = "DOS"
    if x == 3:
        unidad = "TRES"
    if x == 4:
        unidad = "CUATRO"
    if x == 5:
        unidad = "CINCO"
    if x == 6:
        unidad = "SEIS"
    if x == 7:
        unidad = "SIETE"
    if x == 8:
        unidad = "OCHO"
    if x == 9:
        unidad = "NUEVE"
    return unidad

def teens(x):
    if x == 0:
        teenname = "DIEZ"
    if x == 1:
        teenname = "ONCE"
    if x == 2:
        teenname = "DOCE"
    if x == 3:
        teenname = "TRECE"
    if x == 4:
        teenname = "CATORCE"
    if x == 5:
        teenname = "QUINCE"
    return teenname


def tens(x):
    if x == 1:
        tensname = "DIEZ"
    if x == 2:
        tensname = "VEINTE"
    if x == 3:
        tensname = "TREINTA"
    if x == 4:
        tensname = "CUARENTA"
    if x == 5:
        tensname = "CINCUENTA"
    if x == 6:
        tensname = "SESENTA"
    if x == 7:
        tensname = "SETENTA"
    if x == 8:
        tensname = "OCHENTA"
    if x == 9:
        tensname = "NOVENTA"
    return tensname

def tercia(num):
    numero=str(num)
    if len(numero) == 1:
        numero='00'+numero
    if len(numero) == 2:
        numero='0'+numero
    a=int(numero[0])
    b=int(numero[1])
    c=int(numero[2])
#       print a, b, c
    if a == 0:
        if b == 0:
            resultado=unidades(c)
            return resultado
        elif b == 1:
            if c >= 0 and c <= 5:
                resultado = teens(c)
                return resultado
            elif c >= 6 and c <= 9:
                resultado = 'DIECI'+unidades(c)
                return resultado
        elif b == 2:
            if c == 0:
                resultado = 'VEINTE'
                return resultado
            elif c > 0 and c <= 9:
                resultado ='VEINTI '+unidades(c)
                return resultado
        elif b >=3 and b <= 9:
            if c == 0:
                resultado = tens(b)
                return resultado
            if c >= 1 and c <= 9:
                resultado = tens(b)+' Y '+unidades(c)
                return resultado
    if a == 1:
        if b == 0:
            if c == 0:
                resultado = 'CIEN'
                return resultado
            elif c > 0 and c <= 9:
                resultado ='CIENTO '+unidades(c)
                return resultado
        elif  b == 1:
            if c >= 0 and c <= 5:
                resultado = 'CIENTO '+teens(c)
                return resultado
            elif c >= 6 and c <= 9:
                resultado = 'CIENTO '+tens(b)+' Y '+unidades(c)
                return resultado
        elif b == 2:
            if c == 0:
                resultado = 'CIENTO VEINTE'
                return resultado
            elif c > 0 and c <= 9:
                resultado ='CIENTO VEINTI '+unidades(c)
                return resultado
        elif b >= 3 and b <= 9:
            if c == 0:
                resultado = 'CIENTO '+tens(b)
                return resultado
            elif c > 0 and c <= 9:
                resultado = 'CIENTO '+tens(b)+ ' Y '+unidades(c
)
                return resultado

    elif a >= 2 and a <= 9:
        if a == 5:
            prefix='QUINIENTO '
        elif a == 7:
            prefix='SETECIENTOS '
        elif a == 9:
            prefix='NOVECIENTOS '
        else:
            prefix=unidades(a)+' CIENTOS '
        if b == 0:
            if c == 0:
                resultado = prefix
                return resultado
            elif c > 0 and c <= 9:
                resultado = prefix+unidades(c)
                return resultado
        elif b == 1:
            if c >= 0 and c <= 5:
                resultado = prefix+teens(c)
                return resultado
            elif c >= 6 and c <= 9:
                resultado = prefix+tens(b)+' Y '+unidades(c)
                return resultado
        elif b == 2:
            if c == 0:
                resultado = prefix+' VEINTE'
                return resultado
            elif c > 0 and c <= 9:
                resultado = prefix+' VEINTI '+unidades(c)
                return resultado
        elif b >= 3 and b <= 9:
            if c == 0:
                resultado = prefix+tens(b)
                return resultado
            elif c > 0 and c <= 9:
                resultado = prefix+tens(b)+' Y '+unidades(c)
                return resultado
def main(num):
    result=''
    numero=str(num)
    if len(numero) == 1:
        numero='00000000'+numero
    if len(numero) == 2:
        numero='0000000'+numero
    if len(numero) == 3:
        numero='000000'+numero
    if len(numero) == 4:
        numero='00000'+numero
    if len(numero) == 5:
        numero='0000'+numero
    if len(numero) == 6:
        numero='000'+numero
    if len(numero) == 7:
        numero='00'+numero
    if len(numero) == 8:
        numero='0'+numero
    posicion=1
    for i in [0,3,6]:
        var=numero[i]+numero[i+1]+numero[i+2]
        if int(var) != 0:
            res=tercia(var)
            if i == 0:
                result=res+" MILLONES "
            elif i == 3:
                result=result+res+" MIL "
            elif i == 6:
                result=result+res
    return result 