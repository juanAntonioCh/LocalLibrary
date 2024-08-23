def decorador(divide):
    def envolvente(a,b):
        if (b == 0):
            print("Error, división inválida")
        else:
            return divide(a,b)
    return envolvente


@decorador
def divide(a,b):
    print("a/b", a/b)
    return a/b