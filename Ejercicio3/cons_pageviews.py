#!/usr/bin/env python
import pika, pageviewapi.period, sys, os
#CONSUMIDOR - Recibe mensaje

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',heartbeat=60,
                                       blocked_connection_timeout=30))


    channel = connection.channel()

    channel.queue_declare(queue='pageview_queue')

    def on_request(ch, method, props, body):
        decoded_body = body.decode("utf-8")
        print(" [.] Articulo solicitado: %s" % decoded_body)
        
        #Numero de visitas del articulo. NOTA: El campo donde va el nombre del articulo (decoded_body) es sensible a mayusculas y acentos.
        #El numero de visitas variara completamente dependiendo de si se usaron los acentos de manera debida.
        #En caso de excepcion(si el articulo no existe o esta mal escrito), la respuesta sera 0.
        try:
            response = pageviewapi.period.sum_last('es.wikipedia', decoded_body.capitalize(), last=31, access='all-access', agent='all-agents')
        except:
            response = 0
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=3)
    channel.basic_consume(queue='pageview_queue', on_message_callback=on_request)

    print(" [x] PAGEVIEW: Esperando mensajes...")
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
