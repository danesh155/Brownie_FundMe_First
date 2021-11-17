from scripts.Library import get_account, Local_Blockchain_Env
from scripts.deploy import deploy_fundme
from brownie import (
    network,
    accounts,
    exceptions,
)  # exception is for time we want error happen and that is good
import pytest

# import scripts.Library as lib  --> lib.get_account()


def test_can_fund_withdraw():
    account = get_account()
    FundME_obj = deploy_fundme()

    entrance_fee = FundME_obj.USDToEthereum(50) + 100  # +100 is a tips
    tnx = FundME_obj.fund({"from": account, "value": entrance_fee})
    tnx.wait(1)
    assert FundME_obj.addressToAmountFunded(account.address) == entrance_fee
    tnx2 = FundME_obj.withdraw({"from": account})
    tnx2.wait(1)
    assert FundME_obj.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in Local_Blockchain_Env:
        pytest.skip("only for local testing...")
    # account = get_account()
    FundMe_obj = deploy_fundme()
    not_owner_account = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        FundMe_obj.withdraw({"from": not_owner_account})
