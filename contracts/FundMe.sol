// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public fundersArr;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minimumUSD = 50 * 10**8;
        require(
            EthereumToUSD(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        fundersArr.push(msg.sender);
    }

    // version of AggregatorV3Interface
    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    // decimals of AggregatorV3Interface
    function getdecimals() public view returns (uint8) {
        return priceFeed.decimals();
    }

    // Price of 1 Ethereum in USD
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer); // * 10000000000); //10 -- it has 8 digits by own
    }

    // getConversionRate
    function EthereumToUSD(uint256 ethAmount) public view returns (uint256) {
        return (getPrice() * ethAmount) / (10**8); // / (10 ** _maxDec); // parametrs , uint8 _maxDec - 18
    }

    //getEntraceFee
    // USD To Ethereum
    function USDToEthereum(uint256 _usdAmount) public view returns (uint256) {
        uint256 usdAmount = _usdAmount * 10**8; // becuase getprice() has 8 decimals, it has to has 8 digit by own
        uint256 precision = 1 * 10**18; // parameters, uint8 _maxDec)
        return (usdAmount * precision) / getPrice();
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);

        //reset all address and mapp after withdraw
        for (
            uint256 funderIndex = 0;
            funderIndex < fundersArr.length;
            funderIndex++
        ) {
            address funder = fundersArr[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        fundersArr = new address[](0);
    }
}
