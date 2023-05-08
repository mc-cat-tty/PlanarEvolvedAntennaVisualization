import argparse
import numpy as np
from utils import PolarCoord, plotPath
from math import ceil, floor
from random import randrange
from config import Config
from typing import List, Tuple

CONFIG_FILENAME = "config.yaml"

class Gene:
  def __init__(self, encodedGene: List[PolarCoord] = None):
    if (encodedGene is not None):
      self.encoding = encodedGene
      return

    revolutionAngles = (np.random.rand(Config.GeneEncoding.segmentsNumber) - 0.5) * \
      Config.GeneEncoding.maxAngle
    
    segmentLengths = np.random.uniform(
      low = Config.GeneEncoding.minSegmentLen,
      high = Config.GeneEncoding.maxSegmentLen,
      size = Config.GeneEncoding.segmentsNumber)

    self.encoding = list(zip(revolutionAngles, segmentLengths))
    self.encoding = [PolarCoord(a, l) for (a, l) in self.encoding]

  def __lt__(self, other) -> bool:
    return self.fitness() < other.fitness()
  
  def __repr__(self) -> str:
    res = "<"
    lastItemIdx = len(self.encoding) - 1
    for i in range(lastItemIdx):
      res += f"{self.encoding[i].angle} deg - {self.encoding[i].distance} mm - "
    res += f"{self.encoding[lastItemIdx].angle} deg - {self.encoding[lastItemIdx].distance} mm>"

    return res
  
  def __getitem__(self, itemIdx):
    return self.encoding[itemIdx]
  
  def getPolarCoords(self):
    return self.encoding

  def isValid(self) -> bool:
    """Returns true if the path is not slef-intersecting
    and doesn't come across the inner hole
    """
    return True
  
  def fitness(self) -> np.float16:
    return 1


class Population:
  def __init__(self):
    self.population = [Gene() for _ in range(Config.GeneticAlgoTuning.populationSize)]
    self.generationNumber = 0

  def nextGeneration(self) -> List[Gene]:
    for _ in range(Config.GeneticAlgoTuning.iterationsNumber):
      self.fight()
      self.crossover()
      self.mutate()
      self.generationNumber += 1
      yield self.population, self.generationNumber
    
  
  def fight(self):
    """This step filters out non-valid individuals and
    keeps only some of them according to the turnover rate
    """
    self.population = filter(
      lambda x: x.isValid(),
      self.population
    )

    survivedGenesNumber = ceil(Config.GeneticAlgoTuning.turnoverRate * Config.GeneticAlgoTuning.populationSize)
    self.population = sorted(self.population)[ : survivedGenesNumber]
  
  def crossover(self):
    newGenerationSize = floor((1.0 - Config.GeneticAlgoTuning.turnoverRate) * Config.GeneticAlgoTuning.populationSize)
    oldGenerationSize = len(self.population)

    for _ in range(newGenerationSize):
      cutpointIdx = randrange(Config.GeneEncoding.segmentsNumber)
      momGeneIdx = randrange(oldGenerationSize)
      dadGeneIdx = randrange(oldGenerationSize)
      momGene = self.population[momGeneIdx]
      dadGene = self.population[dadGeneIdx]
      newGene = Gene(momGene[:cutpointIdx] + dadGene[cutpointIdx:])
      self.population.append(newGene)
    
  def mutate(self):
    ...


def main(doPlot: bool):
  with open(CONFIG_FILENAME, "r") as f:
    Config.loadYaml(f)
    
  pop = Population()
  for generation, epoch in pop.nextGeneration():
    print(epoch, generation)

    if doPlot:
      import matplotlib.pyplot as plt
      plotPath(f"Epoch: {epoch}", sorted(generation)[0].getPolarCoords())  # Plot only best performing individual

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description = "Planar evolved antenna proof-of-concept"
  )

  parser.add_argument(
    "-p", "--plot", help="View what's happening in the simulation",
    default=False, action="store_true"
  )
  
  args = parser.parse_args()

  main(args.plot)