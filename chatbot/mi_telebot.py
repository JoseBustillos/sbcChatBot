import json
from snips_prueba import pregunta, tipos, definicion, kichua, grupo, imagen
import telebot
import random
import os.path
import time

# colocar token de acceso
bot = telebot.TeleBot('619649693:AAG3QIMhSymCaJIk9aiSQxp3ExJIrqNOP9U')


# comandos de inicio y ayuda
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # presentar mensaje con los comandos
    bot.reply_to(message, "Hola, en que te puedo ayudar?\n Se de plantas ornamentales")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # archivo de control de palabras erroneas
    chatid = message.chat.id
    f = open('registroError.txt', "a")
    f1 = open('registroChat.txt', 'a')
    print('\n*************    METODO PRINCIPAL    *************')
    # lista de los respuestas cuando existe un error o no entiende la pregunta
    respuestaError = [' ', 'ups, no entendi tu pregunta', 'puedes revizar tu pregunta',
                      'lo lamento para mas tarde te respondo']
    chat_id = message.chat.id
    print('\nCHAT id:')
    nombre = message.chat.first_name
    apellido = message.chat.last_name
    print(nombre)
    print(apellido)
    dia = time.strftime("%d/%m/%y")
    hora = time.strftime("%H:%M:%S")
    f.write('\n' + str(chat_id) + ';' + nombre + ';' + apellido + ';' + dia + ';' + hora)
    f1.write('\n' + str(chat_id) + ';' + nombre + ';' + apellido + ';' + dia + ';' + hora)
    # control para la seleccion del texto ingresado
    try:
        texto = message.json['text']
        print("\nTEXTO: ")
        f.write(';' + texto)
        f1.write(';' + texto)
    except AttributeError:
        texto = "N/A"
    # procesamiento del texto ingresado para su identificacion
    try:
        print(texto)
        respuesta_json = json.loads(pregunta(texto))
        print(pregunta(texto))
        print('\nRESPUESTA JSON: ')
        if (len(respuesta_json['slots']) == 0):
            e = open('entidad.txt', 'r')
            mensaje = e.read()
            print(mensaje)
            e.close()
            texto = message.json['text']
            texto2 = texto, ' ', mensaje
            respuesta_json = json.loads(pregunta(texto2))
        print(respuesta_json)

        # captura de la intencion
        intencion = respuesta_json['slots'][0]['entity']
        # captura de la entidad a preguntar
        entidad = respuesta_json['slots'][0]['value']['value']
        if (len(entidad) > 0):
            e = open('entidad.txt', 'w')
            e.write(entidad)
            e.close()
        print(len(intencion), len(entidad))
        print('\nINTENCION-ENTIDAD: \n' + intencion + '-' + entidad)
        # las condiciones se usan para identificar el tipo de intencion
        respuesta = ''
        if (intencion == 'tipo'):
            for i in respuesta_json['slots']:
                entidad1 = i['value']['value']
                print('\n SEGUNDA ENTIDAD: ')
                print(entidad1)
            # metodo para la consulta a virtuoso
            lista_plantas = tipos(entidad1)
            # control de la consulta si no existe respuesta
            if (len(lista_plantas) != 0):
                respuesta = ""
                # almacena los nombres de preguntas con varias respuestas
                lista_nombres_plantas = []
                # obteniendo los resultados para presentarlos
                for i in lista_plantas:
                    lista_nombres_plantas.append(i[0:])
                # presentacion de datos junto con el conteo
                respuesta = "Por el momento conosco " + str(len(lista_nombres_plantas)) + " plantas:\n "
                for j in lista_nombres_plantas:
                    # condicion para presentar varias respuestas
                    if len(lista_nombres_plantas) == 1:
                        respuesta = j
                        break
                    elif lista_nombres_plantas[-1] == j:
                        respuesta = respuesta + " y " + j
                    elif lista_nombres_plantas[-2] == j:
                        respuesta = respuesta + j + " "
                    else:
                        respuesta = respuesta + j + ", "
                f1.write(';' + respuesta)
                f1.close()
            else:
                # imprimir mensaje de error enviando numero randomico
                respuesta = respuestaError[random.randint(1, 3)]
                print('error 1')
                # almacena la cadena de texto que ocasio error
                f.write(';' + respuesta + ';SKOS NO TIENE RESPUESTA')
                f.close()
        # condicion para encontrar definicon de palabras
        elif (intencion == 'definicion'):
            for i in respuesta_json['slots']:
                entidad1 = i['value']['value']
                print ('hola' + entidad1)
            lista_plantas = definicion(entidad1)
            if (len(lista_plantas) != 0):
                respuesta = lista_plantas
                f1.write(';' + str(respuesta))
                f1.close()
            else:
                # no existe en el SKOS
                respuesta = respuestaError[random.randint(1, 3)]
                print('error 2 NO SKOS')
                f.write(';' + respuesta + ';SKOS NO TIENE RESPUESTA')
                f.close()
        # condicion para traduccion de palabra
        elif (intencion == 'espaniol'):
            for i in respuesta_json['slots']:
                entidad1 = i['value']['value']
            lista_plantas = kichua(entidad1)
            if (len(lista_plantas) != 0):
                respuesta = lista_plantas
                f1.write(';' + respuesta)
                f1.close()
            else:
                respuesta = respuestaError[random.randint(1, 3)]
                print('error 3 NO SKOS')
                f.write(';' + respuesta + ';SKOS NO TIENE RESPUESTA')
                f.close()
        # obtencion del grupo
        elif (intencion == 'grupo'):
            for i in respuesta_json['slots']:
                entidad1 = i['value']['value']
            lista_plantas = grupo(entidad1)
            if (len(lista_plantas) != 0):
                respuesta = lista_plantas
                f1.write(';' + respuesta)
                f1.close()
            else:
                respuesta = respuestaError[random.randint(1, 3)]
                print('error 3 NO SKOS')
                f.write(';' + respuesta + ';SKOS NO TIENE RESPUESTA')
                f.close()
        # bloque para imagen
        elif (intencion == 'imagen'):
            for i in respuesta_json['slots']:
                entidad1 = i['value']['value']
            # obtencion de la direccion de la imagen
            uri = imagen(entidad1)
            # saber si la imagen existe
            valor = os.path.exists(uri)
            # condicion para enviar error si la imagen no existe
            if (valor == True):
                # cargar imagen
                photo = open(uri, 'rb')
                # mensaje de la imagen consultada
                respuesta = 'Imagen de plantas ' + entidad
                # comando para enviar la imagen a la interfaz de chat
                bot.send_photo(chat_id, photo)
                f1.write(';' + str(valor))
                f1.close()
            else:
                respuesta = 'no encontramos la imagen'
                imge = 'bot: ' + str(valor) + '-> NO HAY IMAGEN'
                f.write(';' + imge)
                f.close()
        elif (intencion == 'saludo'):
            respuesta = 'Hola en que te puedo ayudar'
            f1.write(';' + respuesta)
            f1.close()
        else:
            respuesta = respuestaError[random.randint(1, 3)]
            print('error 4 NO INTENCION')
            er = 'bot: ' + respuesta + '-> NO EXISTE ENTIDAD'
            f.write(';' + er)
            f.close()
    # control de errores junto con el almacenamiento de las palabras
    except IndexError:
        respuesta = "Perdon, no pude responder a tu pregunta."
        er1 = 'bot: ' + respuesta + ' *ALERTA* ALGO PASO EXCEPT'
        f.write(';' + er1)
        f.close()
    except:

        respuesta = respuestaError[random.randint(1, 3)]
        print('error 5 EXCEPTION')
    # metodo para enviar el mensaje a telegram
    bot.send_message(chat_id, respuesta)


# mensaje de confirmacion al estar listo el bot
print ("Se inicio el bot")
bot.polling(none_stop=True)
