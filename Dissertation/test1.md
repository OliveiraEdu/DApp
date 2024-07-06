sequenceDiagram
    participant Researcher as "Researcher"
    participant Platform as "Platform"
    participant SmartContract as "Smart Contract"
    participant Blockchain as "Blockchain"

    Researcher->>Platform: Send Enrollment Request (account name, email, institution, public key)
    Platform->>SmartContract: Deploy Account Creation Smart Contract
    SmartContract->>Blockchain: Create New Account on Blockchain
    Blockchain->>SmartContract: Verify Account Creation Successful
    SmartContract->>Platform: Send Enrollment Confirmation to Researcher
    Platform->>Researcher: Send Verification Code (via email)
    Researcher->>Platform: Send Verified Email (verified code)
    Platform->>Researcher: Send Enrollment Completion Message