import random
import time

from kafka import KafkaProducer, KafkaConsumer
from random import randint
from uuid import uuid4

class Bidder:
    def __init__(self, bids_topic, result_topic, new_offer_topic):
        super().__init__()
        self.bids_topic = bids_topic
        self.result_topic = result_topic
        self.new_offer_topic = new_offer_topic

        self.bids_producer = KafkaProducer()

        self.result_consumer = KafkaConsumer(
            self.result_topic,
            auto_offset_reset="earliest"
        )

        self.new_offer_consumer = KafkaConsumer(
            self.new_offer_topic,
            auto_offset_reset="earliest"
        )
        self.sleep_time = random.randint(20, 1000)
        self.my_offer = random.randint(1000, 10_000)
        self.my_id = uuid4()  # identificatorul clientului

    def bid(self):
        # print("Pret prea mare, deci refuz")
        # bid_message = bytearray("reject", encoding="utf-8")  # corpul contine doar mesajul "licitez"
        bid_headers = [  # antetul mesajului contine identitatea ofertantului si, respectiv, oferta sa
            ("identity", bytes("Bidder {}".format(self.my_id), encoding="utf-8"))
        ]
        # self.bids_producer.send(topic=self.bids_topic, value=bid_message, headers=bid_headers)

        print("astept noi oferte")
        for msg in self.new_offer_consumer:
            print(msg.value)
            if msg.value != b'incheiat':
                time.sleep(1./self.sleep_time)
                bid = int.from_bytes(msg.value, byteorder="big")
                if bid < int(self.my_offer * 1.1):
                    print("accept oferta")
                    bid_message = bytearray("accept", encoding="utf-8")  # corpul contine doar mesajul "licitez"
                    self.bids_producer.send(topic=self.bids_topic, value=bid_message, headers=bid_headers)
                    self.bids_producer.flush()
                else:
                    print("refuz oferta")
                    bid_message = bytearray("reject", encoding="utf-8")  # corpul contine doar mesajul "licitez"
                    self.bids_producer.send(topic=self.bids_topic, value=bid_message, headers=bid_headers)
                    self.bids_producer.flush()
            else:
                self.new_offer_consumer.close()
                break
        print("licitatie incheiata")
        self.bids_producer.flush()
        self.bids_producer.close()

    def get_winner(self):
        # se asteapta raspunsul licitatiei
        print("Astept rezultatul licitatiei...")
        result = next(self.result_consumer)

        # se verifica identitatea castigatorului
        for header in result.headers:
            if header[0] == "identity":
                identity = str(header[1], encoding="utf-8")

        if identity == "Bidder {}".format(self.my_id):
            print("[{}] Am castigat!!!".format(self.my_id))
        else:
            print("[{}] Am pierdut...".format(self.my_id))

        self.result_consumer.close()

    def run(self):
        print("BID 1")
        self.bid()
        self.get_winner()

if __name__ == '__main__':
    print("Creez bideer-ul")
    bidder = Bidder(
        bids_topic="topic_oferte",
        result_topic="topic_rezultat",
        new_offer_topic="new_offer_topic"
    )
    bidder.run()

