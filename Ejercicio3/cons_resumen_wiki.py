#!/usr/bin/env python
import pika, wikipedia, sys, os
#CONSUMIDOR - Recibe mensaje

def main():
    #Eatablece el lenguaje de la informacion de los articulos de Wikipedia.
    wikipedia.set_lang("es")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',heartbeat=60,
                                       blocked_connection_timeout=30))


    channel = connection.channel()

    channel.queue_declare(queue='wikipedia_queue')

    def on_request(ch, method, props, body):
        decoded_body = body.decode("utf-8")
        print(" [.] Articulo solicitado: %s" % decoded_body)

        #Se entrgara el resumen del articulo buscado.
        #Puede que el articulo no exista, devolviendo una excepcion que es manejada, asignando una respuesta para tal caso.
        try:
            response = wikipedia.page(decoded_body.capitalize()).summary
        except:
            response = "La pagina no existe!"
        
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=3)
    channel.basic_consume(queue='wikipedia_queue', on_message_callback=on_request)

    print(" [x] WIKIPEDIA_ES : Esperando mensajes...")
    channel.start_consuming()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
