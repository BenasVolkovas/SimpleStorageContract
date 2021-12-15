// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

contract SimpleStorage {
    /* visibility:
        public -> all contracts can get it, same contract too.
        private -> only the same contract can get it.
        internal -> only the same contract and its derivatives can get it.
        external -> only the external contracts can get it
    */

    /* modifiers:
        view -> can read the blockchain
        pure -> cannot read the blockchain, all the data needs to be provided by parameters
    */

    /* data storing way
        memory -> data will only be stored during the execution of the function
        storage -> data will remain on blockchain after the function is ran
    */

    //////////
    // CODE //
    //////////

    uint256 favoriteNumber;

    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    struct Person {
        uint256 favoriteNumber;
        string name;
    }

    Person[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(Person(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
