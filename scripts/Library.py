from brownie import config, network, accounts, MockV3Aggregator

# from web3 import Web3

Forked_Local_Env = ["mainnet-fork" , "mainnet-fork-dev"]
Local_Blockchain_Env = ["development", "ganache-local"]


def get_account():
    if (
        network.show_active() in Local_Blockchain_Env
        or network.show_active() in Forked_Local_Env
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_priceFeed(_decimals=8, _initialAnswer=312300000000):
    # pass pass price feed address tyo our fundme contract
    # if we are on a persistent network use associated address like kovan
    # otherwise , deploy mocks
    if network.show_active() not in Local_Blockchain_Env:
        return config["networks"][network.show_active()]["ethusd_priceFeed"]
    else:
        print(f"active network is {network.show_active()}")
        print("Deploying Mock...")
        if len(MockV3Aggregator) <= 0:
            # mock_aggregator = MockV3Aggregator.deploy(_decimals, Web3.toWei(_initialAnswer, "ether"), {"from": get_account()})
            MockV3Aggregator.deploy(
                _decimals, _initialAnswer, {"from": get_account()}
            )  # _initialAnswer = Web3.toWei(_initialAnswer, "ether")
        print("Mock Deployed!")
        # return mock_aggregator.address
        return MockV3Aggregator[-1].address
