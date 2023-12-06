from pysyt.syt import all_sytx

def test_all_sytx():
    nu = [5, 3, 2]
    assert len(all_sytx(nu)) == 450

