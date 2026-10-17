
import requests


def obtener_datos(url):
    respuesta = requests.get(url, timeout=10)
    respuesta.raise_for_status()
    return respuesta.json()


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts/1"
    resultado = obtener_datos(url)
    print(resultado)
