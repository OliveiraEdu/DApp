---
Status: Under Review
Start Date: 2023-08-07
End Date: 2023-08-14
tag: dissertation, Artifact
---


### General Notes

- Write a representation of the conceptual/theoretical model of the domain specific proposed solution. Including System Entities (Data, operations and functions). 
- Write a specific section on the Proposed Model chapter for the conceptual/theoretical model.
- Write a specific section about the implementation on the Proposed Model chapter.
- Relate the domain specific entities with the Iroha2 entities.


**Operations**

- Specify all the possible operations in the theoretical model
- Specify Iroha2 operations
- RegisterProject -> RegisterAsset
-

**Entities**

- Researcher
- Research
- Project/Experiment

**Functions**
- Register an experiment
- Register an account


1 - What is the representation inside the Metadata field? It is a JSON formatted field?

#### Metadata representation in:

**Account**
- orcid
- role - author, contributor, reviewer etc
- project id

**Asset**
- project_id
- asset_type - file, abstract, comment
- DOI
- file name
- file hash
- IPFS path
- contributors (orcids)


---

# Proposed Model v1

### Notes

Is the Asset class metadata well suited for this demand?
### CONS

Researcher should sign up for every project, a separated key pair (pub/priv). Multiples key pairs handling leads to a bad user experience.

### PROS

All data regarding the research project is under the same hierarchy


```mermaid
classDiagram
		direction TB
        world *-- domain_research_abc: registered in
        world *-- domain_research_n: registered in
        domain_research_abc *-- account_researcher_1: registered in
        domain_research_abc *-- account_researcher_2: registered in
        account_researcher_1 *-- asset_file_1: registered by
        account_researcher_1 *-- asset_file_n: registered by
        domain_research_abc *-- asset_file_1: registered in
        domain_research_abc *-- asset_file_n: registered in


        class world{
            domains
        }
        class domain_research_abc{
            id = "research_abc"
        }
        class domain_research_n{
            id = "research_n"
        }
        class account_researcher_1{
            id = "researcher_1@abc"
        }
        class account_researcher_2{
            id = "researcher_1@abc"
        }
        class asset_file_1{
            id = "file_1#abc"
        }
        class asset_file_n{
            id = "file_1#abc"
        }
  ```
---
# Proposed Model v2


### Notes

#### PROS

A researcher might sign up just once, holding just one key par.

#### CONS

Research assets must be indexed by a unique identifier.


```mermaid
classDiagram
		direction TB
        world *-- domain_research: registered in
        domain_research *-- account_researcher_1: registered in
        account_researcher_1 *-- asset_file_1: registered by
        account_researcher_n *-- asset_file_n: registered by
        domain_research *-- asset_file_1: registered in
        domain_research *-- asset_file_n: registered in

        domain_research *-- account_researcher_2: registered in
        domain_research *-- account_researcher_n: registered in
        


        class domain_research{
            id = "research"
        }
        class account_researcher_1{
            id = "researcher_1@research"
        }
        class account_researcher_2{
            id = "researcher_2@research"
        }
        class account_researcher_n{
            id = "researcher_n@research"
        }
        class asset_file_1{
            id = "file_1#research"
       }
        class asset_file_n{
            id = "file_n#research"
       }
  ```
---
# Proposed Model v3 - System Entities

### Notes


- This model must represent the theoretical model for the platform.
- Evaluate the use of ORCID as the id.
- Evaluate the use of DOI to identify projects and artifacts
- Evaluate ontologies like 
    - FOAF - http://xmlns.com/foaf/spec/
    - PROV-O https://www.w3.org/TR/2013/REC-prov-dm-20130430/#section-entity-activity
    - DOI https://www.doi.org/doi-handbook/HTML/index.html
    - Datacite https://datacite.org/

- Read about provenance in the context of reproducibility https://www.w3.org/2005/Incubator/prov/wiki/images/0/02/Provenance-XG-Overview.pdf


---
### Class Account

|Class|Attribute|Definition|Notes|
|---|---|---|---|
|Account| | Represents any type of authenticated user in the platform and holds the related attributes | |
|Account|id|A unique identification for any authenticated user| |
|Account|orcid|Open Researcher and Contributor ID is a nonproprietary alphanumeric code to uniquely identify authors and contributors of scholarly communication|Evaluate the use of ORCID as the id.|
|Account|email|represents the email address of the user|
|Account|role|enumerator for the account type: author, contributor, reviewer, publisher etc.| |
|Account|project_id|a unique identifier for a scientific form in the platform|Evaluate the use of DOI to identify projects and artifacts https://www.doi.org/|

---
### Class Project

|Class|Attribute|Definition|Notes|
|---|---|---|---|
|Project| | Represents a scientific project and is uniquely identified. It is a placeholder for all project information and data.|Evaluate the use of DOI to identify projects and artifacts https://www.doi.org/|
|Project| owner | Stores the id of the account that owns the project and respective artifacts| |
Project|time_stamps|Stores the creation date, last update date and current version of the project|JSON format 1| Uses ISO 8601 format with UTC timezone.
Project|article_metadata|Stores article metadata: title, abstract, authors, DOI|JSON format 2|
Project|object_metadata|Stores  metadata of the uploaded object: object_name, type, IPFS_CID  |JSON format 3 | This attribute is instantiated as many times as the quantity of objects belonging to the project.

### JSON files

**1 - Project(time_stamps)**

{
  "time_stamps": ["2024-01-27T11:58:17.27556Z", "2024-01-28T21:47:37.364447Z", 1],
}


**2 - Project(article_metadata)**

{
  "article_title": "1,500 scientists lift the lid on reproducibility",
  "article_abstract": "Survey sheds light on the ‘crisis’ rocking research.",
  "article_authors": ["Baker", "Monya"],
  "article_DOI": "10.1038/533452a"
}

**3 - Project(object_metadata)**

{
  "object_name": "article.pdf",
  "description": "main article",
  "type": 
  "IPFS_CID": "bafyreih3874d6j95k4x254h89f98327y9823f7z27w82x"
}

---

### Operations

*TODO -Define the remaining operations*

|Operation|Class|Definition|Attribues|Notes|
|---|---|---|---|---|
|AccountRegister|Account |The process of user sign up to the platform, must inform: user name, email, ORCID and public key |User self sign-up| |
|AccountUpdate|Account| The process of updating an account attributes| | |
|ProjectRegister|Project| The process of registering a project in the platform|project_id |
|ProjectUpdate|Project| Updates attributes of an existing project| |For instance, add a new object



----

## Class Diagram


```mermaid
classDiagram
		direction TB
   
        class Domain{
            id
            accounts
            projects

        }
        class Account{
            id, 
            orcid,
            email,
            role,
            project_id
        }
        class Project{
            owner,
            time_stamps,
            article_metadata,
            object_metadata
        }
        
        Domain *-- Account: registered in
        Domain *-- Project: registered in
        Account *-- Project: registered in

        style Account fill:#fff,stroke:#000,stroke-width:1px
        style Domain fill:#fff,stroke:#000,stroke-width:1px
        style Project fill:#fff,stroke:#000,stroke-width:1px
        
        


  ```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant web as Web Browser
    participant blog as Blog Service
    participant account as Account Service
    participant mail as Mail Service
    participant db as Storage

    Note over web,db: The user must be logged in to submit blog posts
    web->>+account: Logs in using credentials
    account->>db: Query stored accounts
    db->>account: Respond with query result

    alt Credentials not found
        account->>web: Invalid credentials
    else Credentials found
        account->>-web: Successfully logged in

        Note over web,db: When the user is authenticated, they can now submit new posts
        web->>+blog: Submit new post
        blog->>db: Store post data

        par Notifications
            blog--)mail: Send mail to blog subscribers
            blog--)db: Store in-site notifications
        and Response
            blog-->>-web: Successfully posted
        end
    end
```

  ---

# Iroha2 Canonical Model

### Notes

- Insert operations


```mermaid
classDiagram
		direction TB
        World *-- "many" Domain: registered in
        Domain *-- "many" Account: registered in
        Account *-- "many" Asset: registered by
        Domain *-- "many" Asset: registered in
        Asset *-- "many" AssetDefinition: registered by
        Domain *-- "many" AssetDefinition: registered in
        AssetDefinition -- AssetValue
     
        class Domain
            Domain : id {DomainId}
        
        class Asset
            Asset: id {AssetId}
            Asset: metadata {Metadata}

        class AssetDefinition
            AssetDefinition: id {AssetDefinitionId}
            AssetDefinition: metadata {Metadata}
            AssetDefinition: value_type {AssetTypeValue}

        class Account
            Account : id {AccountId}
            Account : metadata {Metadata}
        
        class AssetValue
            <<enumeration>> AssetValue 
            AssetValue: Quantity
			AssetValue: BigQuantity
			AssetValue: Fixed
			AssetValue: Store
  ```