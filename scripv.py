# Importar las librerias imaplib, email, decode_header re y request
import imaplib
import email
from email.header import decode_header
import re
import requests

# Datos del usuario
username = ""
password = ""
remitente = ""

# Creación de la conexión con el servidor IMAP de Gmail
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# Inicio de sesión con las credenciales del usuario
imap.login(username, password)

# Selección de la bandeja de entrada
imap.select("INBOX")

# Busqueda de mensajes en la bandeja de entrada del remitente especificado
status, mensajes_filtrados = imap.search(None, f'FROM "{remitente}"')

# Calculo del número de mensajes a recibir
N = len(mensajes_filtrados)+1

# Creación de una lista vacía para almacenar los enlaces PDF
pdf_links = []

# Definición de una función para obtener los enlaces en el cuerpo de un correo electrónico
def get_links_from_email_body(email_body):
    # Búsqueda de enlaces en el cuerpo del correo usando una expresión regular
    linksOr = re.findall(r'http[s]?://mvb451.fe32.fdske.com/ec(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_body)
    return linksOr

# Definición de una función para obtener los enlaces PDF a partir de una URL
def get_pdf_links(url):
    # Realizar una petición GET a la URL
    response = requests.get(url)
    # Verificación del éxito de la petición
    if response.status_code == 200:
        # Obtener el tipo de contenido de la respuesta
        content_type = response.headers.get("Content-Type")
        # Verificación si el tipo de contenido es "application/pdf"
        if content_type == "application/pdf":
            # Adición de la URL a la lista de enlaces PDF
            pdf_links.append(url)

# Convertir la lista de mensajes en una lista de enteros
mensajes_filtrados = mensajes_filtrados[0].split()
mensajes_filtrados = [int(i) for i in mensajes_filtrados]

# Seleccionar los primeros N mensajes
mensajes_filtrados = mensajes_filtrados[:N]

# Obtener el último mensaje de la lista
ultimo_mensaje = mensajes_filtrados[-1]

def get_link_last_email(correo):
# Intentar obtener el mensaje de correo electrónico
    try:
        res, mensaje = imap.fetch(str(correo), "(RFC822)")
    except:
        print("Error")
    # Recorrer las respuestas de mensaje
    for respuesta in mensaje:
        # Recorrer las respuestas de mensaje
        if isinstance(respuesta, tuple):
            # Obtener el contenido del mensaje
            mensaje = email.message_from_bytes(respuesta[1])
            # Decodificar el asunto del mensaje
            subject = decode_header(mensaje["Subject"])[0][0]
            # Si el asunto está en formato de bytes, convertirlo a string
            if isinstance(subject, bytes):
                subject = subject.decode()
            # Obtener el remitente, la fecha y el contenido del mensaje
            from_ = mensaje.get("From")
            date_ = mensaje.get("Date")
            print("Subject:", subject)
            print("From:", from_)
            print("Date:",date_)
            print("Mensaje obtenido con exito")
            # Obtener los enlaces del cuerpo del mensaje
            body = mensaje.get_payload(decode=True).decode()
            linksOr = get_links_from_email_body(body)
            # Recorrer los enlaces y obtener los enlaces a PDF
            for link in linksOr:
                get_pdf_links(link)
            # Obtener el último enlace en la lista de enlaces PDF
            ultimo_elemento = pdf_links[-1]
            print(ultimo_elemento)

#ejecutar el script
get_link_last_email(ultimo_mensaje)

#cerrar la conexion
imap.close()
imap.logout()