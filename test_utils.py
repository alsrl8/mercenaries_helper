import unittest
import utils


class TestUtils(unittest.TestCase):

    def test_mercenary_is_valid(self):
        mercenary_names = utils.read_all_mercenary_names_from_local()
        self.assertTrue(len(mercenary_names) > 0)

        roles = ['Caster', 'Fighter', 'Protector']
        rarities = ['Rare', 'Epic', 'Legendary']
        minion_types = ['Draenei', 'Dwarf', 'Gnome', 'High Elf', 'Human', 'Night Elf', 'Worgen', 'Blood Elf', 'Goblin',
                        'Half-Orc', 'Orc', 'Tauren', 'Troll', 'Undead', 'None', 'Beast', 'Centaur', 'Demon', 'Dragon',
                        'Egg', 'Elemental', 'Furbolg', 'Gronn', 'Mech', 'Murloc', 'Naga', 'Ogre', 'Old God', 'Pandaren',
                        'Pirate', 'Quilboar', 'Totem', 'Treant']
        factions = ['Alliance', 'Horde', 'None']

        for name in mercenary_names:
            mercenary = utils.read_mercenary_from_local(name)
            self.assertEqual(name, mercenary['Name'])
            self.assertEqual('Mercenary', mercenary['Card type'])
            self.assertIn(mercenary['Role'], roles)
            self.assertIn(mercenary['Rarity'], rarities)
            self.assertIn(mercenary['Minion type'], minion_types)
            self.assertIn(mercenary['Faction'], factions)
