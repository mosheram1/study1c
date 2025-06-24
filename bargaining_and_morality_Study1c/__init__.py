from otree.api import *
from otree.api import BaseConstants
from otree.api import models
from otree.api import widgets
from otree.api import WaitPage
from otree.api import Page
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer

import random
#c = cu
doc = "This research study includes a 2 players bargaining game, a private questionnaire, and a guessing" \
      " task that affects both players. \nParticipant's payment will be determined by his/her" \
      " performance in the bargaining phase and by the task phase results."


# TODO - TB: It seems that the group interaction is synchronised, but you don't set any timer on the Pages
# (except for Negotiation). Participants matched with dropouts will be stuck on the Wait_Payoff page.
# Similarly, there isn't any system in place to detect dropouts in this part of the study.

class C(BaseConstants):
    NAME_IN_URL = 'bargaining_and_morality_Study1b'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    ZOPA = 100
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'
    NN = 48
    INSTRUCTIONS_TEMPLATE = 'bargaining_and_morality_Study1b/instructions.html'
    ROLL_TEMPLATE = 'bargaining_and_morality_Study1b/roll.html'


class Subsession(BaseSubsession):
    pass
# Functions

def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        p.participant.excluded = False
        p.participant.unmatched = False


def waiting_too_long(player):
    import time
    arrival = player.participant.vars.get('wait_page_arrival', None)
    if arrival is None:
        return False
    return time.time() - arrival > 300



def group_by_arrival_time_method(subsession, waiting_players):
    if len(waiting_players) >= 2:
        return waiting_players[:2]
    for player in waiting_players:
        if waiting_too_long(player):
            player.participant.unmatched = True
            return [player]


class Group(BaseGroup):
    SRP = models.IntegerField()
    BRP = models.IntegerField()
    is_finished = models.BooleanField(initial=False)
    NegPayS = models.FloatField()
    NegPayB = models.FloatField()
    deal_price = models.FloatField()
    Did_not_report_same = models.LongStringField(initial=' ')
    Group_Type = models.IntegerField()
    BRP_NN = models.FloatField()
    abc00 = models.FloatField()
    abc01 = models.FloatField()
    abc10 = models.FloatField()
    abc11 = models.FloatField()
    abc20 = models.FloatField()
    abc21 = models.FloatField()
    abc30 = models.FloatField()
    abc31 = models.FloatField()
    abc40 = models.FloatField()
    abc41 = models.FloatField()
    abc50 = models.FloatField()
    abc51 = models.FloatField()
    abc60 = models.FloatField()
    abc61 = models.FloatField()
    abc70 = models.FloatField()
    abc71 = models.FloatField()
    abc80 = models.FloatField()
    abc81 = models.FloatField()
    partner_condition = models.StringField()


def RP(group: Group):
    import random
    import numpy as np
    group.SRP = round(np.random.normal(loc=100.0, scale=16.66, size=1)[0])
    group.BRP = group.SRP + C.ZOPA
    group.BRP_NN = group.SRP + C.NN
    gType = random.choice([1, 2, 3, 4])
    group.Group_Type = gType
    group.deal_price = group.in_round(1).BRP_NN

# def set_payoffs(group: Group):

#    p1 = group.get_player_by_id(1)
#    p2 = group.get_player_by_id(2)

#   p1_chosen_value_s = sum([p.chosen_letter_value_for_self for p in p1.in_all_rounds()]) / len(p1.in_all_rounds())
#   p2_chosen_value_s = sum([p.chosen_letter_value_for_self for p in p2.in_all_rounds()]) / len(p2.in_all_rounds())
#   p1_chosen_value_o = sum([p.chosen_letter_value_for_other for p in p1.in_all_rounds()]) / len(p1.in_all_rounds())
#   p2_chosen_value_o = sum([p.chosen_letter_value_for_other for p in p2.in_all_rounds()]) / len(p2.in_all_rounds())

#   if group.in_round(1).Group_Type <= 2:

#      if p1.in_round(1).is_deal == 0:
#           group.NegPayS = ((group.in_round(1).deal_price) - (group.in_round(1).SRP)) / 100
#           group.NegPayB = (group.in_round(1).BRP - (group.in_round(1).deal_price)) / 100

#       else:
#           group.NegPayS = 0
#           group.NegPayB = 0
#           group.Did_not_report_same = 'You and the other participant did not reach an agreement'
#   if group.in_round(1).Group_Type >= 3:
#       group.NegPayS = ((group.in_round(1).deal_price) - (group.in_round(1).SRP)) / 100
#       group.NegPayB = (group.in_round(1).BRP - (group.in_round(1).deal_price)) / 100

#   p1.payoff = (p1_chosen_value_s + p2_chosen_value_o) / 2
#   p2.payoff = (p1_chosen_value_o + p2_chosen_value_s) / 2

def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    def avg_value(player, field):
        rounds = player.in_all_rounds()
        return sum(getattr(p, field, 0) for p in rounds) / max(len(rounds), 1)  # Prevent division by zero

    p1_chosen_value_s = avg_value(p1, 'chosen_letter_value_for_self')
    p2_chosen_value_s = avg_value(p2, 'chosen_letter_value_for_self')
    p1_chosen_value_o = avg_value(p1, 'chosen_letter_value_for_other')
    p2_chosen_value_o = avg_value(p2, 'chosen_letter_value_for_other')

    if group.in_round(1).Group_Type <= 2:
        if p1.in_round(1).is_deal == 0:
            group.NegPayS = ((group.in_round(1).deal_price) - (group.in_round(1).SRP)) / 100
            group.NegPayB = (group.in_round(1).BRP - (group.in_round(1).deal_price)) / 100
        else:
            group.NegPayS = 0
            group.NegPayB = 0
            group.Did_not_report_same = 'You and the other participant did not reach an agreement'
    else:
        group.NegPayS = ((group.in_round(1).deal_price) - (group.in_round(1).SRP)) / 100
        group.NegPayB = (group.in_round(1).BRP - (group.in_round(1).deal_price)) / 100

    p1.payoff = (p1_chosen_value_s + p2_chosen_value_o) / 2
    p2.payoff = (p1_chosen_value_o + p2_chosen_value_s) / 2



def Chat_nickname(player):
    group = player.group
    if player.id_in_group == 1:
        return "Seller"
    if player.id_in_group == 2:
        return "Buyer"


class Player(BasePlayer):
    Age_dec = models.StringField(
        choices=["I am over 18 and agree to participate"],
        label="Consent",
        widget=widgets.RadioSelect,
    )
    MTurk_ID = models.StringField(label="Please write your MTurk ID (for verification):")
    Residence = models.StringField(
        choices=["Yes", "No"],
        label="Do you live in the United States?",
        widget=widgets.RadioSelect,
    )
    English = models.StringField(
        choices=["Yes", "No"],
        label="Do you speak, read, and write English fluently?",
        widget=widgets.RadioSelect,
    )
    Verification = models.StringField(
        choices=["Yes", "No"],
        label="Are you reading carefully? Please mark 'no' in this question.",
        widget=widgets.RadioSelect,
    )
    chosen_letter_value_for_self = models.FloatField()
    chosen_letter_value_for_other = models.FloatField()
    Age = models.StringField(choices=[['18-29', '18-29'], ['30-39', '30-39'], ['40-49', '40-49'], ['50-59', '50-59'],
                                      ['60+', '60 or older']], label='Which category below includes your age?')
    Gender = models.StringField(choices=[['Male', 'Male'], ['Female', 'Female'], ['Not listed', 'Not listed']],
                                label='What is your gender?')

    my_RP = models.IntegerField(label='My reservation price was')
    my_AP = models.IntegerField(label='My aspiration price was ')
    First_offer = models.IntegerField(label='First offer was')
    Agreed = models.IntegerField(label='The agreed price was')
    Other_RP = models.IntegerField(label='I think that the other participant’s reservation price was', max=250, min=50)
    conflict1 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7 '], [0, 'N/A']],
        label='The other participant sent aggressive messages ', widget=widgets.RadioSelectHorizontal)
    conflict2 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                    label='I viewed the other participant as a competitor',
                                    widget=widgets.RadioSelectHorizontal)
    conflict3 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                    label='The other participant and I had similar interests',
                                    widget=widgets.RadioSelectHorizontal)
    conflict4 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                    label='Helping the other participant was important to me',
                                    widget=widgets.RadioSelectHorizontal)
    conflict5 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                    label='Harming the other participant was important to me',
                                    widget=widgets.RadioSelectHorizontal)
    conflict6 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                    label='The other participant and I had conflicting interests',
                                    widget=widgets.RadioSelectHorizontal)
    conflict7 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                    label='I would want to work with the other participant again',
                                    widget=widgets.RadioSelectHorizontal)
    trust1 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
                                 label='The other participant thinks that I am very concerned about his or her welfare',
                                 widget=widgets.RadioSelectHorizontal)
    trust2 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
                                 label='The other participant thinks that his needs and desires are very important to me',
                                 widget=widgets.RadioSelectHorizontal)
    trust3 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
                                 label='The other participant thinks that I would not knowingly do anything to hurt him',
                                 widget=widgets.RadioSelectHorizontal)
    trust4 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
                                 label='The other participant thinks that I really look out for what is important to him',
                                 widget=widgets.RadioSelectHorizontal)
    trust5 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
                                 label='The other participant thinks that I will go out of my way to help him',
                                 widget=widgets.RadioSelectHorizontal)
    guilt1 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                 label='I feel guilty for some of the things I did or planned to do during the first stage',
                                 widget=widgets.RadioSelectHorizontal)
    guilt2 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                 label='I feel guilty for how I treated or planned to treat the other participant during the negotiation',
                                 widget=widgets.RadioSelectHorizontal)
    guilt3 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                 label='I regret how I treated or planned to treat the other participant during the negotiation',
                                 widget=widgets.RadioSelectHorizontal)
    Relative_outcome_perception = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='How do you feel you performed (achieved your goals) in this negotiation as compared to the other participant? (Please pay attention that for this question, 1 indicates much worse and 7 indicates much better)',
        widget=widgets.RadioSelectHorizontal)
    anger1 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                 label='I am happy after closing the agreement', widget=widgets.RadioSelectHorizontal)
    anger2 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
                                 label='I am angry after closing the agreement', widget=widgets.RadioSelectHorizontal)
    competitive_mindset1 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='Even in a group working towards a common goal, I still want to outperform others',
        widget=widgets.RadioSelectHorizontal)
    competitive_mindset2 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='My self-worth could be validated only if I outperform others in a group',
        widget=widgets.RadioSelectHorizontal)
    competitive_mindset3 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='Sometimes I consider appraisals as an opportunity to prove that I am smarter than others',
        widget=widgets.RadioSelectHorizontal)
    competitive_mindset4 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='I like competition because it gives me a chance to discover my own potential',
        widget=widgets.RadioSelectHorizontal)
    competitive_mindset5 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='I like challenges that are brought by competing with other team members',
        widget=widgets.RadioSelectHorizontal)
    competitive_mindset6 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='I like competition because it allows me to play my best', widget=widgets.RadioSelectHorizontal)
    competitive_mindset7 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='Being outperformed by other members in the group annoys me', widget=widgets.RadioSelectHorizontal)
    competitive_mindset8 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='Losing in sport contests makes me feel sad', widget=widgets.RadioSelectHorizontal)
    competitive_mindset9 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='I get jealous when other team members get rewarded for their achievements',
        widget=widgets.RadioSelectHorizontal)
    competitive_mindset10 = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']],
        label='I cannot stand being beaten in an argument by other team members', widget=widgets.RadioSelectHorizontal)
    dist_nego_behavior1 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
                                              label='The other participant tried to impose his or her own will upon me',
                                              widget=widgets.RadioSelectHorizontal)
    dist_nego_behavior2 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
                                              label='The other participant tried to search for gains',
                                              widget=widgets.RadioSelectHorizontal)
    dist_nego_behavior3 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
                                              label='The other participant fought for good outcome for himself',
                                              widget=widgets.RadioSelectHorizontal)
    dist_nego_behavior4 = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
                                              label='The other participant tried to do everything to win',
                                              widget=widgets.RadioSelectHorizontal)
    amount_proposed = models.IntegerField(initial=0)
    amount_accepted = models.IntegerField()
    feedback = models.LongStringField(blank=True,
                                      label='Is there any feedback you’d like to give about this research study?')
    first_offeror = models.StringField(choices=[['Yes', 'Yes'], ['No', 'No'], ['N/A', 'N/A']],
                                       label='I made the first offer', widget=widgets.RadioSelect)
    timeSpent = models.FloatField()
    propose_time = models.LongStringField(blank=True, initial='None')
    my_field = models.StringField()
    is_deal = models.FloatField(initial=0)
    chosen_letter = models.CharField(initial=None, choices=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])


def get_or_none(instance, field):
    try:
        return getattr(instance, field)
    except TypeError:
        return None

def custom_export(players):
    yield ['participant_code', 'id_in_group']
    for p in players:
        pp = p.participant
        yield [pp.code, p.id_in_group]


class GroupingPage(WaitPage):
    group_by_arrival_time = True
    after_all_players_arrive = RP
    title_text = 'Please wait for other participants to join'

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.unmatched:
            return upcoming_apps[0]

    @staticmethod
    def is_displayed(player: Player):
        import time
        if 'wait_page_arrival' not in player.participant.vars:
            player.participant.vars['wait_page_arrival'] = time.time()
        return player.round_number == 1


class Seller_instructions(Page):
    form_model = 'group'

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 1 and player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        pass


class Buyer_instructions(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2 and player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        pass


class No_Neg_Agreed(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.round_number == 1 and group.Group_Type >= 3


class Wait_negotiation(WaitPage):
    title_text = 'Negotiation will start in few seconds'

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.round_number == 1 and group.Group_Type <= 2


class Negotiation(Page):
    form_model = 'player'
    form_fields = ['timeSpent', 'propose_time']
    timeout_seconds = 300
    timer_text = 'Time left for negotiation'

    @staticmethod
    def is_displayed(player: Player):
        group = player.group

        return player.round_number == 1 and group.Group_Type <= 2
        # deal_price = get_or_none(group, 'deal_price')
        # return deal_price is None

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(nickname=Chat_nickname(player), other_role=player.get_others_in_group()[0].role)

    @staticmethod
    def js_vars(player: Player):
        group = player.group
        return dict(my_id=player.id_in_group)

    @staticmethod
    def before_next_page(player, timeout_happened):
        group = player.group

        if timeout_happened and not group.is_finished:
            [other] = player.get_others_in_group()
            offer = other.amount_proposed

            if offer is not None:
                if player.role() == "Buyer" and offer > group.BRP:
                    deal = group.BRP
                elif player.role() == "Seller" and offer < group.SRP:
                    deal = group.SRP
                else:
                    deal = offer

                group.deal_price = deal
                group.is_finished = True

                for p in group.get_players():
                    p.amount_accepted = deal
                    p.is_deal = 1

    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        [other] = player.get_others_in_group()

        # אם כבר הסתיים
        if group.is_finished:
            return {
                p.id_in_group: dict(finished=True)
                for p in group.get_players()
            }

        if 'amount' in data:
            try:
                amount = int(data['amount'])
            except Exception:
                print('Invalid message received', data)
                return

            # אם התקבלה הצעה חדשה
            if data['type'] == 'propose':
                player.amount_proposed = amount
                return {
                    p.id_in_group: dict(proposals=[(player.id_in_group, amount)])
                    for p in group.get_players()
                }

            # אם התקבלה הסכמה רגילה
            elif data['type'] == 'accept':
                if amount == other.amount_proposed:
                    player.amount_accepted = amount
                    group.deal_price = amount
                    group.is_finished = True
                    return {
                        p.id_in_group: dict(finished=True)
                        for p in group.get_players()
                    }

            # אם התקבלה הסכמה אוטומטית
            elif data['type'] == 'force_accept':
                player.amount_accepted = amount
                group.deal_price = amount
                group.is_finished = True
                return {
                    p.id_in_group: dict(force_accept=True, finished=True)
                    for p in group.get_players()
                }

        proposals = []
        for p in [player, other]:
            amount_proposed = get_or_none(p, 'amount_proposed')
            if amount_proposed is not None:
                proposals.append([p.id_in_group, amount_proposed])

        return {0: dict(proposals=proposals)}

    @staticmethod
    def error_message(player: Player, values):
        group = player.group

        def error_message(player: Player, values):
            group = player.group
            if not group.is_finished:
                return "Game not finished yet"


class Neg_Results(Page):
    form_model = 'group'

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.round_number == 1 and group.Group_Type <= 2

class ReassignWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        import random

        players = subsession.get_players()
        random.shuffle(players)

        # מחלק את השחקנים לזוגות
        new_groups = [players[i:i + 2] for i in range(0, len(players), 2)]

        # מעדכן את מטריצת הקבוצות (עכשיו אלה קבוצות אמיתיות מסוג Group)
        subsession.set_group_matrix(new_groups)

        # מחלק מחצית הקבוצות ל"same", ומחצית ל"random"
        for i, group in enumerate(subsession.get_groups()):
            if i < len(new_groups) // 2:
                group.partner_condition = 'same'
            else:
                group.partner_condition = 'random'




class Intro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            condition=player.group.partner_condition
        )

class Choice(Page):
    form_model = 'player'
    form_fields = ['chosen_letter']

    @staticmethod
    def vars_for_template(player: Player):

        group = player.group
        abc = [[1, 0], [1, 1], [1, -1], [0, 1], [0, 0], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
        random.shuffle(abc)

        group.abc00 = abc[0][0]
        group.abc01 = abc[0][1]
        group.abc10 = abc[1][0]
        group.abc11 = abc[1][1]
        group.abc20 = abc[2][0]
        group.abc21 = abc[2][1]
        group.abc30 = abc[3][0]
        group.abc31 = abc[3][1]
        group.abc40 = abc[4][0]
        group.abc41 = abc[4][1]
        group.abc50 = abc[5][0]
        group.abc51 = abc[5][1]
        group.abc60 = abc[6][0]
        group.abc61 = abc[6][1]
        group.abc70 = abc[7][0]
        group.abc71 = abc[7][1]
        group.abc80 = abc[8][0]
        group.abc81 = abc[8][1]

        return dict(
            abc00=group.abc00,
            abc01=group.abc01,
            abc10=group.abc10,
            abc11=group.abc11,
            abc20=group.abc20,
            abc21=group.abc21,
            abc30=group.abc30,
            abc31=group.abc31,
            abc40=group.abc40,
            abc41=group.abc41,
            abc50=group.abc50,
            abc51=group.abc51,
            abc60=group.abc60,
            abc61=group.abc61,
            abc70=group.abc70,
            abc71=group.abc71,
            abc80=group.abc80,
            abc81=group.abc81
        )

    @staticmethod
    def set_chosen_letter_values(player: Player):
        group = player.group
        if player.chosen_letter == 'A':
            player.chosen_letter_value_for_self = group.abc00
            player.chosen_letter_value_for_other = group.abc01
        elif player.chosen_letter == 'B':
            player.chosen_letter_value_for_self = group.abc10
            player.chosen_letter_value_for_other = group.abc11
        elif player.chosen_letter == 'C':
            player.chosen_letter_value_for_self = group.abc20
            player.chosen_letter_value_for_other = group.abc21
        elif player.chosen_letter == 'D':
            player.chosen_letter_value_for_self = group.abc30
            player.chosen_letter_value_for_other = group.abc31
        elif player.chosen_letter == 'E':
            player.chosen_letter_value_for_self = group.abc40
            player.chosen_letter_value_for_other = group.abc41
        elif player.chosen_letter == 'F':
            player.chosen_letter_value_for_self = group.abc50
            player.chosen_letter_value_for_other = group.abc51
        elif player.chosen_letter == 'G':
            player.chosen_letter_value_for_self = group.abc60
            player.chosen_letter_value_for_other = group.abc61
        elif player.chosen_letter == 'H':
            player.chosen_letter_value_for_self = group.abc70
            player.chosen_letter_value_for_other = group.abc71
        elif player.chosen_letter == 'I':
            player.chosen_letter_value_for_self = group.abc80
            player.chosen_letter_value_for_other = group.abc81
        else:
            player.chosen_letter_value_for_self = 0
            player.chosen_letter_value_for_other = 0

    def before_next_page(player, timeout_happened):
        Choice.set_chosen_letter_values(player)


class Questionnaire_1(Page):
    form_model = 'player'
    form_fields = ['First_offer', 'my_RP', 'my_AP', 'Agreed', 'Other_RP', 'first_offeror']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(GT=group.in_round(1).Group_Type, BRP_NN=group.in_round(1).BRP_NN,)


class Instructions(Page):
    form_model = 'player'
    form_fields = ['Age_dec', 'MTurk_ID', 'Residence', 'English', 'Verification']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Questionnaire_2(Page):
    form_model = 'player'
    form_fields = ['conflict1', 'conflict2', 'conflict3', 'conflict4', 'conflict5', 'conflict6', 'conflict7']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(GT=group.in_round(1).Group_Type)


class Questionnaire_3(Page):
    form_model = 'player'
    form_fields = ['trust1', 'trust2', 'trust3', 'trust4', 'trust5']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


class Questionnaire_4(Page):
    form_model = 'player'
    form_fields = ['guilt1', 'guilt2', 'guilt3', 'Relative_outcome_perception', 'anger1', 'anger2',
                   'competitive_mindset1', 'competitive_mindset2', 'competitive_mindset3', 'competitive_mindset4',
                   'competitive_mindset5', 'competitive_mindset6', 'competitive_mindset7', 'competitive_mindset8',
                   'competitive_mindset9', 'competitive_mindset10']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


class Questionnaire_5(Page):
    form_model = 'player'
    form_fields = ['dist_nego_behavior1', 'dist_nego_behavior2', 'dist_nego_behavior3', 'dist_nego_behavior4']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


class Demographic(Page):
    form_model = 'player'
    form_fields = ['Age', 'Gender', 'feedback']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


class Wait_Payoff(WaitPage):
    after_all_players_arrive = set_payoffs
    title_text = 'Please wait for the other participant to complete his/her task'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


# class Payoff(Page):
#   form_model = 'group'

#   @staticmethod
#   def is_displayed(player: Player):
#       return player.round_number == 2

#   @staticmethod
#   def vars_for_template(player: Player):
#       group = player.group
#       return dict(payoff1=player.payoff + 2.5, PID=player.id_in_group, TaskPayS=player.payoff,
#                   TaskPayB=player.payoff, )

class Payoff(Page):
    form_model = 'group'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        participation_fee = 2.5  # Fixed amount given to all participants

        # Assign task payoff based on player role
        if player.id_in_group == 1:
            task_payoff = player.payoff
            negotiation_payoff = group.NegPayS  # Seller's negotiation earnings
        else:
            task_payoff = player.payoff
            negotiation_payoff = group.NegPayB  # Buyer's negotiation earnings

        # Total payoff = Participation Fee + Task Payoff + Negotiation Payoff
        total_payoff = participation_fee + task_payoff + negotiation_payoff

        return dict(
            payoff1=total_payoff,  # Correct total payoff
            PID=player.id_in_group,
            TaskPayS=task_payoff if player.id_in_group == 1 else None,  # Only for sellers
            TaskPayB=task_payoff if player.id_in_group == 2 else None,  # Only for buyers
        )

page_sequence = [
    #Instructions,
    GroupingPage, Seller_instructions,
                 Buyer_instructions, No_Neg_Agreed, Wait_negotiation, Negotiation, Neg_Results, ReassignWaitPage, Intro, Choice,
                 Demographic, Wait_Payoff, Payoff]
