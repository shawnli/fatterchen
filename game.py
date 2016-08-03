import logging

from lushi import gen_random_data, play_game


if __name__ == '__main__':
    gen_random_data()
    from choice import LinearChoice, FaceChoice, RandomChoice, ScoreChoice
    play_game(ScoreChoice(), FaceChoice())
