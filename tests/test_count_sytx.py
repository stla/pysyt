from pysyt.syt import count_sytx

def test_count_sytx():
    nu = [5, 3, 2]
    assert count_sytx(nu) == 450

