import numpy as np
import typing as ty
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import FloatVector


def symmetry_test(
    x: ty.Union[tuple, list, np.ndarray],
    test_statistic: str = 'MI',
    test_k: int = 1,
    _module: str = 'symmetry',
    _method: str = 'symmetry_test',
    **kw,
) -> dict:
    test = getattr(get_module(_module), _method)
    result = test(
        x=FloatVector(x),
        stat=test_statistic,
        k=test_k,
        **kw,
    )
    return _result_to_dict(result)


def p_symmetry(x: np.ndarray, **kw) -> float:
    return float(symmetry_test(x, **kw)['p.value'])


def get_module(name: str = 'symmetry'):
    if not rpackages.isinstalled(name):
        if name == 'symmetry':
            _install_package_on_the_fly(name)
        else:
            # I'm not doing this for any package for safety reasons
            raise ModuleNotFoundError(
                f'{name} is not installed in R, you can use '
                f'_install_package_on_the_fly(\'{name}\')"'
            )
    return rpackages.importr(name)


def _install_package_on_the_fly(package: str) -> None:
    from rpy2.robjects.vectors import StrVector

    utils = rpackages.importr('utils')
    packnames = (package,)
    utils.chooseCRANmirror(ind=1)
    utils.install_packages(StrVector(packnames))


def _float_or_str(x) -> ty.Union[str, float]:
    """Try making x a float, or a string otherwise"""
    try:
        return float(x)
    except ValueError:
        pass
    return str(x)


def _result_to_dict(res) -> dict:
    """Extract htest results from a rpy2.robjects.vectors.ListVector object"""
    res_dict = {}
    for i, n in enumerate(res.names):
        v = res[i]
        if len(v) == 1:
            v = _float_or_str(v[0])
        res_dict[n] = v
    return res_dict
