import math
import numba
import numpy as np
from typing import TypeAlias

"""
原始根 (p,q)
"""
pq: TypeAlias = tuple[int, int]

"""
原子根符号
int型でmodをとって計算するのでexactに計算可能
const_powerd_samplesだと誤差が出る
"""
@numba.njit("c16[:](i8,i8,i8)")
def primitive_root_code(p: int, q: int, k: int=1) -> np.ndarray:
	result = [1.0]
	prev = k
	for i in range(p-1):
		result.append(np.exp(-1j*2*np.pi*prev/p))
		prev = (prev * q)%p
	return np.complex128(result)

"""
原始根^n符号
pq_list: (p,q)のリスト

2コの場合:
k: N
θn = q^n / p
Ψn = q'^n / p'
Xn = exp(-2j*π*θn*k)*exp(-2j*π*Ψn*k)
"""
def mixed_primitive_root_code(pq_set: list[pq], k: int) -> np.ndarray:
	code_len = math.lcm(*map(lambda pq: pq[0], pq_set))
	code = np.ones(code_len, dtype=np.complex128)
	for p,q in pq_set:
		code *= np.tile(primitive_root_code(p, q, k), code_len//p)
	return code