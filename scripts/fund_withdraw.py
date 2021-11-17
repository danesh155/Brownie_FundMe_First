from brownie import FundMe
from scripts.Library import get_account

# import scripts.Library as lib  --> lib.get_account()


def fund():
    fundme_obj = FundMe[-1]
    account = get_account()

    entrace_fee = fundme_obj.USDToEthereum(50)
    print(
        f"The Current Entrance Fee is: {entrace_fee} as eth - {fundme_obj.EthereumToUSD(entrace_fee)} as USD"
    )
    print("Funding...")
    fundme_obj.fund({"from": account, "value": entrace_fee})


def withdraw():
    fundme_obj = FundMe[-1]
    account = get_account()
    fundme_obj.withdraw({"from": account})


def main():
    fund()
    withdraw()
