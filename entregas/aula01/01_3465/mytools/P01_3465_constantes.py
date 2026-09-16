PI_INT = "1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
E_INT = "7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274"


def pi_real(n: int) -> str:
    if n > len(PI_INT):
        raise ValueError(f"O valor de n é muito grande. O valor máximo deve ser {PI_INT}")
    return f"3,{PI_INT[:n]}"


def e_real(n: int) -> str:
    if n > len(E_INT):
        raise ValueError(f"O valor de n é muito grande. O valor máximo deve ser {E_INT}")
    return f"2,{E_INT[:n]}"
