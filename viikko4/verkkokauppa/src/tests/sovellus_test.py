import runpy
from contextlib import redirect_stdout
from io import StringIO

import index
from kirjanpito import Kirjanpito
from tuote import Tuote
from varasto import Varasto


def test_sovelluksen_esimerkkivirta():
    tuloste = StringIO()

    with redirect_stdout(tuloste):
        runpy.run_path(index.__file__, run_name="__main__")

    assert "tilisiirto:" in tuloste.getvalue()
    assert "otettiin varastosta" in tuloste.getvalue()
    assert "palautettiin varastoon" in tuloste.getvalue()


def test_varasto_ei_palauta_tuntematonta_tuotetta():
    varasto = Varasto(Kirjanpito())

    assert varasto.hae_tuote(999) is None


def test_saman_tuotetunnuksen_tuotteet_ovat_samoja():
    assert Tuote(1, "maito", 5) == Tuote(1, "eri nimi", 99)
