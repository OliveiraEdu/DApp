// SPDX-License-Identifier: Apache-2.0

pragma solidity >=0.7.0 <0.9.0;

contract Detail {
    address public serviceContractAddress;

    event Updated(string indexed name, string indexed key, string indexed value);
    event BatchUpdated(string indexed name, string[] keys, string[] values);

    // Initializing service contract address in constructor
    constructor() {
        serviceContractAddress = 0xA6Abc17819738299B3B2c1CE46d55c74f04E290C;
    }

    // Sets the account detail
    function setAccountDetail(string memory name, string memory key, string memory value) public returns (bytes memory result) {
        bytes memory payload = abi.encodeWithSignature(
            "setAccountDetail(string,string,string)",
            name,
            key,
            value);
        (bool success, bytes memory ret) = address(serviceContractAddress).delegatecall(payload);
        require(success, "Error calling service contract function");
        emit Updated(name, key, value);
        result = ret;
    }

    // Sets multiple account details
    function setAccountDetails(string memory name, string[] memory keys, string[] memory values) public returns (bytes memory result) {
        require(keys.length == values.length, "Keys and values array length must match");
        
        for (uint i = 0; i < keys.length; i++) {
            bytes memory payload = abi.encodeWithSignature(
                "setAccountDetail(string,string,string)",
                name,
                keys[i],
                values[i]);
            (bool success, bytes memory ret) = address(serviceContractAddress).delegatecall(payload);
            require(success, "Error calling service contract function");
        }
        
        emit BatchUpdated(name, keys, values);
        result = "";
    }

    // Sets the account quorum
    function setAccountQuorum(string memory name, string memory quorum) public returns (bytes memory result) {
        bytes memory payload = abi.encodeWithSignature(
            "setAccountQuorum(string,string)",
            name,
            quorum);
        (bool success, bytes memory ret) = address(serviceContractAddress).delegatecall(payload);
        require(success, "Error calling service contract function");
        result = ret;
    }

    // Gets account details
    function getAccountDetail() public returns (bytes memory result) {
        bytes memory payload = abi.encodeWithSignature(
            "getAccountDetail()");
        (bool success, bytes memory ret) = address(serviceContractAddress).delegatecall(payload);
        require(success, "Error calling service contract function");
        result = ret;
    }
}
