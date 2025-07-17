import time
from random import Random

from kafka import KafkaConsumer, KafkaProducer
import random

class Auctioneer:
    def __init__(self,  bids_topic, notify_message_processor_topic, new_offer_topic):
        super().__init__()
        self.bids_topic = bids_topic
        self.notify_message_processor_topic = notify_message_processor_topic
        self.new_offer_topic = new_offer_topic

        # definesc consumerul pt oferte
        self.bids_consumer = KafkaConsumer(
            self.bids_topic,
            auto_offset_reset="earliest",  # mesajele se preiau de la cel mai vechi la cel mai recent
            group_id="auctioneers"
        )
        self.wanted_sum = random.randint(10_000, 100_000)
        self.notify_processor_producer = KafkaProducer()
        self.new_offer_producer = KafkaProducer()

    def receive_bids(self):
        self.new_offer_producer.send(topic=self.new_offer_topic,
                                     value=self.wanted_sum.to_bytes(4, byteorder='big'))
        print("Astept oferte pentru licitatie...")
        for msg in self.bids_consumer:
            print(msg.value)
            for header in msg.headers:
                if header[0] == "identity":
                    identity = str(header[1], encoding="utf-8")
            print("{} a spus {}".format(identity, msg.value))
            if msg.value == b'accept':
                self.bids_consumer.close()
                break
            else:
                time.sleep(0.100)
                self.wanted_sum = int(self.wanted_sum * 0.9)
                self.new_offer_producer.send(topic=self.new_offer_topic,
                                             value=self.wanted_sum.to_bytes(4, byteorder='big'))
                self.new_offer_producer.flush()

        self.finish_auction()

    def finish_auction(self):
        print("Licitatia s-a incheiat!")
        self.new_offer_producer.send(topic=self.new_offer_topic, value=bytearray("incheiat", encoding="utf-8"))
        self.bids_consumer.close()

        # se notifica MessageProcessor ca poate incepe procesarea mesajelor
        auction_finished_message = bytearray("incheiat", encoding="utf-8")
        self.notify_processor_producer.send(topic=self.notify_message_processor_topic, value=auction_finished_message)
        self.new_offer_producer.flush()
        self.new_offer_producer.close()
        self.notify_processor_producer.flush()
        self.notify_processor_producer.close()
        self.bids_consumer.close()

    def run(self):
        self.receive_bids()


if __name__ == '__main__':
    auctioneer = Auctioneer(
        bids_topic="topic_oferte",
        notify_message_processor_topic="topic_notificare_procesor_mesaje",
        new_offer_topic="new_offer_topic"
    )
    auctioneer.run()