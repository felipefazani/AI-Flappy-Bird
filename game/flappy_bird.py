from typing import List
import pygame
import neat
from game.config import Images, Config, CountGen
from game.objects.abstract_object import GameObject
from game.objects.bird import Bird
from game.objects.ground import Ground
from game.objects.pipe import Pipe


def draw_game(
    background: pygame.Surface, birds: List[Bird], pipes: List[Pipe],
    grounds: List[Ground], points: int
):
    def _draw_objects(*args: List[GameObject]):
        for list in args:
            for each in list:
                each.draw(background)

    background.blit(source=Images.BACKGROUND.value, dest=(0, -200))

    _draw_objects(birds, pipes, grounds)

    text = Config.POINTS_FONT.value.render(
        f"Points: {points}",
        1,
        Config.POINTS_RGB.value
    )

    background.blit(source=text, dest=Config.POINTS_POSITION.value)

    if Config.AI.value:
        gen = Config.POINTS_FONT.value.render(
            f"Gen: {CountGen.get_count()}",
            1,
            Config.POINTS_RGB.value
        )
        background.blit(source=gen, dest=Config.GEN_POSITION.value)

    pygame.display.update()


def main(genomes, config): # fitness function
    def _move_objects(*args : List[GameObject]):
        for list in args:
            for each in list:
                each.move()

    CountGen.sum_one()

    pygame.display.set_caption("Flappy Bird")

    bird_position = Config.BIRD_START_POSITION.value
    ground_y = Config.GROUND_START_HEIGHT.value
    pipe_x = Config.PIPE_START_X_POSITION.value

    if Config.AI.value:
        networks = []
        genome_list = []
        birds = []

        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            genome.fitness = 0

            networks.append(network)
            genome_list.append(genome)
            birds.append(Bird(bird_position['x'], bird_position['y']))

    else:    
        birds = [Bird(bird_position['x'], bird_position['y'])]

    grounds = [
        Ground(0, ground_y), 
        Ground(Images.GROUND.value.get_width(), ground_y)
    ]
    pipes = [Pipe(pipe_x)]

    background = pygame.display.set_mode(
        size=(Config.WINDOW_WIDTH.value, Config.WINDOW_HEIGHT.value)
    )

    points = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if not Config.AI.value:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            bird.jump()
        
        pipe_i = 0
        if len(birds) > 0 :
            if len(pipes) > 1 and birds[0].x > pipes[0].x + Images.PIPE.value.get_width():
                pipe_i = 1
        else:
            running = False

        _move_objects(birds, grounds)
        
        for i, bird in enumerate(birds):
            if Config.AI.value:
                genome_list[i].fitness += 0.1
                output = networks[i].activate((
                    bird.y,
                    abs(bird.y - pipes[pipe_i].height),
                    abs(bird.y - pipes[pipe_i].ground_position)
                ))

                if output[0] > 0.5:
                    bird.jump()

        add_pipe = False
        birds_to_remove = []
        pipes_to_remove = []
        for i, pipe in enumerate(pipes):
            for bird in birds:
                if pipe.colision(bird):
                    birds_to_remove.append(bird)

                    if Config.AI.value:
                        genome_list[i].fitness -= 1
                        genome_list.pop(i)
                        networks.pop(i)
                
                if not pipe.left_screen and bird.x > pipe.x:
                    pipe.left_screen = True
                    points += 1
                    if Config.AI.value:
                        for genome in genome_list:
                            genome.fitness += 5
                    add_pipe = True

            for bird_remo in birds_to_remove:
                if bird_remo in birds:
                    birds.remove(bird_remo)
            
            pipe.move()
            if pipe.x + Images.PIPE.value.get_width() < 0:
                pipes_to_remove.append(pipe)

        for pipe_remo in pipes_to_remove:
            pipes.remove(pipe_remo)

        if add_pipe:
            pipes.append(Pipe(Config.NEW_PIPES_X_POSITION.value))

        for i, bird in enumerate(birds):
            if bird.y + Images.BIRD_MIDDLE.value.get_height() > Config.GROUND_START_HEIGHT.value or bird.y < 0:
                birds.pop(i)
                if Config.AI.value:
                    genome_list.pop(i)
                    networks.pop(i)

        draw_game(background, birds, pipes, grounds, points)


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    if Config.AI:
        population.run(main, 50)
    else:
        main(None, None)


if __name__ == "__main__":
    run('config.txt')
