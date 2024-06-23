// SPDX-License-Identifier: Apache-2.0
pragma solidity 0.8.6;

contract Detail {
    address public serviceContractAddress;

    struct Details {
        string key;
        string value;
    }
    
    event Updated(string indexed name, string indexed key, string indexed value);

    constructor() {
        serviceContractAddress = 0xA6Abc17819738299B3B2c1CE46d55c74f04E290C;  // or any address you want to use
    }
    
    function setAccountDetail(string memory name, Details[] memory details) public {
        for (uint i = 0; i < details.length; i++) {
            bytes memory payload = abi.encodeWithSignature("setAccountDetail(string,string,string)", name, details[i].key, details[i].value);
            
            (bool success, ) = serviceContractAddress.call{gas: 30000}(payload);  // call the function on the contract at address serviceContractAddress
        
            require(success, "Error calling service contract function");

            emit Updated(name, details[i].key, details[i].value);
        }
    }
}