import unittest
from unittest.mock import Mock, call

from kauppa import Kauppa
from tuote import Tuote
from varasto import Varasto
from viitegeneraattori import Viitegeneraattori


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock(spec=Viitegeneraattori)
        self.viitegeneraattori_mock.uusi.return_value = 42

        tuotteet = {1: Tuote(1, "maito", 5), 2: Tuote(2, "leipä", 3)}
        self.saldot = {1: 2, 2: 1}

        self.varasto_mock = Mock(spec=Varasto)
        self.varasto_mock.saldo.side_effect = self.saldot.__getitem__
        self.varasto_mock.hae_tuote.side_effect = tuotteet.__getitem__
        self.varasto_mock.ota_varastosta.side_effect = self._vahenna_saldoa

        self.kauppa = Kauppa(
            self.varasto_mock,
            self.pankki_mock,
            self.viitegeneraattori_mock,
        )
        self.kauppa.aloita_asiointi()
        self.asiakas = "pekka"
        self.tili = "12345"

    def _vahenna_saldoa(self, tuote):
        self.saldot[tuote.id] -= 1

    def _maksa_kori(self, *tuote_idt):
        for tuote_id in tuote_idt:
            self.kauppa.lisaa_koriin(tuote_id)
        self.kauppa.tilimaksu(self.asiakas, self.tili)

    def _assert_tilisiirto(self, summa):
        self.pankki_mock.tilisiirto.assert_called_with(
            self.asiakas, 42, self.tili, "33333-44455", summa
        )

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        self._maksa_kori(1)

        self.pankki_mock.tilisiirto.assert_called()

    def test_yhden_tuotteen_maksu(self):
        self._maksa_kori(1)

        self._assert_tilisiirto(5)

    def test_kahden_eri_tuotteen_maksu(self):
        self._maksa_kori(1, 2)

        self._assert_tilisiirto(8)

    def test_kahden_saman_tuotteen_maksu(self):
        self._maksa_kori(1, 1)

        self._assert_tilisiirto(10)

    def test_loppunutta_tuotetta_ei_veloiteta(self):
        self.saldot[2] = 0

        self._maksa_kori(1, 2)

        self._assert_tilisiirto(5)

    def test_uusi_asiointi_ei_sisalla_edellisen_ostoksen_tuotteita(self):
        self._maksa_kori(1)

        self.kauppa.aloita_asiointi()
        self._maksa_kori(2)

        self._assert_tilisiirto(3)

    def test_jokainen_maksu_pyytää_uuden_viitenumeron(self):
        self.viitegeneraattori_mock.uusi.side_effect = [42, 43]

        self._maksa_kori(1)
        self.kauppa.aloita_asiointi()
        self._maksa_kori(2)

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)
        self.assertEqual(
            self.pankki_mock.tilisiirto.call_args_list,
            [
                call(self.asiakas, 42, self.tili, "33333-44455", 5),
                call(self.asiakas, 43, self.tili, "33333-44455", 3),
            ],
        )
