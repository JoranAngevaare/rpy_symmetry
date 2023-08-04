def test_minimal():
    import rpy_symmetry as rsym

    pval = rsym.p_symmetry([1, 2, 3])
    assert pval
