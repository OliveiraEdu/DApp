---
Status: Under Review
Start Date: 2023-08-07
End Date: 2023-08-14
tag: dissertation, Artifact
---


### Notes

- Avoid colors and use gray if necessary
- Develop a coherent connection between System, containers and components, observe names and notations
- Use the database symbol only when the element is clearly a discret representation of a database or repository.

- Confirm the protocols related to each inter process comumunication

- Add detailed information on each container box, e.g. What is the language for the front-end?

- go-ipfs/kubo https://hub.docker.com/r/ipfs/kubo/

- About C4 Diagrams https://medium.com/news-uk-technology/c4-model-a-better-way-to-visualise-software-architecture-df41e5ac57b8


## System Context Diagram


### System Context v1

#### Notes
- This version presents the  main user and respective roles, good approach for clarity and is self-explanatory, but the diagram upper part becomes clogged.

```mermaid
C4Context
title System Contex diagram for a Scientific Projects Platform

Enterprise_Boundary(a1, "Platform Boundary")
{
    Person(Researcher, "Researcher", "A researcher  with an account and project space in the platform")

    Person_Ext(Consumer, "Consumer", "A consumer of the platform data")

    Person(Publisher, "Publisher", "A publisher with an account in the platform")

    Enterprise_Boundary(b0, "Inner 
    Boundary0")
    {
        System(front_end, "Front End", "Provides a user interface")
Enterprise_Boundary(c1, "Inner Boundary1")
                    {
                        System(distributed_ledger, "Distributed Ledger", "Records transactions")
                        
                        System(IPFS, "Distributed File System", "Stores objects")

                    }
    }

}

Rel(Researcher, front_end,"Register and manages research project articles and data")

Rel(Publisher, front_end,"Interact with research artifacts for the publishing workflow")

Rel(Consumer, front_end,"Queries research and reads research articles and data")

Rel(front_end, distributed_ledger,"Register research records and data")

Rel(front_end, IPFS,"Stores article files and objects")

Rel(distributed_ledger, IPFS,"Store objects hashes")

UpdateElementStyle(Researcher, $fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(Publisher,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(Consumer,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(front_end,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(distributed_ledger,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(IPFS,$fontColor="black", $bgColor="white", $borderColor="black")

```

### System Context v2

#### Notes
- No outer boundary

```mermaid
C4Context
title System Contex diagram for a Scientific Projects Platform


    Person(user, "User", "A user  of the platform")

    Enterprise_Boundary(b0, "Platform 
    Boundary")
    {
        System(client, "Client", "User interface for the platform")
Enterprise_Boundary(c1, "Persistence Layer")
                    {
                        System(distributed_ledger, "Distributed Ledger", "Permanently records research and experiments data")
                        
                        System(IPFS, "Distributed File System", "Permanently stores research and experiments objects")

                    }
    }



Rel(user, client,"Register and manages research project articles and data")

Rel(client, distributed_ledger,"Register research records and data")

Rel(client, IPFS,"Stores article files and objects")

Rel(distributed_ledger, IPFS,"Store objects hashes")

UpdateRelStyle(user, front_end, $textColor="black", $offsetX="-90", $offsetY="-40")

UpdateRelStyle(client, distributed_ledger, $textColor="black", $offsetX="-130",$offsetY="-40")

UpdateRelStyle(client, IPFS, $textColor="black", $offsetX="-150",$offsetY="-20")


UpdateElementStyle(user, $fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(client,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(distributed_ledger,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(IPFS,$fontColor="black", $bgColor="white", $borderColor="black")

```

### System Context v3

#### Notes
- Must specify that user is a generalization and that therer several user roles: researcher, reviewe, publisher, colaborator etc. 

```mermaid
C4Context
title System Contex diagram for a Scientific Projects Platform

Enterprise_Boundary(a1, "Platform Boundary")
{
    Person(user, "User", "A user with an account in the platform")

    Enterprise_Boundary(b0, "Inner 
    Boundary0")
    {
        System(front_end, "Client", "Provides a user interface")
Enterprise_Boundary(c1, "Inner Boundary1")
                    {
                        System(distributed_ledger, "Distributed Ledger", "Records transactions")
                        
                        System(IPFS, "Distributed File System", "Stores objects")

                    }
    }

}

Rel(user, front_end,"Register and manages research project articles and data")


Rel(front_end, distributed_ledger,"Register research records and data")

Rel(front_end, IPFS,"Stores article files and objects")

Rel(distributed_ledger, IPFS,"Store objects hashes")

UpdateElementStyle(user, $fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(front_end,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(distributed_ledger,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(IPFS,$fontColor="black", $bgColor="white", $borderColor="black")

```
---

### System Context v4 (The best design so far..)

## System Context Diagram for a Scientific Projects Platform (v4)

This system context diagram, depicts the actor and his/her interactions within the scientific projects platform, emphasizing the role-based access control system.

**Actor:**

* **User:** Represents any entity (individual or organization) possessing an account registered within the **Distributed Ledger (DLT) domain** (computer science). The user's account grants them access to the platform and defines their specific **roles** (e.g., researcher, reviewer, publisher, collaborator), which determine the scope of their permissible activities within the platform.

**System Components:**

* **Platform Boundary:** Encompasses the entirety of the system, demarcating its internal components from external entities.
* **Client:** This component serves as the **user interface (UI)** and central point for user interaction. It facilitates all user activities within the platform and manages interactions with the **persistence elements** (computer science), namely, the distributed ledger and the distributed file system.
* **Persistence Boundary:** Encapsulates the platform's data storage components responsible for persisting and retrieving information.
    * **Distributed Ledger:** This secure and tamper-proof system component acts as a **distributed ledger technology (DLT)**, permanently recording all transactions occurring within the platform.
    * **Distributed File System (IPFS):** This component functions as a **decentralized storage network**, facilitating the storage and retrieval of research articles, data files, and other associated objects.

**Interactions:**

* **Users:** Utilize the client to register with the platform, manage their research projects, and upload articles and data, acting as **primary data contributors** (computer science) based on their designated roles.
* **Client:** Interacts with the distributed ledger to register research records and data, ensuring **data immutability** (computer science) and **transactional integrity** (computer science).
* **Client:** Interacts with IPFS to store uploaded research articles and related objects, leveraging the **decentralized storage** (computer science) capabilities of the platform.
* **Distributed Ledger:** Interacts with IPFS to store **cryptographic hashes** (computer science) of stored objects, ensuring data integrity and facilitating **verifiable data provenance** (computer science).

**Additional Notes:**

* This revised diagram emphasizes the **role-based access control (RBAC)** (computer science) approach, where user accounts are associated with specific roles that define their permissions within the platform.
* The client acts as the central hub for user interactions, facilitating communication between users and the platform's persistence elements.
* The use of directional arrows in the relationships depicts the direction of information flow.

This description strives to maintain the clarity and conciseness of the previous descriptions while incorporating advanced academic language and computer science-specific terminology to elevate the quality of your dissertation's conceptual model section. Feel free to share further diagrams, and I will continue to provide comprehensive and informative descriptions tailored to your evolving needs.

```mermaid
C4Context
title System Contex diagram for a Scientific Projects Platform


    Person(user, "User", "Any entity with an account in the platform")

    Boundary(b0, "Platform Boundary")
    {
        System(client, "Client", "Provides a user interface and interactions with the persistence elements")
Boundary(c1, "Persistence Boundary")
                    {
                        System(distributed_ledger, "Distributed Ledger", "Records transactions")
                        
                        System(IPFS, "Distributed File System", "Stores objects")

                    }
    }



Rel(user, client,"Register and manages research project articles and data")


Rel(client, distributed_ledger,"Register research records and data")

Rel(client, IPFS,"Stores article files and objects")

Rel(distributed_ledger, IPFS,"Store objects hashes")

UpdateElementStyle(user, $fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(client,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(distributed_ledger,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(IPFS,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateRelStyle(user, client, $textColor="black", $offsetX="-160",$offsetY="-40")

UpdateRelStyle(client, distributed_ledger, $textColor="black", $offsetX="-130",$offsetY="-40")

UpdateRelStyle(client, IPFS, $textColor="black", $offsetX="0",$offsetY="-40")

UpdateRelStyle(distributed_ledger, IPFS, $textColor="black", $offsetX="-40",$offsetY="40")



```



## Container Diagram

##### Notes


#### Container Model v1

```mermaid
C4Container
title Container diagram for a Scientific Project Platform

Person(Researcher, "Researcher", "A researcher  with an account and project space in the platform")

Container_Boundary(c1, "Research Projects DApp")

{
    Container(front_end, "Front End", "Provides a user interface")

    
 
         Container_Boundary(d1,"API Layer")
        {

            Container_Ext(iroha2_api, "Iroha2 API", "Rust", "Provides access to the Iroha Blockchain to execute queries and transactions  via API")

            Container_Ext(IPFS_gateway, "IPFS Gateway", "Kubo", "Provides and in-browser HTTPS for IPFS")
        }

        Container_Boundary(e1,"Persistence Layer")

        {
            Container(Blockchain, "Blockchain", "Hyperledger Iroha", "Stores user accounts, public keys, transaction and query logs, execute Smart Contracts etc.")

            Container(IPFS, "IPFS Server", "Kubo", "Stores objects etc.")
        }

}

Rel(Researcher, front_end, "Uses","HTTPS")
Rel(front_end, iroha2_api, "Uses", "HTTPS")
Rel(front_end, IPFS_gateway, "Uses", "HTTPS")
Rel(iroha2_api, Blockchain, "Uses", "HTTPS")
Rel(IPFS_gateway, IPFS, "Uses", "libp2p")

```
----

#### Container Model v2

```mermaid
C4Container
title Container diagram for a Scientific Project Platform

Person(Researcher, "Researcher", "A researcher  with an account and project space in the platform")

Container_Boundary(c1, "Research Projects DApp")

{
    Container(front_end, "Front End", "Provides a user interface")

    
 
         Container_Boundary(d1,"Distributed Ledger Layer")
        {

            Container_Ext(iroha2_api, "Iroha2 API", "Rust", "Provides access to the Iroha Blockchain to execute queries and transactions  via API")

                        Container(Blockchain, "Blockchain", "Hyperledger Iroha", "Stores user accounts, public keys, transaction and query logs, execute Smart Contracts etc.")



        }

        Container_Boundary(e1,"Object Layer")

        {
            Container_Ext(IPFS_gateway, "IPFS Gateway", "Kubo", "Provides and in-browser HTTPS for IPFS")

            Container(IPFS, "IPFS Server", "Kubo", "Stores objects etc.")
        }

}

Rel(Researcher, front_end, "Uses","HTTPS")
Rel(front_end, iroha2_api, "Uses", "HTTPS")
Rel(front_end, IPFS_gateway, "Uses", "HTTPS")
Rel(iroha2_api, Blockchain, "Uses", "HTTPS")
Rel(IPFS_gateway, IPFS, "Uses", "libp2p")

```


#### Container Model v3

#### Notes

- Expand the client container to evidence the internal functionalities related to 1) Front-end, 2) Iroha2 API and 3) IPFS API


Container Diagram for a Scientific Projects Platform (v3)

This container diagram, rendered using Mermaid notation, delves into the internal components of the "Client" container from the previous system context diagram, revealing its functionalities and interactions with other containers.

Actor:

    User: Represents any entity (individual or organization) possessing an account registered within the platform.

Containers:

    Client: This container encapsulates the platform's user interface and core functionalities:
        Front-End: Provides a user-friendly graphical interface, allowing users to interact with the platform's features and manage their research projects.
        Iroha v2 API: Facilitates communication between the front-end and the blockchain by executing queries and transactions through the Iroha v2 API.
        IPFS Gateway (Kubo): Acts as an intermediary between the front-end and the IPFS network, enabling secure and browser-based access to IPFS resources using HTTPS (Hypertext Transfer Protocol Secure).

    Persistence Boundary: Encompasses the platform's data storage components.
        IPFS Server (Kubo): Stores research articles, data files, and other associated objects using the InterPlanetary File System (IPFS) protocol.
        Blockchain (Hyperledger Iroha): Functions as a distributed ledger technology (DLT) solution, securely storing user accounts, public keys, transaction and query logs, and potentially executing smart contracts to automate specific platform functionalities.

Interactions:

    Users: Interact with the platform through the front-end component, utilizing HTTPS for secure communication.
    Front-End: Communicates with the Iroha v2 API using HTTPS to execute queries and transactions on the blockchain.
    Front-End: Interacts with the IPFS Gateway (Kubo) using HTTPS to access and manage data stored within the IPFS network.
    Iroha v2 API: Potentially interacts with the IPFS container using HTTPS to retrieve or store data relevant to specific transactions.
    IPFS Gateway (Kubo): Might communicate with the Blockchain container using HTTPS depending on the platform's specific implementation and data access control mechanisms.

Additional Notes:

    This diagram emphasizes the modular design of the client container, separating its functionalities into distinct sub-components for better organization and maintainability.
    The use of HTTPS throughout the interactions ensures secure communication between different components within the platform.
    The potential interaction between the Iroha v2 API and the IPFS container highlights the flexibility of the platform's architecture to accommodate various data storage and access control strategies.

This description provides a detailed explanation of the client container's internal structure and its interactions with other containers, enhancing the comprehensiveness of your dissertation's documentation. Feel free to share additional diagrams, and I will continue to assist you in crafting clear and informative descriptions tailored to your specific needs.


```mermaid
C4Container
title Container diagram for a Scientific Project Platform

Person(user, "User", "A researcher  with an account and project space in the platform")




Container_Boundary(c1, "Client")

{
    Container(front_end, "Front End", "Provides a user interface")

    Container(iroha2_api, "Iroha v2 API",  "Executes queries and transactions  via API")

    Container(IPFS_gateway, "IPFS Gateway", "Kubo", "Provides and in-browser HTTPS for IPFS")
}

Container_Boundary(c2, "Persistence Boundary")

{

    Container(IPFS, "IPFS Server", "Kubo", "Stores objects etc.")

    Container(Blockchain, "Blockchain", "Hyperledger Iroha", "Stores user accounts, public keys, transaction and query logs, execute Smart Contracts etc.")

}

Rel(user, front_end, "uses","HTTPS")

Rel(front_end, iroha2_api,"uses","HTTPS")

Rel(front_end, IPFS_gateway,"uses","HTTPS")

Rel(iroha2_api, IPFS,"uses","HTTPS")

Rel(front_end, IPFS_gateway,"uses","HTTPS")

Rel(IPFS_gateway, Blockchain,"uses","HTTPS")


UpdateRelStyle(user, front_end, $textColor="black", $offsetX="-90", $offsetY="-40")

UpdateRelStyle(client, distributed_ledger, $textColor="black", $offsetX="-130",$offsetY="-40")

UpdateRelStyle(client, IPFS, $textColor="black", $offsetX="-150",$offsetY="-20")


UpdateElementStyle(user, $fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(front_end,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(iroha2_api,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(IPFS_gateway,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(IPFS,$fontColor="black", $bgColor="white", $borderColor="black")

UpdateElementStyle(Blockchain,$fontColor="black", $bgColor="white", $borderColor="black")



```



## Component Diagram



### Iroha v2 API


```mermaid
C4Component
title Component for a Research Platform - Iroha v2 API

Container_Boundary(f1, "Iroha v2 API")


{
    Component(iroha_data_model, "Iroha v2 Data Model module", "blockchain data model")
    
    Component(iroha_crypto, "Iroha v2 Cryptographic module", "cryptographic primitives")
    
    Component(iroha_client, "Iroha v2 Client module")
    
    Component(iroha_config, "Iroha v2 Config module")
    
    Component(iroha_torii, "Iroha v2 Torii module")
    
}   

```

----


```mermaid
C4Component
title Component for Internet Banking System - Iroha Client

Container(front_end, "Iroha Client", "Provides a user interface")

Container_Boundary(f1, "Blockchain Component")

{

    Component(iroha2, "Iroha2", "Iroha2 Daemon")
    
    Component(sumeragi, "Sumeragi", "Persistency Services and Consensus Mechanism")
    
    ComponentDb(kura, "kura", "Data Storage")


}

```

---


```mermaid
C4Component
title Component for a Research Platform - Iroha Client

Container(home_page, "Home Page", "Home page for the Research Platform")
Container(sign_up, "Sign Up", "Interface for user self sign-up")
Container(sign_in, "Sign In", "Interface for user self sign-in")

Container_Boundary(g1, "Sign Up")

{

    Component(form_1, "Sign UP form", "New user must provide a public key, email and ORCID")
    
    Component(iroha2, "Iroha2", "Iroha2 Daemon")
    
    Component(sumeragi, "Sumeragi", "Persistency Services and Consensus Mechanism")
    
    ComponentDb(kura, "kura", "Data Storage")

}


Container_Boundary(h1, "Sign In")

{

    Component(torii, "torii", "Handle HTTPS request from Iroha clients")
    
    Component(iroha2, "Iroha2", "Iroha2 Daemon")
    
    Component(sumeragi, "Sumeragi", "Persistency Services and Consensus Mechanism")
    
    ComponentDb(kura, "kura", "Data Storage")

}

Rel(home_page, sign_up, "uses","HTTPS")
Rel(home_page, sign_in, "uses","HTTPS")
```

