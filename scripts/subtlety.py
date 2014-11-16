# Simple test program to debug + play with subtlety models.
from os import path
import sys
#sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))

from shadowcraft.calcs.rogue.Aldriana import AldrianasRogueDamageCalculator
from shadowcraft.calcs.rogue.Aldriana import settings

from shadowcraft.objects import buffs
from shadowcraft.objects import race
from shadowcraft.objects import stats
from shadowcraft.objects import procs
from shadowcraft.objects import talents
from shadowcraft.objects import glyphs

from shadowcraft.core import i18n

# Set up language. Use 'en_US', 'es_ES', 'fr' for specific languages.
test_language = 'local'
i18n.set_language(test_language)

# Set up level/class/race
test_level = 100
test_race = race.Race('night_elf')
test_class = 'rogue'

# Set up buffs.
test_buffs = buffs.Buffs(
        'short_term_haste_buff',
        'stat_multiplier_buff',
        'crit_chance_buff',
        'mastery_buff',
        'haste_buff',
        'multistrike_buff',
        'versatility_buff',
        'attack_power_buff',
        'physical_vulnerability_debuff',
        'spell_damage_debuff',
        'flask_wod_agi',
        'food_mop_agi'
    )

# Set up weapons.
test_mh = stats.Weapon(420.5, 1.8, 'dagger', 'dancing_steel')
test_oh = stats.Weapon(420.5, 1.8, 'dagger', 'dancing_steel')

# Set up procs.
test_procs = procs.ProcsList(('primal_combatants_ioc', 620), ('primal_combatants_boc', 620), 'archmages_incandescence') #trinkets, other things (legendary procs)

# Set up gear buffs.
test_gear_buffs = stats.GearBuffs('gear_specialization') #tier buffs located here

# Set up a calcs object..
test_stats = stats.Stats(test_mh, test_oh, test_procs, test_gear_buffs,
                         agi=1957,
                         stam=2426,
                         crit=794,
                         haste=645,
                         mastery=557,
                         readiness=0,
                         versatility=154,
                         multistrike=121,)

# Initialize talents..
test_talents = talents.Talents('3222123', test_class, test_level)

# Set up glyphs.
glyph_list = []
test_glyphs = glyphs.Glyphs(test_class, *glyph_list)

# Set up settings.
test_cycle = settings.SubtletyCycle(5, use_hemorrhage='uptime')
test_settings = settings.Settings(test_cycle, response_time=.5, duration=360, dmg_poison='dp', utl_poison='lp', is_pvp=False,
                                 adv_params="")

# Build a DPS object.
calculator = AldrianasRogueDamageCalculator(test_stats, test_talents, test_glyphs, test_buffs, test_race, test_settings, test_level)

# Compute EP values.
ep_values = calculator.get_ep()
tier_ep_values = calculator.get_other_ep(['rogue_t16_2pc', 'rogue_t16_4pc'])

trinkets_list = [
    #5.4
    'assurance_of_consequence',
    'haromms_talisman',
    'sigil_of_rampage',
    'sigil_of_rampage',
    'ticking_ebon_detonator',
    'thoks_tail_tip',
    'discipline_of_xuen',
    'fury_of_xuen',
]

# Compute DPS Breakdown.
dps_breakdown = calculator.get_dps_breakdown()
total_dps = sum(entry[1] for entry in dps_breakdown.items())
talent_ranks = calculator.get_talents_ranking()

def max_length(dict_list):
    max_len = 0
    for i in dict_list:
        dict_values = i.items()
        if max_len < max(len(entry[0]) for entry in dict_values):
            max_len = max(len(entry[0]) for entry in dict_values)

    return max_len

def pretty_print(dict_list):
    max_len = max_length(dict_list)

    for i in dict_list:
        dict_values = i.items()
        dict_values.sort(key=lambda entry: entry[1], reverse=True)
        for value in dict_values:
            if ("{0:.2f}".format(float(value[1])/total_dps)) != '0.00':
                print value[0] + ':' + ' ' * (max_len - len(value[0])), str(value[1]) + ' ('+str( "{0:.2f}".format(100*float(value[1])/total_dps) )+'%)'
            else:
                print value[0] + ':' + ' ' * (max_len - len(value[0])), str(value[1])
        print '-' * (max_len + 15)

dicts_for_pretty_print = [
    ep_values,
    tier_ep_values,
    talent_ranks,
    #trinkets_ep_value,
    dps_breakdown
]
pretty_print(dicts_for_pretty_print)
print ' ' * (max_length(dicts_for_pretty_print) + 1), total_dps, _("total damage per second.")
