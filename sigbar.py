from rlbot.agents.base_script import BaseScript
from scipy.special import comb


class MyScript(BaseScript):
    def __init__(self):
        super().__init__("Significance Bar")

    def run(self):
        old_score = 0
        # run a loop
        while True:
            # Get the packet
            packet = self.wait_game_tick_packet()

            # check if a goal has been scored
            if packet.teams[0].score + packet.teams[1].score == old_score:
                continue
            old_score = packet.teams[0].score + packet.teams[1].score

            # Calculate the value
            blue_p = sum((
                comb(old_score, r) * .5**old_score for
                r in range(packet.teams[0].score, old_score + 1)
            ))

            blue_section = int(60 * blue_p) * 10

            orange_p = sum((
                comb(old_score, r) * .5**old_score for
                r in range(packet.teams[1].score, old_score + 1)
            ))

            orange_section = int(60 * (1 - orange_p)) * 10

            # Because of the geq, the middle is counted twice. Draw white over that point.
            renderer = self.game_interface.renderer
            renderer.begin_rendering()
            renderer.draw_rect_2d(20, 20, 5, orange_section, renderer.blue())
            renderer.draw_rect_2d(20, orange_section, 5, blue_section - orange_section, renderer.white())
            renderer.draw_rect_2d(20, blue_section, 5, 600 - blue_section, renderer.orange())
            renderer.end_rendering()


