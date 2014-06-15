import random
from wordnik import swagger, WordApi
from utils import check_unique_letters


def _get_word_api():
    access_dict = swagger.ApiClient('50f30864077a0f6b8941c7972f579b28af7de590fab336267',
                                    "http://api.wordnik.com/v4")
    return WordApi.WordApi(access_dict)


class CowsAndBullsGame(object):
    def __init__(self, total_guesses=15, difficulty='medium'):
        self._wordApi = _get_word_api()
        self.total_guesses = int(total_guesses)
        if self.total_guesses < 1 or self.total_guesses > 100:
            raise ValueError('total_guess should be a number 1 through 15')
        self.difficulty = difficulty[0].lower()
        difficulty_levels = {"easy", "medium", "hard"}
        if not self.difficulty in difficulty_levels:
            raise ValueError("difficulty should be 'easy', 'medium' or 'hard'")
        self.current_number_tries = 0
        self._final_word = self._generate_final_word()
        self._guessed_words = set()
        self._game_status = "in_play"

    def get_length_guess(self):
        return len(self._final_word)

    def try_guess(self, guess):
        if self._game_status == "in_play":
            words_in_guess = guess.split()
            if len(words_in_guess) == 0:
                return self._return_word_rejected("empty_guess_error")
            elif len(words_in_guess) > 1:
                return self._return_word_rejected("multiple_word_error")
            guess = words_in_guess[0]

            if guess == self._final_word:
                return self._return_game_won()
            elif len(guess) != len(self._final_word):
                return self._return_word_rejected("exceeded_length_error")
            elif guess.isdigit():
                return self._return_word_rejected("not_a_word")
            elif not check_unique_letters(guess):
                return self._return_word_rejected("repeated_letter_error")
            elif guess in self._guessed_words:
                return self._return_word_rejected("word_previously_guessed")
            elif not self._check_if_word(guess):
                return self._return_word_rejected("not_a_word")
            self.current_number_tries += 1
            self._guessed_words.add(guess)

            if self.current_number_tries >= self.total_guesses:
                return self._return_game_lost()
            cows_bulls = self._get_cows_bulls(guess)
            return self._return_word_accepted(cows=cows_bulls[0], bulls=cows_bulls[1])

    def _check_if_word(self, word):
        try:
            return self._wordApi.getDefinitions(word) is not None
        except:
            return True

    def _get_cows_bulls(self, guess):
        cows, bulls = 0, 0
        for guess_index, guess_letter in enumerate(guess):
            final_word_index = self._final_word.find(guess_letter)
            if final_word_index == -1:
                continue
            elif final_word_index == guess_index:
                cows += 1
            else:
                bulls += 1
        return cows, bulls

    def _generate_final_word(self):
        if self.difficulty == "easy":
            threeLetters = ['dog', 'pig', 'bay', 'ray', 'may', 'hey', 'tan', 'cat', 'sap', 'sat', 'sad', 'rat', 'rap',
                            'ram', 'rag', 'nap', 'Nat', 'mat', 'map', 'mad', 'lap', 'lag', 'lad', 'fat', 'fan', 'fad',
                            'fin', 'fit', 'lid', 'lip', 'lit', 'mid', 'nit', 'nip', 'rid', 'rig', 'rim', 'rip', 'Sid',
                            'sin', 'sip', 'log', 'mop', 'nod', 'rod', 'rot', 'sod', 'fun', 'mud', 'nut', 'rug', 'rut',
                            'sum', 'sun', 'fed', 'led', 'leg', 'met', 'Ned', 'net', 'bag', 'bad', 'bam', 'bat', 'cap',
                            'cab', 'Dan', 'gas', 'ham', 'hat', 'jab', 'jam', 'pan', 'pat', 'tab', 'tag', 'tan', 'tap',
                            'bid', 'dig', 'dip', 'hid', 'hit', 'hip', 'Jim', 'jig', 'kin', 'kid', 'pin', 'pit', 'pig',
                            'tin', 'tip', 'Tim', 'cop', 'con', 'Don', 'dog', 'hop', 'hog', 'job', 'jog', 'pot', 'top',
                            'Tom', 'bug', 'bud', 'bum', 'cup', 'cub', 'dug', 'Gus', 'gun', 'hum', 'jug', 'tub', 'tug',
                            'beg', 'bed', 'bet', 'hen', 'jet', 'Ken', 'pen', 'pet', 'peg', 'and', 'had', 'but', 'not',
                            'can', 'him', 'its', 'get', 'man', 'set', 'put', 'end', 'big', 'ask', 'men', 'got', 'run',
                            'let', 'cut', 'hot', 'ran', 'red', 'sit', 'six', 'ten', 'yes', 'act', 'ant', 'Ben', 'bit',
                            'bu', 'dam', 'den', 'dim', 'gut', 'hug', 'hut', 'ink', 'Jan', 'kit', 'Sam', 'tam', 'van',
                            'wet', 'win', 'box', 'bus', 'dot', 'fib', 'fix', 'fog', 'fox', 'gum', 'lug', 'mob', 'mug',
                            'Pam', 'rub', 'sub', 'wag', 'wax', 'wig', 'zap', 'Kim', 'mix', 'Rex', 'Tad', 'Ted', 'yet',
                            'zip', 'dab', 'Jen', 'lot', 'nab', 'pal', 'rob', 'sag', 'web', 'yak', 'yum', 'ban', 'axe',
                            'cog', 'cot', 'elf', 'elk', 'elm', 'fig', 'gap', 'nag', 'pod', 'rib', 'sob', 'tax', 'vet',
                            'yap', 'zen', 'bog', 'cob', 'cod', 'hem', 'imp', 'jib', 'jut', 'lop', 'pad', 'wed', 'God']
            return str(threeLetters[random.randint(0, len(threeLetters))].lower())
        if self.difficulty == "medium":
            fourLetters = ['from', 'long', 'back', 'just', 'help', 'must', 'went', 'land', 'hand', 'last', 'left',
                           'next', 'stop', 'list', 'song', 'best', 'fast', 'jump', 'pick', 'sing', 'upon', 'band',
                           'bank', 'belt', 'bend', 'bent', 'bled', 'blot', 'brag', 'brat', 'bred', 'brig', 'brim',
                           'bump', 'bunt', 'bust', 'camp', 'cast', 'clad', 'clam', 'clan', 'clap', 'clip', 'clot',
                           'club', 'crab', 'cram', 'crib', 'crop', 'damp', 'dent', 'drag', 'drip', 'drop', 'drug',
                           'drum', 'dump', 'dust', 'fact', 'felt', 'film', 'fist', 'flag', 'flap', 'flat', 'fled',
                           'flip', 'flop', 'frog', 'gasp', 'glad', 'glum', 'golf', 'grab', 'gram', 'grim', 'grin',
                           'grip', 'gulp', 'gust', 'held', 'hint', 'honk', 'hung', 'hunt', 'junk', 'kept', 'lamp',
                           'lick', 'lift', 'limp', 'lock', 'luck', 'lump', 'Mack', 'mask', 'mast', 'melt', 'mend',
                           'Mick', 'milk', 'mint', 'mist', 'neck', 'nest', 'pant', 'past', 'pest', 'plan', 'plot',
                           'plug', 'plum', 'plus', 'pond', 'punk', 'raft', 'rock', 'romp', 'Runs', 'runt', 'rust',
                           'sack', 'sand', 'sank', 'scab', 'scan', 'scat', 'self', 'send', 'sent', 'sick', 'skid',
                           'skim', 'skin', 'skip', 'skit', 'slam', 'slap', 'slat', 'sled', 'slim', 'slip', 'slob',
                           'slot', 'slug', 'slum', 'smog', 'smug', 'snag', 'snap', 'snip', 'snub', 'snug', 'sock',
                           'soft', 'span', 'spat', 'sped', 'spin', 'spit', 'spot', 'spun', 'stab', 'stem', 'step',
                           'stun', 'suck', 'sung', 'swam', 'swim', 'tack', 'trap', 'trim', 'trip', 'twig', 'twin',
                           'weld', 'wind', 'bang', 'deck', 'fang', 'Fran', 'gift', 'hang', 'Hank', 'Jack', 'king',
                           'loft', 'lost', 'lung', 'pack', 'rest', 'ring', 'sang', 'sink', 'stub', 'sunk', 'tank',
                           'tick', 'vent', 'vest', 'wing', 'wink', 'Bing', 'bong', 'Buck', 'Nick', 'peck', 'ping',
                           'pong', 'Rick', 'zing', 'body', 'bunk', 'desk', 'duck', 'dunk', 'dusk', 'hump', 'hunk',
                           'kits', 'lack', 'link', 'nips', 'pink', 'rack', 'rang', 'rink', 'taps', 'tusk', 'ugly',
                           'Zack', 'blip', 'bond', 'brad', 'bran', 'cask', 'clod', 'cost', 'disk', 'dock', 'flit',
                           'fond', 'Fred', 'fret', 'glen', 'glob', 'grit', 'husk', 'lend', 'lent', 'lint', 'mock',
                           'musk', 'pelt', 'plod', 'prim', 'prod', 'punt', 'rant', 'rent', 'risk', 'rung', 'scum',
                           'sift', 'silk', 'slid', 'slit', 'slop', 'snob', 'spud', 'Stan', 'sulk', 'swig', 'swum',
                           'task', 'tend', 'tock', 'tram', 'trek', 'trod', 'wept', 'west', 'wick', 'wilt', 'zest',
                           'copy']
            return str(fourLetters[random.randint(0, len(fourLetters))].lower())
        if self.difficulty == "hard":
            fiveLetters = ['maple', 'study', 'plant', 'along', 'often', 'until', 'black', 'bring', 'drink', 'blast',
                           'blend', 'blimp', 'blink', 'block', 'blond', 'blunt', 'brand', 'brunt', 'clamp', 'clasp',
                           'cling', 'clink', 'clump', 'clung', 'craft', 'cramp', 'crisp', 'crust', 'draft', 'drank',
                           'drift', 'fling', 'flung', 'flunk', 'frank', 'frisk', 'frost', 'gland', 'glint', 'grand',
                           'grant', 'grasp', 'grump', 'grunt', 'plank', 'prank', 'print', 'scalp', 'scram', 'scrap',
                           'slang', 'slant', 'slept', 'sling', 'slump', 'smack', 'snack', 'spank', 'spend', 'spent',
                           'splat', 'split', 'spunk', 'stack', 'stamp', 'stand', 'sting', 'stink', 'stomp', 'strap',
                           'strip', 'stuck', 'stump', 'swift', 'swing', 'swung', 'tramp', 'trend', 'trick', 'trunk',
                           'twang', 'admit', 'album', 'blank', 'crept', 'index', 'upset', 'stick', 'Texas', 'brick',
                           'cabin', 'camel', 'candy', 'habit', 'lemon', 'model', 'robin', 'sandy', 'scrub', 'slick',
                           'stung', 'truck', 'unzip', 'wagon', 'brisk', 'clang', 'flick', 'flock', 'plums', 'smock',
                           'speck', 'swept', 'track', 'given', 'adult', 'angry', 'empty', 'extra', 'nasty']
            return str(fiveLetters[random.randint(0, len(fiveLetters))].lower())

    def _return_game_won(self):
        self._game_status = "won"
        self.try_status = "won"
        return self._create_return_dict(game_status=self._game_status, try_status=self.try_status)

    def _return_game_lost(self):
        self._game_status = "lost"
        self.try_status = "lost"
        return self._create_return_dict(game_status=self._game_status, try_status=self.try_status)

    def _return_word_rejected(self, reject_reason):
        self.try_status = "rejected"
        return self._create_return_dict(try_status=self.try_status, reject_reason=reject_reason)

    def _return_word_accepted(self, cows, bulls):
        self.try_status = "accepted"
        dict = self._create_return_dict(try_status=self.try_status, cows=cows, bulls=bulls)
        return dict

    def _create_return_dict(self, game_status="in_play", try_status=None, reject_reason=None, cows=None, bulls=None):
        dict = {"game_status": game_status}
        dict["try_status"] = try_status
        dict["tries_used"] = self.current_number_tries
        if reject_reason != None:
            dict["reject_reason"] = reject_reason
        if cows != None:
            dict["cows"] = cows
        if bulls != None:
            dict["bulls"] = bulls
        return dict

    def add_tries(self, added_tries):
        self.total_guesses += added_tries

