# KafkaDutchAuction
## Capition
1. [Introduction](#introduction)
2. [Dutch Auction](#dutch-auction)
3. [Techincal aspects](#technical-aspects)
    1. [Kafka](#1-kafka)
    2. [Microservice architecture](#2-micorservices-archiecture)
4. [Microservices](#microservices)
    1. [BidderMicroservice](#1-biddermicroservice)
    2. [AuctioneerMicroservice](#2-auctioneermicroservice)
    3. [MessageProcessor](#3-messageprocessor)
    4. [BiddingProcessorMicroservice](#4-biddingprocessormicroservice)
5. [Activity diagram](#activity-diagram)
6. [Class Diagram](#class-diagram)

## Introduction

This project implements an example of a bidding process using Kafka. The chosen bidding strategy is the Dutch Auction, which will be explained later in this document. Kafka is used as the messaging backbone, enabling scalable and decoupled communication between auction participants and the auction controller.

The goal of the project is to demonstrate how Kafka can coordinate time-sensitive operations in a distributed environment. This example highlights event-driven design, asynchronous message processing, and basic fault tolerance in the context of a real-world auctioning mechanism.

## Dutch Auction

A Dutch auction is a type of price discovery mechanism where the auctioneer starts with a high asking price and gradually lowers it until a bidder accepts the current price. The process continues until the quantity offered is fully allocated.

This auction format is also known as a descending price auction. It is commonly used in scenarios such as Initial Public Offerings (IPOs) and government securities sales, including Treasury bills, notes, and bonds.

## Technical Aspects

This section explains the most important technical aspects of the project.

### 1. Kafka

Kafka is a publish/subscribe messaging system, often described as a distributed commit log or a distributed streaming platform. Unlike traditional messaging systems, Kafka is designed to store data long-term, allowing clients to read messages deterministically and in the exact order in which they were written.

The basic unit in Kafka is the message, which is conceptually similar to a row in a database table. Each message can have metadata called a key, which is used to determine how messages are distributed across partitions. This enables fine-grained control over message routing and parallel processing.

Messages in Kafka are organized into topics, which can be thought of as folders in a file system or tables in a database. Topics are further divided into partitions, which function as append-only commit logs. Partitions are fundamental to Kafka's scalability and fault-tolerance, enabling distributed storage and parallel processing of messages.

---

### 2. Micorservices archiecture

**Microservices Architecture (MSA)** is an architectural style that structures an application as a collection of loosely coupled, independently deployable services. Each service is responsible for a distinct business capability and communicates with others using lightweight protocols, typically HTTP or messaging systems.

---

### Key Characteristics (Fowler & Lewis, 2014):

- **Componentization via Services**  
  Each part of the system is a separate service, which can be deployed independently and developed in isolation.

- **Business-Oriented Organization**  
  Teams are organized around business capabilities rather than technical layers (e.g., “Order Management” instead of “Database Layer”).

- **Independent Deployment**  
  Each service can be deployed without affecting the others, enabling continuous delivery and rapid iterations.

- **Decentralized Data Management**  
  Each service manages its own database or data store, promoting autonomy and avoiding shared database bottlenecks.

- **Built for Failure**  
  Microservices embrace the reality of failure. They use patterns like circuit breakers and retries to build fault-tolerant systems.

- **Infrastructure Automation**  
  Continuous integration, automated testing, and deployment pipelines are essential to manage the complexity of microservices.

---

## Microservices

In this section will be presented the microservices that we use.

### 1. BidderMicroservice

This microservice represents the bidder in the auction process. It receives offers from the auctioneer and responds by either accepting or rejecting them.

---

#### Responsibilities

- **`receive_offer`**  
  Receives data (the offer) from the auctioneer via Kafka.

- **`accept_offer`**  
  Sends a message to the auctioneer to notify that the bidder accepts the offer.

- **`reject_offer`**  
  Sends a message to the auctioneer to notify that the bidder rejects the offer.

- **`wait_for_result`**  
  Waits for the result of the auction and prints a message informing the bidder whether they won or lost.

---

#### Technologies Used

- Kafka  
- Python

---

#### Architecture Role

Acts as the **bidder** in the auction process, reacting to offers and auction results.

---

#### SOLID Principles Applied

- **Single Responsibility Principle (SRP)**  
  The microservice is responsible for a single business capability: bidding in an auction.

- **Interface Segregation Principle**: The microservice exposes only the operations necessary for handling commands.

- **Inversion of Control (IoC)**  
  The microservice uses Kafka for communication with external components, decoupling its logic from direct service calls.

### 2. AuctioneerMicroservice

This microservice represent the auctioneer in the auction process. It sends offer to the bidders and receive their response: accept or reject the offer.

---

#### Responsibilities

- **`make an offer`**
  
  This responsibilities send an offer to the bidders. If the offer is rejected by all bidders than it sends another offer with a lower price than previous one.

- **`receive response`**

  This responsibilities receive the bidder's responses for the offer it sends.

- **`finish auction`**

  This responsibilities send a message to the MassageProcessor to notify it that the auction is over because a bidder accept last offer send.

---

#### Technologies Used

- Kafka  
- Python

---

#### Architecture Role

Acts as the **auctioneer** in the auction process, sending offers and closing the auction procees when an offer is accepted.

---

#### SOLID Principles Applied

- **Single Responsibility Principle (SRP)**  
  The microservice is responsible for a single business capability: auctioneer capabilities: sending an offer, close the auction process.

- **Interface Segregation Principle**  
  The microservice exposes only the operations necessary for handling commands.

- **Inversion of Control (IoC)**  
  The microservice uses Kafka for communication with external components, decoupling its logic from direct service calls.

### 3. MessageProcessor

This microservice is responsible for processing all the messages it receives: it sorts the messages by date.

---

#### Responsibilities

- **`receive and process messages`**

  This responsibility receives messages form bidders and auctioneer and sort the messages.

- **`finish processing`**

  This responsibility send a message to the bidder microservice to notify BiddingProcessorMicroservice that it has finished to processs the messages.

---

#### Technologies Used

- Kafka  
- Python

---

#### Architecture Role

Acts as the **message processor** in the auction process, sorting the messages by date.

---

#### SOLID Principles Applied

- **Single Responsibility Principle (SRP)**  
  The microservice is responsible for a single business capability: process the messages and sort them by date.

- **Interface Segregation Principle**  
  The microservice exposes only the operations necessary for processing messages.

- **Inversion of Control (IoC)**  
  The microservice uses Kafka for communication with external components, decoupling its logic from direct service calls.
 
### 4. BiddingProcessorMicroservice

It decides who wins the auction based on the offers received from the MessageProcessorMicroservice. It announces the winner by sending the message of the winning bidder to the BidderMicroservice.

---

#### Responsibilities

- **`receive processed Bidds`**
  
  This responsibility received processed bidds from MessageProcessor microservice.

- **`decide AUction Winner`**

  This responsibility decide the acution winner based on the processed bidds received from the MessageProcessor. The result is sent to the bidders.

---

#### Technologies Used

- Kafka  
- Python

---

#### Architecture Role

Acts as the **biddig processor** in the auction process processing the offer and than send a message to the bidders to anouce the auction winner.

---

#### SOLID Principles Applied

- **Single Responsibility Principle (SRP)**  
  The microservice is responsible for a single business capability: process the bidds and decide the auction winner.

- **Interface Segregation Principle**  
  The microservice exposes only the operations necessary for processing messages.

- **Inversion of Control (IoC)**  
  The microservice uses Kafka for communication with external components, decoupling its logic from direct service calls.

![Microservice Diagram](/Images/MicroserviceDiagram.png)

---

## Activity Diagram

![Activity Diagram](/Images/ActivityDiagram.png)

**In this activity diagram, colors are used to distinguish the actions of each microservice:**

- **$$\color{Green}Green$$** (Auctioneer Microservice)
- **$$\color{lightblue}Blue$$** (Bidder Microservice)
- **$$\color{red}Red$$** (MessageProcessor Microservice)
- **$$\color{Orange}Orange$$** (BiddingProcessor Microservice)
---

## Class Diagram

![Class Diagram](/Images/ClassDiagram.png)

## Bibiliography

- **Bidding rules** are taken from [here](https://corporatefinanceinstitute.com/resources/economics/english-auction/)

- Martin Fowler & James Lewis. ["Microservices"](https://martinfowler.com/articles/microservices.html), March 2014.