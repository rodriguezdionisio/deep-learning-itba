# Funciones para interactuar con la API de Fudo

import json
import requests

def get_access_token():   
    """Get the access token required for accessing the Fudo API.

    Returns:
        str: The access token.
    """
    
    with open('fudo_credentials.json', 'r') as f:
        config = json.load(f)
    
    # Acceder a la apikey y apisecret
    apiKey = config['apikey']
    apiSecret = config['apisecret']

    auth_url = "https://auth.fu.do/api" # URL de autenticación

    payload = {"apiKey": apiKey, "apiSecret": apiSecret} # Defino el payload con las credenciales
 
    header = {"Content-Type": "application/json"} # Defino el header con el tipo de contenido

    response = requests.post(auth_url, json=payload, headers=header) # Hago la petición POST al endpoint de autenticación

    # Verifico si la respuesta es exitosa
    if response.status_code == 200: 
        token = response.json()["token"] # Obtengo el token de la respuesta
        return token
    else:
        print("Error:", response.status_code, response.reason) # Si hay un error, se imprime el código y el mensaje de error
        return None

def fetch_sales_data(access_token, page_size=500, from_page=1, until_page=16):
    base_url = "https://api.fu.do/v1alpha1/items"
    page_size = page_size
    page_number = from_page
    all_sales = []

    while page_number <= until_page:
        query_params = {
            "fields[product]": "active",
            "page[size]": page_size,
            "page[number]": page_number
        }

        # Solicitud a la API
        response = requests.get(base_url, headers={"Authorization": f"Bearer {access_token}"}, params=query_params)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            sales_data = response.json()
            all_sales.extend(sales_data.get("data", []))
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

        if len(sales_data.get("data", [])) < page_size:
            break

        page_number += 1

    return all_sales

def fetch_product_data(access_token):
    
    base_url = "https://api.fu.do/v1alpha1/products"
    page_size = 500
    page_number = 1


    while page_number < 2:
    
        query_params = { #parámetros de la consulta
            "page[size]": page_size,
            "page[number]": page_number
        }

        # Realizar la solicitud a la API
        response = requests.get(base_url, headers={"Authorization": f"Bearer {access_token}"}, params=query_params)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            product_data = response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

        if len(product_data.get("data", [])) < page_size:
            break

        page_number += 1

    return product_data


def fetch_prod_categories_data(access_token):
    
    base_url = "https://api.fu.do/v1alpha1/product-categories"
    page_size = 500
    page_number = 1

    while page_number < 2:
    
        query_params = { # parámetros de la consulta
            "page[size]": page_size,
            "page[number]": page_number
        }

        # Realizar la solicitud a la API
        response = requests.get(base_url, headers={"Authorization": f"Bearer {access_token}"}, params=query_params)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            prod_cat_data = response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

        if len(prod_cat_data.get("data", [])) < page_size:
            break

        page_number += 1

    return prod_cat_data