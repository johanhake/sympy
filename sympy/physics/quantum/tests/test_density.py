from sympy import pprint, latex, symbols
from sympy.physics.quantum.density import Density
from sympy.physics.quantum.state import Ket, Bra
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.represent import represent
from sympy.physics.quantum.dagger import Dagger
from sympy.physics.quantum.cartesian import XKet, PxKet, PxOp, XOp
from sympy.functions import sqrt
from sympy.utilities.pytest import raises

def test_eval_args():
    # check instance created
    assert isinstance(Density([Ket(0), 0.5], [Ket(1), 0.5]), Density)

    # check for value error, when prob is not provided
    raises(ValueError, lambda: Density([Ket(0)], [Ket(1)]))

def test_doit():
    x,y = symbols('x y')
    d = Density([XKet(),0.5], [PxKet(),0.5])
    assert (0.5*(PxKet()*Dagger(PxKet())) +
            0.5*(XKet()*Dagger(XKet()))) == d.doit()

    # check for kets with expr in them
    d_with_sym = Density([XKet(x*y),0.5], [PxKet(x*y),0.5])
    assert (0.5*(PxKet(x*y)*Dagger(PxKet(x*y))) +
            0.5*(XKet(x*y)*Dagger(XKet(x*y)))) == d_with_sym.doit()

def test_apply_op():
    d = Density([Ket(0), 0.5], [Ket(1), 0.5])
    assert d.apply_op(XOp()) == Density([XOp()*Ket(0), 0.5],
                                          [XOp()*Ket(1), 0.5])

def test_represent():
    x,y = symbols('x y')
    d = Density([XKet(),0.5], [PxKet(),0.5])
    assert (represent(0.5*(PxKet()*Dagger(PxKet()))) +
            represent(0.5*(XKet()*Dagger(XKet())))) == represent(d)

    # check for kets with expr in them
    d_with_sym = Density([XKet(x*y),0.5], [PxKet(x*y),0.5])
    assert (represent(0.5*(PxKet(x*y)*Dagger(PxKet(x*y)))) +
            represent(0.5*(XKet(x*y)*Dagger(XKet(x*y))))) == \
        represent(d_with_sym)

    # check when given explicit basis
    assert (represent(0.5*(XKet()*Dagger(XKet())), basis=PxOp()) +
            represent(0.5*(PxKet()*Dagger(PxKet())), basis=PxOp())) == \
        represent(d, basis=PxOp())

def test_states():
    d = Density([Ket(0), 0.5], [Ket(1), 0.5])
    states = d.states()
    assert states[0] == Ket(0) and states[1] == Ket(1)

def test_probs():
    d = Density([Ket(0), .75], [Ket(1), 0.25])
    probs = d.probs()
    assert probs[0] == 0.75 and probs[1] == 0.25

    #probs can be symbols
    x,y = symbols('x y')
    d = Density([Ket(0), x], [Ket(1), y])
    probs = d.probs()
    assert probs[0] == x and probs[1] == y

def test_get_state():
    x,y = symbols('x y')
    d = Density([Ket(0), x], [Ket(1), y])
    states = (d.get_state(0), d.get_state(1))
    assert states[0] == Ket(0) and states[1] == Ket(1)

def test_get_prob():
    x,y = symbols('x y')
    d = Density([Ket(0), x], [Ket(1), y])
    probs = (d.get_prob(0), d.get_prob(1))
    assert probs[0] == x and probs[1] == y
