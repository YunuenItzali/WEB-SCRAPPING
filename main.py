import re
from bs4 import BeautifulSoup
import requests

def web_scraping(url):
    # Realiza una solicitud a la página web
    r = requests.get(url)

    # Parsea el contenido de la página con BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')

    # Busca todas las etiquetas img con la clase específica
    img_tags = soup.find_all('img', {'class': 'stylesSliderProductoDesktop_imagenActual__E09ko'})

    # Verifica si se encontraron etiquetas de imagen
    if img_tags:
        # Obtiene la etiqueta de imagen en la posición 1
        img_tag = img_tags[1]

        # Obtiene la URL de la imagen
        img_url = img_tag['src']

        # Imprime la URL de la imagen
        print("URL de la imagen: " + img_url)
    else:
        print("No se encontraron imágenes del producto.")

    # Busca la etiqueta li con las clases específicas
    li_tag = soup.find('li', {'class': ['stylesTabs_react_tabs__tab__K6CXq', 'stylesTabs_react_tabs__tab__selected__nJ2fq']})

    # Verifica si se encontró la etiqueta li
    if li_tag:
        # Obtiene el texto dentro de la etiqueta li
        text = li_tag.text

        # Imprime el texto
        print(text + ": ")
    else:
        print("No se encontró información adicional del producto.")

    # Busca la etiqueta div con la clase específica para descripción y precios
    div_tag_desc = soup.find('div', {'class': 'stylesTabs_textDescriptionSears__dSv_W'})
    div_tag_price = soup.find('div', {'class': 'stylesShopData_pPrice__PvS_6'})

    # Verifica si se encontró la descripción del producto
    if div_tag_desc:
        # Obtiene el texto dentro de la etiqueta div para descripción
        description = div_tag_desc.text

        # Imprime la descripción
        print(description)
    else:
        print("No se encontró una descripción del producto.")

    # Verifica si se encontró información de precios del producto
    if div_tag_price:
        # Obtiene el texto dentro de la etiqueta div para precios
        text_price = div_tag_price.text

        # Divide el texto de precios en partes usando una expresión regular
        parts_price = re.split(' ', text_price)

        # Elimina los elementos vacíos de la lista
        parts_price = [part for part in parts_price if part]

        try:
            # Elimina "MXN", "$" y "," de las partes y convierte a int
            precio_original = int(parts_price[1].replace("MXN", "").replace("$", "").replace(",", ""))
            precio_con_descuento = int(parts_price[0].replace("$", ""))

            # Calcula el porcentaje de descuento
            descuento = ((precio_original - precio_con_descuento) / precio_original) * 100

            # Almacena los resultados de precios y descuento en una variable
            price_info = "\nPrecio y descuento:\n" + "El precio original es de $" + str(precio_original) + " MXN" + " teniendo un " + str(round(descuento, 2)) + "% de descuento, el precio sería de $" + str(precio_con_descuento) + " MXN"
        except ValueError:
            # Si ocurre un error al convertir a int, almacena solo el precio en la variable
            price_info = "El producto no contiene un descuento, su precio es de: " + parts_price[0] + " MXN"
    else:
        price_info = "No se encontró información de precios del producto."
    

    div_tag_review = soup.find('div', {'class': 'stylesReviews_moduleOpinionDesk__TJ2YG'})

    # Verifica si se encontraron opiniones de los clientes
    if div_tag_review:
        text_review = div_tag_review.text
        parts_review = re.split('(\d+)', text_review)

        # Almacena los resultados concatenando las partes en una sola cadena
        reviews = "\n" + parts_review[0] + " o calificación general de los usuarios: " + parts_review[1] + "." + parts_review[3]
    else:
        reviews = "No se encontraron opiniones de los clientes."
    
    # Al final de la función, devuelve un diccionario con los resultados
    return {
        "img_url": img_url,
        "additional_info": text,
        "description": description,
        "price_info": price_info,
        "reviews": reviews
    }