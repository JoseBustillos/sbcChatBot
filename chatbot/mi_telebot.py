import json
from snips_prueba import pregunta, tipos, definicion, kichua, grupo, imagen
import telebot
import random
import os.path

# colocar token de acceso
bot = telebot.TeleBot('619649693:AAG3QIMhSymCaJIk9aiSQxp3ExJIrqNOP9U')


# comandos de inicio y ayuda
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # presentar mensaje con los comandos
    bot.reply_to(message, "Hola, en que te puedo ayudar?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print('*************    METODO PRINCIPAL    *************')
    # lista de los respuestas cuando existe un error o no entiende la pregunta
    respuestaError = [' ', 'ups, no entendi tu pregunta', 'puedes revizar tu pregunta',
                      'lo lamento para mas tarde te respondo']
    chat_id = message.chat.id
    print('chat id: ',chat_id)
    # control para la seleccion del texto ingresado
    try:
        texto = message.json['text']
    except AttributeError:
        texto = "N/A"
    # procesamiento del texto ingresado para su identificacion
    respuesta_json = json.loads(pregunta(texto))
    print('respuesta json: ',respuesta_json)
    # archivo de control de palabras erroneas
    f = open("registro.txt", "a")
    try:
        # captura de la intencion
        intencion = respuesta_json['slots'][0]['entity']
        # captura de la entidad a preguntar
        entidad = respuesta_json['slots'][0]['value']['value']
        print('\n' + intencion + '-' + entidad)
        # las condiciones se usan para identificar el tipo de intencion
        if (intencion == 'tipo'):
            for i in respuesta_json['slots']:
                entidad1=i['value']['value']
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
            else:
                # imprimir mensaje de error enviando numero randomico
                respuesta = respuestaError[random.randint(1, 3)]
                print('error 1')
                # almacena la cadena de texto que ocasio error
                f.write(texto + '\n')
                f.close()
        # condicion para encontrar definicon de palabras
        elif (intencion == 'definicion'):
            for i in respuesta_json['slots']:
                entidad1=i['value']['value']
                print ('hola'+entidad1)
            lista_plantas = definicion(entidad1)
            if (len(lista_plantas) != 0):
                respuesta = lista_plantas
            else:
                # no existe en el SKOS
                respuesta = respuestaError[random.randint(1, 3)]
                print('error 2 NO SKOS')
                f.write(texto + '\n')
                f.close()
        # condicion para traduccion de palabra
        elif (intencion == 'espaniol'):
            for i in respuesta_json['slots']:
                entidad1=i['value']['value']
            lista_plantas = kichua(entidad1)
            if (len(lista_plantas) != 0):
                respuesta = lista_plantas
            else:
                respuesta = respuestaError[random.randint(1, 3)]
                print('error 3 NO SKOS')
                f.write(texto + '\n')
                f.close()
        # obtencion del grupo
        elif (intencion == 'grupo'):
            for i in respuesta_json['slots']:
                entidad1=i['value']['value']
            lista_plantas = grupo(entidad1)
            if (len(lista_plantas) != 0):
                respuesta = lista_plantas
            else:
                respuesta = respuestaError[random.randint(1, 3)]
                print('error 3 NO SKOS')
                f.write(texto + '\n')
                f.close()
        # bloque para imagen
        elif (intencion == 'imagen'):
            for i in respuesta_json['slots']:
                entidad1=i['value']['value']
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
            else:
                respuesta = 'no encontramos la imagen'
        else:
            respuesta = respuestaError[random.randint(1, 3)]
            print('error 4 NO INTENCION')
            f.write(texto + '\n')
            f.close()
    # control de errores junto con el almacenamiento de las palabras
    except IndexError:
        respuesta = "Perdon, no pude responder a tu pregunta."
        f.write(texto + '\n')
        f.close()
    except:
        respuesta = respuestaError[random.randint(1, 3)]
        print('error 5 EXCEPTION')
        f.write(texto + ' *ALERTA* ' + '\n')
        f.close()
    # metodo para enviar el mensaje a telegram
    bot.send_message(chat_id, respuesta)


# mensaje de confirmacion al estar listo el bot
print ("Se inicio el bot")
bot.polling(none_stop=True)
