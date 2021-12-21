#!/usr/bin/env python
import pika, uuid, sys, os
#PRODUCTOR - Envia mensaje
class WikipediaSearch(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    #Llamada a wikipedia
    def wikipedia_call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='wikipedia_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response
    #Llamada a pageviewapi (Numero de visitas)
    def pageview_call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='pageview_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

def main():
    buscar = WikipediaSearch()
    while(1):
        #Busqueda de articulos.
        data = input(" [*] Sensible a acentos y mayusculas.\n [*] Ser especifico. Ej: 'Cuero' y 'Cuero (leyenda)' daran diferentes resultados.\n [*] Para salir, presione CTRL+C\n [*] Buscar: ")
        print(" [x] Solicitando articulo : %s" % data)
        responses =[ buscar.wikipedia_call(data), buscar.pageview_call(data) ]
        print(" [.] Resumen de la pagina : %s\n [.] Numero de visitas durante los ultimos 30 dias : %s \n" % (responses[0].decode("utf-8").replace('\u200b','').replace('\n',' '), responses[1].decode("utf-8")))

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
