from brownie import FundMe, network, config
from scripts.Library import get_account, get_priceFeed

# import scripts.Library as lib  --> lib.get_account()


def deploy_fundme():

    account = get_account()
    priceFeed_address = get_priceFeed(_decimals=8, _initialAnswer=466732000000)
    FundME_obj = FundMe.deploy(
        priceFeed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    # 10712785924256318
    # 49999999999999998127
    print(f"contract deployed to {FundME_obj.address}")
    return FundME_obj


def main():
    deploy_fundme()
